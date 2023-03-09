import logging, config
from telegram import Update, Bot, Chat, ChatMember
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, AIORateLimiter

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s',
    level=logging.INFO
)

_cfg = config.load_config("./config.json")

async def init(app: Application):
    bot: Bot = app.bot
    chat = await bot.get_chat("@isitnfc")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot: Bot = context.bot
    chat: Chat = await bot.get_chat("@isitnfc")

    member: ChatMember = await chat.get_member(update.effective_user.id)
    if member.status == ChatMember.ADMINISTRATOR or ChatMember.OWNER:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are admin at @isitnfc")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! Your user ID is " + str(update.effective_user.id))



if __name__ == '__main__':
    application = ApplicationBuilder().token(_cfg.telegram_token).post_init(init).rate_limiter(AIORateLimiter()).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()