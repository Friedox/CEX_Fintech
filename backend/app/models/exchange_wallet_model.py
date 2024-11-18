from sqlalchemy import Column, DECIMAL, TIMESTAMP, ForeignKey, func, Integer
from sqlalchemy.orm import relationship
from .base import Base


class ExchangeWallet(Base):
    __tablename__ = "exchange_wallets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    balance = Column(DECIMAL(32, 8), nullable=False, default=0)
    locked_balance = Column(DECIMAL(32, 8), nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    token = relationship("Token", back_populates="exchange_wallets")