from flask import Blueprint
from flask import request

from discord.url import invite
from app import db
from app.models import User
from app.models import Memo
from app.bot.tuples import BotRequest
from app.utils import resp_json
from app.utils import handle_bot_verify
from app.aes import encrypt

bp = Blueprint("bot", __name__, url_prefix="/bot")


@bp.get("/get-url")
def get():
    return resp_json(
        data={
            "invite": invite()
        }
    )


@bp.post("")
@handle_bot_verify
def create():
    json = BotRequest(**request.json)

    if len(json.text.strip()) == 0:
        return resp_json(
            code=400,
            message="빈 메모는 저장 할 수 없습니다."
        )

    u = User.query.filter_by(
        discord_id=json.discord_id
    ).first()

    if u is None:
        return resp_json(
            message="등록되지 않은 유저 입니다.",
            code=400,
        )

    text = json.text.strip()
    if len(text) == 0:
        return resp_json(
            message="빈 메모는 생성 할 수 없습니다.",
            code=400
        )

    m = Memo()
    m.owner_id = u.id
    m.text = encrypt(text=text)
    m.encrypted = False

    db.session.add(m)
    db.session.commit()

    return resp_json(
        message="메모 등록 성공",
        code=201,
    )
