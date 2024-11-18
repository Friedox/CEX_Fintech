import re
import random
import string
import bcrypt
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import settings
from exceptions import EmailInUseError, UserNotFoundError
from schemas.user_scheme import CreateUserScheme, UserScheme, UserDBScheme
from schemas.user_wallet_scheme import UserWalletCreateScheme
from crud.token_crud import get_all_tokens
from crud.user_wallet_crud import create_user_wallet
from models.user_model import User

logger = logging.getLogger(__name__)


def generate_uid(length: int = 12) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def create_user(user_create: CreateUserScheme, db: AsyncSession) -> UserScheme:
    result = await db.execute(select(User).where(User.email == user_create.email))
    if result.scalars().first():
        raise EmailInUseError()

    temp_username = f"user_{''.join(random.choices(string.ascii_lowercase, k=8))}"
    uid = generate_uid()

    while True:
        existing_uid = await db.execute(select(User).where(User.uid == uid))
        if not existing_uid.scalars().first():
            break
        uid = generate_uid()

    hashed_password = bcrypt.hashpw(user_create.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = User(
        email=user_create.email,
        username=temp_username,
        uid=uid,
        password_hash=hashed_password
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    tokens = await get_all_tokens(db)
    if not tokens:
        logger.info("No tokens found. User will have no wallets until tokens are added.")
    else:
        for token in tokens:
            wallet_data = UserWalletCreateScheme(
                user_id=new_user.id,
                token_id=token.id,
                balance=0,
                locked_balance=0,
            )
            await create_user_wallet(wallet_data, db)

    logger.info(f"User created with id={new_user.id}, email={new_user.email}")
    return UserScheme(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        uid=new_user.uid
    )


async def get_user_by_uid(uid: str, db: AsyncSession) -> UserScheme:
    result = await db.execute(select(User).where(User.uid == uid))
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()
    return UserScheme(
        id=user.id,
        email=user.email,
        username=user.username,
        uid=user.uid
    )


async def get_user_by_email(email: str, db: AsyncSession) -> UserDBScheme:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()
    return UserDBScheme(
        id=user.id,
        email=user.email,
        username=user.username,
        uid=user.uid,
        password_hash=user.password_hash,
    )


async def get_user_by_username(username: str, db: AsyncSession) -> UserScheme:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()
    return UserScheme(
        id=user.id,
        email=user.email,
        username=user.username,
        uid=user.uid
    )


async def check_password(user_id: int, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        return user.password_hash is not None
    raise UserNotFoundError()


async def set_password(user_id: int, hashed_password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()
    user.password_hash = hashed_password
    await db.commit()


async def get(param: str | int, db: AsyncSession) -> UserScheme:
    if isinstance(param, str) and re.match(settings.validation.email_pattern, param):
        query = select(User).filter(User.email == param)
    elif isinstance(param, str):
        query = select(User).filter(User.username == param)
    else:
        query = select(User).filter(User.id == param)

    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()

    return UserScheme(
        id=user.id,
        email=user.email,
        username=user.username,
        uid=user.uid
    )


async def get_user_by_id(user_id: int, db: AsyncSession) -> UserScheme:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError()
    return UserScheme(
        id=user.id,
        email=user.email,
        username=user.username,
        uid=user.uid
    )
