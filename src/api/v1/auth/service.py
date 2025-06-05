import logging
from typing import Any

from fastapi.responses import ORJSONResponse
from fastapi_users import BaseUserManager, models, exceptions
from fastapi import Request, status
from fastapi_users.authentication import Strategy, AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import Errors


class AuthService:
    def __init__(
        self,
        user_manager: BaseUserManager[models.UP, models.ID] | None = None,
        backend: AuthenticationBackend[models.UP, models.ID] | None = None,
        session: AsyncSession | None = None,
    ):
        self.user_manager = user_manager
        self.backend = backend
        self.logger = logging.getLogger(__name__)
        self.session = session

    async def login(
            self,
            request: Request,
            credentials: Any,
            strategy: Strategy[models.UP, models.ID],
            requires_verification: bool = False
    ):
        user = await self.user_manager.authenticate(credentials)
        if user is None or not user.is_active:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.BAD_CREDENTIALS_OR_NOT_ACTIVE(),
                }
            )
        if requires_verification and not user.is_verified:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.user_not_verified_emailed(user.email),
                }
            )
        response = await self.backend.login(strategy, user)
        await self.user_manager.on_after_login(user, request, response)
        return response

    async def register(
            self,
            request: Request,
            user_create_schema: Any
    ):
        try:
            created_user = await self.user_manager.create(
                user_create_schema, safe=True, request=request
            )
        except exceptions.UserAlreadyExists:
            self.logger.warning("User %r already exists" % user_create_schema.email)
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.user_already_exists_emailed(user_create_schema.email),
                }
            )
        except exceptions.InvalidPasswordException as e:
            self.logger.warning("Invalid password while registration")
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.invalid_password_reasoned(e.reason),
                }
            )
        return created_user
