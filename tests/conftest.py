from typing import Dict

import pytest
import requests
from requests import Session
from requests.adapters import HTTPAdapter, Response
from sqlalchemy import func, select
from urllib3.util.retry import Retry

from one_time_secret.database.db import database
from one_time_secret.database.models import secrets

CREATE_SECRET_URL = "http://localhost:9123/generate"
GET_SECRET_BASE_URL = "http://localhost:9123/secrets/"

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope="session")
def wait_app_start(session_scoped_container_getter):
    """Fixture. Wait startup application in docker containers."""
    service = session_scoped_container_getter.get('test_api').network_info[0]
    base_url = f"http://{service.hostname}:{service.host_port}"
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )

    session = Session()
    session.mount('http://', HTTPAdapter(max_retries=retry))

    assert session.get(f'{base_url}/docs').status_code == 200


@pytest.mark.asyncio
@pytest.fixture()
async def db_session(wait_app_start):
    """Fixture. Connect to database before test and disconnect after."""
    await database.connect()

    yield

    await database.disconnect()


async def db_count_rows() -> int:
    """Count rows in table 'secret'.

    Returns:
        int: number of rows.
    """
    query = select([func.count()]).select_from(secrets)
    number_of_rows = await database.execute(query=query)
    return number_of_rows


def post_request(url: str, request_body: Dict[str, str]) -> Response:
    """Return response of POST request.

    Args:
        url (str): url for request.
        request_body (Dict[str, str]): request body.

    Returns:
        Response: response of POST request.
    """
    try:
        response = requests.post(url=url, json=request_body)
    except requests.exceptions.ConnectionError:
        assert False
    else:
        response.close()
        return response


def create_secret(url: str) -> Response:
    """Create one secret.

    Args:
        url (str): url for request.

    Returns:
        Response: response of creation request.
    """
    request_body = {
        "secret_phrase": "some secret",
        "code_phrase": "some code phrase",
        "ttl": 1
    }
    return post_request(url, request_body)
