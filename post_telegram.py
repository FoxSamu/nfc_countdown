import log
from config import Config
from post import Post

from telegram import Bot
from telegram.error import Forbidden


class TelegramPost(Post):
    def __init__(self, cfg: Config):
        super().__init__(cfg)

        if cfg.telegram_token == None:
            raise RuntimeError("Missing configuration 'telegram_token'")

        if cfg.telegram_channel == None:
            raise RuntimeError("Missing configuration 'telegram_channel'")

        self.bot = None
        self.channel = cfg.telegram_channel
        self.token = cfg.telegram_token

    async def post(self, img_url: str, message: str):
        if self.bot == None:
            self.bot = Bot(self.token)

        try:
            await self.bot.send_photo(
                chat_id=self.channel,
                caption=message,
                photo=img_url
            )

            log.debug("Posted to Telegram channel " + self.channel + "!")
        except Forbidden:
            log.error("No access to send message in channel " + self.channel + "!")