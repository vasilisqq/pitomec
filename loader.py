from aiogram import Dispatcher, Bot
from config import settings
from pathlib import Path
import pickle
import copy
from pitomec import Pitomec

dp = Dispatcher()
bot = Bot(settings.BOT_TOKEN.get_secret_value())

def import_all_exists_peets():
    for item in Path("pets").rglob("*.pkl"):
        with open(item, "rb") as f:
            pet = pickle.load(f)
            pt = copy.deepcopy(pet)
        Pitomec.all_accesses.update(
            {pt.owner1:pt,
             pt.owner2:pt}
        )
        print(pt)

import_all_exists_peets()