from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.models.users import Base


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    total_price = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    items = relationship('OrderItems', backref='orders')

