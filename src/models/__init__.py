from .base import Base

# Импортируем в правильном порядке - сначала независимые таблицы
from .user import User
from .items import Items
from .orders import Orders
from .orders_items import OrdersItems
from .user_profile import UserProfile
from src.models.customer import Customer
