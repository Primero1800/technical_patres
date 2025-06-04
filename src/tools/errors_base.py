class ErrorsBase:
    CLASS = "Object"
    _CLASS = "object"

    @classmethod
    def HANDLER_MESSAGE(cls):
        return f"Handled by {cls.CLASS}s exception handler"

    @classmethod
    def DATABASE_ERROR(cls):
        return "Error occurred while changing database data"

    @classmethod
    def NOT_EXISTS(cls):
        return f"{cls.CLASS} doesn't exist"

    @classmethod
    def NOT_EXISTS_ID(cls, id: int):
        return "%s with id=%s not exists" % (cls.CLASS, id)

    @classmethod
    def ALREADY_EXISTS(cls):
        return f"{cls.CLASS} already exists"

    @classmethod
    def NO_RIGHTS(cls):
        return "You are not authorized for this operation"

    @staticmethod
    def INVALID_PASSWORD():
        return "Invalid password"

    @staticmethod
    def INVALID_TOKEN():
        return "Invalid token"

    @staticmethod
    def BAD_CREDENTIALS_OR_NOT_ACTIVE():
        return "Bad credentials or user is not active"
