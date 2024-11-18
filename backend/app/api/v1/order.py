from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.order_crud import create_order, get_orders_by_token_pair, get_order_by_id
from models.db_helper import database_helper
from schemas.order_scheme import OrderCreateScheme, OrderResponse

router = APIRouter(tags=["Orders"])


@router.post("/", response_model=OrderResponse)
async def create_order_api(order: OrderCreateScheme, db: AsyncSession = Depends(database_helper.session_getter)):
    return await create_order(db, order.dict())


@router.get("/{id}", response_model=OrderResponse)
async def get_order(id: int, db: AsyncSession = Depends(database_helper.session_getter)):
    order = await get_order_by_id(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
