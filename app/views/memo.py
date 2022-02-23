from datetime import datetime

from flask import Blueprint
from flask import request
from sqlalchemy import and_

from app import db
from app.utils import handle_login
from app.utils import handle_memo
from app.utils import resp_json
from app.models import Memo
from app.aes import encrypt

bp = Blueprint("memo", __name__, url_prefix="/memo")


@bp.get("")
@handle_login
def get(user):
    cur = request.args.get("after")

    if not cur:
        return resp_json(
            message="required argument is not given",
            code=400
        )

    try:
        cur = int(cur)
    except ValueError:
        return resp_json(
            message="malformed after value",
            code=400
        )

    memos = Memo.query.filter(
        and_(
            Memo.id > cur,
            Memo.owner_id == user.id
        )
    ).limit(10).all()

    payload = [memo.to_json() for memo in memos]

    return resp_json(data=payload)


@bp.get("/<int:id_>")
@handle_login
@handle_memo
def get_one(user, memo: Memo, id_: int):
    return resp_json(data=memo.to_json())


@bp.delete("/<int:id_>")
@handle_login
@handle_memo
def delete(user, memo: Memo, id_: int):
    db.session.delete(memo)
    db.session.commit()

    # return resp_json("successfully deleted the memo")
    return resp_json(
        message="성공적으로 메모를 삭제했습니다.",
        code=200
    )


@bp.put("/<int:id_>")
@handle_login
@handle_memo
def edit(user, memo: Memo, id_: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return resp_json(
            message="malformed json payload",
            code=400
        )

    text = payload.get("text", "").strip()
    if len(text) == 0:
        db.session.delete(memo)
        db.session.commit()

        return resp_json(
            message="메모를 삭제했습니다.",
            code=200
        )

    encrypted = payload.get("encrypted", False)
    if not isinstance(encrypted, bool):
        return resp_json(
            message="암호화 여부의 형식이 올바르지 않습니다.",
            code=400
        )

    now = datetime.now()
    edit_timestamp = payload.get("edit", memo.edit)

    if memo.get_edit_timestamp() != edit_timestamp:
        memo.text = memo.get_text()

        date_now = now.strftime("%Y/%m/%d %H:%M:%S")
        text = f"{memo.text}\n\n" \
               f"=== Edited on {date_now} ===\n\n" \
               f"{text}"

    memo.text = encrypt(text=text)
    memo.edit = now
    memo.encrypted = encrypted

    db.session.commit()

    return resp_json(
        # message="successfully edited the memo",
        message="성공적으로 메모를 수정했습니다.",
        code=201
    )


@bp.post("")
@handle_login
def create(user):
    payload = request.get_json(silent=True)

    text = payload.get("text", "").strip()
    if len(text) == 0:
        return resp_json(
            message="빈 메모는 생성 할 수 없습니다.",
            code=400
        )

    encrypted = payload.get("encrypted", False)
    if not isinstance(encrypted, bool):
        return resp_json(
            message="암호화 여부의 형식이 올바르지 않습니다.",
            code=400
        )

    m = Memo()
    m.owner_id = user.id
    m.text = encrypt(text=text)
    m.encrypted = encrypted

    db.session.add(m)
    db.session.commit()

    return resp_json(
        message="메모를 생성했습니다.",
        code=201
    )


@bp.delete("")
@handle_login
def delete_all_memo(user):
    Memo.query.filter_by(
        owner_id=user.id
    ).delete()

    db.session.commit()

    return resp_json(
        message="모든 메모가 삭제되었습니다.",
        code=200
    )
