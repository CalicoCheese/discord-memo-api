from secrets import token_bytes


def get() -> str:
    try:
        with open(".JWT_SECRET", mode="rb") as key_reader:
            jwt_secret = key_reader.read()
    except FileNotFoundError:
        with open(".JWT_SECRET", mode="wb") as key_writer:
            jwt_secret = token_bytes(48)
            key_writer.write(jwt_secret)

    return jwt_secret.hex()
