# Adversarial report: meta-testing the guards, and fixing the reporting bar

Two additions, both done. **Two more real bugs found — both in the guards
themselves, both of which would have silently corrupted every future result.**

---

## 1. The precision bar, encoded

```python
# the frozen reporting implementation.py
REPORTABLE_MIN_PRECISION_LIFT = 0.10   # percentage points over the chance floor
MIN_EVENTS_FOR_REPORT         = 30
```

`Finding.status()` returns one of three values by fixed rule, never by
judgement at read time:

| condition | status |
|---|---|
| `n_events < 30` | `NOT_REPORTABLE` |
| precision lift `< 0.10` | `MEASURED_NOT_ACTIONABLE` |
| fails BH or fails placebo | `MEASURED_NOT_ACTIONABLE` |
| all of the above pass | `REPORTABLE` |

Verified at the boundary:

```
lift +0.040 -> MEASURED_NOT_ACTIONABLE
lift +0.099 -> MEASURED_NOT_ACTIONABLE
lift +0.100 -> REPORTABLE          <- "at least" 10 points, so 0.100 qualifies
lift +0.101 -> REPORTABLE
huge lift but fails BH      -> MEASURED_NOT_ACTIONABLE
huge lift but fails placebo -> MEASURED_NOT_ACTIONABLE
perfect result at 6 events  -> NOT_REPORTABLE
```

A boundary bug had to be fixed: `0.50 - 0.40` is `0.09999999999999998` in
binary floating point, so an exactly-at-bar result was being rejected. Compared
with a `1e-9` tolerance now — the bar stays at 0.10 and does not turn on
representation error.

### It bites immediately

On the real BTC capture the guard stack produces cells that look spectacular:

```
  variable        bin          d    q_BH   plac   prec  chance    lift  status
  abs_ret         [-5,0)    8.62   0.000  0.000  1.000   0.315  +0.685  NOT_REPORTABLE
  vol_of_vol      [-5,0)    7.58   0.000  0.000  1.000   0.197  +0.803  NOT_REPORTABLE
  realized_vol    [-5,0)    6.48   0.000  0.000  0.750   0.183  +0.567  NOT_REPORTABLE
```

d = 8.6, q = 0.000, perfect precision, lift +0.685 — and still not reportable,
because there are 6 events and the minimum is 30. That is the bar working
before there is anything to rationalise with.

---

## 2. Meta-test: can the pipeline find a signal that IS there?

A planted feature is injected as a **time series** — elevated during real event
pre-windows, ordinary elsewhere — so placebo windows genuinely do not see it.
A per-window label would have passed the placebo test trivially.

Effect size is calibrated per trial: noise is generated, the control-window
statistic's SD is measured, and the plant amplitude is set to `target_d × SD`.
Realised d is measured and reported alongside the target.

Every planted signal is tested against the **full real variable set** for the
BH burden (72 real variable × bin tests), not on its own.

### Results, 20 trials per effect size, bin `[-5,0)`, 6 events

| target d | realised d | detect | BH | placebo | precision lift | alerts | all three |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.12 | 5% | 5% | 10% | −0.184 | 2.8 | **5%** |
| 0.3 | 0.31 | 15% | 15% | 15% | −0.199 | 4.3 | 5% |
| 0.5 | 0.41 | 20% | 15% | 15% | −0.215 | 5.5 | 10% |
| 1.0 | 1.06 | 65% | 65% | 55% | −0.168 | 10.2 | 45% |
| 2.0 | 2.04 | 95% | 95% | 95% | **+0.127** | 11.4 | **95%** |

Earliest bin `[-30,-25)`, the one the whole study is about:

| target d | realised d | detect | BH | placebo | precision lift | all three |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | −0.01 | 0% | 0% | 0% | −0.182 | 0% |
| 0.3 | 0.32 | 5% | 5% | 10% | −0.150 | 5% |
| 0.5 | 0.34 | 10% | 10% | 10% | −0.130 | 5% |
| 1.0 | 1.08 | 65% | 65% | 50% | −0.129 | 45% |
| 2.0 | 2.23 | 95% | 95% | 95% | **+0.158** | **95%** |

### SENSITIVITY FLOOR

> **At 6 events, the pipeline reliably recovers a planted effect only at
> d = 2.0.** d = 1.0 is recovered 45% of the time; d = 0.5 and d = 0.3 are
> effectively invisible. This holds at both the latest and earliest lead bin.

**This number belongs beside every null result the system produces.** A
"nothing found" from this pipeline at the current event count means "no effect
of d ≳ 2 was present" — it says almost nothing about d = 0.3–1.0.

