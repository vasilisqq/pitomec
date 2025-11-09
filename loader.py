from aiogram import Bot
from config import settings
import redis.asyncio as redis
from pets.states import StatesP
from dispatcher import DispatcherExpanded
from redis_exp import RedisStorageExpanded


storage = RedisStorageExpanded(
        redis=redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        password=settings.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True,
        )
    )
dp = DispatcherExpanded(storage=storage)
states_p = StatesP()
bot = Bot(settings.BOT_TOKEN.get_secret_value())


    
    

# pending_tasks = []






# async def import_all_exists_peets():
#     await c_scheduler.start_sc()
#     #     await get_all()
#     #     try:
#     #         await load_accesess()
#     #     except:
#     #         ...
#     await clear_all_fsm_data(storage)



# async def load_accesess():
#     with open("accesses.pkl", "rb") as f:
#         Pitomec.all_accesses = pickle.load(f)
#         f.close()

# def check_current_state(pet):
#     if pet.mood == "whole":
#         pet.time_to_crack > datetime.now()


# async def get_all():
#     pets = await DAO.get_all()
#     for pet in pets:
#         if pet.time_to_unhappy:
#             if pet.time_to_unhappy <= datetime.now():
#                 await unhappy(pet)
#         elif pet.time_to_hatch <= datetime.now():
#                 await already_hatched(pet)
#         elif pet.time_to_crack <= datetime.now():
#                 await already_cracked(pet)
#         else:
#             c_scheduler.crack(pet, "time_to_crack")


# async def already_cracked(pet):
#     pet.mood = "nock"
#     await DAO.upd(pet)
#     image = await Pitomec.get_image(pet)
#     await bot.send_photo(
#             chat_id=pet.owner1,
#             photo=image,
#             caption=f"ой.....\nкажется {pet.name} начал шевелиться\n{await Pitomec.calculate_time(pet)}"
#         )
#     await bot.send_photo(
#             chat_id=pet.owner2,
#             photo=image,
#             caption=f"ой.....\nкажется {pet.name} начал шевелиться\n{await Pitomec.calculate_time(pet)}"
#         )
#     c_scheduler.hatch(pet, "time_to_hatch")

# async def already_hatched(pet):
#     pet.essense = "hipopotam"
#     pet.mood = "happy"
#     await DAO.upd(pet)
#     image = await Pitomec.get_image(pet)
#     await bot.send_photo(
#             chat_id=pet.owner1,
#             photo=image,
#             caption=f"{pet.name} вылупился"
#         )
#     await bot.send_photo(
#             chat_id=pet.owner2,
#             photo=image,
#             caption=f"{pet.name} вылупился"
#         )

# async def unhappy(pet):
#     if "unhappy" not in pet.mood:
#         pet.mood+=",unhappy"
#     await DAO.upd(pet)
#     image = await Pitomec.get_image(pet)
#     await bot.send_photo(
#             chat_id=pet.owner1,
#             photo=image,
#             caption=f"{pet.name} грустит.....\n поиграй с ним",
#             reply_markup=to_be_happy_btn
#         )
#     # image.seek(0)
#     await bot.send_photo(
#             chat_id=pet.owner2,
#             photo=image,
#             caption=f"{pet.name} грустит.....\n поиграй с ним",
#             reply_markup=to_be_happy_btn
#         )



