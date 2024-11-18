from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class UserWalletCreateScheme(BaseModel):
    user_id: int
    token_id: int
    balance: Decimal = Decimal("0.0")  # Default balance
    locked_balance: Decimal = Decimal("0.0")  # Default locked balance


class UserWalletUpdateScheme(BaseModel):
    id: int
    balance: Optional[Decimal] = None
    locked_balance: Optional[Decimal] = None


class UserWalletResponse(BaseModel):
    id: int
    user_id: int
    token_id: int
    balance: Decimal
    locked_balance: Decimal

    class Config:
        from_attributes = True
