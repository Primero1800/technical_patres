from src.tools.errors_base import ErrorsBase


class Errors(ErrorsBase):
    CLASS = "BorrowedBook"
    _CLASS = "borrowed_book"

    @classmethod
    def HANDLER_MESSAGE(cls):
        return f"Handled by Library exception handler"

    @staticmethod
    def NOT_ENOUGH_QUANTITY():
        return "Not enough quantity"

    @classmethod
    def INVALID_OPERATION(cls):
        return f"Invalid operation. The item has already been returned"

    @staticmethod
    def LIMIT_REACHED():
        return "Limit by items is reached"

    @staticmethod
    def SIMILAR_EXISTS():
        return "Impossible to borrow similar item"
