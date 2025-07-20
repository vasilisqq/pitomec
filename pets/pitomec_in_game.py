import random


async def create_field_func(user_id, m1, m2):
    return {'hatch':random.randint(0,8),
            'opened' : [],
            'moove':user_id,
            'm1':m1,
            'm2':m2}
