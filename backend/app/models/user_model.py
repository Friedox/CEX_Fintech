from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    uid = Column(String(16), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    wallets = relationship("UserWallet", back_populates="user")

    faucet_logs = relationship("FaucetLog", back_populates="user")

    orders = relationship("Order", back_populates="user")

    trades_as_buyer = relationship(
        "Trade",
        back_populates="buyer",
        foreign_keys="Trade.buyer_id",
    )
    trades_as_seller = relationship(
        "Trade",
        back_populates="seller",
        foreign_keys="Trade.seller_id",
    )
