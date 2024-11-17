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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Finds user_id for a session
        Return:
            - None if session_id is None
            - None if session_id is not a string
            - user_id for session_id
        """
        if session_id is None or type(session_id) != str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
