from aiogram import Router
from contexts.create_name import router as router_create_name

main_router_contexts = Router()
main_router_contexts.include_routers(
    router_create_name
)
