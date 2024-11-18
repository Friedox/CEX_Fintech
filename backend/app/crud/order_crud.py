from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models.order_model import Order
from typing import List, Optional


async def create_order(db: AsyncSession, order_data: dict) -> Order:
    new_order = Order(**order_data)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def get_order_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalars().first()


async def get_orders_by_token_pair(db: AsyncSession, token_pair: str, order_type: str) -> List[Order]:
    result = await db.execute(
        select(Order)
        .where(Order.token_pair == token_pair, Order.order_type == order_type, Order.is_filled == False)
        .order_by(Order.price.desc() if order_type == "buy" else Order.price.asc())
    )
    return result.scalars().all()


async def mark_order_as_filled(db: AsyncSession, order_id: int):
    order = await get_order_by_id(db, order_id)
    if order:
        order.is_filled = True
        await db.commit()


async def delete_order(db: AsyncSession, order_id: int):
    order = await get_order_by_id(db, order_id)
    if order:
        await db.delete(order)
        await db.commit()
