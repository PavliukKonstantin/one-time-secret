from pydantic import BaseModel, PositiveInt, constr, validator

uuid4_regex = "^[a-z0-9]{32}$"


class SecretKey(BaseModel):
    """
    Validation model for response that contains secret key.

    fields:
        secret_key (str): secret key in 32 characters uuid4 format.
    """

    secret_key: constr(
        strip_whitespace=True,
        regex=uuid4_regex,
    )


class SecretPhrase(BaseModel):
    """
    Validation model for response that contains secret phrase.

    fields:
        secret_phrase (str): decrypted secret phrase.
    """

    secret_phrase: constr(strip_whitespace=True, min_length=1)


class CreateSecret(BaseModel):
    """
    Validation model for POST request that create secret in DB.

    fields:
        secret_phrase (str): secret phrase.
        code_phrase (str): code phrase.
        ttl (PositiveInt, optional): storage time of the secret phrase in DB.
                Defaults to '86400' seconds (one day).
    """

    secret_phrase: constr(strip_whitespace=True, min_length=1)
    code_phrase: constr(strip_whitespace=True, min_length=1)
    ttl: PositiveInt = PositiveInt(86400)

    @validator('ttl', pre=True)
    def size_is_some(cls, value):  # noqa
        """Validation values float type."""
        if isinstance(value, float):
            raise ValueError('value is not a valid integer')
        return value


class GetSecret(BaseModel):
    """
    Validation model for POST request body that get secret phrase from DB.

    fields:
        code_phrase (str): code phrase for decrypting a secret phrase.
    """

    code_phrase: constr(strip_whitespace=True, min_length=1)
