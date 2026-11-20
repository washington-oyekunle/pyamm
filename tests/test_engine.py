import pytest
from pyamm.engine import Pool, Token
from pyamm.analytics import impermanent_loss
from decimal import Decimal


def test_add_liquidity_initial():
    pool = Pool(Token("A", 18), Token("B", 18))
    pos = pool.add_liquidity(1000, 2000)
    assert pool.reserve0 == 1000
    assert pool.reserve1 == 2000
    assert pool.total_liquidity_shares > 0
    assert pos.liquidity_shares == pool.total_liquidity_shares


def test_swap_basic():
    pool = Pool(Token("USDC", 6), Token("ETH", 18), fee_bps=30)
    pool.add_liquidity(1_000_000_000, 500_000_000_000_000_000)

    amount_out, _ = pool.swap(Token("USDC", 6), 100_000_000)
    assert amount_out > 0
    assert pool.reserve0 > 1_000_000_000
    assert pool.reserve1 < 500_000_000_000_000_000


def test_slippage_protection():
    pool = Pool(Token("A", 18), Token("B", 18))
    pool.add_liquidity(1000, 1000)

    with pytest.raises(ValueError, match="slippage"):
        pool.swap(Token("A", 18), 100, min_amount_out=200)


def test_impermanent_loss_at_parity():
    assert impermanent_loss(Decimal(1)) == 0


def test_impermanent_loss_2x():
    il = impermanent_loss(Decimal(2))
    # Known value ~5.7%
    assert Decimal("0.05") < il < Decimal("0.06")
