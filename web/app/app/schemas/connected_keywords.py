from .. import ma
from ..models.keyword import ConnenctedKeywords


class ConnectedKeywordsSchema(ma.ModelSchema):

    class Meta:
        model = ConnenctedKeywords
        fields = ("keyword1_id", "keyword2_id", "article_id")

connected_keyword_schema = ConnectedKeywordsSchema()
connected_keywords_schema = ConnectedKeywordsSchema(many=True)
