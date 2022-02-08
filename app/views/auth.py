from flask import Blueprint
from flask import request

from discord.url import auth
from discord.fetch import token_by_code
from discord.fetch import current_user
from discord.parse import parse_token
from discord.parse import parse_user
from app.token.payload import create
from app.token.encode import encode
from app.utils import resp_json

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/get-url")
def get_url():
    # endpoint for client
    return resp_json(
        data={
            "auth": auth()
        }
    )


@bp.get("/callback")
def callback():
    code = request.args.get("code", None)
    if code is None:
        return resp_json(
            message="code is empty",
            code=400
        )

    try:
        token = parse_token(
            json=token_by_code(
                code=code
            )
        )
    except TypeError:
        return resp_json(
            message="fail to load access token",
            code=400
        )

    payload, exp = create(
        user=parse_user(
            json=current_user(
                token=token
            )
        )
    )

    return resp_json(
        message="login success",
        code=201,
        data={
            "token": encode(payload=payload),
            "exp": exp
        }
    )
