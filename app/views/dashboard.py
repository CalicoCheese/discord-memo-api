from flask import Blueprint

from app.models import User
from app.models import Memo
from app.utils import resp_json
from app.utils import handle_login

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.get("")
@handle_login
def return_info(user: User):
    memo_count = Memo.query.filter_by(
        owner_id=user.id
    ).count()

    enc_memo_count = Memo.query.filter_by(
        owner_id=user.id,
        encrypted=True
    ).count()

    return resp_json(
        data={
            "creation_date": round(user.creation_date.timestamp()),
            "tos_agree_date": round(user.tos_agree.timestamp()),
            "memo_count": memo_count,
            "enc_memo_count": enc_memo_count,
            "last_login": round(user.last_login.timestamp()),
            "admin": user.is_admin,
        }
    )
