from aiogram import Dispatcher, Bot
from config import settings
from pathlib import Path
import pickle
from datetime import datetime
from pitomec import Pitomec
from aiogram.types import BufferedInputFile
from db.DAO import DAO
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis 

pending_tasks = []

storage = RedisStorage(
    redis=redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        password=settings.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True
    )
)

dp = Dispatcher(storage=storage)
bot = Bot(settings.BOT_TOKEN.get_secret_value())
from c_apscheduler import C_scheduler

c_scheduler = C_scheduler()
async def import_all_exists_peets(dispatcher):
    # await get_all()
    c_scheduler.start_sc()
    await load_accesess()
    # await clear_all_fsm_data(storage)

async def clear_all_fsm_data(storage: RedisStorage):
    prefix = storage.key_builder.prefix
    separator = storage.key_builder.separator
    pattern = f"{prefix}{separator}*"
    keys = []
    async for key in storage.redis.scan_iter(match=pattern):
        keys.append(key)
    if keys:
        await storage.redis.delete(*keys)

async def load_accesess():
    with open("accesses.pkl", "rb") as f:
        Pitomec.all_accesses = pickle.load(f)
        f.close()

def check_current_state(pet):
    if pet.mood == "whole":
        pet.time_to_crack > datetime.now()


async def get_all():
    """Асинхронная обработка PKL файлов"""
    pets = await DAO.get_all()
    print(pets)
    for pet in pets:
        if pet.time_to_unhappy:
            ...
        elif pet.time_to_hatch:
            ...
        elif pet.time_to_crack:
            if pet.time_to_crack <= datetime.now():
                await already_cracked(pet)
            else:
                # Планируем отправку через APScheduler
                c_scheduler.crack(pet, "time_to_crack")
       

async def already_cracked(pet):
    image = await Pitomec.get_image(pet)
    await bot.send_photo(
            chat_id=pet.owner1,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} скоро уже вылупится"
        )
    image = await Pitomec.get_image(pet)
    await bot.send_photo(
            chat_id=pet.owner1,
            photo=BufferedInputFile(image.read(), "f.JPEG"),
            caption=f"{pet.name} скоро уже вылупится"
        )
    print(f"Отправка сообщения: {pet.id}")
