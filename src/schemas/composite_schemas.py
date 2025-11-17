from typing import Optional, List

from pydantic import BaseModel

from src.schemas.base_schemas import (User, UserProfile, UserCreate, UserProfileCreate, UserUpdate, UserProfileUpdate,
                                      OrdersItems, Orders, Items, Customer, OrdersCreate, ItemsCreate, OrdersUpdate, CustomerCreate, CustomerUpdate, ItemsUpdate)


class UserWithProfile(User):
    user_profile: Optional[UserProfile] = None


class UserProfileWithUser(UserProfile):
    user: Optional[User] = None


class UserCreateWithProfile(BaseModel):
    user: UserCreate
    user_profile: UserProfileCreate


class UserUpdateWithProfile(BaseModel):
    user: UserUpdate
    user_profile: UserProfileUpdate


class OrdersItemsWithDetails(OrdersItems):
    order: Optional['Orders'] = None
    item: Optional['Items'] = None


class ItemsWithOrders(Items):
    order_items: List[OrdersItemsWithDetails] = []


class OrdersWithItemsAndCustomer(Orders):
    customer: Optional['Customer'] = None
    order_items: List[OrdersItemsWithDetails] = []
    items: List[Items] = []


class OrdersCreateWithItems(BaseModel):
    order: OrdersCreate
    items: List[ItemsCreate] = []


class OrdersUpdateWithItems(BaseModel):
    order: OrdersUpdate
    items: List[ItemsCreate] = []


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