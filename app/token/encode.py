from jwt import encode as _encode

from . import JWT_SECRET
from . import ALGORITHM


def encode(payload: dict) -> str:
    return _encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=ALGORITHM,
    )
