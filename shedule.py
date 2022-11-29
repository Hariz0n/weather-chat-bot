import json

import schedule
import threading
# from pytz import timezone
import time


class ScheduleBot:

    def __init__(self):
        self.s = schedule.Scheduler()
        self.stop_run_continuously = ScheduleBot.run_continuously(self)
        self.weekdays = {
            "Mon": lambda s, user_time, func, *args: s.every().monday.at(user_time).do(func, *args),
            "Tue": lambda s, user_time, func, *args: s.every().tuesday.at(user_time).do(func, *args),
            "Wed": lambda s, user_time, func, *args: s.every().wednesday.at(user_time).do(func, *args),
            "Thu": lambda s, user_time, func, *args: s.every().thursday.at(user_time).do(func, *args),
            "Fri": lambda s, user_time, func, *args: s.every().friday.at(user_time).do(func, *args),
            "Sat": lambda s, user_time, func, *args: s.every().saturday.at(user_time).do(func, *args),
            "Sun": lambda s, user_time, func, *args: s.every().sunday.at(user_time).do(func, *args),
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

    def add_task(self, user_time, func, *args):
        self.s.every().day.at(user_time).do(func, *args)

    def add_week_tasks(self, weekdays, user_time, func, *args):
        for weekday in weekdays:
            self.weekdays[weekday](self.s, user_time, func, *args)

    def stop_schedule(self):
        self.stop_run_continuously.set()

    def delete_all_tasks(self):
        self.s.clear()

    def print_schedule(self):
        print(self.s.get_jobs())
