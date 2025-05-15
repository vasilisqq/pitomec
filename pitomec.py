from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import os
import pickle

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


    def __init__(self, user_id:int|str) -> None:
        self.birthday = None
        self.owner1 = user_id
        self.id = hashlib.sha256(
            str(user_id).encode()
        ).hexdigest()
        Pitomec.all_accesses.update({str(user_id):self})
        self.owner2 = None
        self.photo = ""
        self.egg = None
        self.time_to_born = None 

    async def add_owner(self, user_id) -> None:
        self.owner2 = user_id
        os.makedirs(f"pets/{self.id}")
        image = Image.open(f"photos/eggs/whole.png")
        image.save(f"pets/{self.id}/image.png")
        self.birthday = datetime.now()
        self.time_to_born = self.birthday + timedelta(seconds=10)

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



