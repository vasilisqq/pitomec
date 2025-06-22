import random


class PetGame():

    games = {}

    def __init__(self, message1, message2, pet):
        self.message1 = [message1]
        self.message2 = [message2]
        self.hatch = random.randint(1,10)
        self.pet = pet
        self.id = message1.from_user.id
        PetGame.games.update({self.id: self})