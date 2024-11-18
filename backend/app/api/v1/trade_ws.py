from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from models.db_helper import database_helper
from models.order_model import Order
from crud.order_crud import create_order, get_orders_by_token_pair
from services.trade_service import match_orders
from services.connection_manager import manager
from services.auth_service import get_user_from_session_id

router = APIRouter(tags=["WebSocket"])


@router.websocket("/{token_pair}")
async def websocket_endpoint(
    token_pair: str,
    websocket: WebSocket,
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(database_helper.session_getter)
):
    try:
        if not session_id:
            raise HTTPException(status_code=403, detail="Session ID missing")

        user = await get_user_from_session_id(session_id, db)
        user_id = user.id

        print(f"[INFO] User {user_id} connected for token pair: {token_pair}")

        token_pair = token_pair.replace("-", "/")
        await manager.connect(token_pair, websocket)

        while True:
            try:
                data = await websocket.receive_json()

                if data["action"] == "create_order":
                    order_data = data["order"]
                    order_data["user_id"] = user_id
                    print(f"[INFO] Creating order: {order_data}")
                    await create_order(db, order_data)

                    print(f"[INFO] Matching orders for {token_pair}")
                    await match_orders(db, token_pair)

                    buy_orders = await get_orders_by_token_pair(db, token_pair, "buy")
                    sell_orders = await get_orders_by_token_pair(db, token_pair, "sell")

                    print(f"[INFO] Broadcasting updated order book for {token_pair}")
                    await manager.broadcast(token_pair, {
                        "type": "order_book_update",
                        "data": {
                            "buy_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in buy_orders],
                            "sell_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in sell_orders],
                        }
                    })

                elif data["action"] == "get_order_book":
                    buy_orders = await get_orders_by_token_pair(db, token_pair, "buy")
                    sell_orders = await get_orders_by_token_pair(db, token_pair, "sell")

                    print(f"[INFO] Sending order book for {token_pair}")
                    await websocket.send_json({
                        "type": "order_book_update",
                        "data": {
                            "buy_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in buy_orders],
                            "sell_orders": [{"id": o.id, "price": o.price, "quantity": o.quantity} for o in sell_orders],
                        }
                    })
            except Exception as e:
                print(f"[ERROR] WebSocket inner loop error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })

    except WebSocketDisconnect:
        print(f"[WARNING] WebSocket disconnected for {token_pair}")
        manager.disconnect(token_pair, websocket)
    except Exception as e:
        print(f"[ERROR] WebSocket endpoint error: {e}")
        await websocket.close(code=1011)