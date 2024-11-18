#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """
        Return:
            - User object
        """
        user = User(
                email=email,
                hashed_password=hashed_password
        )
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """ Finds users base on the kwargs provided
        Return:
            - firt row found in the users
        """
        keys = ['email', 'id', 'session_id']
        for key in kwargs:
            if key not in keys:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user base on user id
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError
        keys = ['email', 'id', 'session_id', 'hashed_password', 'reset_token']
        for key, value in kwargs.items():
            if key not in keys:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None
