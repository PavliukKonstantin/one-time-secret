import os
from datetime import datetime

from cryptography.fernet import InvalidToken
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every

from one_time_secret.app import crud, crypto, schemas
from one_time_secret.database.db import database

app = FastAPI()

DELETION_FREQUENCY = int(os.getenv("FREQUENCY_OF_DELETION", 3600))


@app.on_event("startup")
async def db_connect():
    """Connect to the database when the application startup."""
    await database.connect()


@app.on_event("shutdown")
async def db_disconnect():
    """Disconnect from the database when the application shutdown."""
    await database.disconnect()


@app.on_event("startup")
@repeat_every(seconds=DELETION_FREQUENCY, wait_first=True)
async def delete_outdated_secrets():
    """Pereodic deletion outdated secrets."""
    await crud.db_delete_outdated_secrets()


@app.post("/generate", status_code=201, response_model=schemas.SecretKey)
async def create_secret(request_body: schemas.CreateSecret) -> dict:
    """
    POST request that create secret in database.

    Args:
        request_body (schemas.CreateSecret): validation schema for
            request body. Look description in schemas.CreateSecret.

    Returns:
        dict: secret key of the created secret phrase.
    """
    created_secret = await crud.db_create_secret(
        request_body=request_body,
    )
    return {"secret_key": created_secret["secret_key"]}


@app.post("/secrets/{secret_key}", response_model=schemas.SecretPhrase)
async def get_secret(
    secret_key: str,
    request_body: schemas.GetSecret,
) -> dict:
    """
    Get secret phrase.

    Args:
        secret_key (str): secret key in 32 characters uuid4 format.
        request_body (schemas.GetSecret): validation schema for
            request body. Look description in schemas.GetSecret.

    Raises:
        HTTPException_404: if the secret key does not exist.
        HTTPException_404: if the secret exists but is outdated
            and has not yet been deleted. Secret delete before exception raise.
        HTTPException_400: if the secret key exists, but the code phrase
            in the request body is incorrect.

    Returns:
        dict: decrypted secret phrase.
    """
    row = await crud.db_get_one_row(secret_key=secret_key)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=("Secret key does not exist or "
                    "deleted because ttl is over"),
        )

    if datetime.utcnow() > row["deletion_datetime"]:
        await crud.db_delete_one_row(secret_key=secret_key)
        raise HTTPException(
            status_code=404,
            detail=("Secret key does not exist or "
                    "deleted because ttl is over"),
        )

    try:
        decrypted_secret_phrase = crypto.decrypt_secret_phrase(
            code_phrase=request_body.code_phrase,
            encrypted_secret_phrase=row["secret_phrase"],
            salt=row["salt"],
        )
    except InvalidToken:
        raise HTTPException(status_code=400, detail="Incorrect code phrase")
    await crud.db_delete_one_row(secret_key=secret_key)
    return {"secret_phrase": decrypted_secret_phrase}
