from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мой питомец"),
            KeyboardButton(text="магазин")
        ]
    ]
)