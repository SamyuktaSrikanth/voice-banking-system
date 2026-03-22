import bcrypt

password = "1234"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print(hashed.decode())