from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import timezone
from aiogram.fsm.context import FSMContext
from loader import states_p, set_states, set_data
from zoneinfo import ZoneInfo
from pets.pitomec_in_game import PetGame
from aiogram.types import FSInputFile
from keyboards import create_field

router = Router()
@router.callback_query(F.data == "game")
async def start_game(query: CallbackQuery, pet, state : FSMContext):
    if await state.get_state() == states_p.game:
        await query.answer(
            text="Ты уже играешь с питомцем",
            show_alert=True
        )
    elif pet.mood.find("unhappy") != -1:
        time = pet.time_to_unhappy.astimezone(ZoneInfo("UTC"))
        time = time.replace(microsecond=0)
        if query.message.date < time:
            await query.answer(
                "Это старое сообщение",
                show_alert=True)
        else:
            await set_states(states_p.game, pet)
            await set_data(pet, await PetGame.create_field(query.from_user.id))
            photo=FSInputFile("photos/hided.png")
            kb = create_field()
            await query.message.answer_photo(
                photo,
                caption=f"{pet.name} спрятался за одним из этих деревьев, выбирайте по очереди, пока не найдете своего питомца \n делай первый ход",
                reply_markup=kb
            )
            await query.bot.send_photo(
                chat_id=pet.owner2,
                photo=photo,
                caption=f"{pet.name} спрятался за одним из этих деревьев, выбирайте по очереди, пока не найдете своего питомца",
                reply_markup=kb
            )
    else:
        await query.answer(f"{pet.name} больше не грустит")
    await query.bot.delete_message(
        chat_id=query.from_user.id,
        message_id=query.message.message_id
    )

@router.callback_query(F.data.in_([str(i) for i in range(9)]))
async def answer_on_moove(query: CallbackQuery, state: FSMContext, pet):
    # print(query.data)
    st = await state.get_data()
    if query.data == st["hatch"]:
        await query.message.delete()
        await query.message.answer_photo(
            FSInputFile("photos/hipopotam/happy.png")
        )
    # await query.message.answer(str(st))
