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
