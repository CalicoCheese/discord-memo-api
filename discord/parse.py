from .tuples import DiscordToken, DiscordUser


def parse_token(json: dict) -> DiscordToken:
    return DiscordToken(**json)


def parse_user(json: dict) -> DiscordUser:
    x = [x for x in ['bot', 'system', 'mfa_enabled', 'banner',
                     'accent_color', 'locale', 'verified',
                     'email', 'flags', 'premium_type',
                     'public_flags', 'banner_color']]

    for x in x:
        if x not in json.keys():
            json[x] = None

    return DiscordUser(**json)
