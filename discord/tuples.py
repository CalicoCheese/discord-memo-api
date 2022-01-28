from collections import namedtuple as _namedtuple

Token = _namedtuple("Token",
                    "access_token expires_in refresh_token scope token_type")

User = _namedtuple("User",
                   "id username avatar discriminator public_flags flags banner banner_color"
                   "accent_color locale mfa_enabled")
