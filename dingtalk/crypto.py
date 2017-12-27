#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/12/25 下午3:11
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : crypto.py
# @Software: PyCharm
import uuid
import struct
import base64
import hashlib
from Crypto.Cipher import AES

__author__ = 'blackmatrix'


def generate_signature(access_token: str, encrypt_text: str, timestamp: str, nonce: str):
    """
    创建签名
    :param access_token:
    :param encrypt_text:
    :param timestamp:
    :param nonce:
    :return:
    """
    sign = hashlib.sha1(''.join(sorted([access_token, timestamp, nonce, encrypt_text])).encode())
    return sign.hexdigest()


def check_signature(access_token, data, signature, timestamp, nonce):
    sign = generate_signature(access_token, data, timestamp, nonce)
    return sign == signature


def pkcs7_unpad(text):
    """
    删除 PKCS#7 方式填充的字符串
    :param text:
    :return: str
    """
    return text[0: text.index((text[-1]))]


def pkcs7_pad(multiple, text):
    """
    :param multiple:
    :param text: str
    :return: str
    """
    return text + (multiple - len(text) % multiple) * chr(multiple - len(text) % multiple)


def decrypt_text(aes_key, ciphertext):
    aes_key = base64.b64decode(aes_key + '=')
    ciphertext = base64.b64decode(ciphertext)
    aes = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
    raw = aes.decrypt(ciphertext)
    raw = pkcs7_unpad(raw)
    return raw


def decrypt(aes_key, ciphertext):
    raw = decrypt_text(aes_key, ciphertext)
    buf = raw[:16].decode().strip()
    length = struct.unpack('!i', raw[16:20])[0]
    msg = raw[20: 20 + length].decode().strip()
    key = raw[20 + length:].decode().strip()
    return msg, key, buf


def encrypt_text(aes_key, plaintext):
    aes_key = base64.b64decode(aes_key + '=')
    aes = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
    ciphertext = pkcs7_pad(16, plaintext)
    ciphertext = aes.encrypt(ciphertext)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def encrypt(aes_key, plaintext, key, buf=None):
    buf = buf or str(uuid.uuid4()).replace('-', '')
    buf = buf[:16]
    length = struct.pack('!i', len(plaintext)).decode()
    ciphertext = encrypt_text(aes_key, buf + length + plaintext + key)
    return ciphertext

if __name__ == '__main__':
    pass