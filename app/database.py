from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sqlalchemy_database_url = 'postgresql://postgres:12@localhost/fastapi'

engine = create_engine(sqlalchemy_database_url)

Session_Local = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()