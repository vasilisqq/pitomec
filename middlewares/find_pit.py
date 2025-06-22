from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
from pets.pitomec import Pitomec
from db.DAO import DAO

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        #        есть какаято функция которой мы передаем Update и какие то данные в dict и вызывается это все асинхронно
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        current_event = (
            event.message
            or event.callback_query
            or event.inline_query
            or event.chosen_inline_result
        )
        if not current_event:
            return 
        data["pet"] = await DAO.find_pet(current_event.from_user.id)
        return await handler(event, data)