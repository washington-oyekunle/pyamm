# pyamm

**Pure Python Automated Market Maker (AMM) Engine**

A zero-dependency implementation of a constant-product AMM (Uniswap V2 style). Perfect for educational purposes, simulations, portfolio demonstrations, and understanding DeFi mechanics without external libraries.

## Features

- Constant product formula: \(x \cdot y = k\)
- Multi-asset liquidity pools
- Add / remove liquidity with proportional shares
- Token swaps with configurable fee (default 0.3%)
- Slippage protection
- Fee collection tracking
- Multi-hop routing
- Impermanent loss calculator
- Monte-Carlo style volatility simulation
- Clean CLI interface
- Comprehensive unit tests
- Fully typed, modern Python 3.10+

## Quick Start

```bash
git clone https://github.com/washington-oyekunle/pyamm.git
cd pyamm
python -m pyamm.cli demo
```

Or use as a library:

```python
from pyamm.engine import Pool, Token

usdc = Token("USDC", 6)
eth = Token("ETH", 18)

pool = Pool(usdc, eth, fee_bps=30)
pool.add_liquidity(1_000_000_000, 500_000_000_000_000_000)  # 1000 USDC + 0.5 ETH

# Swap 100 USDC for ETH
amount_out, new_price = pool.swap(usdc, 100_000_000, min_out=0)
print(f"Received {amount_out / 10**18:.6f} ETH")
```

## Multi-hop Example

```python
from pyamm.router import Router

router = Router([pool_a_b, pool_b_c])
out, prices = router.swap_exact_in([token_a, token_b, token_c], amount_in)
```

## Architecture

- `pyamm/models.py` — Token, Position dataclasses
- `pyamm/engine.py` — Core AMM math and Pool class
- `pyamm/router.py` — Multi-hop swap routing
- `pyamm/analytics.py` — Impermanent loss, price impact, TVL
- `pyamm/simulation.py` — Volatility simulation helpers
- `pyamm/cli.py` — Interactive command-line interface
- `docs/MATH.md` — Mathematical derivations
- `tests/` — Full test suite

## Math

See [docs/MATH.md](docs/MATH.md) for the constant-product formula, swap derivation, and impermanent loss.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
