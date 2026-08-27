# Internal audit notes — research note

Not part of the built note. `build.py` only concatenates files matching `NN-`,
so this file is excluded by construction.

**Standing rule: the artifact wins over the prose.** Where a run report's
summary sentence and the recorded evidence disagree, the evidence is
authoritative and the sentence is corrected. This applies to the run reports in
`results/` as much as to drafts of this note — those reports are prose too, and
two of the entries below are cases where a report's own summary was incomplete.

---

## A1 — `−0.643` attributed to the wrong file

**Status: corrected. Caught by the automated traceability check, on a real slip.**

The note stated the one-day correlation between `new_wallet_frac` and
minute-of-day as **r = −0.643**, and traced it to
`results/oneday_2026-08-21.md`.

The number is correct. The attribution was not. The one-day report states the
figure twice and rounds it both times:

- line 64: *"correlation −0.64 with minute-of-day"*
- line 490: *"Correlation with minute-of-day over the live region: **−0.64**"*

The three-decimal figure appears in the *three-day* report's comparison table
(`multiday_2026-08-19_to_2026-08-21.md`, line 52: `| one-day run | −0.643 | — |`).

This matters more than the two decimal places suggest. The traceability check in
`build.py` requires every headline number to appear **verbatim** in a named
artifact, and it failed on exactly this: `0.643` was not findable in the file
the note pointed at. Had the check been written to re-derive the value, or to
search all artifacts rather than the named one, it would have passed and the
mis-attribution would have shipped.

**This was not a planted test case.** It was a genuine slip made while drafting,
found by the checker on its first full run. That is the strongest available
evidence the checker does something — an assertion suite that has never caught a
real error is in exactly the position §7 of the note describes: indistinguishable
from one that cannot fire.

The note now states the rounding difference explicitly rather than silently
quoting the more precise figure.

---

## A2 — Liquidation lead bins: report prose vs CSVs

**Status: corrected. The CSVs are authoritative. This is the most consequential
correction in the set.**

Getting lead time wrong on the one surviving positive result, in a note about
lead time, is the worst available error here, so both cells were checked against
two independent artifacts.

`multiday_2026-08-19_to_2026-08-21.md` summarises:

> *"`liq_count` / `liq_vol` are the only variables with genuine separation before
> the final ten minutes: d = 0.78 at `[-20,-15)` (q = 0.035), d = 1.15 at
> `[-15,-10)` (q = 0.001, placebo p = 0.001)."*

What the artifacts actually carry:

| source | cell | d | q | placebo p |
|---|---|---:|---:|---:|
| `stats_4d_2026-08-21.csv` (57 events) | `[-20,-15)` | 0.69 | 0.0352 | — |
| `stats_4d_2026-08-21.csv` (57 events) | `[-15,-10)` | 1.07 | 0.0011 | — |
| `targeted_4d_2026-08-21.csv` (strict subset) | `[-20,-15)` | 0.78 | 0.0352 | **0.054** |
| `targeted_4d_2026-08-21.csv` (strict subset) | `[-15,-10)` | 1.15 | 0.0011 | **0.0005** |

Three separate problems with the summary sentence:

1. **It mixes two samples without saying so.** The d values quoted (0.78, 1.15)
   are from the strict hour-matched placebo subset. The full-sample values are
   0.69 and 1.07. Both are correct for what they measure; quoting one without
   naming the sample is not.
2. **It omits the placebo p for `[-20,-15)`, which is 0.054 — a failure.** That
   cell survives BH and then does not beat its hour-matched placebo. The
   sentence quotes a placebo p for the second cell only, which reads as though
   both cleared.
3. **`placebo p = 0.001` for `[-15,-10)` is `0.0005` in the file.** Rounding up
   at three decimals, so directionally harmless, but the file is more precise.

The corrected §8 reports both samples in a table, states which is which, and
says plainly that only `[-15,-10)` clears both bars. `liq_vol` has no
strict-placebo cell in `targeted_4d_2026-08-21.csv` at all — that file covers
six variables — so no placebo claim is made for it in either direction.

