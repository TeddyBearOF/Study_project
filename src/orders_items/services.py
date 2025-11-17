import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.orders import Orders
from src.models.items import Items
from src.models.orders_items import OrdersItems
from src.schemas.base_schemas import OrdersCreate, OrdersUpdate, ItemsCreate, ItemsUpdate


class OrdersItemsService:

    @staticmethod
    async def create_order_with_items(db: Session, order_data: OrdersCreate, items_data: List[ItemsCreate]):
        # Создаем заказ
        db_order = Orders(
            total_price=order_data.total_price,
            customer_id=order_data.customer_id
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Создаем товары и связи
        created_items = []
        for item_data in items_data:
            # Создаем или находим товар (по названию и цене)
            db_item = db.query(Items).filter(
                Items.title == item_data.title,
                Items.price == item_data.price
            ).first()

            if not db_item:
                db_item = Items(**item_data.dict())
                db.add(db_item)
                db.commit()
                db.refresh(db_item)

            # Создаем связь в промежуточной таблице
            order_item = OrdersItems(
                order_id=db_order.id,
                item_id=db_item.id
            )
            db.add(order_item)
            created_items.append(db_item)

        db.commit()

        # Формируем результат
        result = db_order.__dict__
        result['items'] = created_items
        result['order_items'] = db_order.order_items
        return result

    @staticmethod
    async def get_order_with_items(db: Session, order_id: uuid.UUID):
        order = db.query(Orders).filter(Orders.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Получаем все товары через связи
        items = []
        for order_item in order.order_items:
            items.append(order_item.item)

        order_data = order.__dict__
        order_data['items'] = items
        order_data['order_items'] = order.order_items
        order_data['customer'] = order.customer
        return order_data

    @staticmethod
    async def update_order_with_items(db: Session, order_id: uuid.UUID, order_update_data: OrdersUpdate,
                                      items_data: List[ItemsCreate]):
        # Обновляем заказ
        db_order = db.query(Orders).filter(Orders.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        db_order.total_price = order_update_data.total_price
        db.add(db_order)

        # Удаляем старые связи
        db.query(OrdersItems).filter(OrdersItems.order_id == order_id).delete()

        # Создаем новые связи с товарами
        updated_items = []
        for item_data in items_data:
            # Создаем или находим товар
            db_item = db.query(Items).filter(
                Items.title == item_data.title,
                Items.price == item_data.price
            ).first()

            if not db_item:
                db_item = Items(**item_data.dict())
                db.add(db_item)
                db.commit()
                db.refresh(db_item)

            # Создаем новую связь
            order_item = OrdersItems(
                order_id=order_id,
                item_id=db_item.id
            )
            db.add(order_item)
            updated_items.append(db_item)

        db.commit()
        db.refresh(db_order)

        # Формируем результат
        result = db_order.__dict__
        result['items'] = updated_items
        result['order_items'] = db_order.order_items
        return result

    @staticmethod
    async def delete_order_with_items(db: Session, order_id: uuid.UUID):
        db_order = db.query(Orders).filter(Orders.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Каскадное удаление связей благодаря cascade='all, delete-orphan'
        db.delete(db_order)
        db.commit()

        return {"message": "Order and associated items deleted successfully"}


class ItemsService:

    @staticmethod
    async def create_item(db: Session, item_data: ItemsCreate):
        # Проверяем, существует ли уже товар с таким названием и ценой
        existing_item = db.query(Items).filter(
            Items.title == item_data.title,
            Items.price == item_data.price
        ).first()

        if existing_item:
            raise HTTPException(status_code=400, detail="Item with this title and price already exists")

        db_item = Items(**item_data.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_item_with_orders(db: Session, item_id: uuid.UUID):
        item = db.query(Items).filter(Items.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        item_data = item.__dict__
        item_data['order_items'] = item.order_items
        return item_data

    @staticmethod
    async def update_item(db: Session, item_id: uuid.UUID, item_update_data: ItemsUpdate):
        db_item = db.query(Items).filter(Items.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

        for field, value in item_update_data.dict().items():
            setattr(db_item, field, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    async def delete_item(db: Session, item_id: uuid.UUID):
        db_item = db.query(Items).filter(Items.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Проверяем, используется ли товар в заказах
        if db_item.order_items:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete item that is used in orders. Remove from orders first."
            )

        db.delete(db_item)
        db.commit()

        return {"message": "Item deleted successfully"}

    @staticmethod
    async def get_all_items(db: Session):
        items = db.query(Items).all()
        return items