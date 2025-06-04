import logging
from typing import Optional, Union, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, InvalidPasswordException
from sqlalchemy import Integer

from src.core.settings import settings

if TYPE_CHECKING:
    from src.core.models import User
    from fastapi import Request, Response

logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager["User", Integer]):

    # reset_password_token_secret = settings.auth.AUTH_RESET_PASSWORD_TOKEN_SECRET
    # reset_password_token_lifetime_seconds = settings.auth.AUTH_RESET_PASSWORD_TOKEN_LIFETIME_SECONDS
    # verification_token_secret = settings.auth.AUTH_VERIFICATION_TOKEN_SECRET
    # verification_token_lifetime_seconds = settings.auth.AUTH_VERIFICATION_TOKEN_LIFETIME_SECONDS

    async def on_after_register(
            self,
            user: "User",
            request: Optional["Request"] = None,
    ):
        logger.warning("%r has registered." % (user, ))

    async def on_after_login(
            self,
            user: "User",
            request: Optional["Request"] = None,
            response: Optional["Response"] = None,
    ):
        logger.info("%r logged in." % (user,))

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        if len(password) < settings.users.USERS_PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                reason=f"Password should be at least "
                       f"{settings.users.USERS_PASSWORD_MIN_LENGTH} characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

