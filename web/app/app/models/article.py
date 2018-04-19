from .. import db

association_table = db.Table('article_keyword', db.Model.metadata,
                             db.Column('article_id', db.Integer,
                                       db.ForeignKey('article.id')),
                             db.Column('keyword_id', db.Integer,
                                       db.ForeignKey('keyword.id')),
                             db.Column('weight', db.Integer)
                             )


class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text)
    summary = db.Column(db.Text)
    main_photo = db.Column(db.Text)
    scraped_date = db.Column(db.DateTime)
    published_on = db.Column(db.DateTime)
    category = db.Column(db.String)
    keywords = db.relationship(
        'Keyword', secondary=association_table, backref='articles')
    # Processing fields
    downloaded = db.Column(db.Boolean, default=False)
    processed = db.Column(db.Boolean, default=False)
    title = db.Column(db.String)
    content = db.Column(db.Text)

    def __repr__(self):
        return 'Article {}>'.format(self.id)