Lead-bin conclusion, authoritative: **the surviving liquidation cell is
`[-15,-10)`, i.e. 10–15 minutes of lead, not 15–20.**

---

## A3 — Model B edge range: earlier figure superseded

**Status: corrected. Later artifact wins.**

Two artifacts report the Model A vs Model B best-variable edge on the same BTC
capture, and they disagree at the last bin:

| artifact | `[-30,-25)` | `[-5,0)` | range |
|---|---:|---:|---|
| `coverage_and_live_pipeline_2026-08-23.md` (earlier) | +0.0011 | −0.0786 | −0.079 … +0.010 |
| `live_pipeline_BTC_2026-08-23.json` (later) | +0.0032 | **−0.1093** | **−0.109 … +0.010** |

**The JSON supersedes the markdown.** It is the machine-written output of the
run; the markdown table is a hand-transcribed snapshot taken during an earlier
pass of the same work. The note quotes **−0.109 to +0.010** and `build.py`
re-derives that range from the JSON on every check rather than matching a string.

The earlier **−0.0786** should not be cited anywhere. It is recorded here so that
a reader who finds it in the coverage report knows it is stale rather than
contradictory.

---

## A4 — "Controls sat between 15:00 and 20:00"

**Status: removed. Not present in any artifact.**

The phrasing appeared in an early draft. No artifact supports it, and it implies
a contiguous block, which is the wrong picture: the controls are scattered.
`oneday_2026-08-21.md` supports only:

> *"controls concentrated at 10, 14, 15, 17, 19, 20 with mean 16.7"*

The note now uses exactly that. The distinction is not cosmetic — a contiguous
afternoon block and a scattered set with an afternoon mean imply different things
about why same-hour matching failed.

---

## A5 — Test decomposition

**Status: corrected.**

An early draft factorised the 120 tests as *10 variables × 6 bins × direction*.
The correct factorisation is **20 variables × 6 lead bins**, which is what
`stats_2026-08-21.csv` and `stats_4d_2026-08-21.csv` contain (120 rows each, 20
distinct variable names). Same total, wrong structure. There is no direction
term in the test count.

---

## A6 — Section 8 moved to Appendix A

**Status: moved. Contract language is broader than the earlier reading.**

The measure-validation section cites `prototype/edge_semantics.py`. The question
was whether the evaluation contract permits that in this note. The relevant
clause, `EVALUATION_CONTRACT.md` §0.1, verbatim — first sentence and last
sentence:

> **"Nothing in `prototype/` is evidence about real markets."**

> **"The prototype is frozen as of this document. No result in it may be cited
> in any real-data report, in any direction, including as a sanity check."**

The earlier call rested on the first sentence, which is narrow — it prohibits
using prototype output as evidence *about markets*, and a demonstration about
the behaviour of a scoring rule is not that.

**That reading does not survive the last sentence.** It is broader in three
ways, each independently decisive:

- the object is *any result*, not any market claim;
- the scope is *any real-data report*, and the body of this note is one;
- *"in any direction, including as a sanity check"* closes precisely the
  exemption the earlier call relied on. A methodological sanity check is the
  named example of a thing that is still prohibited.

The contract is hashed and cannot be amended without a new pre-registration, so
the section moves rather than the rule bending. Appendix A now carries an
explicit classification: no market-data result, synthetic inputs only, exists to
validate a measurement method.

Consequential renumbering: former §9 → §8, former §10 → §9, former §8 →
Appendix A. Cross-references in §1, §3 and §9 updated. The §1 failure table
lists the fifth failure under `A` rather than `8`.

---

## A7 — 14 of 24 hours: new derivation, not a quotation

**Status: retained, labelled.**

No run report states it. It is derived in this note from
the derived window-variable table by counting distinct populated hours among
the 744 control windows, and `figures/make_figures.py` computes it at render
time rather than hard-coding it — the figure subtitle prints whatever the
parquet currently says.

