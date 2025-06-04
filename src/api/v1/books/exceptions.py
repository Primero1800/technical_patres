from src.tools.errors_base import ErrorsBase


class Errors(ErrorsBase):
    CLASS = "Book"
    _CLASS = "book"

    @classmethod
    def not_exists_id(cls, id: int):
        return "%s with id=%s not exists" % (cls.CLASS, id)
