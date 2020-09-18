from time import sleep

import pytest

from one_time_secret.app import crud, schemas
from tests import conftest


@pytest.mark.asyncio
async def test_ttl_less_than_await(db_session):
    await crud.db_delete_outdated_secrets()
    number_of_rows_before_creation = await conftest.db_count_rows()
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
        ttl=1,
    )
    created_row = await crud.db_create_secret(request_body=request_body)
    row_in_db = await crud.db_get_one_row(
        created_row["secret_key"],
    )
    number_of_rows_after_creation = await conftest.db_count_rows()

    assert number_of_rows_after_creation == number_of_rows_before_creation + 1
    assert created_row == row_in_db

    sleep(1)
    await crud.db_delete_outdated_secrets()

    number_of_rows_after_deletion = await conftest.db_count_rows()
    row_in_db = await crud.db_get_one_row(
        created_row["secret_key"],
    )

    assert number_of_rows_after_deletion == number_of_rows_before_creation
    assert row_in_db is None


@pytest.mark.asyncio
async def test_ttl_more_than_await(db_session):
    await crud.db_delete_outdated_secrets()
    number_of_rows_before_creation = await conftest.db_count_rows()
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
        ttl=5,
    )
    created_row = await crud.db_create_secret(request_body=request_body)
    row_in_db = await crud.db_get_one_row(
        created_row["secret_key"],
    )
    number_of_rows_after_creation = await conftest.db_count_rows()

    assert number_of_rows_after_creation == number_of_rows_before_creation + 1
    assert created_row == row_in_db

    sleep(1)
    await crud.db_delete_outdated_secrets()

    number_of_rows_after_deletion = await conftest.db_count_rows()
    row_in_db = await crud.db_get_one_row(
        created_row["secret_key"],
    )

    assert number_of_rows_after_creation == number_of_rows_after_deletion
    assert created_row == row_in_db
