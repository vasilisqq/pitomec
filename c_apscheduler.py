from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pitomec import Pitomec
from aiogram.types import BufferedInputFile


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
        await Pitomec.crack(pet)
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
        self.hatch(pet, "time_to_hatch")
    

    @scheduled_task
    async def hatch(self, pet: Pitomec, att: str):
        await Pitomec.hatch(pet)
        image = await Pitomec.get_image(pet)
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} вылупился\n через какое-то время он может заскучать, проголодаться или захотеть гулять, следи за своим питомцем вместе с партнером, все задания нужно выполнять вдвоем, а не по отдельности!!"
        )
        image.seek(0)
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} вылупился\n через какое-то время он может заскучать, проголодаться или захотеть гулять, следи за своим питомцем вместе с партнером, все задания нужно выполнять вдвоем, а не по отдельности!!"
        )

