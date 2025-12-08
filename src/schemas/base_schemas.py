import uuid
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    title: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    pass

    class Config:
        from_attributes = True



class UserProfileBase(BaseModel):
    title: str
    bio: str
    user_id: uuid.UUID


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    pass

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    title: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrdersBase(BaseModel):
    total_price: int


class OrdersCreate(OrdersBase):
    customer_id: uuid.UUID


class OrdersUpdate(OrdersBase):
    pass


class Orders(OrdersBase):
    id: uuid.UUID
    customer_id: uuid.UUID

    class Config:
        from_attributes = True


class ItemsBase(BaseModel):
    title: str
    price: int


class ItemsCreate(ItemsBase):
    pass


class ItemsUpdate(ItemsBase):
    pass


class Items(ItemsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrdersBaseI(BaseModel):
    total_price: int


class OrdersCreateI(OrdersBaseI):
    customer_id: uuid.UUID
    items: List[ItemsCreate] = []  # Для создания заказа с товарами


class OrdersUpdateI(OrdersBaseI):
    items: List[ItemsCreate] = []  # Для обновления товаров в заказе


class OrdersI(OrdersBaseI):
    id: uuid.UUID
    customer_id: uuid.UUID

    class Config:
        from_attributes = True


class OrdersItemsBase(BaseModel):
    order_id: uuid.UUID
    item_id: uuid.UUID


class OrdersItemsCreate(OrdersItemsBase):
    pass


class OrdersItems(OrdersItemsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


