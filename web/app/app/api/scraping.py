import pickle
from datetime import datetime

from flask import jsonify
from sqlalchemy.sql.expression import func

from . import api
from .. import db
from ..models.article import Article
from ..models.keyword import Keyword, ConnectedKeywords
from ..nlp import ArticleInfo
from ..nlp.blacklist import BLACKLISTED_DOMAINS
from ..nlp.key_phrase_extraction import KeyPhraseExtraction
from ..scraping.newsapi_scraping import Scraper
from psycopg2 import IntegrityError

article_info = ArticleInfo()

def is_blacklisted_url(url):
    for blacklisted_domain in BLACKLISTED_DOMAINS:
        if blacklisted_domain in url:
            return True
    return False

def is_article_file (url):
    return url.endswith(('.pdf', '.jpg', '.png', '.gif', '.avi', '.mp3', '.mp4'))

# @api.route('/get_links', methods=['GET'])
def get_news_links():
    with db.app.app_context():
        scraper = Scraper(api_key='8aec566025d24cb4a6b44bff235bcca2')
        articles = scraper.scrape_all_articles(
            language='en', categories=[
                'general', 'business', 'politics',
                'health-and-medical', 'science-and-nature',
                'technology']
        )
        new_articles = 0
        for a in articles:
            if not is_blacklisted_url(a['url']) and not is_article_file(a['url']) and Article.query.filter_by(link=a['url']).first() is None:
                article = Article(link=a['url'], main_photo=a['urlToImage'])
                db.session.add(article)
                new_articles += 1
        db.session.commit()
        print("New articles added %d" % new_articles)
        return "New articles added %d" % new_articles

# @api.route('/download_articles', methods=['GET'])
def download_articles():
    with db.app.app_context():
        articles = Article.query.filter_by(
            downloaded=False).order_by(func.random()).limit(50).all()
        downloaded_articles = 0
        for article in articles:
            try:
                content, title = article_info.download_article(article)
                article.content = content
                article.title = title
                article.scraped_date = datetime.now()
                article.downloaded = True
                downloaded_articles += 1
                print("Downloaded ", article.link)
            except Exception as e:
                print(e)
                print("Error while downloading " + article.link)
        db.session.commit()
        return "Downloaded articles %d" % downloaded_articles


@api.route('/generate_tfidf', methods=['GET'])
def generate_tdidf_pickle():
    with db.app.app_context():
        articles = Article.query.filter_by(downloaded=True).order_by(
            Article.scraped_date.desc()).limit(2000).all()
        kpe = KeyPhraseExtraction()
        tfidf, dictionary = kpe.generate_tfidf(articles)

        with open('tfidf.pickle', 'wb') as f:
            pickle.dump(tfidf, f)

        with open('dictionary.pickle', 'wb') as f:
            pickle.dump(dictionary, f)
        return "Generated pickled tf-idf"


def new_or_existing_keyword(content):
    keyword = Keyword.query.filter_by(content=content).first()
    if keyword is None:
        keyword = Keyword(content=content, created_on=datetime.now())
        db.session.add(keyword)
    return keyword


def process_articles():
    with db.app.app_context():
        articles = Article.query.filter_by(
            downloaded=True, processed=False).limit(25).all()
        processed_articles = 0
        print("Trying to process ", len(articles))
        for article in articles:
            result = article_info.process_article(article)
            article.summary = result["summary"]
            keywords = [new_or_existing_keyword(
                keyword) for keyword in result["keyphrases_entites"]]
            article.keywords = keywords
            keyword_pairs = []
            created_associations = []
            for i in range(0, len(keywords)):
                for j in range(0, i):
                    keyword_pairs.append((keywords[i], keywords[j]))
            for (k1, k2) in keyword_pairs:
                aid = article.id
                k1id = k2.id
                k2id = k1.id
                key = ({k1id, k2id}, aid)
                if key in created_associations:
                    continue
                created_associations.append(key)
                association = ConnectedKeywords(article_id = aid, keyword1_id = k2id, keyword2_id = k1id )
                db.session.add(association)
            article.published_on = datetime.now()
            article.processed = True
            processed_articles += 1
            db.session.commit()
            print("Processed ", article.link)
        return "Processed articles %d" % processed_articles

# @api.route('/scrapings', methods=['GET'])


def scrape():
    scraper = Scraper(api_key='1fba1772badc4af19e37b3a442d8140a')
    articles = scraper.scrape_all_articles(
        language='en', categories=[
            'business', 'politics'])
    downloaded_articles = []
    for a in articles:
        if is_blacklisted_url(a['url']):
            continue
        content, title = article_info.download_article(a)
        if content:
            a['title'] = title
            a['content'] = content
            downloaded_articles.append(a)

    articles_keywords = article_info.find_keywords(downloaded_articles)

    processed = []
    for (i, a) in enumerate(downloaded_articles):
        info = article_info.process_article(a)
        info['keywords'] = articles_keywords[i]
        processed.append(info)

    return jsonify(processed)
