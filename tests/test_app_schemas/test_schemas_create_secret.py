from pydantic import ValidationError

from one_time_secret.app import schemas


def test_good_arguments():
    validation_model = schemas.CreateSecret(
        secret_phrase="some secret phrase",
        code_phrase="some code phrase",
        ttl=60,
    )
    expected_secret_phrase = "some secret phrase"
    expected_code_phrase = "some code phrase"
    expected_ttl = 60
    assert validation_model.secret_phrase == expected_secret_phrase
    assert validation_model.code_phrase == expected_code_phrase
    assert validation_model.ttl == expected_ttl


def test_empty_secret_phrase():
    try:
        schemas.CreateSecret(
            secret_phrase="",
            code_phrase="some code phrase",
            ttl=60,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_secret_phrase_is_whitespaces():
    try:
        schemas.CreateSecret(
            secret_phrase="   ",
            code_phrase="some code phrase",
            ttl=60,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_empty_code_phrase():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="",
            ttl=60,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_code_phrase_is_whitespaces():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="  ",
            ttl=60,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_without_ttl():
    validation_model = schemas.CreateSecret(
        secret_phrase="some secret phrase",
        code_phrase="some code phrase",
    )
    expected_secret_phrase = "some secret phrase"
    expected_code_phrase = "some code phrase"
    expected_ttl = 86400
    assert validation_model.secret_phrase == expected_secret_phrase
    assert validation_model.code_phrase == expected_code_phrase
    assert validation_model.ttl == expected_ttl


def test_negative_ttl():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="some code phrase",
            ttl=-60,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_zero_ttl():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="some code phrase",
            ttl=0,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_float_ttl():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="some code phrase",
            ttl=10.6,
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_string_ttl():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="some code phrase",
            ttl="asdasd",
        )
    except ValidationError:
        assert True
    else:
        assert False


def test_empty_ttl():
    try:
        schemas.CreateSecret(
            secret_phrase="some secret phrase",
            code_phrase="some code phrase",
            ttl="",
        )
    except ValidationError:
        assert True
    else:
        assert False
