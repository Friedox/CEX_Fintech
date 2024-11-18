from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import database_helper
from schemas.faucet_claim_schema import FaucetClaimRequest
from crud.token_crud import get_all_tokens
from services.faucet_service import faucet_token
from services.response_service import ResponseService
from services.auth_service import get_info

router = APIRouter(tags=["Faucet"])


@router.get("/tokens")
async def get_available_tokens(
    db: AsyncSession = Depends(database_helper.session_getter)
):
    tokens = await get_all_tokens(db)
    return await ResponseService.response(
        [{"ticker": token.ticker, "total_supply": float(token.total_supply)} for token in tokens]
    )


@router.post("/claim")
async def claim_faucet(
    request: FaucetClaimRequest,
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(database_helper.session_getter),
):
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Session ID is required. User not authenticated.",
        )

    user_info = await get_info(session_id, db)
    user_id = user_info["id"]

    result = await faucet_token(user_id, request.token_ticker, db)
    return await ResponseService.response(result)
