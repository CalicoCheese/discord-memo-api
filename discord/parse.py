from .tuples import DiscordToken, DiscordUser


def parse_token(json: dict) -> DiscordToken:
    return DiscordToken(**json)


def parse_user(json: dict) -> DiscordUser:
    for x in DiscordUser._fields:
        if x not in json.keys():
            json[x] = None

    return DiscordUser(**json)
