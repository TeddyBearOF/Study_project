from sqlalchemy import Column, Integer, String, ForeignKey

from src.models.users import Base


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))