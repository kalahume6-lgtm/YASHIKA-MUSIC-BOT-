from pyrogram import Client, filters
from pyrogram.types import Message
import config
from utils.logger import LOGGER

userbots = []

if config.USERBOT_SESSION1:
    ub1 = Client(
        "Userbot1",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.USERBOT_SESSION1,
    )
    userbots.append(ub1)

if config.USERBOT_SESSION2:
    ub2 = Client(
        "Userbot2",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.USERBOT_SESSION2,
    )
    userbots.append(ub2)

if config.USERBOT_SESSION3:
    ub3 = Client(
        "Userbot3",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=config.USERBOT_SESSION3,
    )
    userbots.append(ub3)


async def start_userbots():
    for ub in userbots:
        try:
            await ub.start()
            LOGGER(__name__).info(f"Userbot Started as {ub.me.first_name}")
        except Exception as e:
            LOGGER(__name__).error(f"Userbot start error: {e}")


async def stop_userbots():
    for ub in userbots:
        try:
            await ub.stop()
        except:
            pass
