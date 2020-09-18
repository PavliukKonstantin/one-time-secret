import base64
import binascii
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _get_key(code_phrase: bytes, salt: bytes) -> bytes:
    """
    Get encryption key.

    Args:
        code_phrase (bytes): code phrase for generating an encryption key.
        salt (bytes): salt for generating an encryption key.

    Returns:
        bytes: encryption key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(code_phrase))


def _get_salt():
    """
    Get random generated 32 bytes.

    Returns:
        bytes: random generated 32 bytes.
    """
    return os.urandom(16)


def encrypt_phrases(secret_phrase: str, code_phrase: str) -> tuple:
    """
    Encrypt secret and code phrase.

    Args:
        secret_phrase (str): secret phrase that will be encrypt.
        code_phrase (str): code phrase that will be encrypt.

    Returns:
        tuple: encrypted secret phrase, encrypted code phrase, salt
    """
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


def decrypt_secret_phrase(
    code_phrase: str,
    encrypted_secret_phrase: str,
    salt: str,
) -> str:
    """
    Decrypt secret phrase.

    Args:
        code_phrase (str): code phrase for generating an decryption key.
        encrypted_secret_phrase (str): encrypted secret phrase.
        salt (str): salt for generating an decryption key.

    Raises:
        InvalidToken: if code phrase is incorrect.

    Returns:
        str: decrypted secret phrase.
    """
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
