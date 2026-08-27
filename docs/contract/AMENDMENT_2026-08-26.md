# Amendment — 2026-08-26 — clarification only

**v1 is preserved at `EVALUATION_CONTRACT.v1.md`, its hash at
`CONTRACT_HASH.v1.txt`. Neither is overwritten or deleted.**

| version | sha256 | bytes |
|---|---|---:|
| v1 | `505b12d0999665230127fcc630aeabe40a83aefdb78f07359a1ecd176c291869` | 31,178 |
| **v2** | `937ce309d5c01f1f135a63dffa60507f3a4d9606cdffc9afdda32aa9411b4161` | 40,343 |

## The clause that governs this amendment

> **The amendment adds executable definitions only. It alters no threshold, no
> score, and no outcome criterion.**

Two clauses of v1 pointed at procedures that were never defined. Neither could
be executed as written. §1.11 and §1.12 supply the definitions.

**Diff: 182 lines added, 1 line replaced.** The replaced line is the status
header, which now records the amendment and carries no methodological content.
Every other v1 line survives byte-identical into v2. The `SURVIVES` and
`SUSPICIOUS` blocks are byte-identical, verified programmatically.

An earlier draft of this record claimed the diff was "purely additive". It is
not, by one line, and the claim is corrected here rather than left to stand.

**Constraint honoured: no live-capture data was read during this work.** The
placebo was validated on synthetic data; the tolerance rule was demonstrated
against the archive. Resolving these ambiguities now is only meaningful because
the answer is not yet visible, and touching live data would have made the choice
informed by the result in exactly the way this contract exists to prevent.

---

## Ambiguity 1 — SURVIVES criterion 4

### The exact ambiguous text (v1 §3)

> 4. **Beats placebo** — hour-matched placebo p < 0.05.

### Why it could not be executed as written

The criterion is defined over **events**. The primary quantity is defined over
**anchors** (v1 §1.7):

> ```
> EDGE = mean_over_test_anchors[ CRPS_A(t) − CRPS_B(t) ]
> ```

There are no events in EDGE. "Hour-matched placebo" describes drawing fake
events at the same hours as the real ones — the archive's event-versus-control
procedure. v1 does not say how that applies to a mean over every test anchor,
and no reading of the text resolves it.

### The question the criterion exists to answer

Could the measured skill have been produced by the shared temporal structure of
the inputs and the target — time of day, volatility clustering — rather than by
event-linked information in the PRESAGE internals?

### What was added

§1.11, defining the **day-shift placebo**: for every whole-day shift `k` in
`1 … D−1`, circularly shift Model B's extra features by `k × 1440` minutes,
re-standardise on TRAIN, refit both models, recompute EDGE. The p-value is the
standard permutation form `(1 + #{null ≥ real}) / (1 + (D−1))`.

A whole-day shift preserves hour-of-day exactly — the literal analogue of
"hour-matched" — and moving the block as one piece preserves autocorrelation,
destroying only the alignment that the criterion tests.

### Validation — synthetic only

| check | rejection rate | nominal |
|---|---:|---:|
| strict null — extras carry no information | **0.000** | 0.05 |
| confounded null — extras share seasonality, no event link | **0.033** | 0.05 |
| prohibited permutation variant, strict null | 0.367 | 0.05 |
| prohibited permutation variant, confounded null | 0.100 | 0.05 |

| planted signal β | mean EDGE | pass rate |
|---:|---:|---:|
| 0.02 | +0.00006 | 0.15 |
| 0.05 | +0.00044 | 0.45 |
| 0.10 | +0.00175 | 0.80 |
| 0.20 | +0.00703 | 1.00 |

Smallest signal caught in ≥80% of trials: **β = 0.10**.

The confounded null is the one that matters. There the extras genuinely predict
the target's scale through shared seasonality, and the placebo correctly
declines to call that event-linked skill — which is precisely what criterion 4
was written to do.

### Three defects found while validating, before anything was locked

Each was caught by the validation and each would have produced a wrong answer.

1. **Numerically broken harness.** The synthetic world's AR(1) was
   unnormalised, so at a 21-day window the volatility process spanned
   `exp(±4)`, the location-scale fit stopped converging, and EDGE came out as
   exactly `0.000` for the real configuration and every placebo draw alike. An
   entire earlier set of numbers was produced by this and discarded.
2. **Non-exchangeable standardisation.** The real feature block was
   standardised on TRAIN and the placebo was shifted *after* standardisation,
   so the placebo's TRAIN block did not have mean 0 and sd 1 while the real
   one did. The placebo was handicapped and the real model flattered.
