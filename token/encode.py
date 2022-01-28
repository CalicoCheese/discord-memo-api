from jwt import encode as _encode

from . import SECRET_KEY
from . import ALGORITHM


def encode(payload: dict) -> str:
    return _encode(
        payload=payload,
        secrets=SECRET_KEY,
        algorithm=ALGORITHM,
    )
