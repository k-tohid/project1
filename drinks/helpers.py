import random

def create_uuid():
    letters = '1234567890abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(5))
