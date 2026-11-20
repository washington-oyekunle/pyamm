from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Tuple

from .models import Position, Token


@dataclass
class Pool:
    """Constant-product AMM pool (Uniswap V2 style)."""

    token0: Token
    token1: Token
    fee_bps: int = 30  # 0.30%
    reserve0: int = 0
    reserve1: int = 0
    total_liquidity_shares: int = 0
    fee_growth0: int = 0
    fee_growth1: int = 0
    positions: dict[str, Position] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.fee_bps < 0 or self.fee_bps > 1000:
            raise ValueError("fee_bps must be between 0 and 1000")
        if self.token0.symbol == self.token1.symbol:
            raise ValueError("tokens must be different")

    @property
    def k(self) -> int:
        return self.reserve0 * self.reserve1

    @property
    def price(self) -> Decimal:
        """Price of token0 in terms of token1."""
        if self.reserve0 == 0:
            return Decimal(0)
        return Decimal(self.reserve1) / Decimal(self.reserve0)

    def add_liquidity(
        self, amount0: int, amount1: int, owner: str = "default"
    ) -> Position:
        if amount0 <= 0 or amount1 <= 0:
            raise ValueError("amounts must be positive")

        if self.total_liquidity_shares == 0:
            shares = int((Decimal(amount0) * Decimal(amount1)).sqrt())
        else:
            share0 = Decimal(amount0) * Decimal(self.total_liquidity_shares) / Decimal(self.reserve0)
            share1 = Decimal(amount1) * Decimal(self.total_liquidity_shares) / Decimal(self.reserve1)
            shares = int(min(share0, share1))

        if shares <= 0:
            raise ValueError("insufficient liquidity contribution")

        self.reserve0 += amount0
        self.reserve1 += amount1
        self.total_liquidity_shares += shares

        if owner in self.positions:
            pos = self.positions[owner]
            pos.token0_amount += amount0
            pos.token1_amount += amount1
            pos.liquidity_shares += shares
        else:
            pos = Position(owner, amount0, amount1, shares)
            self.positions[owner] = pos

        return pos

    def remove_liquidity(self, shares: int, owner: str = "default") -> Tuple[int, int]:
        if owner not in self.positions:
            raise ValueError("no position for owner")
        pos = self.positions[owner]
        if shares > pos.liquidity_shares or shares <= 0:
            raise ValueError("invalid share amount")

        fraction = Decimal(shares) / Decimal(self.total_liquidity_shares)
        amount0 = int(Decimal(self.reserve0) * fraction)
        amount1 = int(Decimal(self.reserve1) * fraction)

        self.reserve0 -= amount0
        self.reserve1 -= amount1
        self.total_liquidity_shares -= shares
        pos.liquidity_shares -= shares
        pos.token0_amount = max(0, pos.token0_amount - amount0)
        pos.token1_amount = max(0, pos.token1_amount - amount1)

        if pos.liquidity_shares == 0:
            del self.positions[owner]

        return amount0, amount1

    def swap(
        self,
        token_in: Token,
        amount_in: int,
        min_amount_out: int = 0,
    ) -> Tuple[int, Decimal]:
        if amount_in <= 0:
            raise ValueError("amount_in must be positive")

        if token_in.symbol == self.token0.symbol:
            reserve_in, reserve_out = self.reserve0, self.reserve1
            is_token0 = True
        elif token_in.symbol == self.token1.symbol:
            reserve_in, reserve_out = self.reserve1, self.reserve0
            is_token0 = False
        else:
            raise ValueError("token not in pool")

        fee_multiplier = Decimal(10_000 - self.fee_bps) / Decimal(10_000)
        amount_in_with_fee = int(Decimal(amount_in) * fee_multiplier)

        # Constant product: (x + dx) * (y - dy) = x * y
        # dy = y * dx / (x + dx)
        amount_out = (reserve_out * amount_in_with_fee) // (reserve_in + amount_in_with_fee)

        if amount_out < min_amount_out:
            raise ValueError(f"slippage: got {amount_out}, min {min_amount_out}")

        if is_token0:
            self.reserve0 += amount_in
            self.reserve1 -= amount_out
            self.fee_growth0 += amount_in - amount_in_with_fee
        else:
            self.reserve1 += amount_in
            self.reserve0 -= amount_out
            self.fee_growth1 += amount_in - amount_in_with_fee

        return amount_out, self.price

    def get_amount_out(self, token_in: Token, amount_in: int) -> int:
        """Preview swap without state change."""
        if token_in.symbol == self.token0.symbol:
            reserve_in, reserve_out = self.reserve0, self.reserve1
        else:
            reserve_in, reserve_out = self.reserve1, self.reserve0

        fee_multiplier = Decimal(10_000 - self.fee_bps) / Decimal(10_000)
        amount_in_with_fee = int(Decimal(amount_in) * fee_multiplier)
        return (reserve_out * amount_in_with_fee) // (reserve_in + amount_in_with_fee)
