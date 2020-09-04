from sqlalchemy import Column, DateTime, Integer, String, Text

from one_time_secret.database.db import Base


class Secret(Base):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True, index=True)
    # TODO make secret key unique
    secret_key = Column(String, unique=False, index=True)
    secret_phrase = Column(Text)
    code_phrase = Column(String(200), index=True)
    date_time = Column(DateTime)
