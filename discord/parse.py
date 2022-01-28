from .tuples import *


def parse_token(json: dict) -> Token:
    return Token(**json)


def parse_user(json: dict) -> User:
    x = [x for x in ['bot', 'system', 'mfa_enabled', 'banner',
                     'accent_color', 'locale', 'verified',
                     'email', 'flags', 'premium_type',
                     'public_flags', 'banner_color']]

    for x in x:
        if x not in json.keys():
            json[x] = None

    return User(**json)
