from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButtonRequestChat, SwitchInlineQueryChosenChat, CopyTextButton
from aiogram.types import InlineKeyboardMarkup

to_be_happy_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="поиграть", callback_data="game")
        ]
    ]
)

def create_field():
    find_pet = InlineKeyboardBuilder()
    for i in range(9):
        find_pet.button(text="⏺️", callback_data=f"{i}")
    find_pet.adjust(3,3,3)
    return find_pet.as_markup()

