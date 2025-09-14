from aiogram.fsm.state import State, StatesGroup

class StatesP(StatesGroup):
    name = State()
    game = State()
    feed = State()