3. **Missing permutation correction.** Shifts were sampled with replacement and
   the p-value omitted the standard `+1` in both terms. With `D−1` distinct
   shifts the test's true size was roughly `2/(D+1)`, not 0.05; measured at
   **0.167** against a nominal 0.05 before the fix.

### Fallback path

Defined in §1.11.1, and labelled there with when it was decided: **after** the
day-shift numbers were visible. It is not a blind pre-commitment for this
decision and does not claim to be. It binds any future re-validation.

Day-shift passed, so the fallback is not exercised. Order of resort: day-shift,
then stationary block permutation at the §2.5 block length (weaker, because it
breaks seasonality as well as alignment, and admissible only after passing the
same four conditions), then **declare criterion 4 unimplementable and escalate**
rather than lock a weaker method.

### The resolution requirement this surfaced

The smallest attainable p-value is `1/D`. **A capture window shorter than 21
whole days cannot produce `p < 0.05` for any result, however strong.**

This interacts with the run trigger and is reported rather than acted on: at the
live event rate observed so far, 75 events accumulate in roughly 12.5 days,
which would **not** be enough days for criterion 4 to be evaluable. §1.10's
event-count trigger is unchanged, and no new outcome condition was added; the
resolution limit is a property of the definition and is recorded as such.

### What was deliberately NOT changed

- The threshold stays `p < 0.05`, exactly as v1 states it.
- Criterion 4's text in §3 is untouched. §1.11 supplies what it refers to.
- No other SURVIVES criterion was examined or altered.
- EDGE (§1.7) is unchanged.
- The block-bootstrap CI (§2.5) is unchanged; §1.11 governs the placebo only.
- The §1.10 event trigger is unchanged, despite the resolution finding.

---

## Ambiguity 2 — "declared tolerance"

### The exact ambiguous text (v1 §3, SUSPICIOUS)

> - control matching quality is outside its **declared tolerance**;

### Why it could not be executed as written

**v1 declares no tolerance anywhere.** The phrase has no referent in the
document.

What the code assumed instead: the frozen analysis implementation carries
`max_hour_tol=12`. On a 24-hour circle 12 is the maximum possible distance, so
the pipeline widened the hour match without limit until it found enough
controls. The effective tolerance was unbounded — the SUSPICIOUS condition could
never fire, however badly matched a run was.

### What was added

§1.12, declaring the tolerance on **covariate balance** rather than on hours:
absolute standardised mean difference ≤ **0.25** on log notional traded, log
trade count and realised volatility, each over the window immediately preceding
the anchor.

0.25 is the conventional adequate-balance threshold in the matching literature
(≤0.10 good, ≤0.25 acceptable), used because it is an external standard that
predates this project.

### The justification stands independently of the archive

No value was chosen by checking what the data would pass. The archive **fails**
this rule in both configurations — standardised mean differences of **0.54**
before the control repair and **0.51** after, against the 0.25 bound.

That the archive fails it is the evidence the rule has content. A tolerance the
existing data passed trivially would not be a tolerance.

### What was deliberately NOT changed

- The SUSPICIOUS criterion's text is untouched.
- `max_hour_tol` and `min_controls` were **not** retuned. The amendment declares
  what "in tolerance" means; it does not adjust the matcher.
- Hour offset is reported under §2.11, not bounded.

---

## Kept prominent — code-versus-methodology drift

**`min_controls=20` is a Python default, not a contract requirement.**

It lives in the frozen analysis implementation. It appears nowhere in v1 — no control
count, no per-event minimum, no matching tolerance. The only `20` in v1 sits
inside a lead-bin label.

`repair_2026-08-26.md` §3 twice asserted otherwise: it described "the contract's
20-per-event requirement", and stated that relaxing `min_controls` "Requires a
contract amendment and a new hash". **Both statements were wrong.** Relaxing it
requires no amendment at all — which is exactly what makes it dangerous. A
parameter with methodological force is changeable without any of the ceremony
that governs the contract.

**This is the first documented instance of code-versus-methodology drift in this
project, and it is its own failure class.** A number that behaves like
methodology while living in a function signature is not covered by a hashed
pre-registration, does not appear in any diff of the contract, and can be
altered by someone who believes they are only adjusting a default.

It is worth separating from the earlier failures. The `liq_count`-scores-1.000
bug and the control-overlap defect were errors *in* code — the code did
something other than what was intended. This one is different: the code is
correct and does exactly what it says. The failure is that what it says was
never written down where the methodology lives, so the contract could be
audited, hashed and frozen while a load-bearing methodological choice sat
entirely outside it.

No fix is proposed here. Recording it is the deliverable.

---

## Frozen

v2 is frozen. No further changes on account of how the archive looks — it has
done its job.
