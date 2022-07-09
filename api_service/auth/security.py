# encoding: utf-8

import json
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token
from api_service.api.exceptions import UnauthorizedException

from api_service.models import User


def authenticate(username: str, password: str) -> json:
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return {"access_token": create_access_token(identity=user.id)}
    else:
        raise UnauthorizedException("Username or password incorrect")


def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)
