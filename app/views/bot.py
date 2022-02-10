from flask import Blueprint

from discord.url import invite
from app.utils import resp_json

bp = Blueprint("bot", __name__, url_prefix="/bot")


@bp.get("/get-url")
def get():
    return resp_json(
        data={
            "invite": invite()
        }
    )


@bp.post("")
def create():
    return resp_json(
        code=500,
        message="not implemented"
    )
