import random

def choose_food() -> str:
    food_vars = "🍇🍈🍉🍊🍋‍🟩🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🧅🧄🥦🥬🥒🫑🌶🌽🥕🥔🍆🥑🥥🫒🍅🥝🥜🍗🫘🌰🫚🫛🍄‍🟫"
    #return random.choice(food_vars)
    return random.choices(
        food_vars, k=2
    )

print(choose_food())