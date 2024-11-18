from pydantic import BaseModel


class ExchangeWalletScheme(BaseModel):
    id: int
    token_id: int
    balance: float
    locked_balance: float

    class Config:
        from_attributes = True
