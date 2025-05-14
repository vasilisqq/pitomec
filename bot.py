import asyncio
from handlers import main_router_handler
from contexts import main_router_contexts
from loader import bot, dp


from pitomec import Pitomec

async def main() -> None:
    dp.include_routers(
        main_router_contexts,
        main_router_handler
    )
    bot.delete_webhook(True)
    await dp.start_polling(Pitomec.bot)


if __name__ == "__main__":
    asyncio.run(main())
    
