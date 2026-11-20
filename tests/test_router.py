from pyamm.engine import Pool, Token
from pyamm.router import Router


def test_multi_hop_swap():
    usdc = Token("USDC", 6)
    eth = Token("ETH", 18)
    dai = Token("DAI", 18)

    pool_usdc_eth = Pool(usdc, eth, fee_bps=30)
    pool_eth_dai = Pool(eth, dai, fee_bps=30)

    pool_usdc_eth.add_liquidity(1_000_000_000, 500_000_000_000_000_000)
    pool_eth_dai.add_liquidity(500_000_000_000_000_000, 1_000_000_000_000_000_000)

    router = Router([pool_usdc_eth, pool_eth_dai])

    # USDC -> ETH -> DAI
    out, prices = router.swap_exact_in([usdc, eth, dai], 100_000_000)
    assert out > 0
    assert len(prices) == 2
