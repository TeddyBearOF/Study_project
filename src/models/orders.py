import uuid
from typing import List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import Base



class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    total_price: Mapped[int] = mapped_column(Integer)

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('customer.id'),
        nullable=False,
        index=True
    )

    user: Mapped['Customer'] = relationship('Customer', back_populates='orders')

    order_items: Mapped[List['OrdersItems']] = relationship(
        'OrdersItems',
        back_populates='orders',
        cascade='all, delete-orphan'
    )