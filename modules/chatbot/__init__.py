from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from core.bot import bot
from core.database import word_db, chatbot_status
from utils.logger import LOGGER
import random
import google.generativeai as genai
import config

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


async def get_learned_reply(text: str):
    try:
        result = await word_db.find_one({"word": text})
        if result:
            return result["reply"]
        return None
    except Exception:
        return None


async def save_learned_reply(word: str, reply: str):
    try:
        await word_db.update_one(
            {"word": word},
            {"$set": {"reply": reply}},
            upsert=True
        )
    except Exception as e:
        LOGGER(__name__).error(f"Save reply error: {e}")


async def gemini_reply(text: str):
    if not model:
        return None
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        LOGGER(__name__).error(f"Gemini error: {e}")
        return None


@bot.on_message(filters.text & filters.incoming & \~filters.bot & \~filters.command(["start", "help", "ping", "play", "stop", "skip"]))
async def chatbot_handler(_, message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()

        # Check if chatbot enabled in group
        if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            status = await chatbot_status.find_one({"chat_id": chat_id})
            if not status or status.get("status") != "enabled":
                return

        # First try learned reply
        learned = await get_learned_reply(text)
        if learned:
            await message.reply_text(learned)
            return

        # Then try Gemini
        ai_reply = await gemini_reply(text)
        if ai_reply:
            await message.reply_text(ai_reply)
            # Save for learning
            await save_learned_reply(text, ai_reply)
            return

        # Default
        await message.reply_text(random.choice(["Haan bolo?", "Kya hua?", "Ji?", "Samjha nahi 😅"]))

    except Exception as e:
        LOGGER(__name__).error(f"Chatbot error: {e}")
