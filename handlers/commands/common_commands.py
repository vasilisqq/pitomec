from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from config import settings
from aiogram.fsm.context import FSMContext
from pitomec import Pitomec
from datetime import datetime
from aiogram.types import FSInputFile
from text import create_ref

router = Router()

@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext, pet):
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
                await state.set_state(Pitomec.name)
                await message.answer("Введите имя питомца")
    else:
        await message.answer_photo(
            caption="Вот твой питомец",
            photo=FSInputFile(f"pets/{pet.id}/photo.jpg"))

