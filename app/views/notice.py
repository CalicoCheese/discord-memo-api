from flask import Blueprint

from app.utils import resp_json

bp = Blueprint("notice", __name__, url_prefix="/notice")


@bp.get("")
def get_latest():
    return resp_json(
        message="Not Implemented",
        code=400
    )


@bp.get("/<int:notice_id>")
def get_custom(notice_id: int):
    return resp_json(
        message="Not Implemented",
        code=400,
        data={
            "id": notice_id
        }
    )


@bp.post("")
def create():
    return resp_json(
        message="Not Implemented",
    )


@bp.post("/<int:notice_id>")
def update(notice_id: int):
    return resp_json(
        message="Not Implemented",
        code=400,
        data={
            "id": notice_id
        }
    )
