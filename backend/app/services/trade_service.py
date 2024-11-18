from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import InvalidRequestError
from models.order_model import Order
from crud.trade_crud import record_trade
from crud.order_crud import mark_order_as_filled
from services.connection_manager import manager
from sqlalchemy import select


async def match_orders(db: AsyncSession, token_pair: str):
    print(f"[INFO] Starting match process for {token_pair}")

    try:
        print("[INFO] Fetching buy and sell orders...")
        buy_orders = await db.execute(
            select(Order)
            .where(Order.token_pair == token_pair, Order.order_type == "buy", Order.is_filled == False)
            .order_by(Order.price.desc(), Order.created_at.asc())
        )
        buy_orders = buy_orders.scalars().all()

        sell_orders = await db.execute(
            select(Order)
            .where(Order.token_pair == token_pair, Order.order_type == "sell", Order.is_filled == False)
            .order_by(Order.price.asc(), Order.created_at.asc())
        )
        sell_orders = sell_orders.scalars().all()

        if not buy_orders or not sell_orders:
            print("[INFO] No orders available for matching.")
            return

        trades = []

        print("[INFO] Matching orders...")
        while buy_orders and sell_orders:
            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            print(f"[INFO] Evaluating match: Buy {buy_order}, Sell {sell_order}")
            if buy_order.price >= sell_order.price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = sell_order.price

                print(f"[INFO] Match found! Quantity: {trade_quantity}, Price: {trade_price}")

                trade = await record_trade(db, {
                    "buyer_id": buy_order.user_id,
                    "seller_id": sell_order.user_id,
                    "token_pair": token_pair,
                    "price": trade_price,
                    "quantity": trade_quantity,
                })
                trades.append(trade)

                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                if buy_order.quantity == 0:
                    buy_order.is_filled = True
                    buy_orders.pop(0)

                if sell_order.quantity == 0:
                    sell_order.is_filled = True
                    sell_orders.pop(0)

                db.add(buy_order)
                db.add(sell_order)

                print(f"[INFO] Trade executed: {trade}")

            else:
                print("[INFO] No more matches possible.")
                break

        await db.commit()

        print("[INFO] Broadcasting updated order book...")
        await manager.broadcast(token_pair, {
            "type": "order_book_update",
            "data": {
                "buy_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in buy_orders],
                "sell_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in sell_orders],
                "filled_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in trades]
            }
        })

        for trade in trades:
            print(f"[INFO] Broadcasting trade: {trade}")
            await manager.broadcast(token_pair, {
                "type": "trade_update",
                "data": {
                    "trade_id": trade.id,
                    "buyer_id": trade.buyer_id,
                    "seller_id": trade.seller_id,
                    "price": trade.price,
                    "quantity": trade.quantity,
                    "timestamp": trade.timestamp.isoformat(),
                }
            })

        print("[INFO] Match process completed successfully.")

    except InvalidRequestError as e:
        print(f"[ERROR] Transaction issue: {e}")
        await db.rollback()
    except Exception as e:
        print(f"[ERROR] Match orders failed: {e}")
        await db.rollback()
