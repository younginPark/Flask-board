from flaskr import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Users('%s', '%s')>" % (self.username, self.password)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.DateTime)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    def __init__(self, author_id, created, title, body):
        self.author_id = author_id
        self.created = created
        # self.deleted = deleted
        self.title = title
        self.body = title

    def __repr__(self):
        return "<Posts('%s', '%s', '%s', '%s', '%s')>" % (self.author_id, self.created, self.deleted, self.title, self.body)