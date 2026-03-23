from security.encryption import encrypt_data, decrypt_data

data = b"hello voice embedding"

encrypted = encrypt_data(data)
print("Encrypted:", encrypted)

decrypted = decrypt_data(encrypted)
print("Decrypted:", decrypted)