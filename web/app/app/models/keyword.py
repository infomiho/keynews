from .. import db

# association_table = db.Table('keyword_keyword', db.Model.metadata, db.Column('keyword1_id', db.Integer, db.ForeignKey('keyword.id')), db.Column(
#    'keyword2_id', db.Integer, db.ForeignKey('keyword.id')), db.Column('article_id', db.Integer, db.ForeignKey('article.id')))


class ConnectedKeywords(db.Model):
    keyword1_id = db.Column('keyword1_id', db.Integer,
                            db.ForeignKey('keyword.id'), primary_key=True)
    keyword2_id = db.Column('keyword2_id', db.Integer,
                            db.ForeignKey('keyword.id'), primary_key=True)
    article_id = db.Column('article_id', db.Integer,
                           db.ForeignKey('article.id'), primary_key = True)

    keyword1 = db.relationship(
        "Keyword", foreign_keys=[keyword1_id])
    keyword2 = db.relationship(
        "Keyword", foreign_keys=[keyword2_id])
    # article = db.relationship(
    #     "Article", foreign_keys=[article_id])


class Keyword(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    type = db.Column(db.String)
    created_on = db.Column(db.Date)
    #this_keyword = db.relationship("ConnectedKeywords",
    #                                     backref='this',
    #                                     primaryjoin=id == ConnectedKeywords.keyword1_id)
    connected_keywords = db.relationship("ConnectedKeywords", backref = 'connected', primaryjoin = id == ConnectedKeywords.keyword2_id or id == ConnectedKeywords.keyword1_id)



    def __repr__(self):
        return 'Keyword {}>'.format(self.id)
