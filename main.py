from config import *
from bot import Bot


def main():
    bot = Bot(api_token)
    bot.start()


if __name__ == '__main__':
    main()