It is labelled in §5 as new to this note. Worth keeping because it measures the
constraint on the *corrected* three-day run: hour-matching improved enough to be
usable, and the underlying scarcity did not go away.

---

## A8 — `new_wallet_frac` d column: sample mixing, second instance

**Status: corrected. Found while regenerating Figure 2 from artifacts.**

Rebuilding Figure 2 by parsing `stats_4d_2026-08-21.csv` instead of using
transcribed constants produced a series that disagreed with Table 1 in §4.
Tracing every cell to its source:

| lead bin | report / old Table 1 | `stats_4d` (57 ev) | `targeted_4d` (strict 48) | report took |
|---|---:|---:|---:|---|
| `[-30,-25)` | −0.04 | −0.05 | −0.04 | targeted |
| `[-25,-20)` | +0.23 | +0.24 | +0.23 | targeted |
| `[-20,-15)` | +0.20 | +0.19 | +0.20 | stats |
| `[-15,-10)` | −0.02 | −0.02 | −0.02 | either |
| `[-10,-5)` | +0.03 | +0.03 | +0.06 | stats |
| `[-5,0)` | **−0.20** | **−0.12** | **−0.20** | targeted |

**This is the A2 defect again, and worse.** A2 mixed two samples across two
cells. Here the mixture alternates *row by row inside one table*, under a
heading that states "57 events, 744 hour-matched controls". Three rows are not
that sample. The `[-5,0)` cell is the decisive one: −0.20 against −0.12 is not
a rounding difference.

Every other column — event mean, control mean, ratio, q, placebo p — reconciles
with the artifacts exactly. Only `d` was mixed.

Table 1 is rebuilt from `stats_4d` for all six rows, with the placebo column
explicitly labelled as the strict subset, since a placebo can only be built on
that sample.

**Two checks added**, because this class of error has now occurred twice:

- Table 1's `d` column must match `stats_4d` for every bin, and the table must
  name both sources.
- The figure generator must contain no transcribed series (`D_ONEDAY`,
  `D_MULTIDAY`, `CRPS_EDGE = [`) and must call its parsers at render time.

The old generator's approach — hold constants, then assert they appear
somewhere in a report — was not provenance. It passed while the plot and the
artifact diverged, because a substring check cannot see which of two files the
number came from.

---

## A9 — §2 citations: verification standard and what it excluded

**Status: written. One canonical source was dropped as unreadable, then
restored once it turned out to be readable. The drop was the error, and it had
consequences for the argument — see below.**

Every other number in this note can be checked against a file on disk. A
citation cannot — the failure mode is fabrication, and it is invisible to
`build.py --check`, which can confirm a DOI is well-formed but not that the
paper says what the sentence claims. The standard adopted was therefore
stricter than the rest of the note requires:

1. **Bibliographic existence**, confirmed against the Crossref REST API by DOI
   (`scratchpad/crossref.py`), independently of the page found by search. All
   seven journal DOIs resolved with matching title, authors, container,
   volume, and pages.
2. **Body text obtained and read.** Not the abstract. Every quotation in §2
   was extracted from the paper's own PDF with `pdftotext` locally, not copied
   from a search summary or a fetch tool's paraphrase.
3. **The quoted passage located in a named section**, so the claim attached to
   it can be checked by a reader.

### Kyle (1985): dropped, then restored — and the drop was the error

`Continuous Auctions and Insider Trading`, *Econometrica* 53(6), 1315–1336, is
the canonical citation for this section. It was **first excluded, then cited**,
and the reversal is the most instructive thing in this entry.

