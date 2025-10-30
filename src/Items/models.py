from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.users import Base


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    orders = relationship('OrderItems', backref='items')