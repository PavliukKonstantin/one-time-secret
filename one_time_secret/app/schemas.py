from pydantic import BaseModel


class SecretKey(BaseModel):
    secret_key: str


class SecretPhrase(BaseModel):
    secret_phrase: str


class CreateSecret(BaseModel):
    secret_phrase: str
    code_phrase: str


class GetSecret(BaseModel):
    code_phrase: str
