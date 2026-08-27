#!/usr/bin/env python3
"""Meta-testing a guard stack — synthetic demonstration of the method.

WHAT THIS IS
------------
A standalone, fully synthetic reimplementation of the *methodology* used to
meta-test PRESAGE's analysis guards. It demonstrates the argument made in
section 7 of the research note: a suite of checks that has never fired is
indistinguishable from a suite that cannot fire, so the checks themselves must
be tested in both directions.

WHAT THIS IS NOT
----------------
This is NOT the harness that runs against the production pipeline. It imports
no PRESAGE module, reads no captured data, and contains no feature definitions,
tolerances, alignment rules, capture configuration or pipeline structure. Every
series here is generated from a seeded RNG inside this file. Numbers it prints
are properties of that synthetic world and are not results about any market.

THE TWO DIRECTIONS, BOTH REQUIRED
---------------------------------
  POSITIVE CONTROL — plant an effect of known size and require the stack to
  recover it: raw detection, survival of Benjamini-Hochberg against a realistic
  burden of simultaneous tests, and beating an hour-matched placebo. If a large
  planted effect cannot be recovered, every "no signal found" the stack ever
  produces is worthless.

  NEGATIVE CONTROL — plant nothing, shuffle labels, feed constants. The stack
  must stay quiet. A stack that fires on noise is equally worthless.

The output is a SENSITIVITY FLOOR: the smallest planted effect recovered
reliably at a given event count. That number belongs beside every null result a
system like this reports, because "we found nothing" means nothing without it.

WHY THE PLANTED EFFECT IS A TIME SERIES, NOT A PER-WINDOW LABEL
---------------------------------------------------------------
A per-window label would pass an hour-matched placebo trivially: placebo
windows would never carry it, so the contrast would be guaranteed. Planting
into an underlying series -- elevated during real pre-event windows, ordinary
everywhere else -- means the placebo can in principle pick the elevation up by
chance, which is what makes it a real test.

Usage:
    python meta_test_synthetic.py                 # default sweep
    python meta_test_synthetic.py --events 40 --trials 200
"""
from __future__ import annotations

import argparse
import numpy as np
from scipy import stats

HOURS_PER_DAY = 24
WINDOW_MIN = 30          # analysis window length, synthetic
SEP_MIN = 30             # minimum separation between anchors


# ----------------------------------------------------------------- synthetic
def make_series(rng, n_minutes, seasonal=True):
    """A minute series with autocorrelation and a diurnal component.

    Both properties matter. Autocorrelation is what makes naive permutation
    tests anticonservative; the diurnal component is what makes hour-matching
    necessary rather than decorative.
    """
    x = np.zeros(n_minutes)
    phi = 0.97
    innov = rng.normal(0, 1, n_minutes)
    for i in range(1, n_minutes):
        x[i] = phi * x[i - 1] + innov[i]
    x /= x.std() or 1.0
    if seasonal:
        t = np.arange(n_minutes)
        hour = (t // 60) % HOURS_PER_DAY
        x = x + 0.8 * np.sin(2 * np.pi * hour / HOURS_PER_DAY)
    return x


def draw_anchors(rng, n_minutes, k, sep=SEP_MIN, hour_bias=None):
    """Non-overlapping anchors. Optionally concentrated in given hours.

    Non-overlap is enforced rather than assumed: overlapping windows reuse the
    same minutes and inflate the apparent number of independent observations.
    """
    out = []
    for _ in range(4000):
        if len(out) >= k:
            break
        t = int(rng.integers(WINDOW_MIN, n_minutes - WINDOW_MIN))
        if hour_bias is not None and ((t // 60) % HOURS_PER_DAY) not in hour_bias:
            continue
        if all(abs(t - u) >= sep for u in out):
            out.append(t)
    return sorted(out)


def window_means(x, anchors):
    return np.array([x[t - WINDOW_MIN:t].mean() for t in anchors])


def plant(x, anchors, d):
    """Elevate the series during pre-event windows by d standard deviations."""
    y = x.copy()
    for t in anchors:
        y[t - WINDOW_MIN:t] += d
    return y


# --------------------------------------------------------------------- stack
def benjamini_hochberg(pvals, alpha=0.05):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    thresh = alpha * (np.arange(1, m + 1) / m)
    passed = p[order] <= thresh
    if not passed.any():
        return np.zeros(m, bool)
    kmax = np.max(np.flatnonzero(passed))
    keep = np.zeros(m, bool)
    keep[order[:kmax + 1]] = True
    return keep


def cohens_d(a, b):
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1))
                 / (na + nb - 2))
    return 0.0 if sp == 0 else (a.mean() - b.mean()) / sp


