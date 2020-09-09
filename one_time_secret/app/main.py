from cryptography.fernet import InvalidToken
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from one_time_secret.app import crypto, schemas
from one_time_secret.database import models
from one_time_secret.database.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO create a function that will generates secret_key
# on base of secret_phrase and code_phrase
def generate_secret_key(secret_phrase, code_phrase):
    secret_key = f"{secret_phrase}-{code_phrase}"
    return secret_key


# TODO add func that write row in db
def db_create_secret(
    db: Session,
    phrases: schemas.CreateSecret,
):
    encrypted_secret_phrase, encrypted_code_phrase, salt = crypto.encrypt(
        phrases.secret_phrase,
        phrases.code_phrase,
    )

    new_secret = models.Secret(
        secret_phrase=encrypted_secret_phrase,
        code_phrase=encrypted_code_phrase,
        salt=salt,
    )
    db.add(new_secret)
    db.commit()
    # TODO think about db.refresh
    db.refresh(new_secret)
    return new_secret


# TODO add method generate, ?secret=some_secret&code_phrase=some_phrase
# TODO add response model
# if secret_key and code phrase is exits??? add salt on generation
# type of the secret and code_phrase???
# @app.post("/generate", response_model=schemas.SecretCreate)
@app.post("/generate")
def create_secret(
    phrases: schemas.CreateSecret,
    db: Session = Depends(get_db),
):
    created_secret = db_create_secret(db=db, phrases=phrases)
    response = {
        "create_date_time": created_secret.create_date_time,
        "secret_key": created_secret.secret_key,
        "secret_phrase": created_secret.secret_phrase,
        "code_phrase": created_secret.code_phrase,
        "salt": created_secret.salt,
    }
    return response


def db_get_secret_row(
    db: Session,
    secret_key: str,
):
    return db.query(models.Secret).\
        filter(models.Secret.secret_key == secret_key).first()


# TODO add func that remove row after successful access


# TODO add func that get row from db
# TODO add response codes if error!!!
@app.post("/secrets/{secret_key}")
def get_secret(
    secret_key: str,
    get_secret_body: schemas.GetSecret,
    db: Session = Depends(get_db),
):
    response = {}
    secret_row = db_get_secret_row(db=db, secret_key=secret_key)
    if secret_row is None:
        response.update({"Error": "Secret key does not exist"})
        return response
    try:
        decrypted_secret_phrase = crypto.decrypt_secret_phrase(
            code_phrase=get_secret_body.code_phrase,
            encrypted_secret_phrase=secret_row.secret_phrase,
            salt=secret_row.salt,
        )
    except InvalidToken:
        response.update({"Error": "Code phrase is wrong"})
        return response

    response.update({
        "secret_phrase": decrypted_secret_phrase,
        })
    return response
