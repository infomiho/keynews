from newsapi.articles import Articles
from newsapi.sources import Sources


class Scraper:

    # example code
    # -----------------------
    # x = Scraper(api_key='xyz')
    # print(x.scrape_all_articles(language='en'))

    articles = None
    sources = None
    api_key = None

    def __init__(self, api_key) -> None:
        super().__init__()
        self.api_key = api_key
        self.articles = Articles(API_KEY=self.api_key)
        self.sources = Sources(API_KEY=self.api_key)

    def scrape_articles_for_sources(self, sources):
        '''
        Accepts the list of source names and returns all articles downloaded from the given sources
        :param sources: List of source id's
        :return: List of article json objects, containing:
            'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt'
        '''
        articles = []
        for source in sources:
            try:
                # list of json objects
                # author, title, description, url, urlToImage, publishedAt
                articles_for_source = self.articles.get(source=source).articles
            except BaseException:  # if the server does not respond
                continue
            for article in articles_for_source:
                articles.append(article)
        return articles

    def scrape_sources(self, categories=[], language=None):
        '''
        Gets the newsapi sources associated with the given category (optional) and language (optional)
        :param categories: List of categories (optional)
        :param language: Language (optional)
        :return: List of source id's
        '''
        sources_dict = []
        for category in categories:
            sources_dict += self.sources.get(category, language).sources
        sources = set([source['id'] for source in sources_dict])
        return sources

    def scrape_all_articles(self, categories=[], language=None):
        '''
        Scrapes and returns all articles for the given category and language (parameters are optional)
        :param categories: list of categories (optional)
        :param language: language (optional)
        :return: List of article json objects, containing:
            'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt'
        '''
        return self.scrape_articles_for_sources(self.scrape_sources(categories, language))
