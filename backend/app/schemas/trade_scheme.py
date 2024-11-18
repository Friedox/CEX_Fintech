from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class TradeCreateScheme(BaseModel):
    user_id: int
    token_id: int
    trade_type: str  # "buy" or "sell"
    amount: Decimal
    price: Decimal


class TradeResponse(BaseModel):
    id: int
    user_id: int
    token_id: int
    trade_type: str  # "buy" or "sell"
    amount: Decimal
    price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
