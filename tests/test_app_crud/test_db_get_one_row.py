import pytest

from one_time_secret.app import crud, schemas


@pytest.mark.asyncio
async def test_good_arguments(db_session):
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
    )
    created_secret_row = await crud.db_create_secret(request_body=request_body)
    row_in_db = await crud.db_get_one_row(
        secret_key=created_secret_row["secret_key"],
    )
    assert created_secret_row == row_in_db


@pytest.mark.asyncio
async def test_non_existent_secret_key(db_session):
    secret_row_in_db = await crud.db_get_one_row(
        secret_key="asd123"
    )
    assert secret_row_in_db is None
