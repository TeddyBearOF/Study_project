# schemas.py
import uuid
from typing import List, Optional
from pydantic import BaseModel


# Customer Schemas
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


# Orders Schemas
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


# Composite Schemas
class OrdersWithCustomer(Orders):
    customer: Optional[Customer] = None


class CustomerWithOrders(Customer):
    orders: List[Orders] = []


class CustomerCreateWithOrders(BaseModel):
    customer: CustomerCreate
    orders: List[OrdersCreate] = []


class CustomerUpdateWithOrders(BaseModel):
    customer: CustomerUpdate
    orders: List[OrdersCreate] = []