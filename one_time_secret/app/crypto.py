import base64
import binascii
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _get_key(code_phrase, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(code_phrase))


def _get_salt():
    return os.urandom(16)


# TODO add func that will encrypt secret_phrase and code phrase
# add salt
def encrypt(secret_phrase, code_phrase):
    salt = _get_salt()
    encryption_key = _get_key(code_phrase.encode(), salt)
    cipher_suite = Fernet(encryption_key)
    encrypted_secret_phrase = cipher_suite.encrypt(secret_phrase.encode())
    encrypted_code_phrase = cipher_suite.encrypt(code_phrase.encode())
    return (
        encrypted_secret_phrase.decode(),
        encrypted_code_phrase.decode(),
        binascii.hexlify(salt).decode(),
    )


def decrypt_secret_phrase(code_phrase, encrypted_secret_phrase, salt):
    encryption_key = _get_key(
        code_phrase.encode(),
        binascii.unhexlify(salt.encode()),
    )
    cipher_suite = Fernet(encryption_key)
    try:
        decrypted_secret_phrase = cipher_suite.decrypt(
            encrypted_secret_phrase.encode(),
        )
    except InvalidToken as exception:
        raise exception
    return decrypted_secret_phrase.decode()
