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
        Notice.type,
        Notice.date,
        Notice.title,
    ).order_by(
        Notice.id.desc()
    ).filter(
        and_(
            Notice.id > cur,
            Notice.type == TP_NOTICE
        )
    ).limit(10).all()

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
def get_one(notice: Notice, id_: int, type_=TP_NOTICE):
    return resp_json(data=notice.to_json())


@bp.post("")
@handle_login
def create(user: User):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json
    return resp_json(
        data={
            "json": json
        }
    )


@bp.post("/<int:id_>")
@handle_login
@handle_notice
def update(user: User, notice: Notice, id_: int, type_=TP_NOTICE):
    if not user.is_admin:
        return resp_json(code=403, message="당신은 관리자가 아닙니다.")

    json = request.json
    return resp_json(
        data={
            "db": notice.to_json(),
            "json": json
        }
    )
