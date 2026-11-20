from __future__ import annotations

from decimal import Decimal
from typing import List, Sequence, Tuple

from .engine import Pool, Token


class Router:
    """Simple multi-hop swap router over multiple pools."""

    def __init__(self, pools: Sequence[Pool]) -> None:
        self.pools = list(pools)
        self._index: dict[tuple[str, str], Pool] = {}
        for p in self.pools:
            key = tuple(sorted([p.token0.symbol, p.token1.symbol]))
            self._index[key] = p  # type: ignore[assignment]

    def find_pool(self, a: Token, b: Token) -> Pool | None:
        key = tuple(sorted([a.symbol, b.symbol]))
        return self._index.get(key)

    def swap_exact_in(
        self,
        path: List[Token],
        amount_in: int,
        min_amount_out: int = 0,
    ) -> Tuple[int, List[Decimal]]:
        if len(path) < 2:
            raise ValueError("path must contain at least two tokens")

        current = amount_in
        prices: List[Decimal] = []

        for i in range(len(path) - 1):
            token_in = path[i]
            token_out = path[i + 1]
            pool = self.find_pool(token_in, token_out)
            if pool is None:
                raise ValueError(f"no pool for {token_in.symbol}/{token_out.symbol}")

            current, price = pool.swap(token_in, current, min_amount_out=0)
            prices.append(price)

        if current < min_amount_out:
            raise ValueError(f"final output {current} below min {min_amount_out}")

        return current, prices
