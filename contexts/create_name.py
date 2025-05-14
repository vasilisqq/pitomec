from aiogram import Router
from pitomec import Pitomec
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Pitomec.name)
async def set_pit_name(message: Message, state: FSMContext):
    pit = Pitomec.all_accesses[str(message.from_user.id)]
    pit.name = message.text
    await message.answer("ты создал питомца")
    await pit.add_owner(message.from_user.id)
    state.clear
    await pit.init_photo("1.png")
    await message.answer_photo(
        photo=FSInputFile("photos/eggs/1.png"),
        caption=pit.name
    )
    await message.bot.send_photo(
        chat_id=pit.owner1,
        photo=FSInputFile("photos/eggs/1.png"),
        caption=pit.name
    )