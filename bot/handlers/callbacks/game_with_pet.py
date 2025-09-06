from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import timezone
from aiogram.fsm.context import FSMContext
from loader import states_p, set_states, set_data, clear_state
from zoneinfo import ZoneInfo
from pets.pitomec_in_game import create_field_func
from aiogram.types import FSInputFile, InlineKeyboardMarkup
from bot.keyboards.inline import create_field
from loader import c_scheduler
from pets.pitomec import Pitomec

router = Router()
@router.callback_query(F.data == "game")
async def start_game(query: CallbackQuery, pet, state : FSMContext):
    if await state.get_state() == states_p.game:
        await query.answer(
            text="Ты уже играешь с питомцем",
            show_alert=True
        )
        await query.message.delete()
    elif pet.mood.find("unhappy") != -1:
        time = pet.time_to_unhappy.astimezone(ZoneInfo("UTC"))
        time = time.replace(microsecond=0)
        if query.message.date < time:
            await query.answer(
                "Это старое сообщение",
                show_alert=True)
            await query.message.delete()
        else:
            await set_states(states_p.game, pet)
            
            photo=FSInputFile("photos/hided.png")
            kb = create_field()
            m1 = await query.bot.send_photo(
                chat_id=pet.owner1,
                photo=photo,
                caption=f"{pet.name} спрятался за одним из этих деревьев, выбирайте по очереди, пока не найдете своего питомца",
                reply_markup=kb
            )
            m2 = await query.bot.send_photo(
                chat_id=pet.owner2,
                photo=photo,
                caption=f"{pet.name} спрятался за одним из этих деревьев, выбирайте по очереди, пока не найдете своего питомца",
                reply_markup=kb
            )
            await set_data(
                pet, 
                await create_field_func(
                    query.from_user.id,
                    m1.message_id,
                    m2.message_id))
    else:
        await query.answer(f"{pet.name} больше не грустит")
    await query.bot.delete_message(
        chat_id=query.from_user.id,
        message_id=query.message.message_id
    )

@router.callback_query(F.data.in_([str(i) for i in range(9)]))
async def answer_on_moove(query: CallbackQuery, state: FSMContext, pet):
    # print(query.data)
    data = int(query.data)
    st = await state.get_data()
    kb = query.message.reply_markup.inline_keyboard
    if st["moove"] != query.from_user.id:
        await query.answer(
            text="Сейчас не твоя попытка",
            show_alert=True
        )
    elif data == st["hatch"]:
        await query.bot.delete_message(
            chat_id=pet.owner1,
            message_id=st["m1"]
        )
        await query.bot.delete_message(
            chat_id=pet.owner2,
            message_id=st["m2"]
        )
        await query.bot.send_photo(
            chat_id=pet.owner1,
            photo=FSInputFile("photos/hipopotam/happy.png"),
            caption=f"Ура ты поиграл с {pet.name}\n теперь он счастлив"
        )
        await query.bot.send_photo(
            chat_id=pet.owner2,
            photo=FSInputFile("photos/hipopotam/happy.png"),
            caption=f"Ура ты поиграл с {pet.name}\n теперь он счастлив"
        )
        await clear_state(pet)
        await Pitomec.unhappy(pet, "unhappy")
        c_scheduler.unhappy(pet, "time_to_unhappy")
    elif kb[data // 3][data%3].text == "X":
        await query.answer(
            text=f"Это дерево вы уже обыскали и не нашли там {pet.name}",
            show_alert=True
        )
    else:
        kb[data // 3][data%3].text = "X"
        st["opened"].append(data)
        st["moove"] = pet.owner2 if pet.owner1 == query.from_user.id else pet.owner1
        await set_data(pet,
            st
        )
        await query.bot.edit_message_reply_markup(
            chat_id=pet.owner1,
            message_id=st["m1"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
        await query.bot.edit_message_reply_markup(
            chat_id=pet.owner2,
            message_id=st["m2"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
    # await query.message.answer(str(st))
