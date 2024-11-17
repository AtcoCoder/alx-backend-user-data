#!/usr/bin/env python3
""" Session_auth
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Authenciation class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session id for a user_id
        Return:
            - None if user_id is  None
            - None if user_id is not a string
            - Otherwise session id generated
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
