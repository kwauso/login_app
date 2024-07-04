import hashlib
import string
import random

def make_hash_from_password(password, add, n):
    password = password + add
    for i in range(n):
        password = hashlib.sha256(password.encode())
        password = password.hexdigest()
    return password

def make_salt(n):
    salt = ""
    for i in range(n):
        salt += random.choice(string.ascii_letters)
    return salt

def make_pepper(n):
    pepper = ""
    for i in range(n):
        pepper += random.choice(string.ascii_letters)
    return pepper