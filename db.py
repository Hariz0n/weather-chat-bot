import json
import re
import sqlite3
from shedule import ScheduleBot


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

    def add_user(self, user_id):
        """Добавление пользователя"""
        self.cursor.execute("INSERT INTO users (userId) VALUES (?)", (user_id,))
        self.cursor.execute("INSERT INTO locations (userId) VALUES (?)", (user_id,))
        return self.connect.commit()

    def update_location(self, user_id, city):
        """Смена города для оповещения о погоде"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("UPDATE locations SET city = ? WHERE userId = ?", (city, user_id,))
        return self.connect.commit()

    def update_rating(self, user_id, rating):
        """Обновить рейтинг пользователя"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("UPDATE users SET rating = ? WHERE userId = ?",
                            (rating, user_id,))
        return self.connect.commit()

    def get_time_zone(self, user_id):
        """Получение часового пояса для погодного оповещения"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("SELECT timeZone FROM locations WHERE userId = ?",
                            (user_id,))
        return self.cursor.fetchall()[0][0]

    def update_time_zone(self, user_id, time_zone):
        """Смена часового пояса города для оповещения о погоде"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("UPDATE locations SET timeZone = ? WHERE userId = ?", (time_zone, user_id,))
        return self.connect.commit()

    def get_location(self, user_id):
        """Получение города для погодного оповещения"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("SELECT city FROM locations WHERE userId = ?",
                            (user_id,))
        return self.cursor.fetchall()[0][0]

    def update_schedule(self, user_id, schedule):
        """Обновить расписание пользователя"""
        if not self.is_user_exists(user_id):
            self.add_user(user_id)
        self.cursor.execute("UPDATE locations SET schedule = ? WHERE userId = ?",
                            (json.dumps(schedule), user_id,))
        return self.connect.commit()

    def get_schedule(self, user_id):
        """Получение расписания для погодного оповещения"""
        if not self.is_user_exists(user_id):
            return {}
        self.cursor.execute("SELECT schedule FROM locations WHERE userId = ?",
                            (user_id,))
        return json.loads(self.cursor.fetchall()[0][0])

    def get_users(self):
        """Получение всех пользователей в БД"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        """Удаление пользователя из БД"""
        if not self.is_user_exists(user_id):
            raise UserDoesNotExistError("User does not exist")
        self.cursor.execute("DELETE FROM locations WHERE userId = ?", (user_id,))
        self.cursor.execute("DELETE FROM users WHERE userId = ?", (user_id,))
        return self.connect.commit()

    def close(self):
        """Завершить соединение с БД"""
        self.connect.close()
