from datetime import datetime

from flask import Blueprint
from flask import request

from discord.url import auth
from discord.fetch import token_by_code
from discord.fetch import current_user
from discord.parse import parse_token
from discord.parse import parse_user
from app.token.payload import create
from app.token.encode import encode
from app.utils import resp_json
from app.utils import handle_login
from app.utils import parse_authorization

from app import db
from app.models import User
from app.models import Memo
from app.models import Notice

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/get-url")
def get_url():
    # endpoint for client
    return resp_json(
        data={
            "auth": auth()
        }
    )


@bp.get("/callback")
def callback():
    code = request.args.get("code", None)
    if code is None:
        return resp_json(
            message="code is empty",
            code=400
        )

    try:
        token = parse_token(
            json=token_by_code(
                code=code
            )
        )
    except TypeError:
        return resp_json(
            message="fail to load access token",
            code=400
        )

    user = parse_user(
        json=current_user(
            token=token
        )
    )

    payload, exp = create(
        user=user
    )

    u = User.query.filter_by(
        discord_id=user.id
    ).first()

    if u is None:
        return resp_json(
            message="사용자 등록이 필요합니다.",
            code=200,
            data={
                "token": encode(payload=payload),
                "exp": exp
            }
        )

    return resp_json(
        message="로그인 성공",
        code=201,
        data={
            "token": encode(payload=payload),
            "exp": exp
        }
    )


@bp.get("/check")
def check():
    token = parse_authorization()
    if isinstance(token, tuple):
        return token

    user = User.query.filter_by(
        discord_id=token['user']['id']
    ).first()

    if user is None:
        return resp_json(
            message="등록되지 않은 유저입니다.",
            code=404,
        )

    tos = Notice.query.filter_by(
        type=2
    ).order_by(
        Notice.id.desc()
    ).first()

    passed = False
    skipped = False

    if tos is None:
        skipped = True
    else:
        passed = tos.date <= user.tos_agree

    return resp_json(
        message="조회 성공",
        code=200,
        data={
            "tos_agree": user.tos_agree,
            "passed": passed,
            "skipped": skipped,
            "admin": user.is_admin
        }
    )


@bp.post("/update")
def update():
    token = parse_authorization()
    if isinstance(token, tuple):
        return token

    try:
        user = User.query.filter_by(
            discord_id=token['user']['id']
        ).first()
    except KeyError:
        return resp_json(
            message="인증 토큰이 올바르지 않습니다.",
            code=401,
        )

    if user is not None:
        user.tos_agree = datetime.now()
        db.session.commit()

        return resp_json(
            message="이미 등록된 유저입니다.",
            code=400,
            data=True
        )

    u = User()
    u.discord_id = token['user']['id']
    u.is_admin = False
    u.tos_agree = datetime.now()

    db.session.add(u)
    db.session.commit()

    return resp_json(
        message="사용자 등록이 완료되었습니다.",
        code=200,
    )


@bp.delete("/@me")
@handle_login
def delete_me(user: User):
    c = Memo.query.filter_by(
        owner_id=user.id
    ).count()

    if c != 0:
        return resp_json(
            message="계정을 삭제하려면 모든 메모를 삭제해야 합니다.",
            code=400
        )

    db.session.delete(user)
    db.session.commit()

    return resp_json(
        message="등록된 계정을 삭제했습니다.",
        code=200
    )
