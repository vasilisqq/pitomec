from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from datetime import datetime, timedelta
import os
from pathlib import Path
import pickle

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()
    bot: Bot = None
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


    def __init__(self, born_time:datetime, user_id:int|str) -> None:
        try:
            with open(f"pets/{self.id}/backup.pkl", "wb") as file:
                pickle.dump(self, file)
                file.close()
            self.time_born = born_time
            self.owner1 = user_id
            self.id = hashlib.sha256(
                str(user_id).encode()
            ).hexdigest()
            Pitomec.all_accesses.update({str(user_id):self})
            self.owner2 = None
            self.photo = ""
            self.hour_timer_first = None
            self.hour_timer_second = None
            self.egg = None
        except:
            with open(f"pets/{self.id}/backup.pkl", "rb") as file:
                self = pickle.load(file)
                file.close()
            Pitomec.all_accesses.update({str(user_id):self, })
        


    async def add_owner(self, user_id) -> None:
        Pitomec.scheduler.start()
        self.owner2 = user_id
        self.hour_timer_first = random.randint(5,10)
        self.hour_timer_second = random.randint(1,3)
        await self.create_task()
    
    async def init_photo(self, photo_name:str) -> None:
        image = Image.open(f"photos/eggs/{photo_name}")
        image.save(f"pets/{self.id}/image.png")

    async def create_task(self):
        Pitomec.scheduler.add_job(
            self.send_message,
            trigger='date',
            run_date=datetime.now()+timedelta(seconds=10),
            kwargs={"text":str(self.hour_timer_first)}
        )


    async def send_message(self, text:str):
        await Pitomec.bot.send_message(
            self.owner1,
            text=text
        )
        self.hour_timer_first = random.randint(5,10)
        await self.create_task()

