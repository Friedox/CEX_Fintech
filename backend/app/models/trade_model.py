from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_pair = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    buyer = relationship("User", back_populates="trades_as_buyer", foreign_keys=[buyer_id])
    seller = relationship("User", back_populates="trades_as_seller", foreign_keys=[seller_id])
