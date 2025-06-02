import asyncio
from handlers import main_router_handler
from contexts import main_router_contexts
from loader import bot, dp, import_all_exists_peets
from middlewares.find_pit import UserMiddleware
from loader import c_scheduler
from pitomec import Pitomec

async def main() -> None:
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        main_router_contexts,
        main_router_handler
    )
    dp.startup.register(import_all_exists_peets)
    await bot.delete_webhook(True)
    print("succes_start")
    await dp.start_polling(bot, close_bot_session=True)


if __name__ == "__main__":
    asyncio.run(main())
    
