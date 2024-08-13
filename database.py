from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base

DATABASE_URL = os.getenv('DATABASE_URL')

database = Database(DATABASE_URL)
metadata = Base.metadata

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    metadata.create_all(bind=engine)
