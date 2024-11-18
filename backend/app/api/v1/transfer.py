from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import database_helper
from schemas.transfer_scheme import TransferCreateScheme, TransferResponse, TransferHistoryResponse
from services.transfer_service import transfer_tokens, get_transfer_history

router = APIRouter(tags=["Transfers"])


@router.post("/", response_model=TransferResponse)
async def create_transfer(
    data: TransferCreateScheme,
    db: AsyncSession = Depends(database_helper.session_getter),
):
    print(data)
    transfer_result = await transfer_tokens(
        sender_id=data.sender_id,
        receiver_id=data.receiver_id,
        token_ticker=data.token_ticker,
        amount=data.amount,
        db=db,
    )
    print(data)
    return TransferResponse(**transfer_result)


@router.get("/history", response_model=list[TransferHistoryResponse])
async def get_transfer_history(
    user_id: int,
    db: AsyncSession = Depends(database_helper.session_getter),
):
    history = await get_transfer_history(user_id=user_id, db=db)
    return [TransferHistoryResponse.from_attributes(entry) for entry in history]
