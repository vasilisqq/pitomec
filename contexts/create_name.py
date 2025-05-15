from aiogram import Router
from pitomec import Pitomec
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Pitomec.name)
async def set_pit_name(message: Message, state: FSMContext):
    pet = Pitomec.all_accesses[str(message.from_user.id)]
    pet.name = message.text
    await message.answer("ты создал питомца")
    await pet.add_owner(message.from_user.id)
    state.clear
    await message.answer_photo(
        photo=FSInputFile("photos/eggs/1.png"),
        caption=pet.name
    )
    await message.bot.send_photo(
        chat_id=pet.owner1,
        photo=FSInputFile("photos/eggs/1.png"),
        caption=pet.name
    )
