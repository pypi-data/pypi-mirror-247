# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     cipher
   Description :
   Author :       yangzhixiang
   date：          2020/9/18
-------------------------------------------------
"""

import logging
import base64
from Cryptodome.Cipher import AES, DES
from Cryptodome import Random

BLOCK_SIZE = 16
LOGGER = logging.getLogger(__name__)


def padding(s: str, block_size: int = 8):
    return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)


def un_padding(s):
    return s[0:-ord(s[-1])]


class DESCipher:
    def __int__(self, key):
        if len(key) < 8:
            raise ValueError("invalid des key length")
        self.key = key[:8]

    def encrypt(self, raw) -> str:
        cipher = DES.new(self.key)
        msg = cipher.encrypt(padding(raw, DES.block_size))
        return base64.encodebytes(msg).decode("utf-8")

    def decrypt(self, enc: str) -> str:
        msg = base64.decodebytes(enc.encode("utf-8"))
        cipher = DES.new(self.key)
        return cipher.decrypt(msg).decode("utf-8")


class AESCipher:

    def __init__(self, key, mode=AES.MODE_CBC, iv=None, block_size=AES.block_size, to_base64=False):
        if isinstance(key, str):
            self.key = key.encode("utf-8")
        else:
            self.key = key
        self.iv = iv or Random.new().read(AES.block_size)
        self.mode = mode
        self.block_size = block_size
        self.to_base64 = to_base64

    def encrypt(self, raw) -> str:
        if self.mode == AES.MODE_CBC:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        cipher_text = cipher.encrypt(padding(raw, self.block_size).encode("utf-8"))
        if self.to_base64:
            cipher_text = base64.b16encode(cipher_text)
        return cipher_text

    def decrypt(self, enc) -> str:
        if self.to_base64:
            enc = base64.b16decode(enc)
        if self.mode == AES.MODE_CBC:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        plain_text = cipher.decrypt(enc)
        padding_num = plain_text[-1]
        text = plain_text[0, len(plain_text) - padding_num]
        return str(text, "utf-8")
