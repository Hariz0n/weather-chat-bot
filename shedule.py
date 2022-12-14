import schedule
import threading
import datetime as dt
import time


class ScheduleBot:

    def __init__(self):
        self.s = schedule.Scheduler()
        self.stop_run_continuously = ScheduleBot.run_continuously(self)
        self.weekdays = {
            "ПН": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().monday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "ВТ": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().tuesday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "СР": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().wednesday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "ЧТ": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().thursday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "ПТ": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().friday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "СБ": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().saturday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "ВС": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().sunday.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
            "Ежедн": lambda s, user_time, user_time_zone, user_id, func, *args: s.every().day.at(
                self.localize_time(user_time, user_time_zone)).do(func, *args).tag(
                user_id),
        }

    def run_continuously(self, interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.s.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def add_week_tasks(self, user_schedule, user_time_zone, user_id, func, *args):
        for x in user_schedule:
            for i in x.split(", "):
                self.weekdays[i](self.s, user_schedule[x], user_time_zone, user_id, func, *args)

    def update_week_tasks(self, user_schedule, user_time_zone, user_id, func, *args):
        self.delete_user_tasks(user_id)
        self.add_week_tasks(user_schedule, user_time_zone, user_id, func, *args)

    def stop_schedule(self):
        self.stop_run_continuously.set()

    def delete_all_tasks(self):
        self.s.clear()

    def delete_user_tasks(self, user_id):
        self.s.clear(user_id)

    def print_schedule(self):
        print(self.s.get_jobs())

    @staticmethod
    def localize_time(user_time, current_time_zone):
        loc_time = dt.datetime.strptime(user_time, "%H:%M")
        time_zone = dt.timedelta(seconds=10800 - current_time_zone)
        loc_time = loc_time + time_zone
        loc_time = loc_time.strftime("%H:%M")
        return loc_time
