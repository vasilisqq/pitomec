from aiogram import Router
from .commands.common_commands import router as router_common_commands
from .callbacks.game_with_pet import router as router_game
from .callbacks.hungry import router as router_hungry
main_router_handler = Router()
main_router_handler.include_routers(
    router_common_commands,
    router_hungry,
    router_game,
    
)
