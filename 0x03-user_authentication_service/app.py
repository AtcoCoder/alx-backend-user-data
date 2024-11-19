#!/usr/bin/env python3
"""App
"""
from flask import Flask, jsonify, request, url_for
from flask import make_response, abort, redirect
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


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Logouts user
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("home"))
    return abort(403)


@app.route("/profile")
def profile() -> str:
    """Finds user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    return abort(403)


@app.route("/reset_password", methods=["POST"])
def reset_password() -> str:
    """Reset password route
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
