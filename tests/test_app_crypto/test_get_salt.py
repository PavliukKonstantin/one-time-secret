from one_time_secret.app import crypto


def test_returned_type():
    salt = crypto._get_salt()
    assert isinstance(salt, bytes)


def test_max_length():
    salt = crypto._get_salt()
    assert len(salt) == 16
