from os import getenv
from dotenv import load_dotenv

load_dotenv()

def get_int(key, default=None):
    val = getenv(key)
    if val is None or str(val).strip() == "":
        return default
    try:
        return int(val)
    except:
        return default

API_ID = get_int("API_ID")
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

# Music Assistants
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")

# Userbot Sessions (Owner controlled)
USERBOT_SESSION1 = getenv("USERBOT_SESSION1", "")
USERBOT_SESSION2 = getenv("USERBOT_SESSION2", "")
USERBOT_SESSION3 = getenv("USERBOT_SESSION3", "")

OWNER_ID = get_int("OWNER_ID")
MONGO_URI = getenv("MONGO_URI", "")
GEMINI_API_KEY = getenv("GEMINI_API_KEY", "")

LOGGER_ID = get_int("LOGGER_ID")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "")
