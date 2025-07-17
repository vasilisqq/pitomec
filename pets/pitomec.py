from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pickle
from db.DAO import DAO
from io import BytesIO
from dateutil.relativedelta import relativedelta
import random
from aiogram.types import BufferedInputFile
# from datetime import timezone

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()


    def __init__(self, user_id:int|str, last_message) -> None:
        self.birthday = None
        self.owner1 = user_id
        Pitomec.all_accesses.update({str(user_id):self})
        self.owner2 = None
        self.time_to_crack = None
        self.time_to_hatch = None
        self.last_message_ids = [
            last_message,
            last_message-1,
            last_message-2]
        self.essense = "egg"
        self.mood = "whole"
    

    async def add_owner(self, user_id) -> None:
        self.owner2 = user_id
        self.birthday = datetime.now()
        self.time_to_crack = self.birthday + timedelta(seconds=2)
        self.time_to_hatch = self.birthday + timedelta(seconds=4)
        del self.last_message_ids
        pet = await DAO.insert_pet(self)
        del Pitomec.all_accesses[str(self.owner1)]
        del Pitomec.all_accesses[str(user_id)]
        del self
        return pet


    @classmethod
    async def get_image(cls, pet):
        img_buffer = BytesIO()
        image = Image.open(f"photos/back.JPEG")
        moods = pet.mood.split(" ")
        if len(moods) > 1:
            im2 = Image.open(f"photos/{pet.essense}/{pet.moods[0]}.png")
        else:
            im2 = Image.open(f"photos/{pet.essense}/{pet.mood}.png")
        image.paste(im2, (0,0), mask=im2)
        image.save(img_buffer, format="JPEG", quality=95)
        img_buffer.seek(0)
        return BufferedInputFile(img_buffer.read(), "f.JPEG")
        
    @classmethod
    async def crack(cls, pet):
        pet.mood = "nock"
        await DAO.upd(pet)

    @classmethod
    async def hatch(cls, pet):
        pet.essense = "hipopotam"
        pet.mood = "happy"
        await DAO.upd(pet)

    @classmethod
    async def save_accesses(cls):
        with open("accesses.pkl", "wb") as f:
            pickle.dump(
                Pitomec.all_accesses,
                f
            )
            f.close()
    
    @classmethod
    async def calculate_time(cls, pet):
        delta = pet.time_to_hatch - datetime.now()
        total_seconds = abs(round(delta.total_seconds()))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f"{pet.name} вылупится через: {hours} ч {minutes} мин" 
        return f"{pet.name} вылупится через: {minutes} мин"
    
    @classmethod
    async def unhappy(cls, pet):
        pet.time_to_unhappy = datetime.now() + timedelta(seconds=2)
        
    @classmethod
    async def change_mood(cls, pet, new_mood):
        if pet.mood == "happy":
            pet.mood = new_mood
        else:
            pet.mood += new_mood
        await DAO.upd(pet)

    # @classmethod
    # async def hungry(cls, pet):
    #     pet.time_to_hungry = datetime.now() + timedelta(hours=random.randint(5,6))


    # @classmethod
    # async def walk(cls, pet):
    #     pet.time_to_walk = datetime.now() + timedelta(hours=random.randint(3,5))

        
