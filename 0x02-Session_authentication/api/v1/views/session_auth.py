#!/usr/bin/env python3
"""Session_auth
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login() -> str:
    """POST /auth_session/login
    """
    print("begining")
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
        user = users[0]
    except Exception as error:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    print("Password is valid")
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = make_response(user.to_json())
    res.set_cookie(getenv("SESSION_NAME"), session_id)
    return res


@app_views.route(
        "/auth_session/logout",
        methods=["DELETE"],
        strict_slashes=False
)
def destroy_session() -> str:
    """DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if not destroyed:
        return abort(404)
    return jsonify({}), 200
