#!/usr/bin/env python3
"""Ambiguity 1 — a placebo for an anchor-scored CRPS EDGE.

SYNTHETIC ONLY. No live-capture data is read anywhere in this file. The point
of resolving the ambiguity now is that the answer is not yet visible; running
either implementation against live data would make the choice informed by the
result, which is the thing being avoided.

THE QUESTION SURVIVES 4 WAS WRITTEN TO ANSWER
---------------------------------------------
  Could the measured skill have been produced by the shared temporal structure
  of the inputs and the target -- time of day, volatility clustering -- rather
  than by any event-linked information in the PRESAGE internals?

The archive answered that for an event-vs-control statistic by drawing fake
events at the same hours as the real ones. EDGE has no events in it: it is a
mean over every test anchor. So the placebo has to break the same linkage in an
anchor-scored world.

IMPLEMENTATION UNDER TEST
  P-SHIFT : circularly shift Model B's EXTRA features by a whole number of
            DAYS, refit the whole model, recompute EDGE. A whole-day shift
            preserves hour-of-day exactly -- it is the literal analogue of
            "hour-matched" -- and preserves each series' autocorrelation, while
            destroying the specific alignment between internals and target.

ALTERNATIVE, TESTED AND REJECTED
  P-PERM  : permute the extra features across anchors at random. Destroys the
            autocorrelation as well as the alignment, so the null model is
            handicapped in a way the real model is not.

Both are measured below rather than argued about.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import erf

RESULTS = Path(__file__).resolve().parent.parent / "results"

MIN_PER_DAY = 1440
N_DAYS = 6
T = MIN_PER_DAY * N_DAYS
H = 5                        # forecast horizon, minutes
EMBARGO = MIN_PER_DAY        # 24h, as the contract specifies
TRAIN_FRAC = 0.60
LAM_GRID = [1e-3, 1e-2, 1e-1, 1.0, 10.0]
N_A, N_B = 5, 8


# --------------------------------------------------------------------- #
def ar1(rng, n, phi, sd=1.0):
    """Unit-variance AR(1).

    The raw recursion has stationary variance sd^2/(1-phi^2), which at
    phi=0.995 is ~100x sd^2. Left unnormalised, vol = exp(0.4*x) then spanned
    exp(+/-4) and the location-scale fit broke down numerically at large T --
    every model returned its initial values and EDGE came out identically
    0.000. Normalising keeps the world well conditioned at any T.
    """
    from scipy.signal import lfilter
    x = lfilter([1.0], [1.0, -phi], rng.normal(0, 1.0, n))
    x = x - x.mean()
    v = x.std()
    return sd * x / (v if v > 0 else 1.0)


def world(rng, beta, confound=True):
    """Synthetic market with intraday seasonality in BOTH inputs and target.

    Seasonality is deliberately shared: that is the confound the placebo has to
    be able to see through. beta is how much of the target the extra features
    genuinely explain.
    """
    t = np.arange(T)
    tod = 2 * np.pi * (t % MIN_PER_DAY) / MIN_PER_DAY
    season = 1.0 + 0.6 * np.sin(tod) + 0.3 * np.sin(2 * tod)
    vol = np.exp(0.4 * ar1(rng, T, 0.995)) * season

    A = np.column_stack([
        vol, np.roll(vol, 5), np.roll(vol, 30),
        np.abs(ar1(rng, T, 0.9)) * season,
        ar1(rng, T, 0.98) * season])

    driver = ar1(rng, T, 0.97)
    if confound:
        # extras share the seasonal component with the target's SCALE. At
        # beta=0 they still predict sigma, so EDGE is genuinely positive and
        # the placebo must see through it. This is the interesting null.
        B = np.column_stack(
            [driver * season + 0.5 * ar1(rng, T, 0.9) for _ in range(2)]
            + [ar1(rng, T, 0.95) * season for _ in range(N_B - 2)])
    else:
        # extras carry no information about y at all: the strict null.
        B = np.column_stack([ar1(rng, T, 0.95) for _ in range(N_B)])

    eps = rng.normal(0, 1, T)
    y = vol * (beta * np.roll(driver, -H) + np.sqrt(max(1e-9, 1 - beta ** 2)) * eps)
    return A, B, y


def crps_gauss(mu, sigma, y):
    z = (y - mu) / sigma
    pdf = np.exp(-0.5 * z ** 2) / np.sqrt(2 * np.pi)
    cdf = 0.5 * (1 + erf(z / np.sqrt(2)))
    return sigma * (z * (2 * cdf - 1) + 2 * pdf - 1 / np.sqrt(np.pi))


def fit_locscale(X, y, lam):
    """Gaussian location-scale ridge, exactly the class the contract locks."""
    n, p = X.shape
    X1 = np.hstack([np.ones((n, 1)), X])

    def nll_grad(th):
        b, g = th[:p + 1], th[p + 1:]
        mu = X1 @ b
        ls = np.clip(X1 @ g, -8, 8)
        s = np.exp(ls)
        z = (y - mu) / s
        pb = np.r_[0.0, b[1:]]
        pg = np.r_[0.0, g[1:]]
        f = (0.5 * z ** 2 + ls).sum() + lam * (pb @ pb + pg @ pg)
        gb = -X1.T @ (z / s) + 2 * lam * pb
        gg = X1.T @ (1.0 - z ** 2) + 2 * lam * pg
        return f, np.concatenate([gb, gg])

    th0 = np.zeros(2 * (p + 1))
    th0[p + 1] = np.log(y.std() + 1e-9)
    r = minimize(nll_grad, th0, jac=True, method="L-BFGS-B",
                 options={"maxiter": 500, "maxfun": 2000})
    b, g = r.x[:p + 1], r.x[p + 1:]
    return b, g


def predict(b, g, X):
    n = X.shape[0]
    X1 = np.hstack([np.ones((n, 1)), X])
    return X1 @ b, np.exp(np.clip(X1 @ g, -8, 8))


def edge(A, B, y, tr, te, lam):
    """EDGE = mean over TEST anchors of CRPS_A - CRPS_B. Model B nests A."""
    XA, XB = A, np.hstack([A, B])
    mA = fit_locscale(XA[tr], y[tr], lam)
    mB = fit_locscale(XB[tr], y[tr], lam)
    cA = crps_gauss(*predict(*mA, XA[te]), y[te])
    cB = crps_gauss(*predict(*mB, XB[te]), y[te])
    return float(np.mean(cA - cB)), cA - cB


def standardise(X, tr):
    m, s = X[tr].mean(0), X[tr].std(0)
    s[s == 0] = 1
    return (X - m) / s


def split():
    cut = int(T * TRAIN_FRAC)
    tr = np.arange(0, cut)
    te = np.arange(cut + EMBARGO, T - H)
    return tr, te


def pick_lam(A, B, y, tr, te):
    best, bl = -np.inf, LAM_GRID[0]
    k = len(tr) // 2
    for lam in LAM_GRID:
        e, _ = edge(A, B, y, tr[:k], tr[k:], lam)
        if e > best:
            best, bl = e, lam
    return bl


def placebo(A, B_raw, y, tr, te, lam, mode, draws, rng):
    """Null distribution of EDGE with the internals' linkage broken.

    Takes B UNSTANDARDISED and re-standardises after the shift. Standardising
    once and then shifting leaves the placebo's TRAIN block with a mean and sd
    that are not 0/1, while the real configuration's are -- the two are then
    not exchangeable and the real model is flattered. Measured: that mistake
    put the strict-null rejection rate at 0.167 against a nominal 0.05.
    """
    out = []
    if mode == "shift":
        # ENUMERATE every distinct whole-day shift exactly once. Sampling them
        # with replacement adds no information -- each shift's EDGE is
        # deterministic -- and only coarsens the null.
        ks = [k * MIN_PER_DAY for k in range(1, N_DAYS)]
    else:
        ks = [None] * draws
    for k in ks:
        Bp = (np.roll(B_raw, int(k), axis=0) if k is not None
              else B_raw[rng.permutation(T)])
        e, _ = edge(A, standardise(Bp, tr), y, tr, te, lam)
        out.append(e)
    return np.array(out)


def one_trial(seed, beta, draws, mode, confound=True, fixed_lam=None):
    """fixed_lam bypasses selection. Selecting lambda on the REAL configuration
    and then handing it to the placebo can favour the real model; whether it
    actually does is measured rather than assumed."""
    rng = np.random.default_rng(seed)
    A, B, y = world(rng, beta, confound)
    tr, te = split()
    A, Bs = standardise(A, tr), standardise(B, tr)
    lam = fixed_lam if fixed_lam is not None else pick_lam(A, Bs, y, tr, te)
    real, per_anchor = edge(A, Bs, y, tr, te, lam)
    null = placebo(A, B, y, tr, te, lam, mode, draws, rng)
    # Standard Monte-Carlo permutation p-value. The +1 in both terms counts the
    # observed configuration as one of the exchangeable arrangements; omitting
    # it makes the test anticonservative, which is what put the strict-null
    # rejection rate at 0.167 against a nominal 0.05.
    p = float((1 + (null >= real).sum()) / (1 + len(null)))
    return real, p, per_anchor, null


def autocorr_note(per_anchor):
    x = per_anchor - per_anchor.mean()
    ac = [float(np.corrcoef(x[:-k], x[k:])[0, 1]) for k in (1, 5, 30, 120)]
    n_eff = len(x) / max(1.0, 1 + 2 * sum(max(0.0, a) for a in ac))
    return ac, len(x), n_eff


def merge(frag):
    f = RESULTS / "placebo_for_edge.json"
    d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    d.update(frag)
    f.write_text(json.dumps(d, indent=1), encoding="utf-8")
    print("  merged:", ", ".join(frag))


def main():
    global N_DAYS, T
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if len(sys.argv) > 2:                    # override the capture window
        N_DAYS = int(sys.argv[2]); T = MIN_PER_DAY * N_DAYS
    print(f"PLACEBO FOR AN ANCHOR-SCORED CRPS EDGE -- SYNTHETIC ONLY [{stage}]",
          flush=True)

    if stage == "anchor":
        real, p, pa, _ = one_trial(1, 0.0, 20, "shift")
        ac, n, n_eff = autocorr_note(pa)
        for k, a in zip((1, 5, 30, 120), ac):
            print(f"  autocorr lag {k:>3} min : {a:+.3f}", flush=True)
        print(f"  test anchors {n}, effective ~{n_eff:.0f} "
              f"({n/n_eff:.0f}x over-count)", flush=True)
        merge({"T": T, "days": N_DAYS, "horizon": H,
               "anchor_autocorr": dict(zip(["1","5","30","120"], ac)),
               "n_test_anchors": n, "effective_n": n_eff})

    elif stage.startswith("null"):
        parts = stage.split("-")              # null-shift-strict[-fixlam]
        mode, kind = parts[1], parts[2]
        fl = 1.0 if len(parts) > 3 else None
        conf = (kind == "confound")
        TR, DR = 30, 25
        ps, es = [], []
        for i in range(TR):
            r = one_trial(200 + i, 0.0, DR, mode, conf, fl)
            es.append(r[0]); ps.append(r[1])
        rate = float(np.mean(np.array(ps) < 0.05))
        print(f"  {kind} null, mode={mode}: mean EDGE {np.mean(es):+.4f}  "
              f"rejection {rate:.3f}", flush=True)
        key = f"null_{mode}_{kind}" + ("_fixlam" if fl is not None else "")
        merge({key: {"rate": rate,
                                       "mean_edge": float(np.mean(es)),
                                       "trials": TR, "draws": DR}})

    elif stage.startswith("pos"):
        beta = float(stage.split("-")[1])
        TR, DR = 20, 25
        res = [one_trial(500 + i, beta, DR, "shift", True) for i in range(TR)]
        es = [r[0] for r in res]
        pr = float(np.mean([r[1] < 0.05 for r in res]))
        print(f"  beta {beta:.2f}: mean EDGE {np.mean(es):+.5f}  "
              f"pass {pr:.2f}", flush=True)
        f = RESULTS / "placebo_for_edge.json"
        d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        pos = d.get("positive_control", [])
        pos = [x for x in pos if x["beta"] != beta]
        pos.append({"beta": beta, "mean_edge": float(np.mean(es)),
                    "pass_rate": pr})
        merge({"positive_control": sorted(pos, key=lambda x: x["beta"])})


if __name__ == "__main__":
    main()
