from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
            return result.get("reply")
        return None
    except:
        return None


async def save_learned_reply(word: str, reply: str):
    try:
        await word_db.update_one(
            {"word": word},
            {"$set": {"reply": reply}},
            upsert=True
        )
    except Exception as e:
        LOGGER(__name__).error(f"Save error: {e}")


async def gemini_reply(text: str):
    if not model:
        return None
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        LOGGER(__name__).error(f"Gemini error: {e}")
        return None


@bot.on_message(filters.command("chatbot") & filters.group)
async def chatbot_toggle(_, message: Message):
    buttons = [
        [
            InlineKeyboardButton("Enable", callback_data="chatbot_enable"),
            InlineKeyboardButton("Disable", callback_data="chatbot_disable"),
        ]
    ]
    await message.reply_text(
        "Chatbot Control:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@bot.on_callback_query(filters.regex("chatbot_"))
async def chatbot_callback(_, query):
    chat_id = query.message.chat.id
    data = query.data

    if data == "chatbot_enable":
        await chatbot_status.update_one(
            {"chat_id": chat_id},
            {"$set": {"status": "enabled"}},
            upsert=True
        )
        await query.answer("Chatbot Enabled", show_alert=True)
        await query.edit_message_text("Chatbot **Enabled**")
    elif data == "chatbot_disable":
        await chatbot_status.update_one(
            {"chat_id": chat_id},
            {"$set": {"status": "disabled"}},
            upsert=True
        )
        await query.answer("Chatbot Disabled", show_alert=True)
        await query.edit_message_text("Chatbot **Disabled**")


@bot.on_message(filters.text & filters.incoming & \~filters.bot & \~filters.command(["start", "help", "ping", "play", "stop", "skip", "chatbot", "pause", "resume"]))
async def chatbot_handler(_, message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()

        # Group me check karo enabled hai ya nahi
        if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            status = await chatbot_status.find_one({"chat_id": chat_id})
            if not status or status.get("status") != "enabled":
                return

        # 1. Learned reply
        learned = await get_learned_reply(text)
        if learned:
            await message.reply_text(learned)
            return

        # 2. Gemini AI
        ai_reply = await gemini_reply(text)
        if ai_reply:
            await message.reply_text(ai_reply)
            await save_learned_reply(text, ai_reply)
            return

        # 3. Default
        await message.reply_text(random.choice([
            "Haan bolo?",
            "Kya hua?",
            "Ji?",
            "Samjha nahi 😅",
            "Hmm..."
        ]))

    except Exception as e:
        LOGGER(__name__).error(f"Chatbot error: {e}")
