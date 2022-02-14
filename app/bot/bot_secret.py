from secrets import token_bytes


def get() -> str:
    try:
        with open(".BOT_SECRET", mode="rb") as key_reader:
            bot_secret = key_reader.read()
    except FileNotFoundError:
        with open(".BOT_SECRET", mode="wb") as key_writer:
            bot_secret = token_bytes(120)
            key_writer.write(bot_secret)

    return bot_secret.hex()
