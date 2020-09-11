from datetime import datetime

from cryptography.fernet import InvalidToken
from fastapi import FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every

from one_time_secret.app import crud, crypto, schemas
from one_time_secret.database.db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.on_event("startup")
@repeat_every(seconds=3600, wait_first=True)
async def delete_outdated_secrets():
    await crud.db_delete_outdated_secrets()


# TODO add method generate, ?secret=some_secret&code_phrase=some_phrase
# TODO add response model
# if secret_key and code phrase is exits??? add salt on generation
# type of the secret and code_phrase???
@app.post("/generate", status_code=201, response_model=schemas.SecretKey)
async def create_secret(
    create_secret_body: schemas.CreateSecret,
) -> dict:
    created_secret = await crud.db_create_secret(
        create_secret_body=create_secret_body,
    )
    return {"secret_key": created_secret}


# TODO add func that get row from db
# TODO add response codes if error!!!
@app.post("/secrets/{secret_key}", response_model=schemas.SecretPhrase)
async def get_secret(
    secret_key: str,
    get_secret_body: schemas.GetSecret,
) -> dict:
    secret_row = await crud.db_get_secret_row(secret_key=secret_key)
    if secret_row is None:
        raise HTTPException(
            status_code=404,
            detail=("Secret key does not exist or "
                    "deleted because the is over"),
        )

    if datetime.utcnow() > secret_row.get("deletion_datetime"):
        await crud.db_delete_secret(secret_key=secret_key)
        raise HTTPException(
            status_code=404,
            detail=("Secret key does not exist or "
                    "deleted because ttl is over"),
        )

    try:
        decrypted_secret_phrase = crypto.decrypt_secret_phrase(
            code_phrase=get_secret_body.code_phrase,
            encrypted_secret_phrase=secret_row.get("secret_phrase"),
            salt=secret_row.get("salt"),
        )
    except InvalidToken:
        raise HTTPException(status_code=400, detail="Incorrect code phrase")
    # TODO uncomment after testing
    # await crud.db_delete_secret(secret_key=secret_key)
    return {"secret_phrase": decrypted_secret_phrase}
