from collections import namedtuple as _namedtuple

DiscordToken = _namedtuple("DiscordToken",
                           "access_token expires_in refresh_token scope "
                           "token_type")

DiscordUser = _namedtuple("DiscordUser",
                          "id username discriminator avatar bot system "
                          "mfa_enabled banner banner_color accent_color "
                          "locale verified email flags premium_type "
                          "public_flags")
