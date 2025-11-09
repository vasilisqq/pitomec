from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import states_p
from zoneinfo import ZoneInfo
from loader import states_p, dp
from pets.pitomec_in_game import choose_ingridients

router = Router()

@router.callback_query(F.data == "hungry")
async def start_feed(query: CallbackQuery, pet, state : FSMContext):
    if await state.get_state() == states_p.feed:
        await query.answer(
            text="Ты уже кормишь питомца",
            show_alert=True
        )
    elif pet.mood.find("hungry") != -1:
        time = pet.time_to_hungry.astimezone(ZoneInfo("UTC"))
        time = time.replace(microsecond=0)
        if query.message.date < time:
            await query.answer(
                "Это старое сообщение",
                show_alert=True)
        else:
            await dp.set_states(states_p.feed, pet, query.bot)
            ing = await choose_ingridients(pet)
            await query.bot.send_message(
                chat_id=pet.owner1,
                text=f"пришли {ing[pet.owner1][0]} чтобы покормить {pet.name}"
            )
            await query.bot.send_message(
                chat_id=pet.owner2,
                text=f"пришли {ing[pet.owner2][0]} чтобы покормить {pet.name}"
            )
            await dp.set_data(
                pet, 
                ing,query.bot)
    await query.message.delete()




