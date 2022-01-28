from flask import Blueprint
from flask import jsonify
from flask import request

from discord.url import auth
from discord.fetch import token_by_code
from discord.fetch import current_user
from discord.parse import parse_token
from discord.parse import parse_user
from app.token.payload import create
from app.token.encode import encode

bp = Blueprint(
    "auth", __name__,
    url_prefix="/auth"
)


@bp.get("/get-url")
def get_url():
    # endpoint for client
    return jsonify({
        "url": auth()
    })


@bp.get("/callback")
def callback():
    code = request.args.get("code", None)
    if code is None:
        return jsonify({
            "message": "code is empty"
        }), 400

    try:
        token = parse_token(
            json=token_by_code(
                code=code
            )
        )
    except TypeError:
        return jsonify({
            "message": "fail to load access token"
        }), 400

    token = encode(
        payload=create(
            user=parse_user(
                json=current_user(
                    token=token
                )
            )
        )
    )

    return jsonify({
        "message": "login success",
        "token": token
    }), 201
