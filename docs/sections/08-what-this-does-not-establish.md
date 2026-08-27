## 9 — What this does not establish

The core hypothesis is untested. Nothing here demonstrates that market
internals predict price moves in advance, and nothing here demonstrates that
they don't.

**Sample.** Four days of archived data, three analysed, 57 events, one asset,
one venue. The sensitivity analysis in §7 puts hard bounds on what could have
been detected at that size, and those bounds are low.

**Confounded correction.** In §4, two things changed between the original result
and its refutation: the wallet definition and the control matching. Their
contributions cannot be separated from what was run. The refutation stands —
d = −0.04 where d = +1.85 was claimed, at power sufficient to have caught it —
but the attribution does not.

**Mechanism versus precursor — superseded by the control-overlap repair.**

The strongest surviving pre-move signal was liquidation build-up. It no longer
survives. On 2026-08-26 an audit found that control anchors were selected one
minute apart, so 744 "independent" control windows described 32 non-overlapping
30-minute spans. Every statistic weighted by the control count was inflated.
After repair (`results/repair_2026-08-26.md`):

| `liq_count` | before repair | **after repair** |
|---|---|---|
| controls | 744 overlapping | **39 non-overlapping** |
| `[-20,-15)` | d = 0.692, q = 0.0352 | **d = 0.218, q = 0.3199** |
| `[-15,-10)` | d = 1.073, q = 0.0011 | **d = 0.363, q = 0.1680** |
| BH survivors, all 120 tests | 25 | **3 / 120** |
| BH survivors in any early bin | 10 | **0** |

**Neither liquidation cell survives Benjamini-Hochberg after the repair.** The
only three cells that survive anywhere in the table sit in `[-5,0)`, the bin
adjacent to the move. The strict-subset figure of d = 1.15 quoted in earlier
drafts was computed on the same overlapping controls and is superseded twice
over — once by the exploration, which showed the elevation was pooled-SD
arithmetic, and again by the repair.

A liquidation cascade may in any case *be* the move rather than precede it, and
this design cannot distinguish those readings. That caveat now applies to a cell
that no longer clears the bar.

**Coverage, not nulls.** The archived order book runs 20 levels per side, and
20 levels reach a median of **0.029% from mid** — about $19 on a ~$70k book. The
liquidity bands the hypothesis is actually about are 0.10%, 0.25% and 0.50%,
which are wider than the entire recorded book: **in 0 of 5,739 snapshots** does
it reach even the tightest of them. All three bands equal total depth exactly.
That is not evidence against the liquidity hypothesis. It is a dataset that
cannot address it, and reporting it as a null would have been a fifth
manufactured result — the most tempting of the five, because a null is
publishable and "we cannot see the thing" is not.

The order-book run has a second structural limit worth stating alongside the
first: at 1-minute cadence a 5-minute lead bin contains five observations, and
every change variable is a single last-minus-first difference across roughly
four minutes. A liquidity pull that happens and reverses inside a minute is
invisible. Neither limit is fixable with more days. They are properties of the
dataset, which is why the live recorder captures at a finer cadence instead.

**Reading the nulls correctly.** Every null in this note means "no effect larger
than the measured sensitivity floor was detected". At these sample sizes that
floor is d ≈ 2.0, which is very high — high enough that the phrase "we found
nothing" would be actively misleading without it attached.
