from aiogram import Router
from pitomec import Pitomec
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from loader import c_scheduler
from aiogram import Bot
from pitomec import Pitomec

router = Router()

@router.message(Pitomec.name)
async def set_pit_name(message: Message, state: FSMContext, pet):
    print(await state.get_state())
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
    image = await Pitomec.get_image(pet)
    await message.answer_photo(
        photo=BufferedInputFile(image.read(), "f.JPEG"),
        caption=f"теперь нужно подождать, когда {pet.name} вылупится"
    )
    image.seek(0)
    await message.bot.send_photo(
        chat_id=pet.owner1,
        photo=BufferedInputFile(image.read(), "f.JPEG"),
        caption=f"теперь нужно подождать, когда {pet.name} вылупится"
    )
    c_scheduler.crack(pet, "time_to_crack")

