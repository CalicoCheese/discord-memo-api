from datetime import datetime

from flask import Blueprint
from flask import request
from sqlalchemy import and_

from app import db
from app.models import User
from app.models import Notice
from app.models import TP_NOTICE
from app.utils import resp_json
from app.utils import handle_login
from app.utils import handle_notice

bp = Blueprint("notice", __name__, url_prefix="/notice")


@bp.get("")
def get_list():
    try:
        cur = request.args.get("after", "0")
        cur = int(cur)
    except TypeError:
        cur = 0

    n = Notice.query.with_entities(
        Notice.id,
        Notice.date,
        Notice.title,
    ).filter(
        and_(
            Notice.id > cur,
            Notice.type == TP_NOTICE
        )
    ).limit(20).all()

    payload = [
        dict(
            id=notice.id,
            date=round(notice.date.timestamp()),
            title=notice.title
        ) for notice in n
    ]

    return resp_json(data=payload)


@bp.get("/<int:id_>")
@handle_notice
def get_one(notice: Notice, id_: int):
    return resp_json(data=notice.to_json())


@bp.post("")
@handle_login
def create(user: User):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json

    title = json.get("title", "").strip()[:40]
    if len(title) == 0:
        return resp_json(
            message="공지사항의 제목이 비었습니다.",
            code=400
        )

    text = json.get("text", "").strip()
    if len(text) == 0:
        return resp_json(
            message="공지사항의 본문이 비었습니다.",
            code=400
        )

    n = Notice()
    n.type = TP_NOTICE
    n.date = datetime.now()
    n.title = title
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
@handle_notice
def update(user: User, notice: Notice, id_: int):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json

    notice.date = datetime.now()
    notice.title = json.get("title", notice.title).strip()[:40]
    notice.text = json.get("text", notice.text).strip()

    db.session.commit()

    return resp_json(
        message="저장 성공",
        code=201
    )


@bp.delete("/<int:id_>")
@handle_login
@handle_notice
def delete(user: User, notice: Notice, id_: int):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    db.session.delete(notice)
    db.session.commit()

    return resp_json(
        message="삭제 완료",
        code=200
    )
