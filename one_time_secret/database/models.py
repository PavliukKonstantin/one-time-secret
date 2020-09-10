from sqlalchemy import Column, DateTime, String, Text

from one_time_secret.database.db import Base


class Secret(Base):
    __tablename__ = "secret"

    # TODO make secret key unique
    # TODO add ttl index
    secret_key = Column(
        String(32),
        primary_key=True,
        unique=True,
        index=True)
    secret_phrase = Column(Text, nullable=False)
    code_phrase = Column(Text, nullable=False)
    salt = Column(String(32), nullable=False)
    creation_date_time = Column(DateTime)


secrets = Secret.__table__
