from sqlalchemy.ext.asyncio import AsyncSession
from crud.token_crud import create_token, get_all_tokens, delete_token_by_id
from schemas.token_scheme import TokenCreateScheme
from exceptions import TokenNotFoundError, TokenAlreadyExistsError


async def add_token(data: TokenCreateScheme, db: AsyncSession):
    try:
        return await create_token(data, db)
    except TokenAlreadyExistsError:
        raise TokenAlreadyExistsError()


async def list_tokens(db: AsyncSession):
    return await get_all_tokens(db)


async def remove_token(token_id: str, db: AsyncSession):
    token = await get_all_tokens(db)
    if not token:
        raise TokenNotFoundError()
    await delete_token_by_id(token_id, db)
    return {"message": f"Token with ID {token_id} has been deleted."}