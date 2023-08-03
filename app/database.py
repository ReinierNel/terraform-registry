from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

SQLALCHEMY_DATABASE_URL = "postgresql://rnrtfreg:rnrtfreg@localhost/rnrtfreg"

engine = create_engine(
    getenv('TF_REG_SQL_SERVER_CONNECTION_STRING')
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()