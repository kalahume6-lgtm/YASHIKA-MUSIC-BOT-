from pyrogram import Client
import config
from utils.logger import LOGGER

class Assistants:
    def __init__(self):
        self.one = Client(
            "Assistant1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION1 or None,
            no_updates=True,
        ) if config.STRING_SESSION1 else None

        self.two = Client(
            "Assistant2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION2 or None,
            no_updates=True,
        ) if config.STRING_SESSION2 else None

        self.three = Client(
            "Assistant3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.STRING_SESSION3 or None,
            no_updates=True,
        ) if config.STRING_SESSION3 else None

    async def start(self):
        LOGGER(__name__).info("Starting Music Assistants...")
        if self.one:
            await self.one.start()
            LOGGER(__name__).info(f"Assistant 1 started as {self.one.me.first_name}")
        if self.two:
            await self.two.start()
            LOGGER(__name__).info(f"Assistant 2 started as {self.two.me.first_name}")
        if self.three:
            await self.three.start()
            LOGGER(__name__).info(f"Assistant 3 started as {self.three.me.first_name}")

    async def stop(self):
        if self.one:
            await self.one.stop()
        if self.two:
            await self.two.stop()
        if self.three:
            await self.three.stop()

assistants = Assistants()
