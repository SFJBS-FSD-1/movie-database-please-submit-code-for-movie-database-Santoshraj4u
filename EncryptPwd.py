from passlib.hash import pbkdf2_sha256

password = "hi"
hashed = pbkdf2_sha256.hash(password)
print(hashed)
if pbkdf2_sha256.verify("hi",hashed):
    print("password matched")
else:
    print("password not matched")

