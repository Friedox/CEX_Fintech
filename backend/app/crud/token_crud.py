from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.token_model import Token
from schemas.token_scheme import TokenCreateScheme
from schemas.user_wallet_scheme import UserWalletCreateScheme
from crud.user_wallet_crud import create_user_wallet
from models.user_model import User
import logging

logger = logging.getLogger(__name__)


async def create_token(data: TokenCreateScheme, db: AsyncSession) -> Token:
    # Check if the token already exists
    existing_token = await db.execute(select(Token).where(Token.ticker == data.ticker))
    if existing_token.scalars().first():
        raise ValueError("Token with this ticker already exists.")

    new_token = Token(
        name=data.name,
        ticker=data.ticker,
        total_supply=data.total_supply
    )
    db.add(new_token)
    await db.flush()

    users = await db.execute(select(User))
    users = users.scalars().all()

    for user in users:
        wallet_data = UserWalletCreateScheme(
            user_id=user.id,
            token_id=new_token.id,
            balance=0,
            locked_balance=0,
        )
        await create_user_wallet(wallet_data, db)

    await db.commit()
    await db.refresh(new_token)

    logger.info(f"Token '{data.ticker}' created and wallets assigned to all users.")
    return new_token


async def get_token_by_ticker(ticker: str, db: AsyncSession) -> Token:
    result = await db.execute(select(Token).where(Token.ticker == ticker))
    return result.scalars().first()


async def get_all_tokens(db: AsyncSession):
    result = await db.execute(select(Token))
    return result.scalars().all()


async def delete_token_by_id(token_id: str, db: AsyncSession):
    await db.execute(delete(Token).where(Token.id == token_id))
    await db.commit()


async def update_token_supply(token: Token, db: AsyncSession):
    await db.execute(
        update(Token)
        .where(Token.id == token.id)
        .values(total_supply=token.total_supply)
    )
    await db.commit()
