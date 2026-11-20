#!/usr/bin/env python3
"""Interactive CLI for pyamm."""

import argparse
from decimal import Decimal

from .engine import Pool, Token
from .analytics import impermanent_loss


def main() -> None:
    parser = argparse.ArgumentParser(description="Pure Python AMM CLI")
    sub = parser.add_subparsers(dest="cmd")

    demo = sub.add_parser("demo", help="Run a quick demo")
    demo.set_defaults(func=run_demo)

    il = sub.add_parser("il", help="Calculate impermanent loss")
    il.add_argument("ratio", type=float, help="Price ratio (current/entry)")
    il.set_defaults(func=calc_il)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def run_demo(_: argparse.Namespace) -> None:
    print("=== pyamm Demo ===")
    usdc = Token("USDC", 6)
    eth = Token("ETH", 18)
    pool = Pool(usdc, eth, fee_bps=30)

    print("Adding liquidity: 1000 USDC + 0.5 ETH")
    pool.add_liquidity(1_000_000_000, 500_000_000_000_000_000)
    print(f"Price (ETH per USDC): {pool.price:.6f}")
    print(f"k = {pool.k}")

    print("\nSwapping 100 USDC for ETH...")
    out, new_price = pool.swap(usdc, 100_000_000)
    print(f"Received: {out / 10**18:.6f} ETH")
    print(f"New price: {new_price:.6f}")
    print(f"Reserves: {pool.reserve0/10**6:.2f} USDC, {pool.reserve1/10**18:.6f} ETH")


def calc_il(args: argparse.Namespace) -> None:
    loss = impermanent_loss(Decimal(str(args.ratio)))
    print(f"Impermanent loss at ratio {args.ratio}: {loss*100:.4f}%")


if __name__ == "__main__":
    main()
