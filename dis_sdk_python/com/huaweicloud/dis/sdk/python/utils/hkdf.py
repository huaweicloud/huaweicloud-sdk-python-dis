#!/usr/bin/python
# -*- coding:utf-8 -*-

import hmac
import hashlib


def extract(ikm, salt):
    if isinstance(salt, str):
        salt = salt.encode('utf-8')
    if isinstance(ikm, str):
        ikm = ikm.encode('utf-8')
    return hmac.new(salt, ikm, digestmod=hashlib.sha256).digest()


def expand(prk, info):
    if isinstance(info, str):
        info = info.encode('utf-8')
    result = info + b'\x01'
    return hmac.new(prk, result, digestmod=hashlib.sha256).digest()


def getDerKey(ak, sk, info, algorithm):
    if not ak or not sk:
        raise ValueError("The " + ("AK" if not ak else "SK") + " is empty.")
    if algorithm.lower() == "hmacsha256":
        tmp_key = extract(sk.encode('utf-8'), ak.encode('utf-8'))
        derived_key = expand(tmp_key, info.encode('utf-8'))
        return derived_key.hex()
    else:
        raise ValueError("Unsupported algorithm: " + algorithm)