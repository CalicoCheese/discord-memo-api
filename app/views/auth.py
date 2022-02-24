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
from app.models import TP_TOS
from app.models import TP_PRIVACY

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

    u = User.query.filter_by(
        discord_id=user.id
    ).first()

    token = encode(
        payload=create(
            user=user
        )
    )

    if u is None:
        return resp_json(
            message="사용자 등록이 필요합니다.",
            code=200,
            data={
                "token": token
            }
        )

    u.last_login = datetime.now()
    db.session.commit()

    return resp_json(
        message="로그인 성공",
        code=201,
        data={
            "token": token
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
        type=TP_TOS
    ).order_by(
        Notice.id.desc()
    ).first()

    privacy = Notice.query.filter_by(
        type=TP_PRIVACY
    ).order_by(
        Notice.id.desc()
    ).first()

    message = ""

    def p(text: str) -> str:
        return f"<p>{text}</p>"

    if tos is None:
        flag_t = None
    else:
        flag_t = tos.date == user.tos_agree_date
        if not flag_t:
            message += p("서비스 이용약관이 변경 되었습니다.")

    if privacy is None:
        flag_p = None
    else:
        flag_p = privacy.date == user.privacy_agree_date
        if not flag_p:
            message += p("개인정보 처리방침이 변경 되었습니다.")

    if flag_t is None or flag_p is None:
        agree = None
        message = p("약관이 등록되지 않아 서비스를 이용 할 수 없습니다.")
    else:
        agree = (flag_p and flag_t) is True

    # 관리자 여부
    is_admin = user.is_admin

    if not is_admin:
        # 이 유저가 관리자가 아닌경우
        return resp_json(
            message=message,
            code=200,
            data=dict(
                agree=agree,
                admin=is_admin
            )
        )
    else:
        # 이 유저가 관리자인 경우

        # 근데 만약 약관이 등록되지 않았다면
        if agree is None:
            message = p("약관을 등록하지 않아 서비스를 이용 할 수 없습니다.")

        return resp_json(
            message=message,
            code=200,
            data=dict(
                agree=agree,
                admin=is_admin
            )
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

    if user is None:
        user = User()
        user.discord_id = token['user']['id']
        user.is_admin = False

        db.session.add(user)

    json = request.get_json(silent=True)

    try:
        tos = int(json.get("tos"))
        tos = datetime.fromtimestamp(tos)
    except TypeError:
        return resp_json(
            message="서비스 이용약관의 날짜가 올바르지 않습니다.",
            code=400,
        )

    try:
        privacy = int(json.get("privacy"))
        privacy = datetime.fromtimestamp(privacy)
    except TypeError:
        return resp_json(
            message="개인정보 처리방침의 날짜가 올바르지 않습니다.",
            code=400,
        )

    user.tos_agree_date = tos
    user.privacy_agree_date = privacy

    db.session.commit()

    return resp_json(
        message="약관 동의 정보가 업데이트 되었습니다.",
        code=200,
    )


@bp.delete("")
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
