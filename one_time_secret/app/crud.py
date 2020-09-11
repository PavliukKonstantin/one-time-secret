# -*- coding: utf-8 -*-

from typing import Optional

from one_time_secret.app import crypto, schemas, service
from one_time_secret.database.db import database
from one_time_secret.database.models import secrets


async def db_create_secret(create_secret_body: schemas.CreateSecret) -> dict:
    """
    Create one secret in database.

    Args:
        create_secret_body (schemas.CreateSecret): validation schema.
            Look description in schemas.CreateSecret.

    Returns:
        dict: fields of the created secret.
    """
    encrypted_secret_phrase, encrypted_code_phrase, salt = crypto.encrypt(
        create_secret_body.secret_phrase,
        create_secret_body.code_phrase,
    )

    creation_datetime = service.get_current_datetime()
    ttl = service.generate_ttl(create_secret_body.ttl)
    deletion_datetime = creation_datetime + ttl

    created_secret = secrets.insert().values(
        secret_key=service.generate_secret_key(),
        secret_phrase=encrypted_secret_phrase,
        code_phrase=encrypted_code_phrase,
        salt=salt,
        creation_datetime=creation_datetime,
        deletion_datetime=deletion_datetime,
    )
    # TODO think about add try except here
    await database.execute(created_secret)
    return created_secret.parameters


async def db_get_secret_row(secret_key: str) -> Optional[dict]:
    """
    Get one secret row from database.

    Args:
        secret_key (str): secret key.

    Returns:
        Optional[dict]: fields one secret row.
            If secret key does not exist return 'None'.
    """
    query = secrets.select().\
        where(secrets.c.secret_key == secret_key)
    # TODO think about add try except here
    secret_row = await database.fetch_one(query=query)
    if secret_row is not None:
        return dict(secret_row)
    return None


async def db_delete_secret(secret_key: str) -> None:
    """
    Delete one secret in database.

    Args:
        secret_key (str): secret key.
    """
    query = secrets.delete().where(secrets.c.secret_key == secret_key)
    # TODO think about add try except here
    await database.execute(query)


async def db_delete_outdated_secrets() -> None:
    """Delete outdated secrets."""
    query = secrets.delete().\
        where(secrets.c.deletion_datetime < service.get_current_datetime())
    # TODO think about add try except here
    await database.execute(query)
