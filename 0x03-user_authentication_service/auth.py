#!/usr/bin/env python3
"""Auth
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    byts = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(byts, salt)
    return hashed_pwd
