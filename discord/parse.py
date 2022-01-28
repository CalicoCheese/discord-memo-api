from .tuples import *


def parse_token(json: dict) -> Token:
    return Token(**json)


def parse_user(json: dict) -> User:
    return User(**json)
