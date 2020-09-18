import uuid
from datetime import datetime, timedelta


def generate_secret_key() -> str:
    """
    Generate secret key.

    Returns:
        str: secret key in 32 characters uuid4 format.
    """
    return str(uuid.uuid4().hex)


def get_current_datetime() -> datetime:
    """
    Generate datetime in UTC timezone.

    Returns:
        datetime: datetime.
    """
    return datetime.utcnow()


def generate_ttl(seconds: int) -> timedelta:
    """
    Generate time to live for secret.

    Args:
        seconds (int): storage time of the secret phrase in DB.

    Returns:
        timedelta: storage time of the secret phrase in timedelta format.
    """
    return timedelta(seconds=seconds)
