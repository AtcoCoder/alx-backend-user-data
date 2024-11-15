#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth
import base64


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
            return None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password
