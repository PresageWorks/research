## 1 — What I'm testing

A candlestick chart shows the outcome of a process. Price moved, and the candle
records that it moved. The question this project asks is whether the process is
visible before the outcome is: whether information in fills, order book state,
and positioning changes measurably *before* a large price move rather than only
during it.

Stated precisely: does market-internal information add predictive value about
price at 5–30 minute horizons, beyond what price and realised volatility
already provide?

**This note does not answer that question.** The primary test is pre-registered
and has not been run. It requires more data than currently exists: the
contract sets the trigger at 30 out-of-sample events, roughly 75 in total, and
the most recent live run had six.

What this note reports is something else. Five occasions on which the attempt
produced a convincing-looking answer that was wrong.

None of them were crashes. Every one produced clean output and plausible
statistics, and two produced results that survived multiple-comparison
correction. They failed at five different layers:

| § | layer | what it produced |
|---|---|---|
| 4 | the data definition | a leading indicator that was a clock |
| 5 | the experimental design | 63 of 120 tests "significant" |
| 6 | the metric implementation | a perfect classifier made of zeros |
| 7 | the validation machinery | guards that could not detect anything |
| A | the definition of "better" | edge measured on pure noise |

The fourth is the one I did not expect. I built the guards specifically to
catch the first three, and the guards had the same disease.

The fifth is not a bug at all but a definition, and it is established on
synthetic inputs rather than on market data. It therefore sits in Appendix A
rather than in the body, for the reason given there.

Total egress cost of the archived analysis: **$0.26**, across four days of
requester-pays downloads. The expense here was never compute.
