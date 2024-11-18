from pydantic import BaseModel, Field


class FaucetClaimRequest(BaseModel):
    token_ticker: str = Field(..., min_length=1, description="Ticker symbol of the token to claim")
