import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('../db.sqlite3')
        self.cursor = self.conn.cursor()

    def get_user_by_login(self, login):
        self.cursor.execute("SELECT * FROM UsersYa WHERE login=?", (login,))
        return self.cursor.fetchone()

    # Добавьте другие методы для работы с базой данных

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
