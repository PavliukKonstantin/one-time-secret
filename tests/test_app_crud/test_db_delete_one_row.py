import pytest

from one_time_secret.app import crud, schemas
from tests import conftest


@pytest.mark.asyncio
async def test_good_arguments(db_session):
    number_of_rows_before_creation = await conftest.db_count_rows()
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
    )
    created_secret_row = await crud.db_create_secret(request_body=request_body)
    number_of_rows_after_creation = await conftest.db_count_rows()

    assert number_of_rows_after_creation == number_of_rows_before_creation + 1

    await crud.db_delete_one_row(secret_key=created_secret_row["secret_key"])
    number_of_rows_after_deletion = await conftest.db_count_rows()

    assert number_of_rows_before_creation == number_of_rows_after_deletion


@pytest.mark.asyncio
async def test_non_existent_row(db_session):
    number_of_rows_before_deletion = await conftest.db_count_rows()
    await crud.db_delete_one_row(secret_key="asda213")
    number_of_rows_after_deletion = await conftest.db_count_rows()

    assert number_of_rows_before_deletion == number_of_rows_after_deletion
