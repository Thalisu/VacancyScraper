from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from src.utils.config import get_config
import json


def get_key():
    return bytes.fromhex(get_config("AES_KEY"))


def encrypt(data, out_dir):
    key = get_key()

    if not isinstance(data, str):
        data = json.dumps(data)
    data = data.encode()

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    with open(out_dir, "wb") as f:
        f.write(cipher.iv)
        f.write(ciphered_data)


def decrypt(file_dir):
    with open(file_dir, "rb") as f:
        iv = f.read(16)
        ciphered_data = f.read()

    key = get_key()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    data = unpad(cipher.decrypt(ciphered_data), AES.block_size)

    try:
        return json.loads(data.decode())
    except json.JSONDecodeError:
        return data.decode()
