from pyrogram import filters
from pyrogram.types import Message
from core.bot import bot
from utils.logger import LOGGER

@bot.on_message(filters.command(["play", "p"]) & filters.group)
async def play_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /play song name or youtube link")

    query = message.text.split(None, 1)[1]
    await message.reply_text(f"Playing: **{query}**\n\n(Music system abhi basic hai, full version jald aa raha hai)")

@bot.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop_handler(_, message: Message):
    await message.reply_text("Stopped!")

@bot.on_message(filters.command(["skip", "next"]) & filters.group)
async def skip_handler(_, message: Message):
    await message.reply_text("Skipped!")

@bot.on_message(filters.command("pause") & filters.group)
async def pause_handler(_, message: Message):
    await message.reply_text("Paused!")

@bot.on_message(filters.command("resume") & filters.group)
async def resume_handler(_, message: Message):
    await message.reply_text("Resumed!")
