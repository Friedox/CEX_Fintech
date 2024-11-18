from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.trade_history_model import TradeHistory


async def log_trade(data: dict, db: AsyncSession) -> TradeHistory:
    trade = TradeHistory(**data)
    db.add(trade)
    await db.commit()
    await db.refresh(trade)
    return trade


async def get_trade_history(pair: str, db: AsyncSession, limit: int = 50, offset: int = 0) -> list[TradeHistory]:
    query = (
        select(TradeHistory)
        .where(TradeHistory.pair == pair)
        .order_by(TradeHistory.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    trades = result.scalars().all()
    return trades or []