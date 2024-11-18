from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import database_helper
from schemas.token_scheme import TokenCreateScheme, TokenScheme
from services.token_service import add_token, list_tokens, remove_token

router = APIRouter(tags=["Tokens"])


@router.post("/", response_model=TokenScheme)
async def create_token(data: TokenCreateScheme, db: AsyncSession = Depends(database_helper.session_getter)):
    token = await add_token(data, db)
    return TokenScheme.from_orm(token)


@router.get("/", response_model=list[TokenScheme])
async def get_tokens(db: AsyncSession = Depends(database_helper.session_getter)):
    tokens = await list_tokens(db)
    return [TokenScheme.from_orm(token) for token in tokens]


@router.delete("/{token_id}", response_model=dict)
async def delete_token(token_id: str, db: AsyncSession = Depends(database_helper.session_getter)):
    return await remove_token(token_id, db)
