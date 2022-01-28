from os import environ
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    load_dotenv = None

# Who am I
USER_AGENT = "Discord-OAuth"

# API Option
API_VERSION = "v8"

# URLs
DISCORD_BASE = f"https://discord.com/api/{API_VERSION}"
DISCORD_AUTH = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN = "https://discord.com/api/oauth2/token"
DISCORD_REVOKE = "https://discord.com/api/oauth2/token/revoke"

# APP Information
CLIENT_ID = environ.get("DISCORD_CLIENT_ID")
CLIENT_SECRET = environ.get("DISCORD_CLIENT_SECRET")
# set your "REDIRECT_URI" at application menu

# SCOPE for OAuth
OAUTH_SCOPE = environ.get("OAUTH_SCOPE", "identify")
