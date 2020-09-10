from sqlalchemy.orm import Session

from one_time_secret.app import crypto, schemas
from one_time_secret.database import models


# TODO add func that write row in db
def db_create_secret(
    db: Session,
    phrases: schemas.CreateSecret,
) -> models.Secret:
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
    db.refresh(new_secret)
    return new_secret


def db_get_secret_row(db: Session, secret_key: str) -> models.Secret:
    return db.query(models.Secret).get(secret_key)


# TODO add func that remove row after successful access
def db_delete_secret(db: Session, secret_key: str) -> None:
    deleted_secret = db.query(models.Secret).get(secret_key)
    db.delete(deleted_secret)
    db.commit()
