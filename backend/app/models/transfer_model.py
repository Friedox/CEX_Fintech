from sqlalchemy import Column, ForeignKey, TIMESTAMP, DECIMAL, func, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    amount = Column(DECIMAL(32, 8), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    token = relationship("Token", back_populates="transfers")