from typing import List
from pydantic import BaseModel, EmailStr
from schemas.user_wallet_scheme import UserWalletResponse
from schemas.trade_scheme import TradeResponse


class CredentialsScheme(BaseModel):
    login: str
    password: str


class CreateUserScheme(BaseModel):
    email: EmailStr
    password: str


class UserScheme(BaseModel):
    id: int
    email: EmailStr
    username: str
    uid: str


class UserGetScheme(UserScheme):
    wallets: List[UserWalletResponse]
    trades: List[TradeResponse]

    class Config:
        from_attributes = True


class UserDBScheme(UserScheme):
    password_hash: str
