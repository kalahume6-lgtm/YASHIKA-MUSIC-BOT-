from pyrogram import filters
from pyrogram.types import Message
from core.bot import bot
import config
import google.generativeai as genai
from utils.logger import LOGGER

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


@bot.on_message(filters.private & filters.user(config.OWNER_ID) & filters.text & \~filters.command(["start", "help"]))
async def owner_ai_handler(_, message: Message):
    if not model:
        return await message.reply_text("Gemini API Key set nahi hai.")

    try:
        response = model.generate_content(
            f"Tum ek smart aur friendly AI assistant ho. User ka message: {message.text}"
        )
        await message.reply_text(response.text)
    except Exception as e:
        LOGGER(__name__).error(f"Owner AI error: {e}")
        await message.reply_text("Error aa gaya AI se.")
