from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import os
import pickle

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()

    def __init__(self, user_id:int|str, last_message) -> None:
        self.birthday = None
        self.owner1 = user_id
        self.id = hashlib.sha256(
            str(user_id).encode()
        ).hexdigest()
        Pitomec.all_accesses.update({str(user_id):self})
        self.owner2 = None
        self.time_to_crack = None
        self.last_message_ids = [
            last_message,
            last_message-1,
            last_message-2]
        self.essense = "egg"
        self.mood = "whole"
    

    async def add_owner(self, user_id) -> None:
        self.owner2 = user_id
        self.birthday = datetime.now()
        self.time_to_crack = self.birthday + timedelta(seconds=20)
        del self.last_message_ids
        await self.create_back_up()


    async def create_back_up(self):
        with open(f"pets/{self.id}.pkl", "wb") as f:
            pickle.dump(self, f)
            f.close()
    
    async def get_image(self):
        return f"{self.essense}/{self.mood}"

