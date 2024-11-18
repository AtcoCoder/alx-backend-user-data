#!/usr/bin/env python3
"""App
"""
from flask import Flask, jsonify, request
from flask import make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home() -> str:
    """Returns simple message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """Registers user"
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        message = {"email": email, "message": "user created"}
        return jsonify(message)
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Logs user in
    """
    email = request.form.get('email')
    password = request.form.get('password')
    login_valid = AUTH.valid_login(email, password)
    if login_valid:
        session_id = AUTH.create_session(email)
        res = make_response({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")