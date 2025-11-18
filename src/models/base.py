import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column, relationship
import uuid


metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)

