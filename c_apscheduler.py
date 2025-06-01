from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pitomec import Pitomec
from functools import wraps
from aiogram.types import FSInputFile
from PIL import Image
from datetime import timedelta

class C_scheduler():

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    def start_sc(self):
        self.scheduler.start()

    def scheduled_task(func):
        def wrapper(self, pit, att):
            self.scheduler.add_job(
                func,
                trigger="date",
                run_date=getattr(pit, att),
                kwargs={"pet":pit, "self":self, "att":att}
            )
        return wrapper
    

    @scheduled_task
    async def crack(self, pet: Pitomec, att: str):
        # image = Image.open(f"pets/{pet.id}.image.png")

        image = Image.open(f"photos/eggs/nock.png")
        image.save(f"pets/{pet.id}/image.png")
        pet.time_to_born = pet.birthday + timedelta(seconds=10)
        del pet.time_to_crack
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=FSInputFile(f"pets/{pet.id}/image.png"),
            caption=f"{pet.name} скоро уже вылупится"
        )
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=FSInputFile(f"pets/{pet.id}/image.png"),
            caption=f"{pet.name} скоро уже вылупится"
        )
        self.hatch(pet, "time_to_born")
        await pet.create_back_up()
    
    @scheduled_task
    async def hatch(self, pet: Pitomec, att: str):
        # # image = Image.open(f"pets/{pet.id}.image.png")

        image = Image.open(f"photos/pets/cat.jpg")
        image.save(f"pets/{pet.id}/image.png")
        del pet.time_to_born 
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=FSInputFile(f"pets/{pet.id}/image.png"),
            caption=f"{pet.name} вылупился"
        )
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=FSInputFile(f"pets/{pet.id}/image.png"),
            caption=f"{pet.name} вылупился"
        )
        await pet.create_back_up()

c_scheduler = C_scheduler()
