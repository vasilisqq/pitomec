import random


class PetGame:
    @classmethod
    async def create_field(cls):
        return {'hatch':random.randint(1,10),
                'opened' : []}
