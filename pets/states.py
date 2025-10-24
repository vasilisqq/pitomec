from aiogram.fsm.state import State, StatesGroup

class StatesP(StatesGroup):
    name = State()
    game = State()
    feed = State()
    waiting_for_partner = State()


