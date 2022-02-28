from werkzeug.exceptions import HTTPException

from app.utils import resp_json


def f(x: HTTPException, message: str):
    return resp_json(
        message=message,
        code=x.code,
        data={
            "cat": f"https://http.cat/{x.code}.jpg"
        }
    )


emap = {
    # client error
    401: lambda x: f(x, "인증이 필요한 페이지 입니다."),
    403: lambda x: f(x, "접근 권한이 없습니다."),
    404: lambda x: f(x, "페이지를 찾을 수 없음"),

    # server error
    500: lambda x: f(x, "서버에서 알 수 없는 오류가 발생했습니다."),
}
