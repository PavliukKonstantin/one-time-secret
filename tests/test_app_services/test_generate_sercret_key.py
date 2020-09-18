from pydantic import ValidationError

from one_time_secret.app import schemas, service


def test_generate_secret_key():
    secret_key = service.generate_secret_key()
    try:
        schemas.SecretKey(secret_key=secret_key)
    except ValidationError:
        assert False
    else:
        assert True
