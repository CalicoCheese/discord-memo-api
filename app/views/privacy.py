from flask import Blueprint

from app.models import Notice
from app.models import TP_PRIVACY
from app.utils import resp_json

bp = Blueprint("privacy", __name__, url_prefix="/privacy")


@bp.get("")
def get_latest_privacy():
    n = Notice.query.filter_by(
        type=TP_PRIVACY
    ).order_by(
        Notice.id.desc()
    ).first()

    if n is None:
        return resp_json(
            message="등록된 개인정보 처리방침이 없습니다.",
            code=400
        )

    return resp_json(
        data=n.to_json()
    )
