## 4 — How I Manufactured a Signal That Wasn't There

*The data definition lied.*

**The signal wasn't a signal. It was a clock.**

For about four days I thought I had found the thing I was looking for.

The variable was `new_wallet_frac`: the share of wallets trading in a window
that I had not seen trade before. On one day of BTC fills it separated
pre-event windows from ordinary ones at d = 1.85, q = 0.0025.

What made it interesting was not the size. It was the shape.

Every other variable I measured — aggressor volume, trade count, size
distribution, liquidations — did the same unhelpful thing. Nothing at 30
minutes out. Something around 15. A spike in the final five. That profile
describes a thermometer noticing a fire, not a smoke alarm. By the time it
registers, the move is already happening and there is nothing to do with it.

`new_wallet_frac` ran the other way. Strongest at 25–30 minutes out, fading to
nothing by the time price actually moved — d = 1.85 at `[-30,-25)` decaying to
d = 0.81 and non-significant at `[-5,0)` (q = 0.381). That is what a leading
indicator is supposed to look like, and it was the only variable that did it.

Then I looked at the definition.

"New" meant "not seen since 00:00 UTC". That definition decays mechanically
through the day: by evening you have already encountered most of the day's
active wallets, so fewer remain that can qualify as new. Measured across the
day, the variable fell from 0.529 at 00h to 0.087 at 21h, correlating with
minute-of-day at **r = −0.643** (the one-day report rounds this to −0.64; the
three-decimal figure is in the comparison table of the three-day report).

My events clustered in the morning. My controls did not.

So I recomputed it with a rolling 24-hour lookback. That change also required
moving from one day to three, which — as §5 explains — was what finally made
properly hour-matched controls possible. Two things improved at once: the
wallet definition, and the comparison it was being tested against. Their
contributions cannot be separated from what was run, and I am not going to
pretend otherwise.

![Figure 2](figures/fig2-lead-profile.png)

**Figure 2** — The lead-time profile before and after the definition change.

**Table 1 — `new_wallet_frac` with a rolling 24h lookback: 57 events, 744 hour-matched controls**

| lead bin | event mean | control mean | ratio | d | q (BH) | placebo p |
|---|---:|---:|---:|---:|---:|---:|
| **[-30,-25)** | 0.1308 | 0.1328 | 0.984 | **-0.05** | 0.911 | 0.806 |
| [-25,-20) | 0.1435 | 0.1337 | 1.073 | +0.24 | 0.430 | 0.069 |
| [-20,-15) | 0.1412 | 0.1331 | 1.061 | +0.19 | 0.517 | 0.093 |
| [-15,-10) | 0.1322 | 0.1330 | 0.994 | -0.02 | 0.942 | 0.913 |
| [-10,-5) | 0.1345 | 0.1331 | 1.011 | +0.03 | 0.895 | 0.821 |
| [-5,0) | 0.1274 | 0.1323 | 0.963 | -0.12 | 0.523 | 0.215 |

Columns through `q (BH)` are the full 57-event comparison from
`stats_4d_2026-08-21.csv`. The placebo column is necessarily the
strict hour-matched subset from `targeted_4d_2026-08-21.csv`, because
that is the only sample a placebo can be built on — it is a different
sample and is labelled as one.

Not one cell survives correction, and no cell separates from the hour-matched
placebo at 0.05. At the earliest bin the effect is not merely non-significant;
it is very slightly the wrong way round.

The confound is measurably gone. Within-day correlation with minute-of-day fell
from −0.643 under the old definition to **−0.097, −0.078 and −0.191** across the
three analysed days, and the hourly profile flattened from a 0.529 → 0.087 slide
to a range of **0.114–0.149** across all 24 hours. One residual is worth naming:
the daily mean still drifts down across the three days, 0.161 → 0.128 → 0.110.
That is a slow multi-day trend rather than the within-day sawtooth, and since
events and controls are both spread across all three days it is largely
balanced. It could not be hiding anything here in any case — the measured
effect is approximately zero in both directions.

The obvious objection is that the second test simply had different data and got
unlucky. It does not hold, and this is exactly the case where quoting power
matters. At 57 events against 744 controls the design had complete power to
detect d = 0.8 — both at p < 0.05 and at the stricter alpha BH effectively
imposes on a mid-ranked test — and that is well below the 1.85 I was chasing.
**If the original effect had been real at anything near the size claimed, it
could not have hidden from the second test.**

One cell is genuinely unresolved. `[-25,-20)` sits at d = +0.23 with placebo
p = 0.069: too small to distinguish from nothing at this sample size, and
equally consistent with a small real effect. The power table says why — at 57
events, d = 0.2 is detected 31% of the time before correction and 4% after,
d = 0.3 is 59% and 15%. Separating those two possibilities needs roughly
**250–400 events**, about 15–25 trading days. I am not counting it either way.
