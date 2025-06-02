from aiogram import Router
from pitomec import Pitomec
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from loader import c_scheduler
from aiogram import Bot

router = Router()

@router.message(Pitomec.name)
async def set_pit_name(message: Message, state: FSMContext):
    pet = Pitomec.all_accesses[str(message.from_user.id)]
    pet.name = message.text
    await message.bot.delete_messages(
        chat_id=message.from_user.id,
        message_ids=[
            message.message_id,
            message.message_id-1,
            message.message_id-2
        ]
    )
    await message.bot.delete_messages(
        chat_id=pet.owner1,
        message_ids=pet.last_message_ids
    )
    await pet.add_owner(message.from_user.id)
    await state.clear()
    image = f"photos/{await pet.get_image()}.png"
    await message.answer_photo(
        photo=FSInputFile(image),
        caption=f"теперь нужно подождать, когда {pet.name} вылупится"
    )
    await message.bot.send_photo(
        chat_id=pet.owner1,
        photo=FSInputFile(image),
        caption=f"теперь нужно подождать, когда {pet.name} вылупится"
    )
    c_scheduler.crack(pet, "time_to_crack")

