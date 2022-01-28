from .secret_key import SECRET_KEY as _SECRET_KEY

SECRET_KEY = _SECRET_KEY.hex()
ALGORITHM = "HS256"
