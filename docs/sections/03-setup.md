## 3 — Setup

Everything in the sections that follow refers back to this one.

### Data

Archived fills and 1-second candles for the BTC perpetual on Hyperliquid,
retrieved from a public requester-pays S3 archive. Four consecutive days,
**2026-08-18 → 2026-08-21**. Only three are analysed: the first supplies the
trailing lookback and is never itself tested. Live capture at higher resolution
runs separately and is not used in this note.

Four-day archive volume: **2,252,025,001 bytes**, verified byte-exact against
local files after download.

One schema fact changed every number in the study. **Each trade appears twice,
once per counterparty.** All 6,454,874 `trade_id`s have exactly two rows, with
opposite `side`, opposite `crossed`, and identical price and size. The
aggressor is the `crossed = true` row, confirmed through fees: mean fee 0.8954
for `crossed = true` against 0.0071 for `crossed = false`, with maker fees going
negative to a minimum of −183.88. Every figure in this note uses taker rows
only. Had that gone unread, volume would have doubled and buy/sell aggressor
imbalance would have been identically zero, `side` splits exactly 50/50 across
the raw file precisely because both sides are present.

### Events

An event is a price move large enough to be worth predicting, defined
mechanically so the same rule produces the same list on every run:

| step | rule |
|---|---|
| bars | 1-second candles rolled up to 1-minute |
| σ | rolling stdev of 1-minute log returns, trailing 360 minutes |
| event | absolute log return over any 5-minute window exceeding 4σ |
| de-duplication | keep the largest move in any 30-minute cluster |

**Events across the three analysed days: 57**, distributed 20 / 20 / 17 by day.

The event list is written to disk *before any variable is computed*. This
ordering is not cosmetic. If events are labelled after the variables are in
hand, threshold choices can drift toward whatever produces a result, and
nothing in the output would reveal it. Freezing the list first makes that drift
visible if it happens.

One spec observation, recorded at the time and not adjusted: the rule compares
a *5-minute* return against 4× the standard deviation of *1-minute* returns.
Under a random walk a 5-minute return has standard deviation ≈ √5 × σ₁ₘ, so
4 × σ₁ₘ is ≈ 1.8σ in 5-minute terms: a considerably looser bar than "4 sigma"
sounds. It was implemented exactly as specified. Noting it as an observation
about the specification, not as a change to it.

### Controls

For each event at time T, the pre-window runs from T−30min to T, divided into
six 5-minute lead bins.

**Control construction** is where most of the difficulty in this design lives,
and it is worth being explicit about, because §5 is entirely about getting it
wrong. A control window is a stretch of ordinary market that the event windows
are compared against. Choosing them badly does not add noise: noise would wash
out across 57 events. It introduces a systematic difference with a consistent
sign, which survives every statistical correction you can apply, because the
difference is real. It just isn't the difference you're claiming to measure.

The rules: 30-minute windows with no event in the following 60 minutes, no
overlap with any event pre-window, at least 20 drawn per event, restricted to
the region where the detector is live, and **matched on hour of day**. The
three-day run uses **744** such controls.

![Figure 1](figures/fig1-lead-bins.png)

**Figure 1** — Event, lead bins, and control construction. Schematic; no data.

### Statistical apparatus

Each of these is present for a specific reason.

**Benjamini-Hochberg correction.** The study runs 120 tests (20 variables
across 6 lead bins), so roughly 6 will clear p < 0.05 by chance alone. BH
adjusts the threshold for how many tests were run, and is reported as q. It is
worth being clear about what BH does *not* do: it controls false discoveries
arising from noise. It does nothing whatever about a confound that shifts many
variables in the same direction at once. Section 5 is a case where 63 of 120
tests survived BH and the correction was working perfectly: it was answering a
question about noise, and the problem was not noise.

**Placebo events.** The entire analysis re-run against deliberately fake events
that contain no information about price by construction, drawn at the same
hours as the real ones. A genuine event-linked signal should separate itself
from that null. One that doesn't is indistinguishable from the analysis finding
structure in the background.

**Power.** The probability that a test detects an effect of a given size, given
the sample. It is the reason a null result is not automatically informative: a
study with low power fails to find things that are there. Every null in this
note is quoted against the effect size the design could actually have caught.

**Sensitivity floor.** The smallest effect the pipeline reliably recovers at the
current sample size, measured by planting known signals rather than assumed
from a formula. Section 7 covers how this is measured, and why the number came
out worse than the formula suggested.

**Coverage-matched precision floor.** For any variable proposed as an alert:
how often it fires, against how often events occur, compared against a random
alert *covering the same fraction of time*. A global chance floor is not
sufficient. Section 7 shows what happens when you use one.

**Out-of-sample scoring.** Models compared on data they were not fitted to.
Appendix A shows, on synthetic inputs, that this is not a refinement but the
entire difference between a measure that works and one that reports improvement
on pure noise.

Cohen's d and q appear throughout without further gloss.
