#!/usr/bin/env python3
"""Auth
"""
import bcrypt
from db import DB
from typing import TypeVar
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    byts = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(byts, salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Instance initializer
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        Args:
            - email <string>
            - password <string>
        Return:
            - User object
        """
        try:
            user_exist = self._db.find_user_by(email=email)
            print("user_exist")
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_pwd = _hash_password(password)
        user = self._db.add_user(email=email, hashed_password=hashed_pwd)
        return user
