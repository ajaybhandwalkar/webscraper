from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = local_session()


def create_db_and_tables():
    print(Base.metadata.create_all(bind=engine))


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
