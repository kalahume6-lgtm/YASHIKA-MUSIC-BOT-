import asyncio
from pyrogram import idle
from core.bot import bot
from core.assistants import assistants
from utils.logger import LOGGER

async def main():
    await bot.start()
    await assistants.start()

    # Load modules
    from modules.chatbot import chatbot
    from modules.owner import owner_ai

    LOGGER(__name__).info("Yashika Ultimate Bot Started Successfully!")
    await idle()

    await bot.stop()
    await assistants.stop()

if __name__ == "__main__":
    asyncio.run(main())
