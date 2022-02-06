from flask import request
from flask import jsonify

from app.models import User
from app.token.decode import decode

import re
from time import time
from functools import wraps

token_regex = re.compile(r"Bearer ([a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9])")


def resp_json(message="", code=200, data=None):
    return jsonify({
        "meta": {
            "message": message,
            "code": code
        },
        "data": data
    }), code


def get_user_from_discord(discord_id):
    return User.query.filter_by(discord_id=discord_id).first()


def parse_token_from_header(headerval):
    # TODO: check if rsplit is obsolete. Added for the safety measure
    headerval = headerval.rstrip()
    token_match = token_regex.fullmatch(headerval)

    if token_match:
        return token_match.group(1)
    else:
        return None


def verify_jwt(jwt):
    if jwt['time']['exp'] < time():
        return False

    else:
        return True


def handle_login(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.headers.get("authorization")
        token = parse_token_from_header(auth)
        if not token:
            return resp_json("token is required", 401)

        jwt_payload = decode(token)

        if not verify_jwt(jwt_payload):
            return resp_json("token has been expired", 401)

        user = get_user_from_discord(jwt_payload["user"]["id"])

        if not user:
            return resp_json("failed to query a user", 500)

        return f(*args, **kwargs, user=user)

    return decorator
