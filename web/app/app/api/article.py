from flask import jsonify, request

from . import api
from .. import cache, cache_timeout
from .. import db
from ..models.article import Article
from ..schemas.article import article_schema, articles_schema


@api.route('/articles', methods=['GET'])
def get_articles():
    data, error = articles_schema.dump(Article.query.all())
    return jsonify(data)


@api.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    data, error = article_schema.dump(Article.query.get(id))
    return jsonify(data)


def get_keyword_articles(id1, id2):
    sql = 'SELECT article.id, article.title, article.main_photo, article.summary, article.link, k.content AS keyword1, keyword.content AS keyword2, article.published_on FROM article'\
        ' JOIN connected_keywords ON article.id = connected_keywords.article_id '\
        ' JOIN keyword AS k ON connected_keywords.keyword1_id = k.id ' \
        ' JOIN keyword ON connected_keywords.keyword2_id = keyword.id '\
        'WHERE (connected_keywords.keyword1_id = ' + str(id1) + ' AND connected_keywords.keyword2_id = ' + str(id2) + ' )'\
        'OR (connected_keywords.keyword1_id = ' + str(id2) + \
        ' AND connected_keywords.keyword2_id = ' + str(id1) + ' );'
    articles = db.engine.execute(sql)
    result = []
    for row in articles:
        result.append({'id': row[0], 'title': row[1], 'photo': row[2], 'summary': row[3],
                       'link': row[4], 'keywords': [row[5], row[6]], 'published_on': row[7]})
    return result


@api.route('/articles_connected', methods=['POST'])
def get_connected_articles():
    data = request.get_json()
    main_id = data['id']
    connected = data['connected']
    try :
        result_grouped = get_connected_articles_cached(main_id, connected)
    except BaseException as e:
        print (e)
        return ''
    return jsonify(result_grouped)


@cache.memoize(timeout=cache_timeout)
def get_connected_articles_cached(main_id, connected):
    result = []
    for kw_id in connected:
        single = get_keyword_articles(main_id, kw_id)
        for a in single:
            result.append(a)
    result_grouped = group_articles(result)
    return result_grouped


def group_articles(unfiltered):
    grouped = []
    for article in unfiltered:
        if article['id'] not in [a['id'] for a in grouped]:
            grouped.append(article)
        else:
            from_group = find_article(article['id'], grouped)
            for keyword in article['keywords']:
                if keyword not in from_group['keywords']:
                    from_group['keywords'].append(keyword)
    return grouped


def find_article(id, articles):
    return next((x for x in articles if x['id'] == id), [])
