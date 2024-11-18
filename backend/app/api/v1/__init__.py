from fastapi import APIRouter

from config import settings
from .auth import router as auth_router
from .token import router as token_router
from .trade import router as trade_router
from .wallet import router as wallet_router
from .faucet import router as faucet_router
from .transfer import router as transfer_router
from .order import router as order_router
from .trade_ws import router as trade_ws_router


router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth
)

router.include_router(
    token_router,
    prefix=settings.api.v1.token
)

router.include_router(
    trade_router,
    prefix=settings.api.v1.trade
)

router.include_router(
    wallet_router,
    prefix=settings.api.v1.wallet
)

router.include_router(
    faucet_router,
    prefix=settings.api.v1.faucet
)

router.include_router(
    transfer_router,
    prefix=settings.api.v1.transfer
)

router.include_router(
    order_router,
    prefix=settings.api.v1.order
)

router.include_router(
    trade_ws_router,
    prefix=settings.api.v1.trade_ws
)
