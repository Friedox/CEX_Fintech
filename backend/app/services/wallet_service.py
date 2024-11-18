from sqlalchemy.ext.asyncio import AsyncSession
from crud.user_wallet_crud import get_user_wallet_by_token, update_user_wallet_balance
from crud.exchange_wallet_crud import get_exchange_wallet_by_token, update_exchange_wallet_balance


async def deposit_to_user_wallet(user_id: str, token_id: str, amount: float, db: AsyncSession):
    exchange_wallet = await get_exchange_wallet_by_token(token_id, db)
    if not exchange_wallet or exchange_wallet.balance < amount:
        raise ValueError("Insufficient funds in the exchange wallet.")

    await update_exchange_wallet_balance(token_id, -amount, db)

    return await update_user_wallet_balance(user_id, token_id, amount, db)


async def transfer_between_users(sender_id: str, receiver_id: str, token_id: str, amount: float, db: AsyncSession):
    sender_wallet = await get_user_wallet_by_token(sender_id, token_id, db)
    if not sender_wallet or sender_wallet.balance < amount:
        raise ValueError("Insufficient funds.")

    await update_user_wallet_balance(sender_id, token_id, -amount, db)

    return await update_user_wallet_balance(receiver_id, token_id, amount, db)
