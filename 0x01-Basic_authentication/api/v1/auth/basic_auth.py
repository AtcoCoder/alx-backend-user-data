#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth


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
