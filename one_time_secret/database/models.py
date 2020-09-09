import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from one_time_secret.database.db import Base


def generate_secret_key():
    return str(uuid.uuid4().hex)


class Secret(Base):
    __tablename__ = "secret"

    # TODO make secret key unique
    secret_key = Column(
        String(32),
        primary_key=True,
        default=generate_secret_key,
        unique=True,
        nullable=False,
        index=True)
    secret_phrase = Column(Text, nullable=False)
    code_phrase = Column(Text, nullable=False)
    salt = Column(String(32), nullable=False)
    create_date_time = Column(DateTime, default=datetime.utcnow)
