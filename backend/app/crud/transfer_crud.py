from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models.transfer_model import Transfer
from datetime import datetime


async def create_transfer_log(
        sender_id: int, receiver_id: int, token_id: int, amount: float, db: AsyncSession) -> Transfer:

    transfer = Transfer(
        sender_id=sender_id,
        receiver_id=receiver_id,
        token_id=token_id,
        amount=amount,
        created_at=datetime.utcnow(),
    )
    db.add(transfer)
    await db.commit()
    await db.refresh(transfer)
    return transfer


async def get_user_transfers(user_id: int, db: AsyncSession) -> list[Transfer]:
    query = select(Transfer).where(
        or_(Transfer.sender_id == user_id, Transfer.receiver_id == user_id)
    ).order_by(Transfer.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()
