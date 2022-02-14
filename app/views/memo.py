from datetime import datetime

from flask import Blueprint
from flask import request
from sqlalchemy import and_

from app import db
from app.utils import handle_login
from app.utils import handle_memo
from app.utils import resp_json
from app.models import Memo

bp = Blueprint("memo", __name__, url_prefix="/memo")


@bp.get("")
@handle_login
def get(user):
    cur = request.args.get("after")

    if not cur:
        return resp_json("required argument is not given", 400)

    try:
        cur = int(cur)
    except ValueError:
        return resp_json("malformed after value", 400)

    memos = Memo.query.filter(
        and_(
            Memo.id > cur,
            Memo.owner_id == user.id
        )
    ).limit(10).all()

    payload = [memo.to_json() for memo in memos]

    return resp_json(data=payload)


@bp.get("/<id_>")
@handle_login
@handle_memo
def get_one(user, memo, id_):
    return resp_json(data=memo.to_json())


@bp.delete("/<id_>")
@handle_login
@handle_memo
def delete(user, memo, id_):
    db.session.delete(memo)
    db.session.commit()

    return resp_json("successfully deleted the memo")


@bp.put("/<id_>")
@handle_login
@handle_memo
def edit(user, memo, id_):
    payload = request.get_json(silent=True)

    if payload is None:
        return resp_json("malformed json payload", 400)

    now = datetime.now()

    if memo.get_edit_timestamp() != payload['edit']:
        strftime = now.strftime("%Y/%m/%d %H:%M:%S")
        memo.text = f"{memo.text}\n\n" \
                    f"=== Edited on {strftime} ===\n\n" \
                    f"{payload['text']}"
    else:
        memo.text = payload['text']

    memo.edit = now

    db.session.commit()

    return resp_json(
        message="successfully edited the memo",
        code=201
    )
