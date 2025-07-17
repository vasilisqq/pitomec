import random


class PetGame:
    @classmethod
    async def create_field(cls, user_id):
        return {'hatch':str(random.randint(0,8)),
                'opened' : [],
                'moove':user_id}