def evaluate(rng, x, ev_anchors, n_minutes, n_decoy):
    """Run the guard stack once. Returns (detected, d, q, placebo_p).

    `n_decoy` simultaneous null variables are tested alongside the real one so
    that BH carries a realistic multiple-comparison burden. Correcting against
    a single test would make survival far too easy.
    """
    ev_hours = {(t // 60) % HOURS_PER_DAY for t in ev_anchors}
    ctl = draw_anchors(rng, n_minutes, len(ev_anchors) * 4, hour_bias=ev_hours)
    if len(ctl) < 8:
        return False, 0.0, 1.0, 1.0

    a, b = window_means(x, ev_anchors), window_means(x, ctl)
    d = cohens_d(a, b)
    p_real = stats.mannwhitneyu(a, b, alternative="two-sided").pvalue

    pv = [p_real]
    for _ in range(n_decoy):
        z = make_series(rng, n_minutes)
        pv.append(stats.mannwhitneyu(window_means(z, ev_anchors),
                                     window_means(z, ctl),
                                     alternative="two-sided").pvalue)
    keep = benjamini_hochberg(pv)
    q = min(1.0, p_real * len(pv) / max(1, sum(keep)))

    # Hour-matched placebo: fake events drawn from the SAME hours.
    worse = 0
    D = 200
    for _ in range(D):
        fake = draw_anchors(rng, n_minutes, len(ev_anchors), hour_bias=ev_hours)
        if len(fake) < 4:
            continue
        if abs(cohens_d(window_means(x, fake), b)) >= abs(d):
            worse += 1
    placebo_p = (1 + worse) / (1 + D)   # +1: the observed case is one draw

    return bool(keep[0] and placebo_p < 0.05), d, q, placebo_p


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", type=int, default=30)
    ap.add_argument("--trials", type=int, default=40)
    ap.add_argument("--decoys", type=int, default=19)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--seed", type=int, default=20260827)
    a = ap.parse_args()

    n_minutes = a.days * HOURS_PER_DAY * 60
    rng = np.random.default_rng(a.seed)

    print(f"synthetic meta-test  |  events={a.events}  trials={a.trials}  "
          f"simultaneous tests={a.decoys + 1}  days={a.days}")
    print("=" * 68)

    print("\nNEGATIVE CONTROLS (the stack must stay quiet)")
    fired = 0
    for _ in range(a.trials):
        x = make_series(rng, n_minutes)
        ev = draw_anchors(rng, n_minutes, a.events)
        det, *_ = evaluate(rng, x, ev, n_minutes, a.decoys)
        fired += det
    rate = fired / a.trials
    print(f"  d=0.0, seasonal confound present : fired {fired}/{a.trials} "
          f"({rate:.1%})   {'OK' if rate <= 0.10 else 'FAIL'}")

    xc = make_series(rng, n_minutes) * 0 + 1.0
    ev = draw_anchors(rng, n_minutes, a.events)
    det, d, _, _ = evaluate(rng, xc, ev, n_minutes, a.decoys)
    print(f"  constant variable                : fired={det} d={d:.3f}   "
          f"{'OK' if not det and d == 0.0 else 'FAIL'}")

    print("\nPOSITIVE CONTROLS (sensitivity floor)")
    floor = None
    for d_plant in (0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0):
        hits = 0
        for _ in range(a.trials):
            x = make_series(rng, n_minutes)
            ev = draw_anchors(rng, n_minutes, a.events)
            det, *_ = evaluate(rng, plant(x, ev, d_plant), ev,
                               n_minutes, a.decoys)
            hits += det
        r = hits / a.trials
        mark = ""
        if r >= 0.80 and floor is None:
            floor, mark = d_plant, "   <- sensitivity floor (>=80%)"
        print(f"  planted d={d_plant:<4} recovered {hits:>3}/{a.trials} "
              f"({r:5.1%}){mark}")

    print("\n" + "=" * 68)
    if floor is None:
        print("SENSITIVITY FLOOR: not reached in the swept range.")
        print("Any null result at this event count is uninformative.")
    else:
        print(f"SENSITIVITY FLOOR at {a.events} events: d = {floor}")
        print("A null result from this stack excludes effects at or above that")
        print("size. It says nothing about smaller ones. Report the floor with")
        print("the null, or the null cannot be interpreted.")


if __name__ == "__main__":
    main()
