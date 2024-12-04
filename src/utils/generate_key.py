from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import sys


salt = get_random_bytes(32)
try:
    password = sys.argv[1]
except IndexError:
    print("Please specify a password")
    sys.exit(0)

key = PBKDF2(password, salt, dkLen=32)

print(key.hex())
