import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class OrdersItems(Base):
    __tablename__ = 'orders_items'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('orders.id'),
        nullable=False,
        index=True
    )

    order: Mapped['Orders'] = relationship('Orders', back_populates='orders_items')

    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('items.id'),
        nullable=False,
        index=True
    )

    item: Mapped['Items'] = relationship('Items', back_populates='orders_items')