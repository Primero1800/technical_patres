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
        status_code=status.HTTP_200_OK,
        description="Get jwt-token to authenticate",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "Actual access-token to authenticate",
                                "value": {
                                    "access_token": "eyJhbGciOiJSUzI1NiIsInR_any_access_token__5ufSvph_yTiOmZlAjzg",
                                    "token_type": "Bearer",
                                },
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Bad credentials",
                "content": {
                    "application/json": {
                        "example": {
                            "summary": "Provided bad credentials or user is not registered yet",
                            "value": {
                                "message": "Handled by Auth exception handler",
                                "detail": "Bad credentials or user is not active"
                            }
                        }
                    }
                }
            },
            422: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "examples": {
                            "invalid input": {
                                "summary": "Invalid input data",
                                "value": {
                                    "message": "Handled by Application Exception Handler",
                                    "detail": [
                                        {
                                            "loc": ["username", "password"],
                                            "type": "missing"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }
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
        name="register:register",
        status_code=status.HTTP_201_CREATED,
        description="Creating (registration) of new user, no need in verification",
        response_model=UserRead,
        responses={
            201: {
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "New registered user with unique email",
                                "value": {
                                    "id": 1,
                                    "email": "admin@admin.com",
                                    "is_active": True,
                                    "is_verified": False,
                                    "is_superuser": False,
                                },
                            }
                        }
                    }
                }
            },
            400: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "examples": {
                            "invalid input": {
                                "summary": "Invalid input data",
                                "value": {
                                    "message": "Handled by Application Exception Handler",
                                    "detail": [
                                        {
                                            "loc": ["email", "password"],
                                            "type": "missing"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }

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
