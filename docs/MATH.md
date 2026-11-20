# AMM Mathematics

## Constant Product

The invariant maintained by the pool is:

\[
x \cdot y = k
\]

where \(x\) and \(y\) are the reserves of the two tokens.

## Swap Formula

Given an input amount \(\Delta x\) and fee rate \(f\):

\[
\Delta y = y \cdot \frac{\Delta x \cdot (1-f)}{x + \Delta x \cdot (1-f)}
\]

## Impermanent Loss

For a price ratio \(r = P_{current}/P_{entry}\):

\[
IL = 1 - \frac{2\sqrt{r}}{1+r}
\]

(The function in the library returns the positive loss magnitude.)

## Liquidity Shares

Initial liquidity shares are \(\sqrt{x \cdot y}\).
Subsequent deposits receive shares proportional to the smaller of the two ratios of deposited amount to existing reserves.
