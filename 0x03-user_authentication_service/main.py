#!/usr/bin/env python3
"""Main
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register user
    """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post("http://0.0.0.0:5000/users", data=payload)
    assert res.status_code == 200
    ex_message = {"email": email, "message": "user created"}
    message = res.json()
    assert ex_message == message


def log_in_wrong_password(email: str, password: str) -> None:
    """log with wrong password test
    """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post("http://0.0.0.0:5000/sessions", data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """login with right credentials test
    """
    payload = {
        "email": email,
        "password": password
    }
    res = requests.post("http://0.0.0.0:5000/sessions", data=payload)
    ex_message = {"email": email, "message": "logged in"}
    assert res.status_code == 200
    message = res.json()
    session_id = res.cookies.get("session_id")
    assert message == ex_message
    return session_id


def profile_unlogged() -> None:
    """checking if profile is logged in
    """
    res = requests.get("http://0.0.0.0:5000/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile logged in
    """
    cookies = {
        "session_id": session_id
    }
    res = requests.get("http://0.0.0.0:5000/profile", cookies=cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """log out test
    """
    cookies = {
        "session_id": session_id
    }
    res = requests.delete("http://0.0.0.0:5000/sessions", cookies=cookies)
    assert res.status_code == 200
    assert {"message": "Bienvenue"} == res.json()


def reset_password_token(email: str) -> str:
    """reset_password_test
    """
    payload = {
        "email": email
    }
    res = requests.post("http://0.0.0.0:5000/reset_password", data=payload)
    assert res.status_code == 200
    return res.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update_password_test
    """
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put("http://0.0.0.0:5000/reset_password", data=payload)
    assert res.status_code == 200


if __name__ == "__main__":

    # register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
