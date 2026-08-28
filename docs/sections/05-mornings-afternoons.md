## 5 — I Was Comparing Mornings With Afternoons

*The experimental design lied.*

On the one-day run, **63 of 120 tests survived BH correction**. Seventy-one had
raw p < 0.05, against roughly six expected by chance.

That should have felt good. It did not, because it is not plausible. If half an
arbitrary set of variables genuinely carried information about the next thirty
minutes of price, someone would have noticed before me.

So I stopped looking at what the variables measured and looked at *when* they
were measured.

Ten of the thirteen events fell between **06:45 and 14:25 UTC**, mean hour 12.2.
The controls concentrated at hours 10, 14, 15, 17, 19 and 20, mean hour 16.7.
Not because I chose that. Because one day physically cannot supply same-hour
controls: each hour offers 60 candidate minutes, and excluding the windows
around events consumes most of them. **Hour 9 yielded zero usable controls.** To
obtain any at all, the matching tolerance had to stretch to ±5–7 hours for the
morning events.

Every comparison I was making had a four-and-a-half-hour offset built into it.

The analogy is measuring whether a promotion makes a restaurant busier, where
every promotion night is compared against a control sample taken at 10am. You
will find a huge effect. It is dinner.

![Figure 3](figures/fig3-intraday.png)

**Figure 3** — Volume, spread and participation across the day, measured from
the control windows themselves rather than asserted.

One result in that figure is **new to this note and not stated in any run
report**: across the three analysed days, only **14 of 24 hours contain any
control window at all**. That is derived here directly from
the derived window-variable table by counting distinct populated hours among
the 744 control windows, and it is reported as a derivation rather than as a
quotation. It is the same scarcity that forced the matching tolerance open,
measured on the corrected three-day run rather than on the one-day run where the
problem was first noticed. The constraint did not go away when the
matching improved. It got survivable.

This is why an unmatched control is not merely a noisy one. Noise across 57
events washes out. A systematic difference with a consistent sign does not, and
it survives BH, because BH is designed to suppress false positives arising from
randomness and this difference is not random. It is real. It is simply the
difference between morning and afternoon rather than the difference between
pre-event and ordinary.

Three days supplied enough candidate windows to match properly. **24 of 57
events matched strictly within-hour** and the remainder at ±1–2 hours, against
±5–7 hours before.

**Table 2 — What the fix cost**

| | one day | three days |
|---|---:|---:|
| Events | 13 | 57 |
| Controls | 214 | 744 |
| Raw p < 0.05 | 71 / 120 | 28 / 120 |
| BH survivors | 63 / 120 | **25 / 120** |
| Mean event hour | 12.2 | 10.2 |
| Mean control hour | 16.7 | 10.6 |
| Matching tolerance | ±5–7 h | 24 strict, rest ±1–2 h |
| Events retained by strict placebo | 5 of 13 | 48 of 57 |
| Best precision lift over chance | +0.417 | +0.230 |

Both columns are recomputed here directly from `results/stats_2026-08-21.csv`
and `results/stats_4d_2026-08-21.csv` rather than transcribed from the run
reports, and they agree with them.

No variable was added, removed, or redefined between those two columns. Roughly
sixty percent of the apparent findings disappeared once the time-of-day
mismatch was corrected. So did most of the apparent precision: the best cell on
one day showed a lift of +0.417 over the chance floor, and the best cell on
three days shows +0.230.

The strict placebo line is the one I would draw attention to. On one day, the
placebo test that was supposed to validate everything could only be constructed
from 5 of 13 events, because for events at hours 6, 7, 8, 9 and 22 every
eligible minute was already within 30 minutes of an event. A guard running on
5 events is close to no guard at all. On three days it retains 48 of 57 and
becomes a real test. This is the same underlying scarcity problem as the
control matching, showing up in the validation layer instead of the design
layer. Section 7 is about what happens when that goes unnoticed.

**Both columns were later superseded again.** The control-overlap repair of
2026-08-26 cut the three-day BH survivors from 25 to **3 / 120**, all three in
`[-5,0)`. The paragraph below describes the pre-repair picture, which is what
the time-of-day fix alone produced; §8 carries the repaired numbers.

And the 25 survivors that remain are not a consolation prize. **Fifteen of them
live in `[-5,0)`** — the bin closest to the move, where mean |d| across all
variables jumps to 0.929 against 0.281 in the preceding bin. That is the
profile of detection, not anticipation.

After fixing the controls, the market still became easier to recognise as it
moved. What I had not shown was that it became easier to predict before it
moved.
