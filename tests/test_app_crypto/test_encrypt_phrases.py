from typing import Tuple

from one_time_secret.app import crypto


def test_returned_type():
    secret_phrase = "some secret phrase"
    code_phrase = "some code phrase"
    encrypted_phrases = crypto.encrypt_phrases(
        secret_phrase=secret_phrase,
        code_phrase=code_phrase,
    )
    assert isinstance(encrypted_phrases, Tuple)


def test_returned_len():
    secret_phrase = "some secret phrase"
    code_phrase = "some code phrase"
    encrypted_phrases = crypto.encrypt_phrases(
        secret_phrase=secret_phrase,
        code_phrase=code_phrase,
    )
    assert len(encrypted_phrases) == 3
