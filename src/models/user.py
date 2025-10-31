import uuid
from typing import List

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())

