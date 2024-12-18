#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Subclass of the Auth class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """
        Return:
            - Base64 part of the Authorization header for a
            Basic Authentication
        """
        if authorization_header is None or\
                type(authorization_header) != str or\
                not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """
        Return:
            - decoded value of a Base64 string
            base64_authorization_header
        """
        if base64_authorization_header is None or\
                type(base64_authorization_header) != str:
            return None
        try:
            decoded_va = base64.b64decode(base64_authorization_header.encode())
            return decoded_va.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Return:
            - user email and user password
        """
        if not decoded_base64_authorization_header or\
                type(decoded_base64_authorization_header) != str or\
                ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """
        Return:
            - None if user_email is None or not a string
            - None if user_pwd is None or not a string
            - None if your database (file) is doesn't contain
            any User instance with email to user_email
            - None if user_pwd is not the password of the User
            instance found
            - Otherwise, User instance
        """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - Instance of User for a request
        """
        auth_header = self.authorization_header(request)
        credentials = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(credentials)
        email, pwd = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(email, pwd)
