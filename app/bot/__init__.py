from .bot_secret import get

BOT_SECRET = get()


def verify(secret: str) -> bool:
    return BOT_SECRET == secret
