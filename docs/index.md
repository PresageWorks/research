---
title: PRESAGE — public research record
---

# PRESAGE — public research record

The public research and methodology record for PRESAGE. It exists so our
published claims can be audited from outside the company.

## Read

- **[The research note](research-note.md)** — *I Built the Checks. The Checks
  Were Wrong Too.* Five occasions on which this project produced a
  convincing-looking answer that was wrong, including the case where the
  checks built to catch the first three had the same defect.

## The pre-registration

- [Evaluation contract v2](contract/EVALUATION_CONTRACT.public.md) (public redacted edition)
- [Evaluation contract v1](contract/EVALUATION_CONTRACT.v1.public.md)
- [Amendment record](contract/AMENDMENT_2026-08-26.md)
- [Cryptographic hashes](contract/HASHES.txt) · [what was redacted, and what that costs](contract/REDACTION_NOTE.md)

## Audit trail

- [Audit record](audit/AUDIT.md) — corrections made to the note, and how each was caught
- [Quarantine record](audit/QUARANTINE.md) — why the four-day dataset is exploration-only, permanently
- [Adversarial meta-test](audit/adversarial_meta_test_2026-08-23.md)
- [Repair record](audit/repair_2026-08-26.md)

## Verification tooling

Synthetic and self-contained; none of it requires private data.

- `verification/verify_public_record.py`
- `verification/meta_test_synthetic.py`
- `verification/placebo_edge_synthetic.py`

## Standing caveat

The primary pre-registered test **has not been run**. Any market result here is
either exploratory, from a permanently quarantined dataset, or a demonstration
on synthetic inputs.
