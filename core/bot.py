from pyrogram import Client
import config
from utils.logger import LOGGER

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="YashikaBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention
        LOGGER(__name__).info(f"Bot Started as {self.name} (@{self.username})")

    async def stop(self):
        await super().stop()

bot = Bot()
