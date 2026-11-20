from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Token:
    symbol: str
    decimals: int

    def __post_init__(self) -> None:
        if not 0 <= self.decimals <= 18:
            raise ValueError("decimals must be between 0 and 18")
        if not self.symbol:
            raise ValueError("symbol cannot be empty")


@dataclass
class Position:
    """Liquidity provider position."""
    owner: str
    token0_amount: int
    token1_amount: int
    liquidity_shares: int

    def share_of_pool(self, total_shares: int) -> Decimal:
        if total_shares == 0:
            return Decimal(0)
        return Decimal(self.liquidity_shares) / Decimal(total_shares)
