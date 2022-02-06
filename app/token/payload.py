from time import time

from discord.tuples import DiscordUser


def create(user: DiscordUser) -> dict:
    now = int(time())
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "discriminator": user.discriminator
        },
        "time": {
            "iat": now,
            "exp": now + (3 * 60 * 60)
        }
    }
