import hashlib
import random
import bcrypt
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import user_crud
from exceptions import (
    InvalidSessionError,
    InvalidCredentialsError,
    EmailInUseError,
    UserNotFoundError,
)
from schemas.user_scheme import CredentialsScheme, CreateUserScheme, UserScheme, UserDBScheme
import logging

logger = logging.getLogger(__name__)


async def register_user(user_create: CreateUserScheme, db: AsyncSession) -> dict:
    try:
        existing_user = await user_crud.get_user_by_email(user_create.email, db)
        if existing_user:
            raise EmailInUseError()
    except UserNotFoundError:
        pass

    await user_crud.create_user(user_create, db)
    return {"message": "User registered successfully."}


async def login_user(user_login: CredentialsScheme, db: AsyncSession) -> dict:
    user_data = await authenticate_user(user_login, db)
    session_id = await create_session(user_data.id, user_data.username)
    return {"message": "Logged in successfully", "session_id": session_id}


async def authenticate_user(credentials: CredentialsScheme, db: AsyncSession) -> UserScheme:
    user_data = await user_crud.get_user_by_email(credentials.login, db)
    await authenticate_regular_user(user_data, credentials)
    return user_data


async def authenticate_regular_user(user_data: UserDBScheme, credentials: CredentialsScheme):
    if not bcrypt.checkpw(credentials.password.encode("utf-8"), user_data.password_hash.encode("utf-8")):
        raise InvalidCredentialsError()


async def create_session(user_id: int, username: str) -> str:
    session_id = hashlib.sha256(f"{user_id}{random.random()}".encode()).hexdigest()
    user_data = {
        "username": username,
        "user_id": user_id,
    }

    redis_client = redis.from_url(f'redis://{settings.redis.host}')
    await redis_client.hset(f"session:{session_id}", mapping=user_data)
    await redis_client.expire(f"session:{session_id}", settings.redis.expire_time)
    await redis_client.aclose()

    return session_id


async def logout(session_id: str | None):
    if not session_id:
        raise InvalidSessionError()
    async with redis.from_url(f'redis://{settings.redis.host}') as redis_client:
        await redis_client.delete(f"session:{session_id}")
    return {"message": "Logged out successfully."}


async def set_pass(new_pass: str, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id, db)
    hashed_password = bcrypt.hashpw(new_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    await user_crud.set_password(user.id, hashed_password, db)
    return {"message": "Password successfully updated."}


async def get_info(session_id: str | None, db: AsyncSession):
    user = await get_user_from_session_id(session_id=session_id, db=db)
    user_dict = user.__dict__
    user_dict.pop('password_hash', None)
    return user_dict


async def get_user_from_session_id(session_id: str | None, db: AsyncSession) -> UserScheme:
    if not session_id:
        raise InvalidSessionError()

    async with redis.from_url(f'redis://{settings.redis.host}') as redis_client:
        username = await redis_client.hget(f"session:{session_id}", "username")

    if not username:
        raise InvalidSessionError()

    user_data = await user_crud.get_user_by_username(username.decode('utf-8'), db)
    return user_data


async def get_user(user_id: int, db: AsyncSession) -> dict:
    user = await user_crud.get_user_by_id(user_id, db)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "uid": user.uid,
    }
