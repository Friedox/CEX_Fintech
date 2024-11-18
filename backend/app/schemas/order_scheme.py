from pydantic import BaseModel, Field
from datetime import datetime


class OrderCreateScheme(BaseModel):
    user_id: int
    pair: str
    order_type: str  # buy или sell
    price: float
    amount: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    pair: str
    order_type: str
    price: float
    amount: float
    remaining_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
