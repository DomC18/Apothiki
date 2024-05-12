import random as rr
import constants

def generate_random_password(length=20):
    password = ""
    for _ in range(length):
        password += rr.choice(constants.PASSWORD_CHARS)
    return password

