from post import Post, format_message, format_yes_no
from post_telegram import TelegramPost
from datetime import date, datetime, timedelta
from consts import *
import config
import requests
import asyncio
import log
import traceback
import sys
import threading as t
import logging
import config

from consts import *
from telegram import *
from telegram.ext import *

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(name)s: %(message)s',
    level=logging.INFO
)


_cli_enabled = not ('-s' in sys.argv)

_cfg = config.load_config(CONFIG_PATH)

_posters: list = [
    TelegramPost(_cfg)
]

_stop_threads = []

_stop_loops = []

async def fetch_and_post():
    info = requests.get(_cfg.info_json_url).json()
    msg = format_message(info)
    url = _cfg.banner_image_url

    for post in _posters:
        log.debug("Posting to " + type(post).__name__)
        await post.post(url, msg)

async def fetch_yes_no():
    info = requests.get(_cfg.info_json_url).json()
    msg = format_yes_no(info)

    return msg


def last_12h():
    now = datetime.today()
    out = datetime(year=now.year, month=now.month, day=now.day, hour=12)

    if now < out:
        out -= timedelta(days=1)
    return out


class Status:
    def __init__(self):
        self.last_post = last_12h()

    def next_post(self):
        return self.last_post + timedelta(days=1)

    def remaining(self):
        return self.next_post() - datetime.today()
    
def stop():
    for l in _stop_loops:
        l.stop()

async def cli(status: Status):
    print("Type 'help' for a list of commands")
    print("Press Ctrl+C to interrupt")
    while True:
        try:
            i = input("> ")

            if i == "remaining":
                print("Posting each day at 12:00 noon, local time")
                print("Next post will be in", status.remaining())
                print("Type 'post' to post now")
            elif i == "post":
                await fetch_and_post()
            elif i == "help":
                print("Commands:")
                print(" - stop:      stop the service")
                print(" - exit:      alias for 'stop'")
                print(" - quit:      alias for 'stop'")
                print(" - remaining: print remaining time until next post")
                print(" - post:      immediately post")
                print(" - help:      print this menu")
            elif i == "stop":
                print("Stop")
                stop()
                return
            elif i == "exit":
                print("Exit")
                stop()
                return
            elif i == "quit":
                print("Quit")
                stop()
                return
            else:
                print("Unknown command: " + i)
                print("Type 'help' for a list of commands")

        except KeyboardInterrupt:
            print("")
            print("cli: KeyboardInterrupt")
            stop()
            return
        except SystemExit:
            print("")
            print("cli: SystemExit")
            stop()
            return
        except EOFError:
            print("cli: EOF found, CLI disabled")
            return
        except:
            print(traceback.format_exc())

async def poster(status: Status):
    print("Started posting")
    while True:
        try:
            now = datetime.now()

            delta = now - status.last_post

            if delta.days > 0:
                print("Posting...")
                # Post before updating time, so if it goes wrong it automatically retries in 5 seconds
                await fetch_and_post()
                status.last_post = last_12h()

        except KeyboardInterrupt:
            print("")
            print("post: KeyboardInterrupt")
            stop()
            return
        except SystemExit:
            print("")
            print("post: SystemExit")
            stop()
            return
        except:
            print(traceback.format_exc())

        await asyncio.sleep(5)


def cli_thread(status: Status):
    cliloop = asyncio.new_event_loop()
    _stop_loops.append(cliloop)
    try:
        asyncio.set_event_loop(cliloop)
        cliloop.run_until_complete(cli(status))
    finally:
        cliloop.close()


def post_thread(status: Status):
    postloop = asyncio.new_event_loop()
    _stop_loops.append(postloop)
    try:
        asyncio.set_event_loop(postloop)
        postloop.run_until_complete(poster(status))
    finally:
        postloop.close()












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
        msg = await bot.send_message(
            chat_id=update.effective_chat.id,
            text="Posting..."
        )
        await fetch_and_post()
        await msg.edit_text("Posted!")

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

    msg = await fetch_yes_no()
    await bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg
    )

def build_app(status: Status) -> Application:
    application = ApplicationBuilder()             \
                  .token(_cfg.telegram_token)      \
                  .post_init(init)                 \
                  .rate_limiter(AIORateLimiter())  \
                  .build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('post', post))
    application.add_handler(CommandHandler('isitnfc', isitnfc))

    return application







def main(status: Status, loop: asyncio.AbstractEventLoop):

    app = build_app(status)

    loop.run_until_complete(app.initialize())
    loop.run_until_complete(app.updater.start_polling())
    if app.post_init:
        loop.run_until_complete(app.post_init(app))
    loop.run_until_complete(app.start())

    loop.run_forever()

    if app.updater.running:
        loop.run_until_complete(app.updater.stop())
    if app.running:
        loop.run_until_complete(app.stop())
    if app.post_stop:
        loop.run_until_complete(app.post_stop(app))
    loop.run_until_complete(app.shutdown())
    if app.post_shutdown:
        loop.run_until_complete(app.post_shutdown(app))

    loop.close()


if __name__ == "__main__":
    try:
        status = Status()

        if _cli_enabled:
            thr = t.Thread(target=lambda: cli_thread(status))
            thr.daemon = True
            thr.start()
        
        thr = t.Thread(target=lambda: post_thread(status))
        thr.daemon = True
        thr.start()

        
        loop = asyncio.new_event_loop()
        _stop_loops.append(loop)

        asyncio.set_event_loop(loop)
        main(status, loop)
    except KeyboardInterrupt:
        print("")
        print("KeyboardInterrupt")
    except SystemExit:
        print("")
        print("SystemExit")