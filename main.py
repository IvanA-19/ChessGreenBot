from config import api_token
from bot import Bot
from background import keep_alive


def main():
    bot = Bot(api_token)
    keep_alive()
    bot.start()


if __name__ == '__main__':
    main()
