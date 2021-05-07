from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:admin1234@localhost:5432/flaskr')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    print('Init db!!!!!!!!!')
    import models
    Base.metadata.create_all(engine)