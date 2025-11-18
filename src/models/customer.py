import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from src.models import Base


class Customer(Base):
    __tablename__ = 'customer'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())

    orders: Mapped[List['Orders']] = relationship(
        'Order',
        back_populates='customer'
    )