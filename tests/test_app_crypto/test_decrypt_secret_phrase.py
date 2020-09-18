from cryptography.fernet import InvalidToken

from one_time_secret.app import crypto


def test_good_arguments():
    code_phrase = "some code phrase"
    encrypted_secret_phrase = (
        "gAAAAABfYg351-pOK_cwSHmlIxTFdWifSY11bHeW49uO2mloQuZVgC_nYBKIGsCGJl6"
        "7niKoz180g1ZmCVr9tls8B-spgxBONqIlpincGMIq8zBYHTLr7LA="
    )
    salt = '12491f6148fc82ec06f8671d9b40ec80'

    decrypted_secret_phrase = crypto.decrypt_secret_phrase(
        code_phrase=code_phrase,
        encrypted_secret_phrase=encrypted_secret_phrase,
        salt=salt,
    )
    expected_secret_phrase = "some secret phrase"
    assert decrypted_secret_phrase == expected_secret_phrase


def test_wrong_code_phrase():
    code_phrase = "wrong code phrase"
    encrypted_secret_phrase = (
        "gAAAAABfYg351-pOK_cwSHmlIxTFdWifSY11bHeW49uO2mloQuZVgC_nYBKIGsCGJl6"
        "7niKoz180g1ZmCVr9tls8B-spgxBONqIlpincGMIq8zBYHTLr7LA="
    )
    salt = '12491f6148fc82ec06f8671d9b40ec80'

    try:
        crypto.decrypt_secret_phrase(
            code_phrase=code_phrase,
            encrypted_secret_phrase=encrypted_secret_phrase,
            salt=salt,
        )
    except InvalidToken:
        assert True
    else:
        assert False


def test_wrong_salt():
    code_phrase = "some code phrase"
    encrypted_secret_phrase = (
        "gAAAAABfYg351-pOK_cwSHmlIxTFdWifSY11bHeW49uO2mloQuZVgC_nYBKIGsCGJl6"
        "7niKoz180g1ZmCVr9tls8B-spgxBONqIlpincGMIq8zBYHTLr7LA="
    )
    salt = "ee28f4f6ad49146351bb29eb3686609a"

    try:
        crypto.decrypt_secret_phrase(
            code_phrase=code_phrase,
            encrypted_secret_phrase=encrypted_secret_phrase,
            salt=salt,
        )
    except InvalidToken:
        assert True
    else:
        assert False
