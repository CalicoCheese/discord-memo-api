from time import time

from flask import Blueprint
from flask import request

from app import db
from app.models import User
from app.utils import handle_login
from app.utils import resp_json

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/users")
@handle_login
def get_users(user: User):
    if not user.is_admin:
        return resp_json(
            message="당신은 관리자가 아닙니다.",
            code=400
        )

    try:
        after = int(request.args.get("after", None))
    except (ValueError, TypeError):
        return resp_json(
            message="올바르지 않은 요청",
            code=400
        )

    users = User.query.with_entities(
        User.id,
        User.is_admin,
        User.creation_date,
        User.tos_agree_date,
        User.privacy_agree_date,
        User.last_login,
    ).filter(
        User.id > after
    ).limit(20).all()

    return resp_json(
        data=[
            dict(
                id=u.id,
                admin=u.is_admin,
                creation_date=round(u.creation_date.timestamp()),
                tos_agree_date=round(u.tos_agree_date.timestamp()),
                privacy_agree_date=round(u.privacy_agree_date.timestamp()),
                last_login=round(u.last_login.timestamp()),
                flow=round(time() - u.last_login.timestamp()),
            ) for u in users
        ]
    )
