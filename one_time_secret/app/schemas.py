from pydantic import BaseModel


# TODO add max_length in validation???
class CreateSecret(BaseModel):
    secret_phrase: str
    code_phrase: str


class GetSecret(BaseModel):
    code_phrase: str
