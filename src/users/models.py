import datetime
import uuid
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index = True
    )

    username: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False,
        index = True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False,
        index = True
    )

    user_profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, user_profile_id={self.user_profile_id})>"

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key = True,
        default = uuid.uuid4,
        index = True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    bio: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )

    date_of_birth: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile"
    )

