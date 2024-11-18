from sqlalchemy.ext.asyncio import AsyncSession
from crud.user_wallet_crud import get_user_wallet_by_token, update_user_wallet_balance
from crud.transfer_crud import create_transfer_log
from crud.token_crud import get_token_by_ticker
from exceptions import InvalidUserAssetsOperationError, TokenNotFoundError
from decimal import Decimal


async def transfer_tokens(sender_id: int, receiver_id: int, token_ticker: str, amount: Decimal, db: AsyncSession):
    if amount <= 0:
        raise InvalidUserAssetsOperationError()

    # Fetch token
    token = await get_token_by_ticker(token_ticker, db)
    if not token:
        raise TokenNotFoundError()

    # Fetch sender's wallet
    sender_wallet = await get_user_wallet_by_token(sender_id, token.id, db)
    if not sender_wallet or sender_wallet.balance < amount:
        raise InvalidUserAssetsOperationError()

    # Update sender and receiver wallets
    await update_user_wallet_balance(sender_id, token.id, -amount, db)
    await update_user_wallet_balance(receiver_id, token.id, amount, db)

    # Log transfer
    transfer_entry = await create_transfer_log(sender_id, receiver_id, token.id, amount, db)

    return {"message": f"Successfully transferred {amount} {token.ticker} from {sender_id} to {receiver_id}."}


async def get_transfer_history(user_id: int, db: AsyncSession):
    # Fetch transfer history for the user
    from crud.transfer_crud import get_user_transfers
    return await get_user_transfers(user_id, db)
