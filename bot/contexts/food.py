from aiogram import Router
from pets.pitomec import Pitomec
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from loader import c_scheduler, states_p, clear_state, set_data
from aiogram import Bot
from pets.pitomec import Pitomec

router = Router()

@router.message(states_p.feed)
async def set_pit_name(message: Message, state: FSMContext, pet):

    st = await state.get_data()
    if st[str(message.from_user.id)][1]:
        await message.answer(
            text="Ты уже отправил свой ингридиент, ждем второго"
        )
    elif st[str(message.from_user.id)][0] == message.text:
        await message.answer(
            text="ты правильно прислал свой фрукт"
        )
        st[str(message.from_user.id)][1] = True
        await set_data(
                pet, 
                st)
        if st[str(pet.owner2) if pet.owner1 == message.from_user.id else str(pet.owner1)][1]:
            await message.bot.send_message(
                chat_id=pet.owner1,
                text=f"покормлен"
            )
            await message.bot.send_message(
                chat_id=pet.owner2,
                text=f"покормлен"
            )
            await clear_state(pet)
            await Pitomec.hungry(pet, "hungry")
            c_scheduler.hungry(pet, "time_to_hungry")
    else:
        await message.answer(
            "ты ввел непрвильный ингридиент, попробуй еще раз"
        )    


