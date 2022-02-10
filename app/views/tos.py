from flask import Blueprint

from app.utils import resp_json

bp = Blueprint("tos", __name__, url_prefix="/tos")


@bp.get("")
def get_latest():
    return resp_json(
        message="Not Implemented",
        code=400
    )


@bp.get("/<int:tos_id>")
def get_custom(tos_id: int):
    return resp_json(
        message="Not Implemented",
        code=400,
        data={
            "id": tos_id
        }
    )


@bp.post("")
def create():
    return resp_json(
        message="Not Implemented",
    )


@bp.post("/<int:tos_id>")
def update(tos_id: int):
    return resp_json(
        message="Not Implemented",
        code=400,
        data={
            "id": tos_id
        }
    )
