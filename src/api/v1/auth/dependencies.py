from fastapi import Depends

from src.api.v1.auth.backend import fastapi_users
from src.api.v1.auth.user_manager import UserManager
from src.core.auth.users_db import get_user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


current_user = fastapi_users.current_user(
    active=True,
    verified=True,
)
