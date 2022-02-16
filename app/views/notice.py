from datetime import datetime

from flask import Blueprint
from flask import request

from app import db
from app.models import User
from app.models import Notice
from app.models import TP_LIST
from app.utils import resp_json
from app.utils import handle_login
from app.utils import handle_notice

bp = Blueprint("notice", __name__, url_prefix="/notice")


@bp.get("")
def get_list():
    try:
        page = request.args.get("page", "0")
        page = int(page)

        if page < 1:
            page = 1
    except TypeError:
        page = 1

    n = Notice.query.with_entities(
        Notice.id,
        Notice.type,
        Notice.date,
        Notice.title,
    ).order_by(
        Notice.id.desc()
    ).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    payload = {
        "page": {
            "max": n.pages,
            "this": n.page
        },
        "notice": [
            dict(
                id=notice.id,
                type=notice.type,
                date=round(notice.date.timestamp()),
                title=notice.title
            ) for notice in n.items
        ]
    }

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

    try:
        type_ = int(json.get("type"))
        if type_ not in TP_LIST:
            raise ValueError
    except (ValueError, TypeError):
        return resp_json(
            message="형식이 올바르지 않습니다.",
            code=400
        )

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
    n.type = type_
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

    try:
        type_ = int(json.get("type"))
        if type_ not in TP_LIST:
            raise ValueError
    except (ValueError, TypeError):
        return resp_json(
            message="형식이 올바르지 않습니다.",
            code=400
        )

    notice.date = datetime.now()
    notice.type = json.get("type", notice.type)
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
