## 6 — A Useless Variable Scored Perfectly

*The statistic lied.*

`liq_count` — the number of liquidations in a window — posted an **AUC of 1.000
in every single lead bin**.

A perfect classifier. Six times in a row.

It was a column of zeros. The archive pipeline reads liquidations from the
`is_liquidation` field in the fills schema; the live websocket `trades` channel
does not carry that field, so on the live feed every value was identical.

The mechanism was in my own AUC implementation, which assigned ranks by array
position rather than averaging ranks across ties. With every value tied, the
positive class took ranks 1…n, the statistic came out 0, and the
direction-agnostic flip — the step that lets a variable count as informative
whether it points up or down — turned 0 into 1.0.

A variable containing no information scored perfectly. And it scored perfectly
*consistently*, in every bin, which is precisely the property that makes a
result look like a finding rather than like noise. A single 1.000 invites
suspicion. Six of them look like a mechanism.

The fix has two parts, and only having both is sufficient: average ranks for
ties via `scipy.stats.rankdata`, and outright exclusion of zero-variance
variables before any ranking statistic runs. Verified at the three boundaries —
all values tied gives 0.500, perfect separation gives 1.000, no separation
gives 0.500.

With tie handling corrected and zero-variance columns excluded, the best-variable
edge of Model B over the volatility baseline across the six lead bins came out
between **−0.093 and +0.025**, and the pipeline declined to report any of it,
on the grounds that six events is below the thirty-event minimum. (That range is
from the live pipeline re-run after the 2026-08-26 control repair, on 34
non-overlapping controls; the pre-repair run on 157 overlapping controls gave
−0.109 to +0.010. Neither is reportable and the repair does not change that.)

The failure mode here is not a crash, an exception, or a NaN. It is a beautiful
number, and it would have survived to publication. `liq_count` remains declared
in the pre-registered feature list for exactly that reason — §10 returns to why
a known-dead variable is better left visible than quietly deleted.
