import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY").encode()  # must be 32 bytes

def encrypt_data(data: bytes):
    # Generate random IV
    iv = os.urandom(16)

    # Pad data
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # AES Cipher
    cipher = Cipher(
        algorithms.AES(SECRET_KEY),
        modes.CBC(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted  # store IV + ciphertext


def decrypt_data(encrypted_data: bytes):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(
        algorithms.AES(SECRET_KEY),
        modes.CBC(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data