import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("POSTGRES_USER", "db_user")
db_password = os.getenv("POSTGRES_PASSWORD", "db_password")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "secrets")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