**The first pass.** Every copy I could reach was an image scan. `pdftotext`
returned **23 characters** from one and **1,285** from the other — the latter
being the JSTOR cover sheet alone. Bibliographic existence was verified three
independent ways (Crossref `10.2307/1913210`, RePEc, and the cover sheet, which
also settles the page range as 1315–1336 against RePEc's truncated `1315-35`).
On that basis the paper was dropped, on the stated grounds that citing it would
mean attributing a claim to a paper I had not read.

**That grounds was right. The conclusion drawn from it was not.** The
inference actually made was:

> `pdftotext` returned nothing → the body is unreadable → do not cite.

The middle step is false, and it is false in the specific way this note is
about: a negative result from one instrument was read as a property of the
world. `pdftotext` extracts a *text layer*. A scan has no text layer. That is a
fact about the file format, not about whether the words can be read. The pages
were 3680×5696 CCITT Group 4 images the whole time, and CCITT is a format TIFF
supports natively — so the scan could be rewrapped, without decoding or
re-encoding anything, and simply looked at. It took one script
(`sources/extract_scanned_pdf.py`) and the words were legible.

The tell was available and I did not act on it: **1,285 characters is not a
failed extraction, it is a successful extraction of a cover page.** The tool
worked perfectly. It reported exactly what it found. I read "the tool returned
almost nothing" as "there is almost nothing there."

**What restoring it changed.** Not a tidier bibliography — the argument. Read
from the rendered pages, Kyle says something more specific than the recalled
version of Kyle:

> "The informed trader trades in such a way that his private information is
> incorporated into prices **gradually**. [...] The constant volatility
> reflects the fact that information is incorporated into prices **at a
> constant rate**." (p. 1316, §1)

Constant-rate incorporation predicts **no lead bin in particular**. The
canonical model of informed trading, read rather than remembered, is therefore
an argument *against* expecting the localised pre-move signature this project
looks for — and §2 now says so. The recollection-based version ("Kyle shows
informed trading moves price gradually, so expect a lead") would have been
close enough to pass any reader's sniff test, and would have pointed the
section the wrong way.

So the earlier entry's claim that "nothing in the section is weaker for the
omission" was **false**. The section was materially weaker, and in the
direction that flattered the project.

**Standing correction:** a source is not unverifiable because the first tool
returned nothing. Check what the tool actually measures before concluding
anything from its silence. The scan was supplied on request and read in minutes.

### Verification status by source

| source | bibliographic | body read | quoted from |
|---|---|---|---|
| Glosten & Milgrom 1985 | Crossref | yes, 73,908 ch | §1 Introduction |
| Cont, Kukanov & Stoikov 2014 | Crossref | yes | §1; Table 2 note |
| Easley, López de Prado & O'Hara 2012 | Crossref | yes, accepted ver. | §1 Introduction |
| Andersen & Bondarenko 2014 (dispute) | Crossref | yes, CREATES 2013-42 | Abstract §; §1 |
| Easley et al. 2014 (rejoinder) | Crossref | **no — abstract only** | cited only for the *existence* of a reply |
| Gould et al. 2013 | Crossref | yes, 203,927 ch | §IV opening |
| He et al. 2024 | arXiv | yes, 107,789 ch | Abstract; §1 |
| Garcia Seuma 2026 | arXiv | yes, HTML | §4.5, §4.6 |
| Kyle 1985 | Crossref | yes — scan rendered and read | pp. 1315–1316, §1 |

The rejoinder is the one entry cited without reading the body. It is used for a
single narrow claim — that Easley and co-authors replied and disputed the
findings — which its own abstract states directly. Including it is a fairness
requirement: citing a critique while omitting the reply would misrepresent an
unresolved dispute as a settled one.

### The load-bearing distinction

The most consequential thing found in the sourcing was not a citation but a
**distinction**: Cont, Kukanov and Stoikov regress price change on order flow
imbalance over *the same* interval. Their own text (Table 2 note) reads
"...where ΔP*k* are the 10-second mid-price changes and OFI*k* are the
contemporaneous order flow imbalances."

An earlier draft of this section would have cited that R² of 65% as evidence
that order flow *predicts* price. It does not; it explains price
contemporaneously. Had §2 been drafted from recollection, that sentence would
have been wrong in exactly the way the rest of the note documents — plausible,
citable, and backwards.
