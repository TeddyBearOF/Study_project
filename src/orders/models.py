import uuid

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.users import Base


class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    total_price: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'))
    items = relationship('OrderItems', backref='order')