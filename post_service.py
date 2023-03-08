from post import Post, format_message
from post_telegram import TelegramPost
from datetime import date, datetime, timedelta
import config, requests, asyncio, log, time
import traceback

cfg = config.load_config('./config.json')

__posters: list = [
    TelegramPost(cfg)
]

async def fetch_and_post():
    info = requests.get(cfg.info_json_url).json()
    msg = format_message(info)
    url = cfg.banner_image_url

    for post in __posters:
        log.debug("Posting to " + type(post).__name__)
        await post.post(url, msg)


def _last_12h():
    now = datetime.today()
    out = datetime(year=now.year, month=now.month, day=now.day, hour=12)

    if now < out:
        out -= timedelta(days=1)
    return out


class Status:
    def __init__(self):
        self.last_post = _last_12h()

    def next_post(self):
        return self.last_post + timedelta(days=1)

    def remaining(self):
        return self.next_post() - datetime.today()

async def cli(status: Status, loop):
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
                loop.stop()
                return
            elif i == "exit":
                print("Exit")
                loop.stop()
                return
            elif i == "quit":
                print("Quit")
                loop.stop()
                return
            else:
                print("Unknown command: " + i)
                print("Type 'help' for a list of commands")

        except KeyboardInterrupt:
            print("")
            print("KeyboardInterrupt")
            loop.stop()
            return
        except SystemExit:
            print("")
            print("SystemExit")
            loop.stop()
            return
        except EOFError:
            print("EOF found, CLI disabled")
            return
        except:
            print(traceback.format_exc())


async def main(loop):
    status = Status()
    loop.create_task(cli(status, loop))

    while True:
        try:
            now = datetime.now()

            delta = now - status.last_post

            if delta.days > 0:
                print("Posting...")
                status.last_post = _last_12h()
                await fetch_and_post()

            await asyncio.sleep(5)

        except KeyboardInterrupt:
            print("")
            print("KeyboardInterrupt")
            loop.stop()
            return
        except SystemExit:
            print("")
            print("SystemExit")
            loop.stop()
            return
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main(loop))
    loop.run_forever()