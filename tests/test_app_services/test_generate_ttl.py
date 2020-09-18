from datetime import timedelta

from one_time_secret.app import service


def test_good_argument():
    ttl = service.generate_ttl(seconds=60)
    expected_ttl = timedelta(seconds=60)
    assert ttl == expected_ttl
