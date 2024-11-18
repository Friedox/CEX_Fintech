from sqlalchemy import Column, ForeignKey, TIMESTAMP, DECIMAL, func, Integer
from sqlalchemy.orm import relationship
from .base import Base


class FaucetLog(Base):
    __tablename__ = "faucet_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    amount = Column(DECIMAL(32, 8), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="faucet_logs")
    token = relationship("Token")