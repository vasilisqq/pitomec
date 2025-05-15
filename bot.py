import asyncio
from handlers import main_router_handler
from contexts import main_router_contexts
from loader import bot, dp
from middlewares.find_pit import UserMiddleware

from pitomec import Pitomec

async def main() -> None:
    print("success")
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        main_router_contexts,
        main_router_handler
    )
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
