from aiogram import Dispatcher, Bot
from config import settings
from pathlib import Path
import pickle
from datetime import datetime
from pitomec import Pitomec
from aiogram.types import FSInputFile


pending_tasks = []
dp = Dispatcher()
bot = Bot(settings.BOT_TOKEN.get_secret_value())
from c_apscheduler import C_scheduler

c_scheduler = C_scheduler()
async def import_all_exists_peets(dispatcher):
    await process_pkl_files()
    c_scheduler.start_sc()
    for instance in pending_tasks:
        await send_actual_message(instance)


def check_current_state(pet):
    if pet.mood == "whole":
        pet.time_to_crack > datetime.now()


async def process_pkl_files():
    """Асинхронная обработка PKL файлов"""
    for item in Path("pets").rglob("*.pkl"):
        # Загружаем объект из файла
        with open(item, 'rb') as f:
                pet = pickle.load(f)
                Pitomec.all_accesses.update(
                {pet.owner1:pet,
                pet.owner2:pet})
        # Проверяем время отправки
        if pet.time_to_crack <= datetime.now():
            # Немедленная отправка после запуска бота
            pending_tasks.append(pet)
        else:
            # Планируем отправку через APScheduler
            c_scheduler.crack(pet, "time_to_crack")
       

async def send_actual_message(pet):
    await bot.send_photo(
            chat_id=pet.owner1,
            photo=FSInputFile(f"photos/{await pet.get_image()}.png"),
            caption=f"{pet.name} скоро уже вылупится"
        )
    print(f"Отправка сообщения: {pet.id}")
