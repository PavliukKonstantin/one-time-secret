# -*- coding: utf-8 -*-

import os

import databases
from sqlalchemy.ext.declarative import declarative_base

db_user = os.getenv("POSTGRES_USER", "db_user")
db_password = os.getenv("POSTGRES_PASSWORD", "db_password")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_name = os.getenv("POSTGRES_DB", "secrets")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
