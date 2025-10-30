import uuid
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey
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
    id = Column(Integer, primary_key=True)
    title = Column(String)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))