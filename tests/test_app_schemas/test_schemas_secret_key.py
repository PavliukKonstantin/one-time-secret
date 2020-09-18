from pydantic import ValidationError

from one_time_secret.app import schemas


def test_good_argument():
    validation_model = schemas.SecretKey(
        secret_key="984ae013e1304e54a5b2a1aec57fac36",
    )
    expected = "984ae013e1304e54a5b2a1aec57fac36"
    assert validation_model.secret_key == expected


def test_less_than_32_characters():
    try:
        schemas.SecretKey(secret_key="asdasqwezxcz")
    except ValidationError:
        assert True
    else:
        assert False


def test_more_than_32_characters():
    try:
        schemas.SecretKey(secret_key="asdasqwezxczqweqweqx23123123qweqwe")
    except ValidationError:
        assert True
    else:
        assert False


def test_uuid_with_bad_symbols():
    try:
        schemas.SecretKey(secret_key="984ae013e1304e54a5b2a1aec57fac__")
    except ValidationError:
        assert True
    else:
        assert False


def test_empty():
    try:
        schemas.SecretKey(secret_key="")
    except ValidationError:
        assert True
    else:
        assert False


def test_whitespaces():
    try:
        schemas.SecretKey(secret_key="    ")
    except ValidationError:
        assert True
    else:
        assert False
