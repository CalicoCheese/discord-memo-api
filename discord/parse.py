from .tuples import DiscordToken, DiscordUser


def parse_token(json: dict) -> DiscordToken:
    return DiscordToken(**json)


def parse_user(json: dict) -> DiscordUser:
    return DiscordUser(
        id=json['id'],
        username=json['username'],
        discriminator=json['discriminator'],
    )
