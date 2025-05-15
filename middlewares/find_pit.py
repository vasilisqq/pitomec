from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
from pitomec import Pitomec

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
        try:
            pitomec = Pitomec.all_accesses[current_event.from_user.id]
            data["pit"] = pitomec
        except:
            data["pit"] = None
        return await handler(event, data)