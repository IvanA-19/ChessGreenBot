from telebot.types import BotCommand

api_token = '6912861381:AAFo7jy6Mg8BZuZcwPZ5chR3N8eGsepNdys'
bot_chat_actions = {'text': 'typing',
                    'document': 'upload_document',
                    'sticker': 'choose_sticker ',
                    'location': 'find_location',
                    'photo': 'upload_photo',
                    'video': ('record_video', 'upload_video'),
                    'video_note': ('record_video_note', 'upload_video_note'),
                    'voice': ('record_voice', 'upload_voice')}

help_list = """

/start - начало работы
/menu - открыть меню
/register - зарегистрироваться
/info - прочитать информацию
/support - получить контакты поддержки
/help - открыть меню команд
/instructions - прочитать инструкции
/continue - продолжить отвечать на задания
/time - узнать, сколько осталось времени на выполнение заданий
/exit - завершить работу"""

bot_commands = [BotCommand("/start", "начало работы"),
                BotCommand("/menu", "открыть меню"),
                BotCommand("/register", "зарегистрироваться"),
                BotCommand("/info", "прочитать информацию"),
                BotCommand("/support", "получить контакты поддержки"),
                BotCommand("/help", "открыть меню команд"),
                BotCommand("/instructions", "прочитать инструкции"),
                BotCommand("/time", "узнать, сколько осталось времени на выполнение заданий"),
                BotCommand("/continue", "продолжить отвечать на задания"),
                BotCommand("/exit", "завершить работу")]
