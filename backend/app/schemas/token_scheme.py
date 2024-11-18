from pydantic import BaseModel


class TokenCreateScheme(BaseModel):
    name: str
    ticker: str
    total_supply: float


class TokenScheme(BaseModel):
    id: int
    name: str
    ticker: str
    total_supply: float

    class Config:
        from_attributes = True
