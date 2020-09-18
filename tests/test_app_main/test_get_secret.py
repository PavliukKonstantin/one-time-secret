from time import sleep

from tests import conftest
from tests.conftest import CREATE_SECRET_URL, GET_SECRET_BASE_URL


def test_good_request(wait_app_start):
    response_of_creation = conftest.create_secret(CREATE_SECRET_URL)

    secret_key = response_of_creation.json()["secret_key"]
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "some code phrase",
    }
    response = conftest.post_request(url, request_body)
    expected_secret_phrase = "some secret"

    assert response.status_code == 200
    assert response.json()["secret_phrase"] == expected_secret_phrase


def test_empty_code_phrase(wait_app_start):
    response_of_creation = conftest.create_secret(CREATE_SECRET_URL)

    secret_key = response_of_creation.json()["secret_key"]
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "",
    }
    response = conftest.post_request(url, request_body)
    expected_location = ["body", "code_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_code_phrase_is_whitespaces(wait_app_start):
    response_of_creation = conftest.create_secret(CREATE_SECRET_URL)

    secret_key = response_of_creation.json()["secret_key"]
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "  ",
    }
    response = conftest.post_request(url, request_body)
    expected_location = ["body", "code_phrase"]
    expected_message = "ensure this value has at least 1 characters"

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == expected_location
    assert response.json()["detail"][0]["msg"] == expected_message


def test_non_existent_secret_key(wait_app_start):
    secret_key = "qweasdre123"
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "some code phrase",
    }
    response = conftest.post_request(url, request_body)
    expected_message = ("Secret key does not exist or "
                        "deleted because ttl is over")

    assert response.status_code == 404
    assert response.json()["detail"] == expected_message


def test_outdated_secret(wait_app_start):
    response_of_creation = conftest.create_secret(CREATE_SECRET_URL)

    sleep(1)

    secret_key = response_of_creation.json()["secret_key"]
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "some code phrase",
    }
    response = conftest.post_request(url, request_body)
    expected_message = ("Secret key does not exist or "
                        "deleted because ttl is over")

    assert response.status_code == 404
    assert response.json()["detail"] == expected_message


def test_double_request_one_secret(wait_app_start):
    response_of_creation = conftest.create_secret(CREATE_SECRET_URL)

    secret_key = response_of_creation.json()["secret_key"]
    url = f"{GET_SECRET_BASE_URL}{secret_key}"
    request_body = {
        "code_phrase": "some code phrase",
    }
    first_response = conftest.post_request(url, request_body)
    expected_secret_phrase = "some secret"

    assert first_response.status_code == 200
    assert first_response.json()["secret_phrase"] == expected_secret_phrase

    second_response = conftest.post_request(url, request_body)
    expected_message = ("Secret key does not exist or "
                        "deleted because ttl is over")

    assert second_response.status_code == 404
    assert second_response.json()["detail"] == expected_message
