from motor.motor_asyncio import AsyncIOMotorClient
import config
from utils.logger import LOGGER

if not config.MONGO_URI:
    LOGGER.error("MONGO_URI is missing!")
    raise SystemExit("Please set MONGO_URI")

client = AsyncIOMotorClient(config.MONGO_URI)
db = client.YashikaBot

# Collections
users_db = db.users
chats_db = db.chats
chatbot_db = db.chatbot_status
lang_db = db.chat_lang
word_db = db.word_replies
sudo_db = db.sudoers
