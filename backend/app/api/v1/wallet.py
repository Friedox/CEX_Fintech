from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import database_helper
from schemas.user_wallet_scheme import UserWalletResponse
from services.wallet_service import deposit_to_user_wallet, transfer_between_users

router = APIRouter(tags=["Wallets"])


@router.post("/wallets/deposit", response_model=UserWalletResponse)
async def deposit_to_wallet(user_id: str, token_id: str, amount: float,
                            db: AsyncSession = Depends(database_helper.session_getter)):
    return await deposit_to_user_wallet(user_id, token_id, amount, db)


@router.post("/wallets/transfer", response_model=dict)
async def transfer_tokens(sender_id: str, receiver_id: str, token_id: str, amount: float,
                          db: AsyncSession = Depends(database_helper.session_getter)):
    await transfer_between_users(sender_id, receiver_id, token_id, amount, db)
    return {"message": "Transfer successful"}
