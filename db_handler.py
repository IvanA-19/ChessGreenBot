import sqlite3


class DbHandler:
    def __init__(self):
        self.db = sqlite3.connect('data_base/db.sqlite3', check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(First_name CHAR_FIELD,
        Last_name CHAR_FIELD,
        Email TEXT_FIELD,
        Phone_number TEXTFIELD,
        User_ID INT);""")

        task_list = ", ".join(f"Task{i + 1} INTEGER" for i in range(15))

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS answers(
        {task_list},
        user_id INTEGER);""")

    def write_user_data(self, data: list) -> str:
        self.cursor.execute(f"SELECT User_ID FROM users WHERE User_ID={data[4]}")

        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?)", [element for element in data])
            self.cursor.execute(f'INSERT INTO answers (user_id) VALUES ({data[4]});')
            self.db.commit()
            return "Вы успешно зарегистрированы!"
        return "Вы уже зарегистрированы. Пожалуйста, прочитайте инструкции."

    def check_answer(self, user_id: int, task_number: str):
        self.cursor.execute(f'SELECT {task_number} FROM answers WHERE user_id={user_id};')
        if self.cursor.fetchone()[0] is not None:
            return True
        return False

    def check_task(self, user_id):
        self.cursor.execute(f"SELECT * FROM answers WHERE user_id={user_id}")
        data = self.cursor.fetchall()[0]
        for i in range(len(data)):
            if data[i] is None:
                return i + 1
        return

    def write_answers(self, user_id: int, task_number: int, answer: int) -> str:
        if self.check_answer(user_id, f"Task{task_number}"):
            return "Вы уже дали ответ на это задание!"

        self.cursor.execute(f'UPDATE answers SET Task{str(task_number)}={answer + 1} WHERE user_id={user_id};')
        self.db.commit()
        return "Спасибо за ваш ответ!"

    def check_user(self, user_id: int) -> bool:
        self.cursor.execute(f"SELECT User_ID FROM users WHERE User_ID={user_id}")
        if self.cursor.fetchone() is None:
            return False
        return True
