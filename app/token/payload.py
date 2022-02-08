from time import time

from discord.tuples import DiscordUser


def create(user: DiscordUser) -> (dict, int):
    iat = int(time())
    exp = iat + (3 * 60 * 60)

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "discriminator": user.discriminator
        },
        "time": {
            "iat": iat,
            "exp": exp
        }
    }, exp
