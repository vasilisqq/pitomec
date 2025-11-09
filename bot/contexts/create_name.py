from aiogram import Router
from pets.pitomec import Pitomec
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from loader import states_p
from c_apscheduler import scheduler
from aiogram import Bot
from pets.pitomec import Pitomec


router = Router()

@router.message(states_p.name)
async def set_pit_name(message: Message, state: FSMContext):
    d = await state.get_data()
    pet = await Pitomec.create_pet(
        owner1=d["first"],
        owner2=str(message.from_user.id),
        name = message.text
        )
    await state.clear()
    image = await Pitomec.get_image(pet)
    await message.answer_photo(
        photo=image,
        caption=f"""{pet.name} в яйце 🐣🐣🐣.
Теперь остается ждать, когда он появится на свет!
Проверь статус через команду /me"""
    )
    await message.bot.send_photo(
        chat_id=pet.owner1,
        photo=image,
        caption=f"""{pet.name} в яйце 🐣🐣🐣.
Теперь остается ждать, когда он появится на свет!
Проверь статус через команду /me"""
        )
    scheduler.crack(pet, att="time_to_crack")

