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
/exit - завершить работу"""

bot_commands = [BotCommand("/start", "начало работы"),
                BotCommand("/menu", "открыть меню"),
                BotCommand("/register", "зарегистрироваться"),
                BotCommand("/info", "прочитать информацию"),
                BotCommand("/support", "получить контакты поддержки"),
                BotCommand("/help", "открыть меню команд"),
                BotCommand("/instructions", "прочитать инструкции"),
                BotCommand("/continue", "продолжить отвечать на задания"),
                BotCommand("/exit", "завершить работу")]

info = ("\U0001F451 Шахматы - известная с давних времен и популярная и по сей день игра, которая отлично развивает "
        "логическое мышление и логику. Целью игры является постановка мата вражескому королю. На сегодняшний день"
        "игра является официальным видом спорта. Наш марафон направлен на оценку уровня эрудиции в области "
        "шахмат у участников. Выполнив задания, вы сможете узнать, насколько хорошо вы осведомлены о данной игре "
        "и получить новые знания. \U0001F451 \n\nНа выполнение заданий дается 31 день. "
        "Выполнять все задания за раз не обязательно,"
        "вы всегда сможете вернуться к тому заданию, на котором остановились. \U00002705 \n\nЖелаем удачи! \U0001F60C")

instructions = ("\U0001F4DD Задания марафона представляют из себя тест из 15 заданий. \U0001F4DD"
                "\n\n\U00002757 Выполняйте задания вдумчиво. Если вы дали свой ответ - "
                "изменить его будет невозможно! \U00002757"
                "\n\n\U0000265F Обозначения фигур в задачах: Q - ферзь, R - ладья \U0000265F"
                "\n\n\U0001F3C6 По итогу прохождения всех заданий марафона - "
                "вы сможете узнать свой результат \U0001F3C6"
                "\n\n\U000023FA Если вы готовы дать свой ответ - нажмите на кнопку с выбранным вариантом. \U000023FA"
                "\n\n\U00002705 Чтобы продолжить выполнение заданий "
                "с того задания, на котором закончили - используйте кнопку"
                "в меню или команду /continue \U00002705"
                "\n\n\U0001F4E2 В случае возникновения проблем - вы можете обратиться в службу поддержки. \U0001F4E2")
