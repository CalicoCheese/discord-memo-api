from flask import Blueprint

from app.models import Notice
from app.models import TP_TOS
from app.utils import resp_json

bp = Blueprint("tos", __name__, url_prefix="/tos")


@bp.get("")
def get_latest_tos():
    n = Notice.query.filter_by(
        type=TP_TOS
    ).order_by(
        Notice.id.desc()
    ).first()

    if n is None:
        return resp_json(
            message="등록된 서비스 이용약관이 없습니다.",
            code=400
        )

    return resp_json(
        data=n.to_json()
    )
