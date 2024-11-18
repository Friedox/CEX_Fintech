from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from crud.token_crud import get_token_by_ticker, update_token_supply
from crud.user_wallet_crud import (
    update_user_wallet_balance,
    get_user_wallet_by_token,
    create_user_wallet,
)
from schemas.user_wallet_scheme import UserWalletCreateScheme, UserWalletUpdateScheme
from exceptions import TokenNotFoundError, InsufficientTokenSupplyError
from decimal import Decimal


async def faucet_token(user_id: int, token_ticker: str, db: AsyncSession):
    try:
        token = await get_token_by_ticker(token_ticker, db)
        if not token:
            raise TokenNotFoundError()

        claim_amount = token.total_supply * Decimal(0.05)

        if token.total_supply < claim_amount:
            raise InsufficientTokenSupplyError()

        token.total_supply -= claim_amount
        await update_token_supply(token, db)

        user_wallet = await get_user_wallet_by_token(user_id, token.id, db)

        if not user_wallet:
            wallet_data = UserWalletCreateScheme(
                user_id=user_id,
                token_id=token.id,
                balance=claim_amount,
                locked_balance=Decimal("0.0"),
            )
            await create_user_wallet(wallet_data, db)
        else:

            user_wallet.balance += claim_amount
            await db.commit()
            await db.refresh(user_wallet)

        return {"message": f"Successfully claimed {claim_amount} {token_ticker}."}

    except SQLAlchemyError as e:
        print(f"Database error during faucet operation: {str(e)}")
        raise ValueError(f"Database error during faucet operation: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise ValueError(f"Unexpected error during faucet operation: {str(e)}")
