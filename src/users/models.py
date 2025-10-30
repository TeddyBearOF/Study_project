import uuid
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.users import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())
    user_profile = relationship('UserProfile', backref='user', uselist=False)
    orders = relationship('Orders', backref='user')


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())
    bio: Mapped[str] = mapped_column(String)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'))