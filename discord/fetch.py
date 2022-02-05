from json import loads
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError

from . import DISCORD_TOKEN
from . import DISCORD_BASE
from . import USER_AGENT
from . import CLIENT_ID
from . import CLIENT_SECRET
from .tuples import DiscordToken


def current_user(token: DiscordToken):
    request = Request(
        method="GET",
        url=DISCORD_BASE + "/users/@me",
        headers={
            "User-Agent": USER_AGENT,
            "Authorization": f"{token.token_type} {token.access_token}"
        },
    )

    response = urlopen(request)
    json = loads(response.read().decode())

    return json


def token_by_code(code: str):
    payload = "&".join([
        f"client_id={CLIENT_ID}",
        f"client_secret={CLIENT_SECRET}",
        f"code={code}",
        "grant_type=authorization_code"
    ])

    request = Request(
        method="POST",
        url=DISCORD_TOKEN,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=payload.encode(encoding="utf-8")
    )

    try:
        response = urlopen(request)
        json = loads(response.read().decode())
    except HTTPError:
        return {}

    return json
