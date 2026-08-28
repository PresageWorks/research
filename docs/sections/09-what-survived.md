## 10 — What survived

Not indicators. Rules.

Each of these exists because one of the failures above produced convincing
output in its absence.

1. **Plant known signals at multiple effect sizes and confirm recovery.** A
   suite that cannot recover a planted d = 2.0 makes every null it produces
   meaningless, and a suite that only ever runs adversarial inputs cannot tell
   you it has that problem. *(§7)*

2. **Quote the current sensitivity floor beside every null result**, re-measured
   at that run's own sample size rather than carried forward. *(§7)*

3. **Match controls on time of day, and report the match quality** rather than
   assuming it held. *(§5)*

4. **Freeze the event list to disk before computing any variable.** *(§3)*

5. **Score out-of-sample or don't score.** A strictly proper scoring rule
   applied in-sample still reports edge on pure noise. *(Appendix A)*

6. **Compare precision against a coverage-matched chance floor**, never a global
   one. *(§7)*

7. **Refuse to report below a pre-declared event count**, whatever the result
   looks like. *(§3, §7)*

8. **Exclude zero-variance features and handle ties explicitly** before any
   ranking statistic runs. *(§6)*

9. **Re-run the entire adversarial suite after every fix**, including the parts
   that passed before it. The second guard failure in §7 was created by
   repairing the first.

10. **When a summary sentence and the recorded artifact disagree, the artifact
    wins.** §8's liquidation result was summarised in a run report in a way that
    read as two surviving cells; the CSVs show one of them failing its placebo at
    p = 0.054. The prose was not wrong so much as incomplete, which is harder to
    catch.

Two of these have a property I did not anticipate when I wrote them. Rules 1 and
9 are about the checking apparatus rather than about the analysis, and neither
would have been written without a failure that only the other could find. That
is the actual lesson of §7, and it generalises past this project: a validation
layer is code, code has bugs, and the bugs in a validation layer are invisible
by construction, because its correct output and its broken output look
identical.

11. **Control windows must not overlap.** Separation at least the window
    length, asserted rather than assumed. Overlapping controls are not
    independent observations, and every statistic weighted by the control
    count — pooled SD, Cohen's d, Mann-Whitney p, BH q, the placebo null, the
    power table — silently treats them as if they were. This one cost a factor
    of about three on the headline effect size and doubled the sensitivity
    floor. *(§8)*

### Pre-registration

The primary test — does market-internal information beat a price-and-volatility
baseline out of sample — is specified in a contract written and hashed before
the data existed to run it on.

```
results/EVALUATION_CONTRACT.md            (v2)
sha256   937ce309d5c01f1f135a63dffa60507f3a4d9606cdffc9afdda32aa9411b4161
bytes    40343
ratified 2026-08-24, amended 2026-08-26

results/EVALUATION_CONTRACT.v1.md         (v1, preserved)
sha256   505b12d0999665230127fcc630aeabe40a83aefdb78f07359a1ecd176c291869
bytes    31178
```

v2 is a clarification amendment. Two v1 clauses referred to procedures that were
never defined, the placebo for an anchor-scored EDGE, and a control-matching
"declared tolerance" that the document never declared. §1.11 and §1.12 supply
those definitions. **No threshold, score, or outcome criterion differs from v1**,
and the `SURVIVES` and `SUSPICIOUS` blocks are byte-identical between versions.

The contract fixes in advance: the exact feature list, grouped into nine named
families; the baseline specification; the train/test split rule and its 24-hour
embargo; the predictive model class; the primary score (out-of-sample CRPS); the
mandatory tail diagnostic (log score); the event threshold; the four outcome
states — `SURVIVES`, `INCONCLUSIVE`, `FAILS`, `SUSPICIOUS` — and a run budget of
**one**, with no interim look.

It also fixes the things that are easiest to move after the fact. A single
feature family surviving while the combined model fails is headlined *"Combined
model FAILS; F_x is a surviving lead"* and never *"PRESAGE works, via F_x"*.
`liq_count` stays in the declared feature list despite being known-dead, so its
absence appears in the report as a data-availability finding rather than
vanishing from the list. The 30-event minimum applies to the out-of-sample
partition rather than to the total, which moves the run trigger from 30 events
to roughly 75 and delays the test by weeks.

The stated reason for that last choice is in the contract's standing rules:
someone may eventually pay for this, and a claim sold on an underpowered result
is the seller's fault, not the buyer's.

The hash proves the contract was not edited after the fact. It does not prove
the eventual run honoured it — that depends on the run manifest citing the
digest and on the report emitting every pre-declared item unconditionally. The
scheme is tamper-evident, not tamper-proof, and the contract says so in those
words.

The result will be published whichever way it lands.

---

*This note demonstrates that the process can catch itself producing false
results. Whether the underlying hypothesis is true is a separate question, and
the data has not answered it yet.*
