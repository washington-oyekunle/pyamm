"""Monte-Carlo style simulation helpers for strategy testing."""

from decimal import Decimal
from random import Random
from typing import Callable

from .engine import Pool, Token


def simulate_volatility(
    pool: Pool,
    steps: int = 100,
    volatility: float = 0.02,
    seed: int = 42,
) -> list[dict]:
    """Simulate random walks on the price and record pool state."""
    rng = Random(seed)
    history = []
    for _ in range(steps):
        # Random trade size as fraction of reserve
        direction = rng.choice([0, 1])
        frac = Decimal(str(rng.uniform(0.001, volatility)))
        if direction == 0:
            amount = int(Decimal(pool.reserve0) * frac)
            if amount > 0:
                pool.swap(pool.token0, amount)
        else:
            amount = int(Decimal(pool.reserve1) * frac)
            if amount > 0:
                pool.swap(pool.token1, amount)

        history.append(
            {
                "reserve0": pool.reserve0,
                "reserve1": pool.reserve1,
                "price": float(pool.price),
                "k": pool.k,
            }
        )
    return history
