from db_handler import DbHandler
from telebot import TeleBot
from config import bot_chat_actions
from background import keep_alive
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from time import sleep


def get_inline_keyboard(keyboard_buttons: list = None, callback_data: list = None) -> InlineKeyboardMarkup | None:
    keyboard = InlineKeyboardMarkup()
    if keyboard_buttons and callback_data is not None:
        for button, callback in zip(keyboard_buttons, callback_data):
            keyboard.add(InlineKeyboardButton(button, callback_data=callback))
        return keyboard
    return


class Bot(DbHandler, TeleBot):
    def __init__(self, token):
        super(Bot, self).__init__()
        self.bot = TeleBot(token, parse_mode='HTML')

    def get_reply_keyboard(self, keyboard_buttons: list = None, one_time: bool = True, menu: bool = False,
                           user_id: int = None) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        if menu:
            if not self.check_user(user_id):
                keyboard.add(KeyboardButton('Registration'))
            keyboard.add(KeyboardButton('Help'), KeyboardButton('Support'))
            keyboard.add(KeyboardButton('Info'), KeyboardButton('Exit'))
            return keyboard
        for button in keyboard_buttons:
            keyboard.add(KeyboardButton(button))
        return keyboard

    def send_action(self, chat_id: str | int, action: str, time: int = 2) -> None:
        self.bot.send_chat_action(chat_id, action)
        sleep(time)

    def start(self):
        bot = self.bot

        @bot.message_handler(commands=['start'])
        def start(message):
            user_name = message.from_user.first_name
            if message.from_user.last_name:
                user_name += f" {message.from_user.last_name}"
            self.send_action(message.chat.id, bot_chat_actions['text'])
            keyboard = self.get_reply_keyboard(['Menu'])
            bot.send_message(message.chat.id, f"Hello, {user_name}!", reply_markup=keyboard)

        @bot.message_handler(content_types=['text'])
        def check_message(message):
            if message.text.lower() == 'menu':
                keyboard = self.get_reply_keyboard(menu=True, user_id=message.from_user.id)
                self.send_action(message.chat.id, bot_chat_actions['text'], time=1)
                bot.send_message(message.chat.id, "What do you want?", reply_markup=keyboard)
            elif message.text.lower() == 'registration':
                self.send_action(message.chat.id, bot_chat_actions['text'])
                bot.send_message(message.chat.id, "Please send me your name, last_name and email in format:\n\n"
                                                  "Reg: Name Last name email")
            elif 'reg:' in message.text.lower():
                user_data = list(message.text.split(' '))
                user_data.pop(0)
                user_data.append(message.from_user.id)
                if user_data and len(user_data) == 4:
                    keyboard = self.get_reply_keyboard(['Instructions'])
                    message_text = self.write_user_data(user_data)
                    self.send_action(message.chat.id, bot_chat_actions['text'], time=1)
                    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
                else:
                    self.send_action(message.chat.id, bot_chat_actions['text'])
                    keyboard = self.get_reply_keyboard(menu=True, user_id=message.from_user.id)
                    bot.send_message(message.chat.id, 'Something went wrong. Please try again or write to support',
                                     reply_markup=keyboard)
                # bot.send_message(message.chat.id, f"{user_data}")
            elif message.text.lower() == 'instructions':
                if self.check_user(message.from_user.id):
                    keyboard = self.get_reply_keyboard(['Start tasks'])
                    self.send_action(message.chat.id, bot_chat_actions['text'], time=4)
                    bot.send_message(message.chat.id, "Instructions: ", reply_markup=keyboard)
                else:
                    keyboard = self.get_reply_keyboard(menu=True, user_id=message.from_user.id)
                    self.send_action(message.chat.id, bot_chat_actions['text'])
                    bot.send_message(message.chat.id, "Please register", reply_markup=keyboard)
            elif message.text.lower() == 'start tasks':
                if self.check_user(message.from_user.id):
                    keyboard = get_inline_keyboard(['Start'], ['start'])
                    self.send_action(message.chat.id, bot_chat_actions['text'], time=1)
                    bot.send_message(message.chat.id, "Good luck!", reply_markup=keyboard)
                else:
                    keyboard = self.get_reply_keyboard(menu=True, user_id=message.from_user.id)
                    self.send_action(message.chat.id, bot_chat_actions['text'])
                    bot.send_message(message.chat.id, "Please register", reply_markup=keyboard)

        """
                                                !!!!!    ТЗ    !!!!!
                                                
        Для каждой проверки необходимо вызывать метод check_time, который будет считывать из БД время и проверять,
        есть ли у участника время на прохождение заданий. Предполагается, что олимпиада будет запущена в один
        конкретный день, на ее выполнение будет дано, например 10 дней. Таким образом нам будет известна дата
        окончания. При начале выполнения задач мы фиксируем дату и время, заносим в БД. Далее сообщаем
        участнику, сколько времени у него осталось на выполнение, а также напоминаем про это при каждом взаимодействии
        с ботом. Проверку построим на основании модуля datetime и будем вычислять несложным путем. Также необходимо
        Вместо Task и var указать варианты ответов и вопросы. Не забыть сделать проверку на то, чтобы пользователь не
        смог пройти повторную регистрацию или повторно ответить на задание(написать код, отвечающий за безопасность).
        Разработать систему команд, чат поддержки, прописать всю необходимую информацию, сделать оформление. Перевести 
        на русский язык основной функционал бота. Убрать вспомогательные ненужные участки кода. Добавить обработку 
        колбэка кнопки finish. Предусмотреть возможность вернуться к заданиям, а также узнать, сколько осталось времени.
        Протестировать бота, после разместить его на хостинге.
                                                
                                                !!!!!    ТЗ    !!!!!
        """
        @bot.callback_query_handler(func=lambda call: True)
        def process_inline_keyboard(call):
            if call.data == 'start':
                keyboard = get_inline_keyboard(['9', '11', '5'], [f'var_1_{i}' for i in range(3)])
                bot.edit_message_text("Сколько пешек стоит ферзь?", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_1' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next1'])
                message_text = self.write_answers(call.from_user.id, 1, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next1':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_2_{i}' for i in range(3)])
                bot.edit_message_text("Task2: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_2' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next2'])
                message_text = self.write_answers(call.from_user.id, 2, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next2':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_3_{i}' for i in range(3)])
                bot.edit_message_text("Task3: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_3' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next3'])
                message_text = self.write_answers(call.from_user.id, 3, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next3':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_4_{i}' for i in range(3)])
                bot.edit_message_text("Task4: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_4' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next4'])
                message_text = self.write_answers(call.from_user.id, 4, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next4':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_5_{i}' for i in range(3)])
                bot.edit_message_text("Task5: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_5' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next5'])
                message_text = self.write_answers(call.from_user.id, 5, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next5':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_6_{i}' for i in range(3)])
                bot.edit_message_text("Task6: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_6' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next6'])
                message_text = self.write_answers(call.from_user.id, 6, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next6':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_7_{i}' for i in range(3)])
                bot.edit_message_text("Task7: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_7' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next7'])
                message_text = self.write_answers(call.from_user.id, 7, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next7':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_8_{i}' for i in range(3)])
                bot.edit_message_text("Task8: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_8' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next8'])
                message_text = self.write_answers(call.from_user.id, 8, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next8':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_9_{i}' for i in range(3)])
                bot.edit_message_text("Task9: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_9' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Continue'], ['next9'])
                message_text = self.write_answers(call.from_user.id, 9, int(text))
                bot.edit_message_text(message_text, call.message.chat.id, call.message.id, reply_markup=keyboard)

            elif call.data == 'next9':
                keyboard = get_inline_keyboard(['Var1', 'Var2', 'Var3'], [f'var_010_{i}' for i in range(3)])
                bot.edit_message_text("Task10: ", call.message.chat.id, call.message.id, reply_markup=keyboard)
            elif 'var_010' in call.data:
                text = ""
                for i in range(3):
                    if call.data[len(call.data) - 1] == str(i):
                        text = str(i)
                keyboard = get_inline_keyboard(['Finish'], ['End'])
                self.write_answers(call.from_user.id, 10, int(text))
                bot.edit_message_text("Thanks! We will contact you after summing up the results.",
                                      call.message.chat.id, call.message.id, reply_markup=keyboard)


        """
        delete comments when bot will be deploy        
        keep_alive()
        """
        self.bot.polling(non_stop=True)
        