from flask import request
from flask import jsonify

from app.models import User
from app.models import Memo
from app.token.decode import decode
from app.bot import verify

import re
from time import time
from functools import wraps

token_regex = re.compile(r"Bearer ([a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)")


def resp_json(message: str = "", code: int = 200, data=None) -> tuple:
    return jsonify({
        "meta": {
            "message": message,
            "code": code
        },
        "data": data
    }), code


def get_user_from_discord(discord_id: str) -> User:
    return User.query.filter_by(discord_id=discord_id).first()


def parse_token_from_header(header_value: str) -> str or None:
    if header_value is None:
        header_value = ""

    token_match = token_regex.fullmatch(header_value)

    if token_match:
        return token_match.group(1)
    else:
        return None


def verify_jwt(jwt: dict) -> bool:
    return jwt['time']['iat'] <= time() < jwt['time']['exp']


def parse_authorization() -> dict or tuple:
    auth = request.headers.get("authorization", "")
    token = parse_token_from_header(auth)
    if not token:
        return resp_json(
            message="token is required",
            code=401
        )

    jwt_payload = decode(token=token)

    if not verify_jwt(jwt_payload):
        return resp_json(
            message="token has been expired",
            code=401
        )

    return jwt_payload


def handle_login(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        jwt_payload = parse_authorization()

        if isinstance(jwt_payload, tuple):
            # tuple == resp_json()
            return jwt_payload

        user = get_user_from_discord(jwt_payload["user"]["id"])

        if not user:
            return resp_json(
                message="failed to query a user",
                code=500
            )

        return f(*args, **kwargs, user=user)

    return decorator


def handle_memo(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        id_ = kwargs.get("id_")

        if id_ is None:
            return resp_json(
                message="id is not given",
                code=500
            )

        try:
            id_ = int(id_)
        except ValueError:
            return resp_json(
                message="malformed id value",
                code=400
            )

        memo = Memo.query.filter_by(id=id_).first()

        if memo is None:
            return resp_json("memo not found", 404)
        
        kwargs.update({"memo": memo})
        return f(*args, **kwargs)

    return decorator


def handle_bot_verify(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.headers.get("authorization", "")
        after_bearer = auth[7:]

        if not verify(secret=after_bearer):
            return resp_json(
                message="failed to verify bot",
                code=403
            )

        return f(*args, **kwargs)

    return decorator
