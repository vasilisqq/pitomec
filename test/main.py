import asyncio
import sys
import os
#from bot.handlers import main_router_handler
#from bot.contexts import main_router_contexts
#from loader import bot, dp, import_all_exists_peets
#from bot.middlewares.find_pit import UserMiddleware
#from db.DAO import DAO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from celery_app import celery_app
from loader import dp, bot
from aiogram import Router,F
from aiogram.filters import Command
router = Router()
async def main() -> None:
    #await DAO.delete()
    #dp.update.middleware(UserMiddleware())
    dp.include_routers(
        router,
    #    main_router_handler
    )
    #dp.startup.register(import_all_exists_peets)
    await bot.delete_webhook(True)
    print("succes_start")
    await dp.start_polling(bot, close_bot_session=True)

@router.message(Command("start"))
async def start(message):
    await message.answer("ASDASD")

@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def send_telegram_message(self, chat_id, text, parse_mode='HTML'):
    await bot.send_message(
        
    )
        

if __name__ == "__main__":
    asyncio.run(main())
    
