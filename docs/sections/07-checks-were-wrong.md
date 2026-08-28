## 7 — I Built the Checks. The Checks Were Wrong Too.

*The guards lied, twice, and the second time because I had just fixed the
first.*

After the AUC bug I built a meta-test suite: guards against exactly that class
of failure. Adversarial inputs — all-zero features, constant features, pure
noise, shuffled labels, rare events — which the pipeline must refuse to find
significance in.

Then I noticed the gap in it. **A guard suite that never fires is
indistinguishable from a guard suite that is broken.** A null result cannot tell
you which one you have. Every adversarial test I had written produced a null,
and I had been reading that as evidence the guards worked.

So the suite has to run in the other direction as well: plant a signal that
genuinely predicts the events by construction, at several effect sizes, and
confirm the pipeline finds it. The plant is injected as a *time series* —
elevated during real event pre-windows, ordinary elsewhere — so that placebo
windows genuinely do not see it. A per-window label would have passed the
placebo test trivially and taught nothing. Amplitude is calibrated per trial
against the measured standard deviation of the control-window statistic, and
the realised effect size is measured and reported next to the target.

Both of the following bugs were found this way. Neither was visible from a null
result, and both were in the guards rather than in the thing being guarded.

### The first failure

Planted signal at d = 2.0, as obvious as a signal gets. Precision lift:
**−0.014**.

A perfect signal scored nothing.

The cause was in the de-clustering logic. When a variable crosses its threshold
repeatedly, consecutive alerts are collapsed into one, and the implementation
kept the *first* crossing. A signal elevated across the whole 30-minute
pre-window first crosses about 25 minutes out, outside the ±15-minute hit
tolerance. The alert was therefore never scored as a hit.

![Figure 4](figures/fig4-alert-window.png)

**Figure 4** — Why the bug was invisible: the alert fires correctly, in the
right place, for the right reason, and lands outside the window in which a hit
can be recorded. Schematic; no data.

**Any signal leading by more than the hit tolerance could never register.** The
precision bar was structurally unreachable for exactly the early lead bins this
study exists to measure: the ones §4 and §5 are about.

That bug was inherited from the archive pipeline's evaluation code, which means
the early-bin precision figures in the earlier runs were affected by it too.

The fix scores an alert as a *cluster* over its whole span: a hit if an event
falls within tolerance of any part of it. Verified: a perfect planted signal
now scores precision 1.000 and recall 1.000, and one true plus one false
cluster scores 0.5.

### The second failure

Re-run. Planted d = 2.0 now scored correctly. And **pure noise scored the
highest precision lift of anything measured, +0.571**, beating the planted
perfect signal at +0.252.

The negative control came first.

Thresholding noise at the event median puts roughly half of all anchors over the
line. Under the newly-fixed cluster logic those collapse into one enormous,
permanently-on alert, which trivially contains every event. Precision looked
excellent because the alert covered most of the day.

The chance floor could not see this, because it assumed a *point* alert and
compared against the probability of a randomly-placed instant landing near an
event. The fix matches the floor to the alert's actual footprint:

```
chance = n_events × (cluster_span + 2 × tolerance) / total_minutes
```

Verified at both extremes: a tight 25-minute alert gets a floor of 0.039, and an
always-on alert gets a floor of 1.000 and a lift of approximately zero. After
the fix the ordering is coherent, only the d = 2.0 plant clears the bar, and
the noise control sits below chance.

The second bug was created by fixing the first. Cluster-span scoring is correct
and the point floor was correct for point alerts; together they were wrong. That
is not an argument against fixing things. It is an argument for re-running the
whole adversarial suite after every fix, including the parts that passed before.

Both failures share one shape: **the guard looked strict while being incapable
of measuring what it claimed to measure.**

### What the fixed suite says about sensitivity

**Table 3 — Detection rate by planted effect size, 20 trials each, 6 events**

| target d | realised d | detect | survives BH | beats placebo | precision lift | all three |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.12 | 5% | 5% | 10% | −0.184 | **5%** |
| 0.3 | 0.31 | 15% | 15% | 15% | −0.199 | 5% |
| 0.5 | 0.41 | 20% | 15% | 15% | −0.215 | 10% |
| 1.0 | 1.06 | 65% | 65% | 55% | −0.168 | 45% |
| 2.0 | 2.04 | 95% | 95% | 95% | **+0.127** | **95%** |

Bin `[-5,0)`. The `all three` column requires detection, BH survival and placebo
separation simultaneously, which is the bar a real finding has to clear. The
d = 0.0 row is the negative control, and 5% is α; the suite is quiet when there
is nothing there.

The earliest bin, the one the whole study is about, behaves the same way. On
the same `all three` basis: d = 2.0 clears 95% of the time, d = 1.0 at 45%,
d = 0.5 at 5%, and the d = 0.0 negative control at 0%.

> **At 6 events the pipeline reliably recovers a planted effect only at
> d = 2.0.** d = 1.0 is recovered 45% of the time; d = 0.5 and below are
> effectively invisible.

Which means every null result this system produces has to be read as: *no effect
of d ≳ 2.0 was detected.* It says almost nothing about d = 0.3–1.0. That is a
much weaker statement than "we found nothing", and it is the honest one.

This is also why the bar is encoded rather than applied by judgement at read
time. On the real BTC capture the guard stack produces cells that look
spectacular — `abs_ret` at `[-5,0)` scoring d = 8.62, q = 0.000, placebo 0.000,
precision 1.000, lift +0.685 — and returns `NOT_REPORTABLE` for all of them,
because there are six events and the minimum is thirty. Across that run: 72
testable cells, 64 raw p < 0.05, 64 surviving BH, **0 reportable**. Several
variables score precision *below* the matched chance floor, down to a lift of
−0.44, meaning their alerts are wider than random and genuinely worse than
nothing. The metric now says so.

The floor moves as events accumulate. It has to be re-measured at each run's
actual sample size and quoted from that run, not carried forward from this one.

**And it moves when a defect is repaired.** Re-measured on the 57-event archive
after the control-overlap repair, with the same planted-signal method:

| controls | sensitivity floor |
|---|---|
| 744 overlapping (before) | d = 0.5 |
| 39 non-overlapping (after) | **d = 1.0** |

The floor doubled. Nothing about the market changed; the earlier figure counted
each control window about 23 times. Every null this study reported must be read
against **d ≈ 1.0**, not against the more flattering number the inflated control
count implied.
