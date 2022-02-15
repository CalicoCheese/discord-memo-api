from datetime import datetime

from flask import Blueprint
from flask import request
from sqlalchemy import and_

from app import db
from app.models import User
from app.models import Notice
from app.models import TP_TOS
from app.utils import resp_json
from app.utils import handle_login
from app.utils import handle_tos

bp = Blueprint("tos", __name__, url_prefix="/tos")


@bp.get("/code")
def get_code():
    n = Notice.query.with_entities(
        Notice.id,
        Notice.date,
    ).filter_by(
        type=TP_TOS
    ).all()

    payload = [
        dict(
            id=notice.id,
            date=round(notice.date.timestamp()),
        ) for notice in n
    ]

    return resp_json(data=payload)


@bp.get("/<int:id_>")
@handle_tos
def get_one(tos: Notice, id_: int):
    return resp_json(data=tos.to_json())


@bp.post("")
@handle_login
def create(user: User):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json

    text = json.get("text", "").strip()
    if len(text) == 0:
        return resp_json(
            message="서비스 이용약관의 본문이 비었습니다.",
            code=400
        )

    n = Notice()
    n.type = TP_TOS
    n.date = datetime.now()
    n.title = ""
    n.text = text

    db.session.add(n)
    db.session.commit()

    return resp_json(
        message="생성 완료",
        code=201,
        data={
            "id": n.id
        },
    )


@bp.post("/<int:id_>")
@handle_login
@handle_tos
def update(user: User, tos: Notice, id_: int):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json

    tos.date = datetime.now()
    tos.text = json.get("text", tos.text).strip()

    db.session.commit()

    return resp_json(
        message="저장 성공",
        code=201
    )


@bp.delete("/<int:id_>")
@handle_login
@handle_tos
def delete(user: User, tos: Notice, id_: int):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    db.session.delete(tos)
    db.session.commit()

    return resp_json(
        message="삭제 완료",
        code=200
    )
