from config import settings
import random


async def create_ref(user_id:int|str) -> str:
    link = f"{settings.BOT_LINK.get_secret_value()}?start={user_id}"
    return f'<a href="{link}">Создать долбоебика</a>'

async def choose_food() -> str:
    food_vars = "🍇🍈🍉🍊🍋‍🟩🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🧅🧄🥦🥬🥒🫑🌶🌽🥕🥔🍆🥑🥥🫒🍅🥝🥜🍗🫘🌰🫚🫛🍄‍🟫"
    return random.choices(
        food_vars, k=2
    )

async def make_current_word(days:int) -> str:
    last_digit = days % 10
    last_two_digits = days % 100
    if 11 <= last_two_digits <= 14:
        return f"{days} дней"
    if last_digit == 1:
        return f"{days} день"
    if 2 <= last_digit <= 4:
        return f"{days} дня"
    return f"{days} дней"