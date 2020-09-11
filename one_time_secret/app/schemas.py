# -*- coding: utf-8 -*-

from pydantic import BaseModel, PositiveInt


class SecretKey(BaseModel):
    """
    Validation model for response that contains secret key.

    fields:
        secret_key (str): secret key in 32 characters uuid4 format.
    """

    secret_key: str


class SecretPhrase(BaseModel):
    """
    Validation model for response that contains secret phrase.

    fields:
        secret_phrase (str): decrypted secret phrase.
    """

    secret_phrase: str


class CreateSecret(BaseModel):
    """
    Validation model for POST request that create secret in DB.

    fields:
        secret_phrase (str): secret phrase.
        code_phrase (str): code phrase.
        ttl (PositiveInt, optional): storage time of the secret phrase in DB.
                Defaults to '86400' seconds (one day).
    """

    secret_phrase: str
    code_phrase: str
    ttl: PositiveInt = PositiveInt(86400)


class GetSecret(BaseModel):
    """
    Validation model for POST request body that get secret phrase from DB.

    fields:
        code_phrase (str): code phrase for decrypting a secret phrase.
    """

    code_phrase: str
