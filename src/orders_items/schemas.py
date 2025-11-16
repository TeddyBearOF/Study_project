# schemas.py
import uuid
from typing import List, Optional
from pydantic import BaseModel


# Items Schemas
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


# OrdersItems Schemas
class OrdersItemsBase(BaseModel):
    order_id: uuid.UUID
    item_id: uuid.UUID


class OrdersItemsCreate(OrdersItemsBase):
    pass


class OrdersItems(OrdersItemsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# Orders Schemas (расширяем существующие)
class OrdersBase(BaseModel):
    total_price: int


class OrdersCreate(OrdersBase):
    customer_id: uuid.UUID
    items: List[ItemsCreate] = []  # Для создания заказа с товарами


class OrdersUpdate(OrdersBase):
    items: List[ItemsCreate] = []  # Для обновления товаров в заказе


class Orders(OrdersBase):
    id: uuid.UUID
    customer_id: uuid.UUID

    class Config:
        from_attributes = True


# Composite Schemas with relationships
class OrdersItemsWithDetails(OrdersItems):
    order: Optional['Orders'] = None
    item: Optional['Items'] = None


class ItemsWithOrders(Items):
    order_items: List[OrdersItemsWithDetails] = []


class OrdersWithItemsAndCustomer(Orders):
    customer: Optional['Customer'] = None
    order_items: List[OrdersItemsWithDetails] = []
    items: List[Items] = []  # Упрощенный доступ к товарам


class OrdersCreateWithItems(BaseModel):
    order: OrdersCreate
    items: List[ItemsCreate] = []


class OrdersUpdateWithItems(BaseModel):
    order: OrdersUpdate
    items: List[ItemsCreate] = []