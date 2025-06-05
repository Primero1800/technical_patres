from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from src.core.config import DBConfigurer
from src.core.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.NAMING_CONVENTION
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return DBConfigurer.utils.camel2snake(cls.__name__)
        # return '_'.join([settings.db.DB_TABLE_PREFIX, cls.__name__.lower()])

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            result[column.name] = getattr(self, column.name)
        return result

    def __str__(self):
        text = f"id={self.id}" if hasattr(self, "id") else ""
        return f"{self.__class__.__name__}({text})"

    def __repr__(self):
        return str(self)
