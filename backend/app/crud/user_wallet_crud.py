from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.user_wallet_model import UserWallet
from schemas.user_wallet_scheme import UserWalletCreateScheme, UserWalletUpdateScheme
from decimal import Decimal


async def get_user_wallet_by_token(user_id: str, token_id: str, db: AsyncSession) -> UserWallet | None:
    result = await db.execute(
        select(UserWallet).where(UserWallet.user_id == user_id, UserWallet.token_id == token_id)
    )
    return result.scalars().first()


async def create_user_wallet(data: UserWalletCreateScheme, db: AsyncSession) -> UserWallet:
    wallet = UserWallet(
        user_id=data.user_id,
        token_id=data.token_id,
        balance=data.balance,
        locked_balance=data.locked_balance,
    )
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet


async def update_user_wallet_balance(user_id: int, token_id: int, amount: Decimal, db: AsyncSession) -> None:
    query = (
        update(UserWallet)
        .where(UserWallet.user_id == user_id, UserWallet.token_id == token_id)
        .values(balance=UserWallet.balance + amount)
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(query)

    if result.rowcount == 0:
        raise ValueError(f"Wallet not found for user_id={user_id}, token_id={token_id}")

    await db.commit()


async def get_wallets_by_user(user_id: str, db: AsyncSession) -> list[UserWallet]:
    result = await db.execute(select(UserWallet).where(UserWallet.user_id == user_id))
    return result.scalars().all()
