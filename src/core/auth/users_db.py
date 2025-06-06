from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer
from src.core.models import User


async def get_user_db(
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    yield SQLAlchemyUserDatabase(session, User)
