from aiogram import Dispatcher
from aiogram.fsm.state import State
from aiogram.fsm.strategy import FSMStrategy

class DispatcherExpanded(Dispatcher):
    def __init__(self, *, storage = None, fsm_strategy = FSMStrategy.USER_IN_CHAT, events_isolation = None, disable_fsm = False, name = None, **kwargs):
        super().__init__(storage=storage, fsm_strategy=fsm_strategy, events_isolation=events_isolation, disable_fsm=disable_fsm, name=name, **kwargs)


    async def set_states(self, state: State, pet, bot):
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner1, user_id=pet.owner1)
        await context.set_state(state=state)
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner2, user_id=pet.owner2)
        await context.set_state(state=state)


    async def set_data(self, pet, data, bot):
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner1, user_id=pet.owner1)
        await context.update_data(data)
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner2, user_id=pet.owner2)
        await context.update_data(data)


    async def clear_state(self,pet, bot):
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner1, user_id=pet.owner1)
        await context.clear()
        context = self.dp.fsm.get_context(bot=bot, chat_id=pet.owner2, user_id=pet.owner2)
        await context.clear()