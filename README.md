# PRESAGE — public research record

This repository is the **public research and methodology record** for PRESAGE.
It exists so that the claims we publish can be audited by someone outside the
company. It is not the system that produces the product.

## The separation

There are two repositories.

| | public research record (this repo) | private production system |
|---|---|---|
| **contains** | the research note, its figures, the evaluation contract (redacted), audit records, and synthetic verification tooling | capture recorder, analysis pipeline, live pipeline, forecasting prototype, raw and captured data, feature engineering, model and deployment code |
| **purpose** | let a reader check what we claimed, how we tested it, and what we got wrong | build and operate the product |
| **visibility** | public | private, and remains private |

**The published principle: methodology and verification machinery are public;
edge and implementation are not.** A reader should be able to audit our claims
without being handed the system that generates them.

## What is deliberately not here

No capture recorder, analysis pipeline, live pipeline or prototype source. No
raw or captured market data. No derived feature matrices. No capture
configuration, infrastructure, scheduling or operational tooling. No individual
feature names. No credentials, endpoints, hostnames, or local paths.

Some of these omissions have a cost, and the cost is stated where it applies —
see `docs/contract/REDACTION_NOTE.md` for what redacting the feature list does
and does not preserve, and the note in `docs/verification/` for why the
production checker is not shipped here.

## Contents

    docs/
      research-note.md            the note, assembled from docs/sections/
      sections/                   the note's source, one file per section
      figures/                    publication figures (PNG for web, PDF for print)
      contract/                   evaluation contract v1 and v2, redacted, plus hashes
      audit/                      audit, quarantine, repair and adversarial-test records
      verification/               synthetic verification tooling (see below)
    PROVENANCE.md                 private-repo commit id and contract digests

## The research note in one paragraph

The note is titled *I Built the Checks. The Checks Were Wrong Too.* It reports
five occasions on which this project produced a convincing-looking answer that
was wrong — including the case where the validation machinery built to catch
the first three failures had the same defect. **The primary pre-registered test
has not been run.** It requires more data than currently exists. Anything in
this repository that looks like a market result is either an exploratory result
from a permanently quarantined dataset, or a demonstration on synthetic inputs.

## Verification tooling

Three scripts, all self-contained, none requiring private data:

- `verify_public_record.py` — checks this repository's integrity: contract
  digests, that the note matches its sections, figures, citation hygiene, and a
  disclosure regression test that fails if a private token ever appears here.
- `meta_test_synthetic.py` — demonstrates the guard meta-testing method
  (positive and negative controls, sensitivity floor) on synthetic data.
- `placebo_edge_synthetic.py` — the placebo design for the contract's primary
  skill metric, on synthetic data.

The production checker that re-derives every number in the note from the
analysis artifacts is **not** published, because it cannot run without those
artifacts and publishing them would disclose the exploratory feature set.
Shipping a checker that cannot execute would reproduce the exact failure the
note's section 7 is about.

## Status

The record is complete for what it claims. The headline question — whether
market-internal information adds predictive value at 5–30 minute horizons — is
**unanswered**, by design, until the pre-registered event threshold is reached.
