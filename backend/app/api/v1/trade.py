from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import database_helper
from services.trade_service import match_orders
from crud.order_crud import create_order, get_orders_by_token_pair
from crud.trade_crud import get_trades_by_token_pair

router = APIRouter(tags=["Trade"])


@router.post("/orders")
async def create_new_order(order_data: dict, db: AsyncSession = Depends(database_helper.session_getter)):
    order = await create_order(db, order_data)
    await match_orders(db, order.token_pair)
    return {"message": "Order created", "order_id": order.id}


@router.get("/order-book/{token_pair}")
async def get_order_book(token_pair: str, db: AsyncSession = Depends(database_helper.session_getter)):
    buy_orders = await get_orders_by_token_pair(db, token_pair, "buy")
    sell_orders = await get_orders_by_token_pair(db, token_pair, "sell")
    return {
        "buy_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in buy_orders],
        "sell_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in sell_orders],
    }


@router.get("/trade-history/{token_pair}")
async def get_trade_history(token_pair: str, db: AsyncSession = Depends(database_helper.session_getter)):
    trades = await get_trades_by_token_pair(db, token_pair)
    return [{"price": t.price, "quantity": t.quantity, "timestamp": t.timestamp} for t in trades]
