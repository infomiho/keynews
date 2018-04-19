from .. import ma
from ..models.article import Article


class ArticleSchema(ma.ModelSchema):

    class Meta:
        model = Article
        fields = ("id", "link", "summary", "scraped_date",
                  "published_on", "category", "keywords", "title", "content")

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
