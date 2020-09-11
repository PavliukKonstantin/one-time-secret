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
    creation_datetime = Column(DateTime, nullable=False)
    deletion_datetime = Column(DateTime, nullable=False)


secrets = Secret.__table__
