# Provenance

## Private production repository

    commit 2e80b6b46872759a6e17799cd1bb56033098bd52

This hash identifies the private source state associated with this publication.

**It does not expose, disclose, or authenticate the contents of that repository
by itself.** A SHA-1 commit identifier is a name, not a disclosure: it reveals
nothing about the code, data, or configuration it names. Anyone holding an
authorised copy of that repository can confirm correspondence; nobody can
derive its contents from this value. Publishing it fixes *which* private state
produced this record, so that a later claim of "that is not what we ran" is
checkable by anyone with access.

## Contract digests

Computed at ratification, over the complete unredacted documents, before any
evaluation data existed.

| document | sha256 | bytes | date |
|---|---|---:|---|
| Evaluation contract v2 | `937ce309d5c01f1f135a63dffa60507f3a4d9606cdffc9afdda32aa9411b4161` | 40,343 | ratified 2026-08-24, amended 2026-08-26 |
| Evaluation contract v1 | `505b12d0999665230127fcc630aeabe40a83aefdb78f07359a1ecd176c291869` | 31,178 | ratified 2026-08-24 |

The public redacted editions in `docs/contract/` carry their own, necessarily
different, digests. All four are listed in `docs/contract/HASHES.txt`.

## Scope of what these hashes prove

They prove that the documents they name have not changed since they were
recorded. They do **not** prove that the analysis was correct, that the
pipeline was free of defects, or that any published claim is true. The research
note is explicit that several results in this project looked correct and were
not. Tamper-evidence is a property of the record, not a warranty on the work.
