from datetime import timedelta

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
    created_row = await crud.db_create_secret(request_body=request_body)
    row_in_db = await crud.db_get_one_row(
        created_row["secret_key"],
    )
    number_of_rows_after_creation = await conftest.db_count_rows()
    assert number_of_rows_after_creation == number_of_rows_before_creation + 1
    assert created_row == row_in_db


@pytest.mark.asyncio
async def test_created_row_fields(db_session):
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
    )
    created_row = await crud.db_create_secret(request_body=request_body)
    assert len(created_row) == 6
    assert "secret_key" in created_row
    assert "secret_phrase" in created_row
    assert "code_phrase" in created_row
    assert "salt" in created_row
    assert "creation_datetime" in created_row
    assert "deletion_datetime" in created_row


@pytest.mark.asyncio
async def test_deletion_time(db_session):
    ttl = 86400
    request_body = schemas.CreateSecret(
        secret_phrase="some secret",
        code_phrase="some code phrase",
        ttl=ttl,
    )
    created_row = await crud.db_create_secret(request_body=request_body)
    creation_time = created_row["creation_datetime"]
    deletion_time = created_row["deletion_datetime"]
    assert deletion_time == creation_time + timedelta(seconds=ttl)
