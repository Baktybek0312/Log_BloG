from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(schema='core')
Base = declarative_base(metadata=metadata_obj)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
