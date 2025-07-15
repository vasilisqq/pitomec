from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import timezone


router = Router()
@router.callback_query(F.data == "game")
async def start_game(query: CallbackQuery, pet):
    print("qqq")
    if pet.mood.find("unhappy") != -1:
        pet_time = pet.time_to_unhappy.replace(tzinfo=timezone.utc)
        print(pet_time)
        print(query.message.date)
        if query.message.date <= pet_time:
            await query.answer("Это старое сообщение")
    await query.bot.delete_message(
        chat_id=query.from_user.id,
        message_id=query.message.message_id
    )