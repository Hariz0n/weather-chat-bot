import sqlite3, re


class UserDoesNotExistError(Exception):
    pass


class BotDB:

    def __init__(self, db_file):
        """Подключение к БД"""
        self.connect = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def is_user_exists(self, user_id):
        """Провека на существование пользователя"""
        result = self.cursor.execute("SELECT Id FROM users WHERE userId = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Получение пользовательского ID в БД"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        result = self.cursor.execute("SELECT Id FROM users WHERE userId = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавление пользователя"""
        self.cursor.execute("INSERT INTO users (userId) VALUES (?)", (user_id,))
        self.cursor.execute("INSERT INTO locations (userId) VALUES (?)", (self.get_user_id(user_id),))
        return self.connect.commit()

    def update_location(self, user_id, city):
        """Смена города для оповещения о погоде"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("UPDATE locations SET city = ? WHERE userId = ?", (city, self.get_user_id(user_id),))
        return self.connect.commit()

    def update_notification_time(self, user_id, time):
        """Смена времени оповещения о погоде в формате HH:MM"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        if bool(re.match(r"[0-2][\d]:[0-5][\d]", time)):
            self.cursor.execute("UPDATE locations SET notificationTime = ? WHERE userId = ?",
                                (time, self.get_user_id(user_id),))
            return self.connect.commit()
        else:
            raise ValueError("Time format error")

    def update_rating(self, user_id, rating):
        """Обновить рейтинг пользователя"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("UPDATE users SET rating = ? WHERE Id = ?",
                            (rating, self.get_user_id(user_id)))
        return self.connect.commit()

    def get_location(self, user_id):
        """Получение города и времени для погодного оповещения"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("SELECT city FROM locations WHERE userId = ?",
                            (self.get_user_id(user_id),))
        return self.cursor.fetchall()[0][0]

    def get_users(self):
        """Получение всех пользователей в БД"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        """Удаление пользователя из БД"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("DELETE FROM locations WHERE userId = ?", (self.get_user_id(user_id),))
        self.cursor.execute("DELETE FROM users WHERE userId = ?", (user_id,))
        return self.connect.commit()

    def close(self):
        """Завершить соединение с БД"""
        self.connect.close()

