from pydantic import BaseModel
from datetime import datetime


class TradeHistoryResponse(BaseModel):
    buyer_id: int
    seller_id: int
    pair: str
    price: float
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True
