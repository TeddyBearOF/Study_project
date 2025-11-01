import uuid
from typing import Optional

import sa
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
import sqlalchemy as sa

from src.models.base import Base


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(sa.String())
    bio: Mapped[Optional[str]] = mapped_column(String)
    user_id: Mapped[uuid.UUID] = mapped_column(
                                                ForeignKey('user.id'),
                                                unique=True,
                                                index=True
    )
    user: Mapped['User'] = relationship('User', back_populates='user_profile')

