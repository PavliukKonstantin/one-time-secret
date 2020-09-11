from pydantic import BaseModel, PositiveInt


class SecretKey(BaseModel):
    secret_key: str


class SecretPhrase(BaseModel):
    secret_phrase: str


class CreateSecret(BaseModel):
    secret_phrase: str
    code_phrase: str
    ttl: PositiveInt = PositiveInt(86400)


class GetSecret(BaseModel):
    code_phrase: str
