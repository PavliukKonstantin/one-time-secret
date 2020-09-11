import uuid
from datetime import datetime, timedelta


def generate_secret_key() -> str:
    return str(uuid.uuid4().hex)


def generate_creation_datetime() -> datetime:
    return datetime.utcnow()


def generate_ttl(seconds: int) -> timedelta:
    return timedelta(seconds=seconds)
