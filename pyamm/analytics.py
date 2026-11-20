from decimal import Decimal
from typing import Tuple

from .engine import Pool


def impermanent_loss(price_ratio: Decimal) -> Decimal:
    """
    Calculate impermanent loss for a given price ratio.
    price_ratio = current_price / entry_price
    Returns loss as a positive fraction (0.01 = 1% loss).
    """
    if price_ratio <= 0:
        raise ValueError("price_ratio must be positive")
    # IL = 2 * sqrt(r) / (1 + r) - 1
    sqrt_r = price_ratio.sqrt()
    il = (2 * sqrt_r / (1 + price_ratio)) - 1
    return -il  # return as positive loss


def price_impact(pool: Pool, token_in_symbol: str, amount_in: int) -> Decimal:
    """Approximate price impact of a swap."""
    if token_in_symbol == pool.token0.symbol:
        reserve_in = pool.reserve0
    else:
        reserve_in = pool.reserve1

    if reserve_in == 0:
        return Decimal(1)

    return Decimal(amount_in) / Decimal(reserve_in)


def total_value_locked(pool: Pool, price0: Decimal, price1: Decimal) -> Decimal:
    """TVL in a common unit (e.g. USD)."""
    return (
        Decimal(pool.reserve0) / Decimal(10 ** pool.token0.decimals) * price0
        + Decimal(pool.reserve1) / Decimal(10 ** pool.token1.decimals) * price1
    )
