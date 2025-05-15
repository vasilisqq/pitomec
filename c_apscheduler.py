from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pitomec import Pitomec
from functools import wraps

class C_scheduler():

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    def start_sc(self):
        self.scheduler.start()

    async def scheduled_task(func):
        def wrapper(self, pit):
            self.scheduler.add_job(
                func,
                trigger="date",
                run_date=pit.time_to_born,
                kwargs={"pet":pit, "self":self}
            )
        return wrapper
    

    @scheduled_task
    async def hatch(self, pet: Pitomec):
        print("hello")

c_scheduler = C_scheduler()
