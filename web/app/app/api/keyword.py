from flask import jsonify
from flask import request

from . import api
from .. import db
from ..models.keyword import Keyword
from ..nlp import ArticleInfo
from ..schemas.keyword import keyword_schema, keywords_schema
from .. import cache, cache_timeout
from wikiapi import WikiApi


@api.route('/keywords', methods=['GET'])
def get_keywords():
    data, error = keywords_schema.dump(Keyword.query.all())
    return jsonify(data)

@cache.memoize(timeout=cache_timeout)
def get_connected_keywords(id, limit=10):
    result = []
    connected_sql = 'SELECT connected_keywords.keyword2_id, keyword.content, ' \
                    '(SELECT COUNT(*) FROM article_keyword WHERE article_keyword.keyword_id=connected_keywords.keyword2_id) ' \
                    'AS c FROM connected_keywords ' \
                    'JOIN keyword ON connected_keywords.keyword2_id = keyword.id ' \
                    'WHERE connected_keywords.keyword1_id = ' + str(id) + ' GROUP BY connected_keywords.keyword2_id, ' \
                    'keyword.content ORDER BY c DESC LIMIT ' + str(limit)

    print ('GET CONNECTED KEYWORDS 1')

    connected = db.engine.execute(connected_sql)

    for row in connected:
        result.append({'id': [row[0]], 'value': row[1], 'connected': []})

    connected_sql2 = 'SELECT connected_keywords.keyword1_id, keyword.content, ' \
        '(SELECT COUNT(*) FROM article_keyword WHERE article_keyword.keyword_id=connected_keywords.keyword1_id) ' \
        'AS c FROM connected_keywords ' \
        'JOIN keyword ON connected_keywords.keyword1_id = keyword.id ' \
        'WHERE connected_keywords.keyword2_id = ' + str(id) + ' GROUP BY connected_keywords.keyword1_id, ' \
        'keyword.content ORDER BY c DESC LIMIT ' + str(limit)

    print ('GET CONNECTED KEYWORDS 2')

    connected2 = db.engine.execute(connected_sql2)

    for row in connected2:
        result.append({'id': [row[0]], 'value': row[1], 'connected': []})
    return result


@cache.memoize(timeout=cache_timeout)
def get_wikipedia_details(keyword):
    wiki = WikiApi()
    results = wiki.find(keyword)
    if len(results) > 0:
        article = wiki.get_article(results[0])
        if not 'Disambig' in article.image:
            return {'heading': article.heading, 'image': article.image, 'summary': article.summary, 'url': article.url}
    return None


@api.route('/keywords/<int:id>', methods=['GET'])
@cache.memoize(timeout=cache_timeout)
def get_keyword(id):
    data, error = keyword_schema.dump(Keyword.query.get(id))
    if len(data) == 0:
        return ''
    result = {'id': [id], 'value': data['content'],
              'connected': [], 'wikipedia_details': get_wikipedia_details(data['content'])}
    result['connected'] = get_connected_keywords(id)
    for keyword in result['connected']:
        keyword['connected'] = get_connected_keywords(keyword['id'][0], 3)
    return jsonify(result)


@api.route('/top-keywords', methods=['GET'])
@cache.cached(timeout=cache_timeout, key_prefix="top-keywords")
def get_top_keywords():
    names = get_keywords_from_db()
    return jsonify(names)


@api.route('/search', methods=['GET'])
def search_keyword():
    search = request.args.get("search").lower()
    sql = 'SELECT COUNT(keyword_id), keyword.content, keyword_id AS id ' \
          'FROM article_keyword JOIN keyword ON keyword.id = keyword_id ' \
          'WHERE LOWER(keyword.content) LIKE \'%%' + search + '%%\' ' \
          'GROUP BY keyword_id, keyword.content ' \
          'ORDER BY COUNT(keyword_id) DESC '\
          'LIMIT 10;'
    data = db.engine.execute(sql)
    names = []
    for row in data:
        names.append({'id': row[2], 'value': row[1], 'count': row[0]})
    return jsonify(names)


def group_in_database(keyphrases):
    for kp in keyphrases:
        remove_duplicates_in_db(kp)
        kp['id'] = [kp['id'][0]]
        for connected in kp['connected']:
            remove_duplicates_in_db(connected)
            connected['id'] = [connected['id'][0]]
    return keyphrases


