from jwt import decode as _decode

from . import JWT_SECRET
from . import ALGORITHM


def decode(token: str) -> dict:
    return _decode(
        jwt=token,
        key=JWT_SECRET,
        algorithms=[ALGORITHM],
    )
