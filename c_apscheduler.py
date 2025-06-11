from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pitomec import Pitomec
from aiogram.types import BufferedInputFile
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
        await pet.crack()
        # pet.time_to_born = pet.birthday + timedelta(seconds=10)
        # del pet.time_to_crack
        image = await Pitomec.get_image(pet)
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} скоро уже вылупится"
        )
        image.seek(0)
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} скоро уже вылупится"
        )

    

    @scheduled_task
    async def hatch(self, pet: Pitomec, att: str):
        pet.essense = "cat"
        pet.mood = "happy"
        del pet.time_to_born
        image = await Pitomec.get_image(pet)
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} вылупился"
        )
        image.seek(0)
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} вылупился"
        )
        await pet.create_back_up()

