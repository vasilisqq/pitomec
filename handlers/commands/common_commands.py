from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message, InputFile, BufferedInputFile
from config import settings
from aiogram.fsm.context import FSMContext
from pets.pitomec import Pitomec
from datetime import datetime
from aiogram.types import FSInputFile
from text import create_ref
from loader import c_scheduler, states_p

router = Router()

@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext, pet):
    print(await state.get_data())
    if not pet:
        args = message.text.split(maxsplit=2)
        if len(args)==1: 
            await message.answer_photo(
                photo=FSInputFile("photos/logo.png"),
                caption="Привет, это игра для выращивания питомца со своей второй полвинкой\n перешли следующее сообщение, чтобы создать своего питомца",
            )
            l_m = await message.answer(await create_ref(message.from_user.id),
                            parse_mode="HTML")
            
            Pitomec(message.from_user.id, l_m.message_id)
        if len(args) == 2:
            if args[1] == str(message.from_user.id):
                await message.answer("нельзя создать питомца с самим собой")
            else:
                Pitomec.all_accesses.update(
                    {str(message.from_user.id):Pitomec.all_accesses[args[1]]})
                await Pitomec.save_accesses()
                await state.set_state(states_p.name)
                await message.answer("Введи имя питомца")
    else:
        await message.answer(
            "Чтобы посмотреть на питомца, пропиши команду /me"
        )
        

@router.message(Command("me"))
async def start_bot(message: Message, state: FSMContext, pet):
    photo = await Pitomec.get_image(pet)
    if pet.time_to_hatch > datetime.now():
        await message.answer_photo(
        caption= await Pitomec.calculate_time(pet),
        photo= BufferedInputFile(photo.read(), "f.JPEG")
        )
    else:
        await message.answer_photo(
        caption="Вот твой питомец",
        photo= BufferedInputFile(photo.read(), "f.JPEG")
        )
        # await Pitomec.unhappy(pet)
        # c_scheduler.unhappy(pet, "time_to_unhappy")
    
# @router.message(Command("test"))
# async def start_bot(message: Message, state: FSMContext, pet):
#     c_scheduler.hungry(pet, "time_to_hungry")