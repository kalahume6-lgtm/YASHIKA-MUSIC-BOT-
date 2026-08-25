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


@bot.on_message(filters.private & filters.user(config.OWNER_ID) & filters.text & \~filters.command(["start", "help", "ping"]))
async def owner_ai(_, message: Message):
    if not model:
        return await message.reply_text("Gemini API Key set nahi hai.")

    try:
        prompt = f"Tum ek smart, friendly aur thoda masti bhara AI assistant ho. Short aur natural jawab dena. User ne kaha: {message.text}"
        response = model.generate_content(prompt)
        await message.reply_text(response.text)
    except Exception as e:
        LOGGER(__name__).error(f"Owner AI error: {e}")
        await message.reply_text("AI se error aa gaya.")
