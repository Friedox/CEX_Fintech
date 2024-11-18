from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, func, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    ticker = Column(String(10), unique=True, nullable=False)
    total_supply = Column(DECIMAL(32, 8), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    exchange_wallets = relationship("ExchangeWallet", back_populates="token")
    user_wallets = relationship("UserWallet", back_populates="token")
    transfers = relationship("Transfer", back_populates="token")