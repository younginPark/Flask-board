from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from flaskr.db import Base

# engine = create_engine('postgresql://postgres:admin1234@localhost:5432/board')
# Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Users('%s', '%s')>" % (self.username, self.password)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow())
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    def __init__(self, author_id, created, title, body):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = title

    def __repr__(self):
        return "<Posts('%s', '%s', '%s', '%s')>" % (self.author_id, self.created, self.title, self.body)

# Base.metadata.create_all(engine)