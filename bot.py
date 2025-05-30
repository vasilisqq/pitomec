import asyncio
from handlers import main_router_handler
from contexts import main_router_contexts
from loader import bot, dp, import_all_exists_peets
from middlewares.find_pit import UserMiddleware
from c_apscheduler import c_scheduler
from pitomec import Pitomec

async def main() -> None:
    import_all_exists_peets()  
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        main_router_contexts,
        main_router_handler
    )
    await bot.delete_webhook(True)
    c_scheduler.start_sc()
    print("succes_start")
    await dp.start_polling(bot, close_bot_session=True)


if __name__ == "__main__":
    asyncio.run(main())
    
