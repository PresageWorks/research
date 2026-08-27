## 2 — What's already known

The claim that order flow carries information about price is old, well
supported, and was posed from the beginning as a question about *timing*. Kyle
(1985) opens by asking "how quickly is new private information about the
underlying value of a speculative commodity incorporated into market prices?"
In his model an informed trader conceals himself inside uninformed volume —
noise traders "provide camouflage which enables the insider to make profits at
their expense" — and so trades gradually rather than all at once. The result is
about timing: "The informed trader trades in such a way that his private
information is incorporated into prices gradually," at a constant rate in the
continuous limit, with all of it in price by the end of trading. Glosten and
Milgrom (1985) reach a similar destination by another route: adverse selection
alone produces a bid–ask spread, even for a risk-neutral market maker earning
zero expected profit, and transaction prices thereby convey information.

The modern empirical version is sharper. Cont, Kukanov and Stoikov (2014)
regress 10-second mid-price changes on order flow imbalance — the net change in
queue size at the best bid and ask — across 50 S&P 500 stocks, and report an
average R² of 65%, stable across stocks and across timescales from under a
second to ten minutes. Over short intervals, order flow does not merely
correlate with price; it accounts for most of the variation.

**That result is contemporaneous.** They regress the price change over an
interval on the order flow imbalance over *the same* interval — their text
describes OFI*k* as "the contemporaneous order flow imbalances." Explaining a
move as it happens is not the same as seeing it coming, and the second is what
this project asks about.

The prior work closest to that question is VPIN. Easley, López de Prado and
O'Hara (2012) state that "VPIN predicts short-term toxicity-induced volatility,
particularly as it relates to large price moves" — our question, on another
venue. It is also contested. Andersen and Bondarenko (2014) argue the metric is
"by construction, highly correlated with recent innovations to trading volume
and return volatility," and that once current volume and volatility are
controlled for there is "no evidence of incremental predictive power of VPIN
for future volatility." Easley and co-authors replied, disputing this; the
exchange is unresolved. What matters here is that the dispute is about
**controls**, not about effect size — which is why sections 5 and 7 of this
note are about controls rather than about how large anything was.

Three things differ in what follows. **The venue:** Hyperliquid trades
perpetual futures, the most popular cryptocurrency derivative (He et al. 2024),
and is fully on-chain, so per-fill wallet identity and labelled liquidations are
recorded rather than reconstructed from a leverage model. **The horizon:** 5–30
minutes *ahead of* a large move, not ten seconds around one. **The shape:** what
this project looks for is a *localised* pre-move signature — a variable that
separates in a specific lead bin. That is not what Kyle's model predicts.
Information arriving at a constant rate produces no bin in particular, and a
result that concentrates in one bin is therefore as much a reason for suspicion
as for interest. Section 4 is what happened the first time one did.

Whether on-chain observability changes any previously-tested result is open. The
nearest recent work I could verify — Garcia Seuma (2026), an unrefereed
preprint — tests early-warning signals before seven crypto-perpetual
liquidation cascades and reports that "No variable is event-invariant," using
Binance data rather than an on-chain venue. I found no verified study testing
these quantities where wallet identity is directly observable.

One caution frames all of it. Gould et al. (2013), surveying the limit order
book literature, note that "different studies often present conflicting
conclusions," attributing this to differences in matching algorithms, asset
classes, liquidity, and data quality. A result on one venue over a few days is
a result on one venue over a few days.

---

**References.** Every entry below was verified against the publisher, arXiv, or
Crossref record, and every quotation above was read from the body text of the
paper rather than from its abstract — for Kyle, off the rendered pages of the
scan. Anything not verifiable to that standard was to be dropped rather than
cited; the one source that nearly was, and why that would have been a mistake,
is in `AUDIT.md` (A9).

- Andersen, T. G., & Bondarenko, O. (2014). Reflecting on the VPIN dispute.
  *Journal of Financial Markets*, 17, 53–64. doi:10.1016/j.finmar.2013.08.002
  — summarising Andersen & Bondarenko (2014), VPIN and the flash crash,
  *Journal of Financial Markets*, 17, 1–46. doi:10.1016/j.finmar.2013.05.005
- Cont, R., Kukanov, A., & Stoikov, S. (2014). The price impact of order book
  events. *Journal of Financial Econometrics*, 12(1), 47–88.
  doi:10.1093/jjfinec/nbt003
- Easley, D., López de Prado, M. M., & O'Hara, M. (2012). Flow toxicity and
  liquidity in a high-frequency world. *Review of Financial Studies*, 25(5),
  1457–1493. doi:10.1093/rfs/hhs053
- Easley, D., López de Prado, M. M., & O'Hara, M. (2014). VPIN and the flash
  crash: A rejoinder. *Journal of Financial Markets*, 17, 47–52.
  doi:10.1016/j.finmar.2013.06.007
- Garcia Seuma, R. M. (2026). Where does the criticality live? Early-warning
  signals are event-heterogeneous across seven crypto-perpetual liquidation
  cascades. arXiv:2607.27070. *Preprint; not peer reviewed.*
- Glosten, L. R., & Milgrom, P. R. (1985). Bid, ask and transaction prices in a
  specialist market with heterogeneously informed traders. *Journal of
  Financial Economics*, 14(1), 71–100. doi:10.1016/0304-405X(85)90044-3
- Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J., &
  Howison, S. D. (2013). Limit order books. *Quantitative Finance*, 13(11),
  1709–1742. doi:10.1080/14697688.2013.803148
- He, S., Manela, A., Ross, O., & von Wachter, V. (2024). Fundamentals of
  perpetual futures. arXiv:2212.06888v6. *Preprint; not peer reviewed.*
- Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*,
  53(6), 1315–1336. doi:10.2307/1913210 — quoted from pp. 1315–1316; see
  `sources/README.md` for how the scan was read.
