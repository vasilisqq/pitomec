import asyncio
from bot.handlers import main_router_handler
from bot.contexts import main_router_contexts
from loader import bot, dp
from bot.middlewares.find_pit import UserMiddleware
from db.DAO import DAO
from logger import logger, init_logger
from c_apscheduler import ini_scheduler

async def main() -> None:
    init_logger()
    ini_scheduler()
    try:
        await DAO.delete()
        dp.update.middleware(UserMiddleware())
        dp.include_routers(main_router_contexts, main_router_handler)
        await bot.delete_webhook(True)
        logger.info("успешный старт бота")
        await dp.start_polling(bot, close_bot_session=True)
    except:
        logger.error("Что то пошло не так")


if __name__ == "__main__":
    asyncio.run(main())
