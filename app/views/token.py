from datetime import datetime

from flask import Blueprint

from app import db
from app.token.encode import encode
from app.token.payload import create
from app.utils import handle_login
from app.utils import parse_authorization
from app.utils import resp_json
from discord.tuples import DiscordUser

bp = Blueprint("token", __name__, url_prefix="/token")


@bp.get("")
@handle_login
def regen_token(user):
    user.last_login = datetime.now()
    db.session.commit()

    user_from_token = parse_authorization().get("user", {})
    token = encode(
        payload=create(
            user=DiscordUser(**user_from_token)
        )
    )

    return resp_json(
        code=201,
        data={
            "token": token,
            "is_admin": user.is_admin,
        }
    )
