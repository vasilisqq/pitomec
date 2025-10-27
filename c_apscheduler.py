from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from pets.pitomec import Pitomec
from aiogram.types import BufferedInputFile
from db.DAO import DAO
# from datetime import datetime, timedelta
from bot.keyboards.inline import to_be_happy_btn, hungry_bttn, walk_bttn
from aiogram.fsm.context import FSMContext
import random
# from datetime import timezone

class C_scheduler():

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    def start_sc(self):
        self.scheduler.start()

    def scheduled_task(func):
        def wrapper(self, pit, **kwargs):
            self.scheduler.add_job(
                func,
                trigger="date",
                run_date=getattr(pit, kwargs.get('att')),
                kwargs={"pet":pit, "self":self, "att":kwargs.get('att')}
            )
        return wrapper
    

    @scheduled_task
    async def crack(self, pet, **kwargs):
        await Pitomec.crack(pet)
        await bot.send_message(
            chat_id=pet.owner1,
            text=f"""Яйцо дало первые трещинки!🥚🥚🥚
Еще немного терпения — {pet.name} уже готов вылупиться.
Следи за обновлениями или проверь через /me"""
        )
        await bot.send_message(
            chat_id=pet.owner2,
            text=f"""Яйцо дало первые трещинки!🥚🥚🥚
Еще немного терпения — {pet.name} уже готов вылупиться.
Следи за обновлениями или проверь через /me"""
        )
        self.hatch(pet, att="time_to_hatch")
    

    @scheduled_task
    async def hatch(self, 
                    pet: Pitomec, 
                    **kwargs
                    ):
        await Pitomec.hatch(pet)
        image = await Pitomec.get_image(pet)
        await bot.send_photo(
            chat_id=pet.owner1,
            photo=image,
            caption=f"""{pet.name} вылупился!🎉🎉🎉
Поздравляем! Теперь ваш новый друг рядом.
Он может загрустить без внимания"""
        )
        await bot.send_photo(
            chat_id=pet.owner2,
            photo=image,
            caption=f"""{pet.name} вылупился!🎉🎉🎉
Поздравляем! Теперь ваш новый друг рядом.
Он может загрустить без внимания"""
        )
        await Pitomec.unhappy(pet)
        self.unhappy(pet, att="time_to_unhappy")
        await Pitomec.hungry(pet) 
        self.hungry(pet, att="time_to_hungry")
        await Pitomec.walk(pet)
        self.walk(pet, att="time_to_walk")
        await DAO.upd(pet)

    @scheduled_task
    async def unhappy(self, pet: Pitomec, **kwargs):
        await Pitomec.change_mood(pet, "unhappy")
        image = await Pitomec.get_image(pet)
        #await bot.send_photo(
        await bot.send_message(
            chat_id=pet.owner1,
            #photo=image,
            text=f"{pet.name} грустит.....\n поиграй с ним",
            reply_markup=to_be_happy_btn
        )
        #await bot.send_photo(
        await bot.send_message(
            chat_id=pet.owner2,
            #photo=image,
            text=f"{pet.name} грустит.....\n поиграй с ним",
            reply_markup=to_be_happy_btn
        )
        
    @scheduled_task
    async def hungry(self, pet: Pitomec, **kwargs):
        await Pitomec.change_mood(pet, "hungry")
        keyboard = hungry_bttn()
        await bot.send_message(
            chat_id=pet.owner1,
            text=f"{pet.name} голоден.....\n покорми его",
            reply_markup=keyboard
        )
        await bot.send_message(
            chat_id=pet.owner2,
            text=f"{pet.name} голоден.....\n покорми его",
            reply_markup=keyboard
        )         

    @scheduled_task
    async def walk(self, pet: Pitomec, **kwargs):
        await Pitomec.change_mood(pet, "walk")
        keyboard = walk_bttn()
        await bot.send_message(
            chat_id=pet.owner1,
            text=f"{pet.name} хочет погулять.....\n выведи его на улицу",
            reply_markup=keyboard
        )
        await bot.send_message(
            chat_id=pet.owner2,
            text=f"{pet.name} хочет погулять.....\n выведи его на улицу",
            reply_markup=keyboard
        ) 
