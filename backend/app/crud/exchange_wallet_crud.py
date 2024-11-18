from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.exchange_wallet_model import ExchangeWallet


async def get_exchange_wallet_by_token(token_id: str, db: AsyncSession) -> ExchangeWallet:
    result = await db.execute(select(ExchangeWallet).where(ExchangeWallet.token_id == token_id))
    return result.scalars().first()


async def update_exchange_wallet_balance(token_id: str, amount: float, db: AsyncSession):
    wallet = await get_exchange_wallet_by_token(token_id, db)
    if wallet:
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
    return wallet
