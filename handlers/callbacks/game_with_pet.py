from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()
@router.callback_query(F.data == "game")
async def start_game(query: CallbackQuery, pet):
    ...