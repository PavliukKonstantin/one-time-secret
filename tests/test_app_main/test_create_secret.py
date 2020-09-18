from tests import conftest

from tests.conftest import CREATE_SECRET_URL


def test_good_request(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": 60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)

    assert response.status_code == 201
    assert "secret_key" in response.json()


def test_empty_secret_phrase(wait_app_start):
    request_body = {
        "secret_phrase": "",
        "code_phrase": "some code phrase",
        "ttl": 60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "secret_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_secret_phrase_is_whitespaces(wait_app_start):
    request_body = {
        "secret_phrase": "   ",
        "code_phrase": "some code phrase",
        "ttl": 60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "secret_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_empty_code_phrase(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "",
        "ttl": 60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "code_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_code_phrase_is_whitespaces(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "   ",
        "ttl": 60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "code_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_without_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase"
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)

    assert response.status_code == 201
    assert "secret_key" in response.json()


def test_negative_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": -60
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "ttl"]
    expected_message = "ensure this value is greater than 0"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_zero_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": 0
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "ttl"]
    expected_message = "ensure this value is greater than 0"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_float_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": 10.6
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "ttl"]
    expected_message = "value is not a valid integer"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_string_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": "qweqweqw"
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "ttl"]
    expected_message = "value is not a valid integer"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_empty_ttl(wait_app_start):
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": ""
    }
    response = conftest.post_request(CREATE_SECRET_URL, request_body)
    expected_location = ["body", "ttl"]
    expected_message = "value is not a valid integer"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message
