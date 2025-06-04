from src.tools.errors_base import ErrorsBase


class Errors(ErrorsBase):
    CLASS = "Library"
    _CLASS = "library"

    @staticmethod
    def NOT_ENOUGH_QUANTITY():
        return "Not enough quantity"

    @staticmethod
    def LIMIT_REACHED():
        return "Limit by items is reached"

    @staticmethod
    def SIMILAR_EXISTS():
        return "Impossible to borrow similar item"
