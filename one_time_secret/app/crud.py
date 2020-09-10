import uuid
from datetime import datetime
from typing import Optional

from one_time_secret.app import crypto, schemas
from one_time_secret.database.db import database
from one_time_secret.database.models import secrets


def _generate_secret_key() -> str:
    return str(uuid.uuid4().hex)


def _generate_timestamp() -> datetime:
    return datetime.utcnow()


# TODO add func that write row in db
async def db_create_secret(
    create_secret_body: schemas.CreateSecret,
) -> str:
    encrypted_secret_phrase, encrypted_code_phrase, salt = crypto.encrypt(
        create_secret_body.secret_phrase,
        create_secret_body.code_phrase,
    )
    # TODO think about variable name "query"
    query = secrets.insert().values(
        secret_key=_generate_secret_key(),
        secret_phrase=encrypted_secret_phrase,
        code_phrase=encrypted_code_phrase,
        salt=salt,
        creation_date_time=_generate_timestamp(),
    )
    # TODO think about add try except here
    await database.execute(query)
    return query.parameters.get("secret_key")


async def db_get_secret_row(secret_key: str) -> Optional[dict]:
    query = secrets.select().\
        where(secrets.c.secret_key == secret_key)
    secret_row = await database.fetch_one(query=query)
    if secret_row is not None:
        return dict(secret_row)
    return None


# TODO add func that remove row after successful access
async def db_delete_secret(secret_key: str) -> None:
    query = secrets.delete().where(secrets.c.secret_key == secret_key)
    # TODO think about add try except here
    await database.execute(query)
