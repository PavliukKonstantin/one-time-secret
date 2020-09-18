from one_time_secret.app import crypto


def test_good_arguments():
    salt = b"\xe6\xf1\x9c\x81\xff\xdf\x1f\xe5\x8e7\xc6\xa6\x9cs\x81\xb0"
    code_phrase = "Some code phrase".encode()
    key = crypto._get_key(
            code_phrase=code_phrase,
            salt=salt,
        )
    expected_key = b"E3JMNYRRa61CZBf7c0vqI0xOWiKppZZRlLir-Fp-HMs="
    assert key == expected_key
