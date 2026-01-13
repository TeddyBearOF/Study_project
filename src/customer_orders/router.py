from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.db import get_session
from src.customer_orders.services import CustomerService, OrdersService
from src.schemas.composite_schemas import (
    CustomerWithOrders,
    CustomerCreateWithOrders,
    CustomerUpdateWithOrders,
    OrdersWithCustomer,
    OrdersCreate,
    OrdersUpdate
)

router = APIRouter(prefix="api/v1/customers", tags=["customers"])

@router.post("/", response_model=CustomerWithOrders, status_code=201)
async def create_customer_with_orders(
    customer_data: CustomerCreateWithOrders,
    session: AsyncSession = Depends(get_session)
):
    return await CustomerService.create_customer_with_orders(
        session,
        customer_data.customer,
        customer_data.orders
    )

@router.get("/{customer_id}", response_model=CustomerWithOrders, status_code=200)
async def read_customer(
    customer_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await CustomerService.get_customer_with_orders(session, customer_id)

@router.put("/{customer_id}", response_model=CustomerWithOrders, status_code=200)
async def update_customer_with_orders(
    customer_id: uuid.UUID,
    customer_data: CustomerUpdateWithOrders,
    session: AsyncSession = Depends(get_session)
):
    return await CustomerService.update_customer_with_orders(
        session,
        customer_id,
        customer_data.customer,
        customer_data.orders
    )

@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await CustomerService.delete_customer_with_orders(session, customer_id)

@router.post("/orders/", response_model=OrdersWithCustomer, status_code=201)
async def create_order(
    order_data: OrdersCreate,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersService.create_order(session, order_data)

@router.get("/orders/{order_id}", response_model=OrdersWithCustomer, status_code=200)
async def read_order(
    order_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersService.get_order_with_customer(session, order_id)

@router.put("/orders/{order_id}", response_model=OrdersWithCustomer, status_code=200)
async def update_order(
    order_id: uuid.UUID,
    order_data: OrdersUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersService.update_order(session, order_id, order_data)

@router.delete("/orders/{order_id}", status_code=204)
async def delete_order(
    order_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await OrdersService.delete_order(session, order_id)