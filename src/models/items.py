import uuid
from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import Base


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)

    order_items: Mapped[List['OrdersItems']] = relationship(
        'OrdersItems',
        back_populates='items'
    )