from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import hashlib
from PIL import Image

class Pitomec(StatesGroup):

    all_accesses = {}
    name = State()
    def __init__(self,born_time:datetime, user_id:int|str) -> None:
        self.time_born = born_time
        self.owner1 = user_id
        self.id = hashlib.sha256(
            str(user_id).encode()
        ).hexdigest()
        Pitomec.all_accesses.update({str(user_id):self})
        self.photo = ""

    async def add_owner(self, user_id) -> None:
        self.owner2 = user_id
    
    async def init_photo(self, photo_name:str) -> None:
        image = Image.open(f"photos/eggs/{photo_name}")
        image.save(f"pets/{self.id}.png")

