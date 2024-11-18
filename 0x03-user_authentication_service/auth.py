#!/usr/bin/env python3
"""Auth
"""
import bcrypt
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    byts = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(byts, salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """
    Return:
        - string representaion of a new uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Args:
            - email <string>
            - password <string>
        return:
            - boolean (valid details or not)
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes_pw = password.encode("utf-8")
            user_hashed_pw = user.hashed_password
            valid = bcrypt.checkpw(bytes_pw, user_hashed_pw)
            return valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create_session(email)
        Args:
            - email <string>
        Return:
            - session id created from uuid object
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
    
    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """Finds user from session id
        Args:
            - session_id <string>
        Return:
            - None if session_id is None or no user is found
            - User object
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
    
    def destroy_session(self, user_id: str) -> None:
        """Sets session id of user to None
        Args:
            - user_id <string>
        Return:
            - None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None
