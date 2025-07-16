from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import timezone
from aiogram.fsm.context import FSMContext
from loader import states_p, set_states, set_data
from zoneinfo import ZoneInfo
from pets.pitomec_in_game import PetGame

router = Router()
@router.callback_query(F.data == "game")
async def start_game(query: CallbackQuery, pet, state : FSMContext):
    print("qqq")
    if pet.mood.find("unhappy") != -1:
        time = pet.time_to_unhappy.astimezone(ZoneInfo("UTC"))
        time = time.replace(microsecond=0)
        if query.message.date < time:
            await query.answer(
                "Это старое сообщение",
                show_alert=True)
        else:
            await set_states(states_p.game, pet)
            await set_data(pet, await PetGame.create_field())
    else:
        await query.answer(f"{pet.name} больше не грустит")
    await query.bot.delete_message(
        chat_id=query.from_user.id,
        message_id=query.message.message_id
    )



