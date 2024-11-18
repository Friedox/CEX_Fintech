from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.faucet_log_model import FaucetLog
from datetime import datetime, timedelta


async def get_last_faucet_log(user_id: str, token_id: str, db: AsyncSession) -> FaucetLog | None:
    query = (
        select(FaucetLog)
        .where(FaucetLog.user_id == user_id, FaucetLog.token_id == token_id)
        .order_by(FaucetLog.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().first()


async def create_faucet_log(user_id: str, token_id: str, amount: float, db: AsyncSession) -> FaucetLog:
    faucet_log = FaucetLog(user_id=user_id, token_id=token_id, amount=amount)
    db.add(faucet_log)
    await db.commit()
    await db.refresh(faucet_log)
    return faucet_log
