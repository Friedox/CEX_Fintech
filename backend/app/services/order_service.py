from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from crud.order_crud import create_order, get_open_orders
from crud.trade_history_crud import log_trade
from crud.token_crud import get_token_by_ticker
from crud.user_wallet_crud import get_user_wallet_by_token
from decimal import Decimal


async def create_new_order(data: dict, db: AsyncSession):
    order = await create_order(data, db)
    await match_orders(order.pair, db)
    return order


async def validate_trade_pair(pair: str, db: AsyncSession):
    base_token, quote_token = pair.split("/")
    base = await get_token_by_ticker(base_token, db)
    quote = await get_token_by_ticker(quote_token, db)
    if not base or not quote:
        raise ValueError(f"Invalid trading pair: {pair}")


async def validate_user_balance(user_id: int, token_id: int, amount: Decimal, db: AsyncSession):
    wallet = await get_user_wallet_by_token(user_id, token_id, db)
    if not wallet or wallet.balance < amount:
        raise ValueError(f"Insufficient balance for user {user_id}")


async def match_orders(pair: str, db: AsyncSession):
    buy_orders = await get_open_orders(pair, "buy", db)
    sell_orders = await get_open_orders(pair, "sell", db)

    buy_orders.sort(key=lambda x: (-x.price, x.created_at))
    sell_orders.sort(key=lambda x: (x.price, x.created_at))

    for buy_order in buy_orders:
        for sell_order in sell_orders:
            if buy_order.price >= sell_order.price:
                matched_amount = min(buy_order.remaining_amount, sell_order.remaining_amount)

                await log_trade(
                    {
                        "buyer_id": buy_order.user_id,
                        "seller_id": sell_order.user_id,
                        "token_id": None,
                        "pair": pair,
                        "price": sell_order.price,
                        "amount": matched_amount,
                    },
                    db,
                )


                buy_order.remaining_amount -= matched_amount
                sell_order.remaining_amount -= matched_amount
                if buy_order.remaining_amount == 0:
                    buy_order.status = "closed"
                    break
                if sell_order.remaining_amount == 0:
                    sell_order.status = "closed"

    await db.commit()


async def fetch_order_book(pair: str, db: AsyncSession) -> dict:
    try:
        base_token, quote_token = pair.split("/")
        base = await get_token_by_ticker(base_token, db)
        quote = await get_token_by_ticker(quote_token, db)
        if not base or not quote:
            raise ValidationError(f"Invalid trading pair: {pair}")

        buy_orders = await get_open_orders(pair, "buy", db)
        sell_orders = await get_open_orders(pair, "sell", db)

        return {"buy_orders": buy_orders, "sell_orders": sell_orders}
    except Exception as e:
        raise ValueError(f"Failed to fetch order book: {str(e)}")
