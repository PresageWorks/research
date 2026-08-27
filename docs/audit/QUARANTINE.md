# QUARANTINE — the four-day archived dataset is exploration-only, permanently

**Effective 2026-08-26. Not revocable by finding something interesting in it.**

## Repair status, 2026-08-26

The control-overlap defect described in `audit_2026-08-26.md` was repaired on
2026-08-26 (`repair_2026-08-26.md`). Control anchors must now be separated by at
least one window length, asserted in the frozen analysis implementation.

**The repaired numbers are the ones that stand.** On this dataset: BH survivors
25 -> **3 of 120**, all three in `[-5,0)`; **zero** in any early bin; both
liquidation cells fail BH (`[-15,-10)` q 0.0011 -> **0.1680**); sensitivity floor
d = 0.5 -> **d = 1.0**.

Pre-repair figures in `oneday_*.md`, `multiday_*.md`, `orderbook_*.md`,
`stats_4d_*.csv` and `targeted_4d_*.csv` were computed on overlapping controls
and are superseded. They are kept for provenance, not for citation. The repaired
table is `stats_repaired_4d_2026-08-21.csv`.

**The quarantine is unchanged by the repair.** Repairing a defect does not
un-spend the analyses already run on these events. Repaired numbers are still
exploration-only.

## What is quarantined

Everything derived from the archived pull covering **2026-08-18 → 2026-08-21**,
analysed days 2026-08-19/20/21, **57 events**, BTC perpetual:

```
results/events_4d_2026-08-21.csv          results/stats_4d_2026-08-21.csv
results/events_4d_2026-08-21_meta.json    results/targeted_4d_2026-08-21.csv
results/the derived window-variable table results/precision_4d_2026-08-21.csv
results/the derived order-book window table
results/the derived minute-bar table results/leadtime_4d_2026-08-21.csv
results/the derived participant table results/placebo_4d_2026-08-21.json
results/the derived grid array            results/summary_4d_2026-08-21.json
results/windows_4d_2026-08-21_meta.json   results/*_ob_4d_2026-08-21.*
```

The one-day artifacts (`*_2026-08-21.*` without the `4d` tag) are quarantined on
the same terms: they are a subset of the same window.

## The rule

**Nothing discovered by slicing these 57 events may ever be confirmed on these
57 events.** That covers, without limitation:

- redefining or renormalising a variable and re-testing it here
- classifying events by type and testing per class here
- changing lead-bin boundaries or widths and re-testing here
- dropping, weighting or subsetting events and re-testing here
- inspecting lead-time shapes and then testing the shape you saw

Discovery on this dataset earns exactly one thing: **the right to become a
pre-registered hypothesis, tested on live-capture data the exploration never
touched.** It earns no confirmatory status of any kind, at any effect size, with
any p-value or q-value, however the result comes out.

This is not a statement about data quality. The dataset is fine. It is a
statement about what has already been spent: these events have been looked at,
sliced, and re-tested enough times that no correction can restore a valid null
distribution over them. The multiple-comparison burden is not merely large — it
is unknown, because it includes every analysis choice made after seeing an
intermediate result.

## Why the exploration is still worth doing

An exploratory pass that cannot confirm anything can still do two useful things:
kill a lead cheaply, and sharpen a hypothesis before it is expensive to test.
Both are outcomes worth having. Finding that the `liq_count` result dissolves
under a boring explanation is a *successful* use of quarantined data, and the
cheapest possible way to avoid spending a pre-registered run on it.

## What "confirmatory" means here

A claim is confirmatory if it asserts that an effect **is real**, **is
significant**, **survives correction**, or **should be acted on**. It is
exploratory if it asserts only that something is **worth testing on fresh
data**.

Exploratory claims from this dataset are permitted and must be labelled.
Confirmatory claims from this dataset are prohibited outright.

## Enforcement

`paper/build.py --check` fails the build if a confirmatory claim in the research
note cites a quarantined artifact. The check is deliberately crude — it pairs
confirmatory vocabulary with quarantined filenames in the same sentence — and it
is a tripwire, not a proof. It cannot catch a confirmatory claim phrased
carefully enough to evade it. The rule is the control; the check is a reminder.

The pre-registered primary test in `EVALUATION_CONTRACT.md` is unaffected: it
runs on live-capture data and its trigger is ≥ 30 out-of-sample events. Nothing
in the quarantined window counts toward that threshold. The control repair does
not touch it either — the primary score is CRPS on anchors, not an
event-versus-control comparison (`repair_2026-08-26.md` §3).
