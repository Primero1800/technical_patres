from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
)


from src.core.models import Base
from src.core.models.mixins import IDIntPkMixin


class User(Base, IDIntPkMixin, SQLAlchemyBaseUserTable[int]):
    pass

    def __str__(self):
        return (f"{self.__class__.__name__}("
                f"id={self.id}, "
                f"email={self.email})")

    def __repr__(self):
        return str(self)