The negative control behaves: planting nothing is detected 5% of the time at
the earliest bin's 0% and the late bin's 5%, i.e. α. The suite is quiet when
there is nothing there, and loud when there is something large.

---

## 3. Two bugs the meta-test found

Both were in the guards. Neither would have been visible from a null result.

### Bug A — a perfect signal scored precision 0.000

The planted d=2.0 signal produced a precision lift of **−0.014**: no better
than chance. Cause:

```
planted signal elevates minutes [m-30, m)
bin [-5,0) at anchor t reads [t-5, t)  ->  anchors m-25 .. m are elevated
de-clustering kept the FIRST crossing = m-25
|event - alert| = 25 min > 15 min tolerance  ->  scored as a MISS
```

A signal that leads by more than the hit tolerance could **never** register a
hit, because de-clustering always retained its earliest crossing. The precision
bar was therefore unreachable for exactly the early lead bins the study exists
to measure.

Fixed: an alert is now a *cluster*, scored over its whole span — a hit if an
event falls within tolerance of any part of it. Verified: a perfect planted
signal now scores precision 1.000, recall 1.000; one true plus one false
cluster scores 0.5.

This bug is inherited from the archive pipeline's `evaluate()`, so the archive
precision figures for early lead bins were affected by it too.

### Bug B — pure noise scored the highest precision lift of all

After fixing A, the d=0 negative control scored **+0.571**, beating the planted
d=2.0 (+0.252). Cause: thresholding noise at the event median puts ~half of all
anchors over the line, which collapses into one enormous alert cluster that
trivially contains every event. Precision ≈ 1.0 for a signal that is on
permanently.

The global chance floor assumes a *point* alert and cannot see this. Fixed by
matching the floor to the alert's actual footprint:

```
chance = n_events × (cluster_span + 2·tolerance) / total_minutes
```

Verified: a tight 25-minute alert gets floor 0.039 (lift ≈ +0.96); an always-on
alert gets floor 1.000 (lift ≈ 0). After the fix the ordering is coherent —
only d=2.0 clears the bar, and the noise control sits below chance.

Both bugs shared a shape: **the guard looked strict while being unable to
detect anything.** That is the failure mode meta-testing exists to catch, and
neither was visible from a null result.

---

## 4. Adversarial regressions (run every time)

```
constant variable -> AUC 0.500 (must be 0.500):                  PASS
zero-variance excluded from best_auc:                            PASS
random labels on pure noise detected 4.0% (expect ~5%):          PASS
precision bar: +0.05 -> MEASURED_NOT_ACTIONABLE, +0.20 -> REPORTABLE: PASS
perfect result at 6 events -> NOT_REPORTABLE:                    PASS
```

The AUC tie-handling regression from the previous round is included, so the
"column of zeros scores 1.000" bug cannot return.

---

## 5. Guard stack now wired into the pipeline

`tools/run-live-pipeline.py` runs the full chain on real data: Mann-Whitney per
variable × bin → Benjamini-Hochberg across all cells → hour-matched placebo and
precision for BH survivors → `Finding.status()`.

On BTC 2026-08-23: 72 testable cells, 64 raw p<0.05, 64 survive BH, **0
reportable** — all gated by the 6-event minimum. Several variables score
precision *below* the matched chance floor (lift −0.44), i.e. their alerts are
wider than random and genuinely worse than nothing; the metric now says so.

---

## What this changes about future reports

Every null result from this system must now be stated as:

> No effect of **d ≳ 2.0** was detected. At the current event count the
> pipeline recovers d = 1.0 only 45% of the time and d ≤ 0.5 essentially never.
> Absence of a finding is not evidence of absence below that floor.

And the floor moves as events accumulate: re-run
`tools/meta-test-guards.py` whenever the event count changes materially, and
quote the floor from that run, not this one.

---

## Analysis layer frozen

the frozen loader, the frozen analysis implementation, the frozen reporting implementation and the three tools
(`verify-loader.py`, `run-live-pipeline.py`, `meta-test-guards.py`) are final
for this phase. The recorder was frozen after Job 1. Both now run untouched
while data accumulates.

Regression suite to re-run before trusting any future result:

```
python tools/verify-loader.py    --dir ./data --date <D>
python tools/meta-test-guards.py --dir ./data --date <D> --coin BTC --bin 5
python tools/meta-test-guards.py --dir ./data --date <D> --coin BTC --bin 0
python tools/run-live-pipeline.py --dir ./data --date <D> --coin BTC
```

Still filed, still untested: whether Model B beats the volatility baseline, and
whether liquidity withdraws from or builds into the direction of travel.
