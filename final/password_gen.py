from random import randint
import string
chars = list(string.ascii_uppercase)
password = []
while chars:
    password.append(chars.pop(randint(0, len(chars) - 1)))
password = ''.join(password)
print(password)
