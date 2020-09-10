from typing import Generator

from cryptography.fernet import InvalidToken
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from one_time_secret.app import crud, crypto, schemas
from one_time_secret.database.db import DatabaseSession

app = FastAPI()


def get_db() -> Generator:
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()


# TODO add method generate, ?secret=some_secret&code_phrase=some_phrase
# TODO add response model
# if secret_key and code phrase is exits??? add salt on generation
# type of the secret and code_phrase???
@app.post("/generate", response_model=schemas.SecretKey)
def create_secret(
    phrases: schemas.CreateSecret,
    db: Session = Depends(get_db),
) -> dict:
    created_secret = crud.db_create_secret(db=db, phrases=phrases)
    return {"secret_key": created_secret.secret_key}


# TODO add func that get row from db
# TODO add response codes if error!!!
@app.post("/secrets/{secret_key}", response_model=schemas.SecretPhrase)
def get_secret(
    secret_key: str,
    get_secret_body: schemas.GetSecret,
    db: Session = Depends(get_db),
) -> dict:
    secret_row = crud.db_get_secret_row(db=db, secret_key=secret_key)
    if secret_row is None:
        raise HTTPException(
            status_code=404,
            detail="Secret key does not exist",
        )

    try:
        decrypted_secret_phrase = crypto.decrypt_secret_phrase(
            code_phrase=get_secret_body.code_phrase,
            encrypted_secret_phrase=secret_row.secret_phrase,
            salt=secret_row.salt,
        )
    except InvalidToken:
        raise HTTPException(
            status_code=400,
            detail="Incorrect code phrase",
        )
    # TODO uncomment after testing
    # crud.db_delete_secret(db=db, secret_key=secret_key)
    return {"secret_phrase": decrypted_secret_phrase}
