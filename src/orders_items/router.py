from typing import List

from fastapi import APIRouter, Depends, HTTPException
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.orders_items.services import OrdersItemsService, ItemsService
from src.schemas.composite_schemas import (
    OrdersWithItemsAndCustomer,
    OrdersCreateWithItems,
    OrdersUpdateWithItems,
    ItemsWithOrders,
    ItemsCreate,
    ItemsUpdate,
    Items
)

router = APIRouter(prefix="/orders-items", tags=["orders-items"])

@router.post("/orders/", response_model=OrdersWithItemsAndCustomer, status_code=201)
async def create_order_with_items(
    order_data: OrdersCreateWithItems,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersItemsService.create_order_with_items(
        session, 
        order_data.order, 
        order_data.items
    )

@router.get("/orders/{order_id}", response_model=OrdersWithItemsAndCustomer, status_code=200)
async def read_order_with_items(
    order_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersItemsService.get_order_with_items(session, order_id)

@router.put("/orders/{order_id}", response_model=OrdersWithItemsAndCustomer, status_code=204)
async def update_order_with_items(
    order_id: uuid.UUID,
    order_data: OrdersUpdateWithItems,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersItemsService.update_order_with_items(
        session, 
        order_id, 
        order_data.order, 
        order_data.items
    )

@router.delete("/orders/{order_id}", status_code=204)
async def delete_order_with_items(
    order_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersItemsService.delete_order_with_items(session, order_id)

@router.post("/items/", response_model=Items, status_code=201)
async def create_item(
    item_data: ItemsCreate,
    session: AsyncSession = Depends(get_session)
):
    return await ItemsService.create_item(session, item_data)

@router.get("/items/{item_id}", response_model=ItemsWithOrders, status_code=200)
async def read_item_with_orders(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await ItemsService.get_item_with_orders(session, item_id)

@router.put("/items/{item_id}", response_model=Items, status_code=200)
async def update_item(
    item_id: uuid.UUID,
    item_data: ItemsUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await ItemsService.update_item(session, item_id, item_data)

@router.delete("/items/{item_id}", status_code=204)
async def delete_item(
    item_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await ItemsService.delete_item(session, item_id)

@router.get("/items/", response_model=List[Items], status_code=200)
async def get_all_items(session: Session = Depends(get_session)):
    return await ItemsService.get_all_items(session)