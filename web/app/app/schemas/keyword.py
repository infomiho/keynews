from .. import ma
from ..models.keyword import Keyword


class KeywordSchema(ma.ModelSchema):

    class Meta:
        model = Keyword
        fields = ("id", "content", "type", "created_on")


keyword_schema = KeywordSchema()
keywords_schema = KeywordSchema(many=True)
