import sqlite3


class BotDB:

    def __init__(self, db_file):
        """Подключение к БД"""
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    def user_exists(self, user_id):
        """Провека на существование пользователя"""
        result = self.cursor.execute("SELECT Id FROM users WHERE userId = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Получение пользовательского ID в БД"""
        result = self.cursor.execute("SELECT Id FROM users WHERE userId = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавление пользователя"""
        self.cursor.execute("INSERT INTO users (userId) VALUES (?)", (user_id,))
        self.cursor.execute("INSERT INTO locations (userId) VALUES (?)", (self.get_user_id(user_id),))
        return self.connect.commit()

    def update_location(self, user_id, city):
        """Смена города для оповещения о погоде"""
        self.cursor.execute("UPDATE locations SET city = ? WHERE userId = ?", (city, self.get_user_id(user_id),))
        return self.connect.commit()

    def update_notification_time(self, user_id, time):
        """Смена времени оповещения о погоде"""
        self.cursor.execute("UPDATE locations SET notificationTime = ? WHERE userId = ?",
                            (time, self.get_user_id(user_id),))
        return self.connect.commit()

    def update_rating(self, user_id, rating):
        """Обновить рейтинг пользователя"""
        self.cursor.execute("UPDATE users SET rating = ? WHERE Id = ?",
                            (rating, self.get_user_id(user_id)))
        return self.connect.commit()

    def get_location(self, user_id):
        """Получение города и времени для погодного оповещения"""
        self.cursor.execute("SELECT city, notificationTime FROM locations WHERE userId = ?",
                            (self.get_user_id(user_id),))
        return self.cursor.fetchall()

    def get_users(self):
        """Получение всех пользователей в БД"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        """Удаление пользователя из БД"""
        self.cursor.execute("DELETE FROM locations WHERE userId = ?", (self.get_user_id(user_id),))
        self.cursor.execute("DELETE FROM users WHERE userId = ?", (user_id,))
        return self.connect.commit()

    def close(self):
        """Завершить соединение с БД"""
        self.connect.close()