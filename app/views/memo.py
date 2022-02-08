from flask import Blueprint
from flask import request

from app.utils import handle_login
from app.uilts import resp_json
from app.models import User
from app.models import Memo

bp = Blueprint("memo", __name__, url_prefix="/memo")


@bp.get("/")
@handle_login
def get(user):
    cur = request.args.get("after", None)

    if not cur:
        return resp_json("required argument is not given", 400)

    memos = Memo.query.filter(Memo.id > cur).all()

    payload = [memo.to_json() for memo in memos]
