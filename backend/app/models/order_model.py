from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_pair = Column(String(50), nullable=False)
    order_type = Column(Enum("buy", "sell", name="order_type"), nullable=False)
    price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=False)
    is_filled = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="orders")
