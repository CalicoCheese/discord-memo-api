from jwt import decode as _decode

from . import SECRET_KEY
from . import ALGORITHM


def decode(token: str) -> dict:
    return _decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM],
    )
