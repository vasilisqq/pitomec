from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pickle
from db.DAO import DAO
from io import BytesIO

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()

    def __init__(self, user_id:int|str, last_message) -> None:
        self.birthday = None
        self.owner1 = user_id
        # self.id = hashlib.sha256(
        #     str(user_id).encode()
        # ).hexdigest()
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
        self.time_to_crack = self.birthday + timedelta(seconds=5)
        del self.last_message_ids
        await DAO.insert_pet(self)
        del Pitomec.all_accesses[str(self.owner1)]
        del Pitomec.all_accesses[str(self.owner2)]
        del self


    @classmethod
    async def get_image(cls, pet):
        img_buffer = BytesIO()
        image = Image.open(f"photos/back.JPEG")
        im2 = Image.open(f"photos/{pet.essense}/{pet.mood}.png")
        image.paste(im2, (0,0), mask=im2)
        image.save(img_buffer, format="JPEG", quality=95)
        img_buffer.seek(0)
        return img_buffer
        
    @classmethod
    async def crack(cls, pet):
        pet.time_to_crack = pet.birthday + timedelta(seconds=10)
        pet.mood = "nock"
        await DAO.crack(pet)

    @classmethod
    async def hatch(cls, pet):
        pet.essense = "hipopotam"
        pet.mood = "happy"
        await DAO.hatch(pet)

