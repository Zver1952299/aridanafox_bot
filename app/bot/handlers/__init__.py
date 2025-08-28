from aiogram import Router

from . import admin
from . import user


def get_routers() -> list[Router]:
    return [
        admin.admin_router,
        user.user_router
    ]
