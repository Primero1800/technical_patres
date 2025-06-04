from src.tools.errors_base import ErrorsBase


class Errors(ErrorsBase):

    CLASS = "Auth"
    _CLASS = "auth"

    @classmethod
    def HANDLER_MESSAGE(cls):
        return f"Handled by {cls.CLASS} exception handler"

    @staticmethod
    def user_not_exists_mailed(email: str):
        return f"Email {email!r} isn't bound to any user"

    @staticmethod
    def user_not_verified_emailed(email: str):
        return f"User {email!r} is not verified"

    USER_ALREADY_EXISTS = "User already exists"

    @staticmethod
    def user_already_exists_emailed(email: str):
        return f"User {email!r} already exists"

    @staticmethod
    def invalid_password_reasoned(reason: str):
        return f"Invalid password: {reason}"
