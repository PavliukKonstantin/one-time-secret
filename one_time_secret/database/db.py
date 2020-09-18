import os

import databases
from sqlalchemy.ext.declarative import declarative_base

# Default values used for "./tests/test_app_crud/"
POSTGRES_USER = os.getenv("POSTGRES_USER", "database_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "database_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "54322")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test_secrets")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
