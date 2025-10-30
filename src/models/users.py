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


class OrdersItems(Base):
    __tablename__ = 'orders_items'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    orders_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('orders.id'))
    items_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('items.id'))