def get_string_repr(ids):
    repr = ''
    for id in ids:
        repr += (str(id) + ',')
    return repr[:-1]


def remove_duplicates_in_db(kp):
    if len(kp['id']) == 1:
        return

    main_id = str(kp['id'][0])
    all_id_list = get_string_repr(kp['id'])
    duplicate_id_list = get_string_repr(kp['id'][1:])

    # update article_keyword table
    update_sql = 'UPDATE article_keyword ' \
                 ' SET keyword_id =' + main_id + \
                 ' WHERE keyword_id IN (' + duplicate_id_list + ');'
    db.engine.execute(update_sql)

    # delete entries that connect the same keyword
    delete_sql = 'DELETE FROM connected_keywords ' \
                 ' WHERE keyword1_id IN (' + all_id_list + \
        ') AND keyword2_id IN (' + all_id_list + ');'
    db.engine.execute(delete_sql)

    # update connected_keywords table
    update_sql = 'UPDATE connected_keywords' \
                 ' SET keyword1_id=' + main_id + \
                 ' WHERE keyword1_id IN (' + duplicate_id_list + ')' \
        ' AND (SELECT COUNT(*) FROM connected_keywords AS c2' \
        ' WHERE c2.keyword1_id=' + main_id + ' AND c2.keyword2_id = keyword2_id) = 0;'

    db.engine.execute(update_sql)
    update_sql = 'UPDATE connected_keywords' \
                 ' SET keyword2_id=' + main_id + \
                 ' WHERE keyword2_id IN (' + duplicate_id_list + ')' \
        ' AND (SELECT COUNT(*) FROM connected_keywords AS c2' \
        ' WHERE c2.keyword2_id=' + main_id + ' AND c2.keyword1_id = keyword1_id) = 0;'
    db.engine.execute(update_sql)

    # delete entries in connected_keywords that contain old id's
    delete_sql = 'DELETE FROM connected_keywords ' \
                 ' WHERE keyword1_id IN (' + duplicate_id_list + \
        ') OR keyword2_id IN (' + duplicate_id_list + ');'
    db.engine.execute(delete_sql)

    # update keyword table
    delete_sql = 'DELETE FROM keyword WHERE id IN (' + duplicate_id_list + ');'
    db.engine.execute(delete_sql)


@api.route('/trending', methods=['GET'])
def get_trending_keyphrases():
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    cleaned_keyphrases = get_trending_by_name(date_end, date_start)
    return jsonify(cleaned_keyphrases)

@cache.memoize(timeout=cache_timeout)
def get_connected_keywords_for_list (id_list):
    connected_sql = 'SELECT connected_keywords.keyword2_id, keyword.content,' \
                        ' (SELECT COUNT(*) FROM article_keyword WHERE article_keyword.keyword_id=connected_keywords.keyword2_id) AS c' \
                        ' FROM connected_keywords JOIN keyword ON connected_keywords.keyword2_id = keyword.id' \
                        ' WHERE connected_keywords.keyword1_id IN (' + id_list + ')' \
                        ' GROUP BY connected_keywords.keyword2_id, keyword.content ORDER BY c DESC LIMIT 7;'
    return [{'id': [k[0]], 'value': k[1]} for k in db.engine.execute(connected_sql)]


@cache.memoize(timeout=cache_timeout)
def get_trending_by_name(date_end, date_start):
    main_keyphrases = get_keywords_from_db(date_start, date_end)
    trending_keyphrases = []
    for name in main_keyphrases:
        id_list = get_string_repr(name['id'])
        trending_keyphrases.append({'id': name['id'], 'value': name['value'], 'count': name['count'], 'connected': get_connected_keywords_for_list(id_list)})
    all_keyphrases = []
    for entry in trending_keyphrases:
        all_keyphrases.append(
            {'id': entry['id'], 'value': entry['value'], 'count': entry['count']})
        for connected in entry['connected']:
            all_keyphrases.append(
                {'id': connected['id'], 'value': connected['value']})
    groups = group_similar_keyphrases([x['value'] for x in all_keyphrases])
    cleaned_keyphrases = filter_connected_keyphrases(
        trending_keyphrases, groups, all_keyphrases)
    cleaned_keyphrases = group_in_database(cleaned_keyphrases)
    return cleaned_keyphrases

