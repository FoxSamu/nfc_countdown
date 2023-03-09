import logging
import config

from consts import *
from telegram import *
from telegram.ext import *

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s',
    level=logging.INFO
)


_cfg = config.load_config(CONFIG_PATH)


async def init(app: Application):
    """
    Initialization procedure
    """

    bot: Bot = app.bot

    await bot.set_my_commands(
        [
            BotCommand("start", "Start talking to me"),
            BotCommand("isitnfc", "Get a yes or a no, depending on whether it is NFC or not"),
            BotCommand("post", "If you are an admin at " + _cfg.telegram_channel + ", re-post today's update")
        ]
    )

    pass



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /start
    """

    bot: Bot = context.bot

    ch = _cfg.telegram_channel

    member: ChatMember = await bot.get_chat_member(ch, update.effective_user.id)
    if member.status == ChatMember.ADMINISTRATOR or ChatMember.OWNER:
        await bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are admin at " + ch
        )

    await bot.send_message(
        chat_id=update.effective_chat.id,
        text="Henlo :3"
    )

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /post
    """

    bot: Bot = context.bot

    ch = _cfg.telegram_channel

    member: ChatMember = await bot.get_chat_member(ch, update.effective_user.id)
    if member.status == ChatMember.ADMINISTRATOR or ChatMember.OWNER:
        await bot.send_message(
            chat_id=update.effective_chat.id,
            text="Not yet implemented!"
        )

    else:
        await bot.send_message(
            chat_id=update.effective_chat.id,
            text="You must be an admin or owner of " + ch + " to call /post"
        )

async def isitnfc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /isitnfc
    """

    bot: Bot = context.bot

    await bot.send_message(
        chat_id=update.effective_chat.id,
        text="No"
    )


if __name__ == '__main__':
    application = ApplicationBuilder()             \
                  .token(_cfg.telegram_token)      \
                  .post_init(init)                 \
                  .rate_limiter(AIORateLimiter())  \
                  .build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('post', post))
    application.add_handler(CommandHandler('isitnfc', isitnfc))

    application.run_polling()