from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from src.db import get_session
from src.orders_items.services import OrdersItemsService, ItemsService
from src.orders_items.schemas import (
    OrdersWithItemsAndCustomer,
    OrdersCreateWithItems,
    OrdersUpdateWithItems,
    ItemsWithOrders,
    ItemsCreate,
    ItemsUpdate,
    Items
)

router = APIRouter(prefix="/orders-items", tags=["orders-items"])

# ========== ORDERS WITH ITEMS CRUD OPERATIONS ==========

# CREATE Order with Items
@router.post("/orders/", response_model=OrdersWithItemsAndCustomer)
async def create_order_with_items(
    order_data: OrdersCreateWithItems,
    session: Session = Depends(get_session)
):
    return await OrdersItemsService.create_order_with_items(
        session, 
        order_data.order, 
        order_data.items
    )

# READ Order by ID with Items
@router.get("/orders/{order_id}", response_model=OrdersWithItemsAndCustomer)
async def read_order_with_items(
    order_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await OrdersItemsService.get_order_with_items(session, order_id)

# UPDATE Order and Items
@router.put("/orders/{order_id}", response_model=OrdersWithItemsAndCustomer)
async def update_order_with_items(
    order_id: uuid.UUID,
    order_data: OrdersUpdateWithItems,
    session: Session = Depends(get_session)
):
    return await OrdersItemsService.update_order_with_items(
        session, 
        order_id, 
        order_data.order, 
        order_data.items
    )

# DELETE Order and associated Items relations
@router.delete("/orders/{order_id}")
async def delete_order_with_items(
    order_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await OrdersItemsService.delete_order_with_items(session, order_id)

# ========== ITEMS CRUD OPERATIONS ==========

# CREATE Item
@router.post("/items/", response_model=Items)
async def create_item(
    item_data: ItemsCreate,
    session: Session = Depends(get_session)
):
    return await ItemsService.create_item(session, item_data)

# READ Item by ID with Orders
@router.get("/items/{item_id}", response_model=ItemsWithOrders)
async def read_item_with_orders(
    item_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await ItemsService.get_item_with_orders(session, item_id)

# UPDATE Item
@router.put("/items/{item_id}", response_model=Items)
async def update_item(
    item_id: uuid.UUID,
    item_data: ItemsUpdate,
    session: Session = Depends(get_session)
):
    return await ItemsService.update_item(session, item_id, item_data)

# DELETE Item
@router.delete("/items/{item_id}")
async def delete_item(
    item_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await ItemsService.delete_item(session, item_id)

# GET All Items
@router.get("/items/", response_model=List[Items])
async def get_all_items(session: Session = Depends(get_session)):
    return await ItemsService.get_all_items(session)