@cache.memoize(timeout=cache_timeout)
def get_keywords_from_db(date_start=None, date_end=None):
    if date_start is None or date_end is None:
        sql = 'SELECT COUNT(keyword_id), keyword.content, keyword_id AS id ' \
            'FROM article_keyword JOIN keyword ON keyword.id = keyword_id ' \
            'GROUP BY keyword_id, keyword.content ' \
            'ORDER BY COUNT(keyword_id) DESC ' \
            'LIMIT 50;'
    else:
        sql = 'SELECT COUNT(keyword_id), keyword.content, keyword_id AS id ' \
            'FROM article_keyword JOIN keyword ON keyword.id = keyword_id ' \
            'JOIN  article ON article_keyword.article_id = article.id AND DATE(article.published_on) BETWEEN \'' + date_start + '\' AND \'' + date_end + '\' '\
            'GROUP BY keyword_id, keyword.content ' \
            'ORDER BY COUNT(keyword_id) DESC ' \
            'LIMIT 50;'
    data = db.engine.execute(sql)
    names = []
    for row in data:
        names.append({'id': [row[2]], 'value': row[1], 'count': row[0]})
    names = group_trending_keyphrases(names)
    return sorted(names[:25], key=lambda x: x['count'], reverse=True)


def group_trending_keyphrases(trending_keyphrases):
    grouped_keyphrases = []
    groups = group_similar_keyphrases(
        [kp['value'] for kp in trending_keyphrases])
    for group in groups:
        group_full = [find_keyword(kp, trending_keyphrases) for kp in group]
        representative = get_representative1(group_full)

        id_list = representative['id']
        for kp in group_full:
            for id in kp['id']:
                if id not in id_list:
                    id_list.append(id)
        count = sum([kp['count'] for kp in group_full])
        grouped_keyphrases.append(
            {'id': id_list, 'value': representative['value'], 'count': count})
    return grouped_keyphrases


def find_keyword(keyword, all_keywords):
    return next((x for x in all_keywords if x['value'] == keyword), [])


def get_representative1(group_full):
    max_count = sorted([x['count'] for x in group_full], reverse=True)[0]
    max_len = sorted([len(x) for x in group_full], reverse=True)[0]
    return sorted(list(group_full), reverse=True, key=lambda x: (x['count'] / max_count * 0.3 + len(x) / max_len * 0.7))[0]


def get_representative2(group_full):
    return sorted(list(group_full), reverse=True, key=lambda x: len(x))[0]


def filter_connected_keyphrases(trending_keyphrases, groups, all_keyphrases):
    group_repr = []
    for group in groups:
        group_full = [find_keyword(kp, all_keyphrases) for kp in group]
        representative = get_representative2(group_full)
        group_repr.append(representative)

    filtered_keyphrases = []
    for kp in trending_keyphrases:
        connected_filtered = []
        for connection in kp['connected']:
            if connection['value'] in [kp['value'] for kp in trending_keyphrases]:
                connected_filtered.append(connection)
            else:
                for i in range(0, len(groups)):
                    group = groups[i]
                    if connection['value'] in group:
                        connected_filtered.append(
                            {'id': group_repr[i]['id'], 'value': group_repr[i]['value']})
        filtered_keyphrases.append(
            {'id': kp['id'], 'value': kp['value'], 'count': kp['count'], 'connected': connected_filtered})

    return filtered_keyphrases


def group_similar_keyphrases(keyphrase_values):
    article_info = ArticleInfo()
    grouped_keywords = []
    for i in range(0, len(keyphrase_values)):
        first = keyphrase_values[i]
        for j in range(0, i):
            second = keyphrase_values[j]
            if article_info.keywords_similar(first, second):
                added = False
                for k in range(0, len(grouped_keywords)):
                    current = grouped_keywords[k]
                    if first in current:
                        current.add(second)
                        added = True
                        break
                    if second in current:
                        current.add(first)
                        added = True
                        break
                if not added:
                    grouped_keywords.append({first, second})
        exists = False
        for gk in grouped_keywords:
            if first in gk:
                exists = True
                break
        if not exists:
            grouped_keywords.append({first})
    return grouped_keywords
