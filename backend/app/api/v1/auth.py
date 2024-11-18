from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from models import database_helper
from schemas.user_scheme import CreateUserScheme, CredentialsScheme
from services import auth_service
from services.response_service import ResponseService

router = APIRouter(tags=["Auth"])


async def get_session_id(session_id: str | None = Cookie(default=None)) -> str | None:
    return session_id


@router.post("/signup")
async def sign_up(user: CreateUserScheme, db: AsyncSession = Depends(database_helper.session_getter)) -> Any:
    return await ResponseService.response(
        auth_service.register_user(user, db)
    )


@router.post("/login")
async def login(user: CredentialsScheme, db: AsyncSession = Depends(database_helper.session_getter)) -> Any:
    return await ResponseService.response(
        auth_service.login_user(user, db)
    )


@router.post("/users/set-password")
async def set_pass(new_pass: str, session_id: str | None = Depends(get_session_id),
                   db: AsyncSession = Depends(database_helper.session_getter)) -> Any:
    return await ResponseService.response(
        auth_service.set_pass(new_pass, session_id, db)
    )


@router.get("/users/me/")
async def get_info(session_id: str | None = Depends(get_session_id),
                   db: AsyncSession = Depends(database_helper.session_getter)) -> Any:
    return await ResponseService.response(
        auth_service.get_info(session_id, db)
    )


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(database_helper.session_getter)) -> Any:
    return await ResponseService.response(
        auth_service.get_user(user_id, db)
    )


@router.post("/logout")
async def logout(session_id: str | None = Depends(get_session_id)) -> Any:
    return await ResponseService.response(
        auth_service.logout(session_id)
    )
