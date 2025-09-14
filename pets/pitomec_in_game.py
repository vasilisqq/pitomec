import random
from text import choose_food

async def create_field_func(user_id, m1, m2):
    return {'hatch':random.randint(0,8),
            'opened' : [],
            'moove':user_id,
            'm1':m1,
            'm2':m2}

async def choose_ingridients(pet):
    foods = await choose_food()
    return {
        pet.owner1: [foods[0], False],
        pet.owner2: [foods[1], False]
    }
