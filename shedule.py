import schedule
import threading
# from pytz import timezone
import time

class ScheduleBot:
    def __init__(self):
        self.s = schedule.Scheduler()
        self.stop_run_continuously = ScheduleBot.run_continuously(self)

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

    def stop_schedule(self):
        self.stop_run_continuously.set()

    def print_schedule(self):
        print(self.s.get_jobs())


