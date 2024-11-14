#!/usr/bin/env python3
"""
Authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    def __init__(self):
        """ Initialises the Auth instances
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return:
            - path <string> or excluded_paths <string>
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - None
        """
        return None
