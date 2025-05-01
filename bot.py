import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from handlers import main_router_handler
from contexts import main_router_contexts
import logging


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(settings.BOT_TOKEN.get_secret_value())
    dp.include_routers(
        main_router_contexts,
        main_router_handler
    )
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
