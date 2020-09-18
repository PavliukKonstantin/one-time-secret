from datetime import datetime

from one_time_secret.app import service


def test_returned_type():
    current_datetime = service.get_current_datetime()
    assert isinstance(current_datetime, datetime)
