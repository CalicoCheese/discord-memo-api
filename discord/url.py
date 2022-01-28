from . import DISCORD_AUTH
from . import CLIENT_ID
from . import OAUTH_SCOPE


def auth():
    return DISCORD_AUTH + \
        "?response_type=code" + \
        f"&client_id={CLIENT_ID}" + \
        f"&scope={OAUTH_SCOPE}"
