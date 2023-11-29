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
        User_ID INT);""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS answers(
        Task1 INTEGER,
        Task2 INTEGER,
        Task3 INTEGER,
        Task4 INTEGER,
        Task5 INTEGER,
        Task6 INTEGER,
        Task7 INTEGER,
        Task8 INTEGER,
        Task9 INTEGER,
        Task10 INTEGER,
        user_id INTEGER);""")

    def write_user_data(self, data: list) -> str:
        self.cursor.execute(f"SELECT User_ID FROM users WHERE User_ID={data[3]}")

        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?)", [element for element in data])
            self.cursor.execute(f'INSERT INTO answers (user_id) VALUES ({data[3]});')
            self.db.commit()
            return "Successful registration"
        return "You have already been registered. Please read instructions."

    def check_answer(self, user_id: int, task_number: str):
        self.cursor.execute(f'SELECT {task_number} FROM answers WHERE user_id={user_id};')
        if self.cursor.fetchone()[0] is not None:
            return True
        return False

    def write_answers(self, user_id: int, task_number: int, answer: int) -> str:
        if self.check_answer(user_id, f"Task{task_number}"):
            return "You have already gave your answer!"

        self.cursor.execute(f'UPDATE answers SET Task{str(task_number)}={answer + 1} WHERE user_id={user_id};')
        self.db.commit()
        return "Thank you for answer."

    def check_user(self, user_id: int) -> bool:
        self.cursor.execute(f"SELECT User_ID FROM users WHERE User_ID={user_id}")
        if self.cursor.fetchone() is None:
            return False
        return True
