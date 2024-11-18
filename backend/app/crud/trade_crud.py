from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.trade_model import Trade
from typing import List


async def record_trade(db: AsyncSession, trade_data: dict) -> Trade:
    new_trade = Trade(**trade_data)
    db.add(new_trade)
    await db.commit()
    await db.refresh(new_trade)
    return new_trade


async def get_trades_by_token_pair(db: AsyncSession, token_pair: str) -> List[Trade]:
    result = await db.execute(
        select(Trade).where(Trade.token_pair == token_pair).order_by(Trade.timestamp.desc())
    )
    return result.scalars().all()
