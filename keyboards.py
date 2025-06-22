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