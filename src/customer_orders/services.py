import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.customer import Customer
from src.models.orders import Orders
from src.schemas.base_schemas import CustomerCreate, CustomerUpdate, OrdersCreate, OrdersUpdate


class CustomerService:

    @staticmethod
    async def create_customer_with_orders(db: Session, customer_data, orders_data: List[OrdersCreate]):
        # Create Customer
        db_customer = Customer(**customer_data.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        # Create Orders
        orders_list = []
        for order_data in orders_data:
            order_dict = order_data.dict()
            order_dict['customer_id'] = db_customer.id
            db_order = Orders(**order_dict)
            db.add(db_order)
            orders_list.append(db_order)

        db.commit()

        # Refresh all orders to get their IDs
        for order in orders_list:
            db.refresh(order)

        result = db_customer.__dict__
        result['orders'] = orders_list
        return result

    @staticmethod
    async def get_customer_with_orders(db: Session, customer_id: uuid.UUID):
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer_data = customer.__dict__
        customer_data['orders'] = customer.orders
        return customer_data

    @staticmethod
    async def update_customer_with_orders(db: Session, customer_id: uuid.UUID, customer_update_data,
                                          orders_data: List[OrdersCreate]):
        # Update Customer
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        for field, value in customer_update_data.dict().items():
            setattr(db_customer, field, value)

        # Delete existing orders and create new ones
        db.query(Orders).filter(Orders.customer_id == customer_id).delete()

        # Create new orders
        new_orders = []
        for order_data in orders_data:
            order_dict = order_data.dict()
            order_dict['customer_id'] = customer_id
            db_order = Orders(**order_dict)
            db.add(db_order)
            new_orders.append(db_order)

        db.commit()
        db.refresh(db_customer)

        # Refresh all new orders
        for order in new_orders:
            db.refresh(order)

        result = db_customer.__dict__
        result['orders'] = new_orders
        return result

    @staticmethod
    async def delete_customer_with_orders(db: Session, customer_id: uuid.UUID):
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Delete associated orders first
        db.query(Orders).filter(Orders.customer_id == customer_id).delete()
        db.delete(db_customer)
        db.commit()

        return {"message": "Customer and associated orders deleted successfully"}


class OrdersService:

    @staticmethod
    async def create_order(db: Session, order_data: OrdersCreate):
        # Check if customer exists
        customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        db_order = Orders(**order_data.dict())
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        result = db_order.__dict__
        result['customer'] = customer
        return result

    @staticmethod
    async def get_order_with_customer(db: Session, order_id: uuid.UUID):
        order = db.query(Orders).filter(Orders.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order_data = order.__dict__
        order_data['customer'] = order.customer
        return order_data

    @staticmethod
    async def update_order(db: Session, order_id: uuid.UUID, order_update_data: OrdersUpdate):
        db_order = db.query(Orders).filter(Orders.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        for field, value in order_update_data.dict().items():
            setattr(db_order, field, value)

        db.commit()
        db.refresh(db_order)

        result = db_order.__dict__
        result['customer'] = db_order.customer
        return result

    @staticmethod
    async def delete_order(db: Session, order_id: uuid.UUID):
        db_order = db.query(Orders).filter(Orders.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        db.delete(db_order)
        db.commit()

        return {"message": "Order deleted successfully"}