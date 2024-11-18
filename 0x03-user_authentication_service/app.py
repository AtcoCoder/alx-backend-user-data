#!/usr/bin/env python3
"""App
"""
from flask import Flask, jsonify, request
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
    """Registers user
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
