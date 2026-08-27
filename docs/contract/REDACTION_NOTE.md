# Redaction note — public contract editions

## What these files are

`EVALUATION_CONTRACT.public.md` and `EVALUATION_CONTRACT.v1.public.md` are
**redacted public editions** of PRESAGE's precommitted real-data evaluation
contract. They are not the ratified files.

## Exactly what was removed

Three things, in sections 1.4 and 1.5:

1. **The five individual baseline (Model A) feature names.**
2. **The individual feature names in the nine Model B families.**
3. **The per-family feature counts.**

The counts were withheld on a second review. A count is itself a disclosure:
one family's size revealed how much of a particular data source was actually
locked into the model, and another's implied the internal structure of a
decomposition. Publishing the shape of the table would have leaked what
withholding the names was meant to protect.

Internal module names were replaced with neutral descriptions, and the
project's former working name was replaced with the product name. Nothing else.
The following are reproduced **unchanged**:

- the nine family names, the total feature count, and the baseline count
- the nesting design (Model B ⊇ Model A) and the reason for it
- the locked model class and its full mathematical specification
- every threshold, significance level, correction procedure and tolerance
- every outcome state and the criteria for each
- the placebo design, the coverage requirements, and the event-count trigger
- the amendment record and the ratification history

## Why

The feature names are the engineering PRESAGE sells. The contract exists to fix
the *rules of the test* in advance so the result cannot be steered after the
fact; that purpose is served by the families, the counts, and the thresholds.
Publishing the exact column names would disclose proprietary feature
engineering without making the pre-registration any more binding on us.

## What this costs a reader, stated plainly

**A reader can verify:** that a fixed number of features in a fixed set of
named families was committed to in advance, and that every threshold and
decision rule predates the data.

**A reader cannot verify from these files alone:** which specific features were
pre-registered, how many sat in any one family, or whether a feature was later
substituted for another within the same family. Withholding the counts also
means movement of a feature between families is not publicly detectable.

That is a real limitation and we state it rather than gloss it. It is the
deliberate price of not publishing the engineering.

## How the gap is closed

The **ratified, unredacted documents are retained privately**, and their
sha256 digests are published in `HASHES.txt`. Those digests were computed at
ratification, before any data existed. An authorised auditor given a copy can
confirm it hashes to the published value, and can then check the full feature
table against the report. The commitment is therefore binding even though the
content is not public: we cannot alter the feature list after the fact without
breaking a digest published in advance.

## On the differing digests

The public editions hash to different values than the ratified documents. That
is arithmetic, not tampering — a redacted file is a different file. Both sets of
digests are published in `HASHES.txt` and clearly labelled. Do not expect the
public editions to reproduce the ratified digests; they cannot, by construction.
