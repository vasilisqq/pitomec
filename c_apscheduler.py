from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pitomec import Pitomec
from functools import wraps

class C_scheduler():

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    def start_sc(self):
        self.scheduler.start()

    def scheduled_task(func):
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
        await bot.send_message(
            chat_id=pet.owner1,
            text="питомец вылупился"
        )
        await bot.send_message(
            chat_id=pet.owner2,
            text="питомец вылупился"
        )
        del pet.time_to_born

c_scheduler = C_scheduler()
