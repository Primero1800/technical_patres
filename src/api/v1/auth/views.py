import logging

from fastapi import (
    APIRouter,
    status,
    Request,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, models
from fastapi_users.authentication import Strategy
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.backend import (
    auth_backend,
)
from src.api.v1.auth.user_manager import get_user_manager
from src.core.config import DBConfigurer
from .service import AuthService
from .schemas import (
    UserRead,
    UserCreate,
)


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
        "/login",
        name=f"auth:{auth_backend.name}.login",
)
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
    session: AsyncSession = Depends(DBConfigurer.session_getter),
):
    service = AuthService(
        user_manager=user_manager,
        backend=auth_backend,
        session=session,
    )
    return await service.login(
        request=request,
        credentials=credentials,
        strategy=strategy,
    )


@router.post(
        "/register",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
)
async def register(
    request: Request,
    user_create: UserCreate,
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    service: AuthService = AuthService(
        user_manager=user_manager
    )
    return await service.register(
        request=request,
        user_create_schema=user_create,
    )
