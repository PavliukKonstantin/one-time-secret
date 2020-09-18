from typing import Optional

from sqlalchemy import select, delete, insert

from one_time_secret.app import crypto, schemas, service
from one_time_secret.database.db import database
from one_time_secret.database.models import secrets


async def db_create_secret(request_body: schemas.CreateSecret) -> dict:
    """
    Create one secret in database.

    Args:
        request_body (schemas.CreateSecret): validation schema.
            Look description in schemas.CreateSecret.

    Returns:
        dict: fields of the created secret.
    """
    encripted_phrases = crypto.encrypt_phrases(
        request_body.secret_phrase,
        request_body.code_phrase,
    )
    encrypted_secret_phrase, encrypted_code_phrase, salt = encripted_phrases

    creation_datetime = service.get_current_datetime()
    ttl = service.generate_ttl(request_body.ttl)
    deletion_datetime = creation_datetime + ttl

    query = insert(table=secrets).values(
        secret_key=service.generate_secret_key(),
        secret_phrase=encrypted_secret_phrase,
        code_phrase=encrypted_code_phrase,
        salt=salt,
        creation_datetime=creation_datetime,
        deletion_datetime=deletion_datetime,
    )
    await database.execute(query=query)
    return query.parameters


async def db_get_one_row(secret_key: str) -> Optional[dict]:
    """
    Get one secret row from database.

    Args:
        secret_key (str): secret key.

    Returns:
        Optional[dict]: fields one secret row.
            If secret key does not exist return 'None'.
    """

    query = select([secrets]).where(secrets.c.secret_key == secret_key)
    secret_row = await database.fetch_one(query=query)
    if secret_row is not None:
        return dict(secret_row)
    return None


async def db_delete_one_row(secret_key: str) -> None:
    """
    Delete one secret in database.

    Args:
        secret_key (str): secret key.
    """
    query = delete(table=secrets).where(secrets.c.secret_key == secret_key)
    await database.execute(query=query)


async def db_delete_outdated_secrets() -> None:
    """Delete outdated secrets."""
    query = delete(table=secrets).\
        where(secrets.c.deletion_datetime < service.get_current_datetime())
    await database.execute(query=query)
