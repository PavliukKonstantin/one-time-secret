from pydantic import ValidationError

from one_time_secret.app import schemas


def test_good_argument():
    validation_model = schemas.GetSecret(
        code_phrase="some secret phrase",
    )
    expected = "some secret phrase"
    assert validation_model.code_phrase == expected


def test_empty():
    try:
        schemas.GetSecret(code_phrase="")
    except ValidationError:
        assert True
    else:
        assert False


def test_whitespaces():
    try:
        schemas.GetSecret(code_phrase="    ")
    except ValidationError:
        assert True
    else:
        assert False
