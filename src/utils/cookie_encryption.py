from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from src.utils.config import get_config
from typing import Any
import json


def get_key() -> bytes:
    key = get_config("AES_KEY")
    if not key:
        raise ValueError("AES_KEY is not set")

    return bytes.fromhex(key)


def encrypt(data: Any, out_dir: str) -> None:
    key = get_key()

    if not isinstance(data, str):
        data = json.dumps(data)
    data = data.encode()

    cipher = AES.new(key, AES.MODE_CBC)  # type: ignore
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    with open(out_dir, "wb") as f:
        f.write(cipher.iv)
        f.write(ciphered_data)


def decrypt(file_dir: str) -> Any | list[Any]:
    with open(file_dir, "rb") as f:
        iv = f.read(16)
        ciphered_data = f.read()

    key = get_key()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # type: ignore
    data = unpad(cipher.decrypt(ciphered_data), AES.block_size)

    try:
        return json.loads(data.decode())
    except json.JSONDecodeError:
        return data.decode()
