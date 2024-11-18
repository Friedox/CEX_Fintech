from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class TransferCreateScheme(BaseModel):
    sender_id: int
    receiver_id: int
    token_ticker: str
    amount: Decimal


class TransferResponse(BaseModel):
    message: str


class TransferHistoryResponse(BaseModel):
    sender_id: int
    receiver_id: int
    token_ticker: str
    amount: Decimal
    timestamp: datetime

    class Config:
        from_attributes = True
