from aiogram import Router
from pets.pitomec import Pitomec
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from loader import c_scheduler, states_p
from aiogram import Bot
from pets.pitomec import Pitomec


router = Router()

@router.message(states_p.name)
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
    pet = await pet.add_owner(message.from_user.id)
    await state.clear()
    image = await Pitomec.get_image(pet)
    await message.answer_photo(
        photo=image,
        caption=f"теперь нужно подождать, когда {pet.name} вылупится.\n Чтобы отслеживать состояние своего питомца, используй команду /me"
    )
    await message.bot.send_photo(
        chat_id=pet.owner1,
        photo=image,
        caption=f"теперь нужно подождать, когда {pet.name} вылупится.\n Чтобы отслеживать состояние своего питомца, используй команду /me"
    )
    c_scheduler.crack(pet, "time_to_crack")

