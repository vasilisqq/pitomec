from aiogram import Dispatcher, Bot
from config import settings
from pathlib import Path
import pickle
from pitomec import Pitomec

dp = Dispatcher()
bot = Bot(settings.BOT_TOKEN.get_secret_value())

def import_all_exists_peets():
    for item in Path("pets").rglob("*.pkl"):
        with open(item, "rb") as f:
            pet = pickle.load(f)
            Pitomec.all_accesses.update(
                {pet.owner1:pet,
                pet.owner2:pet})
            f.close()