#!/usr/bin/env python3
"""
Authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Authencation class
    """
    def __init__(self):
        """ Initialises the Auth instances
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return:
            - path <string> or excluded_paths <string>
        """
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None or path not in excluded_paths and \
                path + '/' not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - None
        """
        if request:
            auth = request.headers.get('Authorization')
            if auth is None:
                return None
            return auth
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - None
        """
        return None
