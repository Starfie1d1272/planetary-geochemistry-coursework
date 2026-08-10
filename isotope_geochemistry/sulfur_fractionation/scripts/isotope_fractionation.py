#!/usr/bin/env python3
"""
Sulfur isotope (34S/32S) equilibrium fractionation factors
=============================================================
Systems: H2S, SO2, SO4^2- (Bigeleisen-Mayer / Urey reduced partition function ratios)

Frequencies are read from the Gaussian-derived dataset ``data/frequencies.csv``,
which was extracted from the course Gaussian 16 calculations (private archive).
There is no silent literature fallback: if the dataset is missing, the script
fails loudly.

References:
  - Bigeleisen & Mayer (1947) J. Chem. Phys. 15, 261-267
  - Schauble (2004) RiMG 55, 65-111

Usage:
  python isotope_fractionation.py              # recompute + write results.csv + figure
  python isotope_fractionation.py --check      # read-only regression check vs tracked results.csv
"""

import argparse
import csv
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# Module-relative paths (works from any cwd)
# ---------------------------------------------------------------------------
MODULE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = MODULE_DIR / "data"
FIG_DIR = MODULE_DIR / "figures"
FREQUENCIES_CSV = DATA_DIR / "frequencies.csv"
RESULTS_CSV = DATA_DIR / "results.csv"
FIGURE_PNG = FIG_DIR / "sulfur_isotope_fractionation.png"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HC_K = 1.438777      # hc/k_B in cm*K
SCALE = 0.9619       # B3LYP frequency scale factor used for the course calculations
ABS_TOL_PERMIL = 0.01  # check tolerance for 1000*ln(beta)

# Physical vibration-mode counts (degenerate modes are physical modes and are
# never removed by value-deduplication).
N_MODES = {"H2S": 3, "SO2": 3, "SO4_2-": 9}
ISOTOPES = ("32S", "34S")

T_POINTS = [273, 298, 323, 373, 473, 573, 773, 973, 1273]

MOLECULES = {
    "H2S":    {"label": "H\u2082S",    "method": "B3LYP", "basis": "6-31G(d)"},
    "SO2":    {"label": "SO\u2082",    "method": "B3LYP", "basis": "6-31G(d)"},
    "SO4_2-": {"label": "SO\u2084\u00b2\u207b", "method": "B3LYP", "basis": "6-31+G(d)"},
}

# Publication-style plot settings
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "savefig.dpi": 300,
    "figure.dpi": 150,
    "axes.linewidth": 1.2,
})
COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#F0E442", "#56B4E9"]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_frequencies(path=FREQUENCIES_CSV):
    """Load the Gaussian-derived frequency dataset.

    Returns {molecule: {"32S": [scaled cm-1 ...], "34S": [...]}}.
    Raises SystemExit with a clear message if the file is missing or does not
    satisfy the physical mode-count invariants.
    """
    if not path.exists():
        print(
            "ERROR: frequency dataset not found: {}".format(path),
            file=sys.stderr,
        )
        print(
            "The Gaussian-derived frequency dataset is required for all "
            "calculations and is not replaced by literature values.",
            file=sys.stderr,
        )
        sys.exit(2)

    data = {mol: {iso: [] for iso in ISOTOPES} for mol in N_MODES}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mol = row["molecule"]
            iso = row["isotope"]
            if mol not in N_MODES or iso not in ISOTOPES:
                continue
            data[mol][iso].append(float(row["scaled_frequency_cm-1"]))

    for mol, n_modes in N_MODES.items():
        for iso in ISOTOPES:
            n = len(data[mol][iso])
            if n != n_modes:
                print(
                    "ERROR: {}/{} has {} modes, expected {} "
                    "(degenerate modes are physical modes and must all be present)."
                    .format(mol, iso, n, n_modes),
                    file=sys.stderr,
                )
                sys.exit(2)
    return data


# ---------------------------------------------------------------------------
# Bigeleisen-Mayer beta factors
# ---------------------------------------------------------------------------
def calc_beta(freqs_light, freqs_heavy, T):
    """Reduced partition function ratio beta (Bigeleisen & Mayer 1947, Eq. 10).

    beta = prod_i [ (u_i'/u_i) * f(u_i) / f(u_i') ],
    f(u) = exp(-u/2) / (1 - exp(-u)),  u = hc*w / (k_B T).
    """
    if len(freqs_light) != len(freqs_heavy):
        raise ValueError(
            "mode count mismatch: light={}, heavy={}".format(
                len(freqs_light), len(freqs_heavy))
        )
    ln_beta = 0.0
    for wl, wh in zip(freqs_light, freqs_heavy):
        ul = HC_K * wl / T
        uh = HC_K * wh / T
        ln_beta += math.log(uh / ul) \
            + (-uh / 2.0 - math.log(1.0 - math.exp(-uh))) \
            - (-ul / 2.0 - math.log(1.0 - math.exp(-ul)))
    return math.exp(ln_beta)


def frequency_product_diagnostic(freqs_light, freqs_heavy):
    """Frequency-product ratio prod(omega'_i / omega_i).

    Kept as a first-order self-consistency diagnostic of the frequency data
    (frequency-product diagnostic), not a full Teller-Redlich product-rule
    verification (the translational/rotational right-hand side is not
    implemented here).
    """
    return float(np.prod([h / l for l, h in zip(freqs_light, freqs_heavy)]))


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
def write_results_csv(results, path=RESULTS_CSV):
    """results: {molecule: {T: (beta, ln10beta)}} at T_POINTS."""
    labels = {m: MOLECULES[m]["label"] for m in MOLECULES}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        header = ["T(K)"]
        for mol in MOLECULES:
            header.extend([f"{labels[mol]}_beta", f"{labels[mol]}_1000lnb"])
        writer.writerow(header)
        for T in T_POINTS:
            row = [T]
            for mol in MOLECULES:
                b, ln10b = results[mol][T]
                row.extend([f"{b:.6f}", f"{ln10b:.3f}"])
            writer.writerow(row)
    print("  \u2713 CSV: {}".format(path))


def make_plots(freqs, save_path=FIGURE_PNG):
    """Multi-panel figure: beta vs T, 1000*ln(beta) vs 1000/T, alpha pairs."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.subplots_adjust(hspace=0.30, wspace=0.35)
    names = list(MOLECULES.keys())
    labels = [MOLECULES[n]["label"] for n in names]

    temps = np.linspace(273, 1273, 200)
    series = {}
    for mol in names:
        fl = freqs[mol]["32S"]
        fh = freqs[mol]["34S"]
        betas = np.array([calc_beta(fl, fh, T) for T in temps])
        series[mol] = {"T": temps, "beta": betas, "ln10b": 1000.0 * np.log(betas)}

    ax = axes[0, 0]
    for i, mol in enumerate(names):
        ax.plot(series[mol]["T"], series[mol]["beta"], color=COLORS[i % len(COLORS)],
                lw=2.5, label=labels[i])
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("\u03b2 (Reduced partition function ratio)")
    ax.set_title("(a) \u03b2 factor vs T", fontweight="bold")
    ax.legend(frameon=True, fancybox=True, edgecolor="#cccccc")
    ax.grid(True, alpha=0.25, linestyle=":")

    ax = axes[0, 1]
    for i, mol in enumerate(names):
        ax.plot(1000.0 / series[mol]["T"], series[mol]["ln10b"],
                color=COLORS[i % len(COLORS)], lw=2.5, label=labels[i])
    ax.set_xlabel("1000 / T (K\u207b\u00b9)")
    ax.set_ylabel("1000 \u00b7 ln(\u03b2)")
    ax.set_title("(b) 1000\u00b7ln(\u03b2) vs 1000/T", fontweight="bold")
    ax.legend(frameon=True, fancybox=True, edgecolor="#cccccc")
    ax.grid(True, alpha=0.25, linestyle=":")

    pairs = [("SO2", "H2S"), ("SO4_2-", "H2S"), ("SO4_2-", "SO2")]
    ax = axes[0, 2]
    for k, (hi, lo) in enumerate(pairs):
        ln10a = 1000.0 * (np.log(series[hi]["beta"]) - np.log(series[lo]["beta"]))
        ax.plot(series[hi]["T"], ln10a, color=COLORS[k % len(COLORS)], lw=2.5,
                label="{} \u2014 {}".format(MOLECULES[hi]["label"], MOLECULES[lo]["label"]))
    ax.axhline(y=0, color="grey", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("1000 \u00b7 ln(\u03b1)")
    ax.set_title("(c) 1000\u00b7ln(\u03b1) vs T", fontweight="bold")
    ax.legend(frameon=True, fancybox=True, edgecolor="#cccccc")
    ax.grid(True, alpha=0.25, linestyle=":")

    ax = axes[1, 0]
    for k, (hi, lo) in enumerate(pairs):
        ln10a = 1000.0 * (np.log(series[hi]["beta"]) - np.log(series[lo]["beta"]))
        ax.plot(1e6 / series[hi]["T"] ** 2, ln10a, color=COLORS[k % len(COLORS)],
                lw=2.5, label="{} \u2014 {}".format(MOLECULES[hi]["label"], MOLECULES[lo]["label"]))
    ax.axhline(y=0, color="grey", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel("10\u2076 / T\u00b2 (K\u207b\u00b2)")
    ax.set_ylabel("1000 \u00b7 ln(\u03b1)")
    ax.set_title("(d) 1000\u00b7ln(\u03b1) vs 10\u2076/T\u00b2", fontweight="bold")
    ax.legend(frameon=True, fancybox=True, edgecolor="#cccccc")
    ax.grid(True, alpha=0.25, linestyle=":")

    ax = axes[1, 1]
    for k, (hi, lo) in enumerate(pairs):
        ln10a = 1000.0 * (np.log(series[hi]["beta"]) - np.log(series[lo]["beta"]))
        ax.plot(1000.0 / series[hi]["T"], ln10a, color=COLORS[k % len(COLORS)],
                lw=2.5, label="{} \u2014 {}".format(MOLECULES[hi]["label"], MOLECULES[lo]["label"]))
    ax.axhline(y=0, color="grey", lw=0.8, ls="--", alpha=0.5)
    ax.set_xlabel("1000 / T (K\u207b\u00b9)")
    ax.set_ylabel("1000 \u00b7 ln(\u03b1)")
    ax.set_title("(e) 1000\u00b7ln(\u03b1) vs 1000/T", fontweight="bold")
    ax.legend(frameon=True, fancybox=True, edgecolor="#cccccc")
    ax.grid(True, alpha=0.25, linestyle=":")

    ax = axes[1, 2]
    ax.axis("off")
    info = (
        "Sulfur Isotope Fractionation\n"
        "\u00b3\u2074S/\u00b3\u00b2S  |  B3LYP 6-31G(d)/6-31+G(d)\n"
        "Scale factor = {}\n\n"
        "\u03b2 ordering:\nH\u2082S < SO\u2082 < SO\u2084\u00b2\u207b\n\n"
        "Frequencies: data/frequencies.csv\n"
        "(Gaussian-derived, course archive)"
    ).format(SCALE)
    ax.text(0.1, 0.5, info, transform=ax.transAxes, fontsize=11, va="center",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0f0f0", edgecolor="#cccccc"))

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  \u2713 PNG: {}".format(save_path))


# ---------------------------------------------------------------------------
# --check: read-only scientific regression against tracked results.csv
# ---------------------------------------------------------------------------
def run_check(freqs):
    """Recompute the baseline from frequencies.csv and compare with results.csv.

    Does not modify any tracked output. Exits non-zero on any scientific
    mismatch beyond the rounding tolerance.
    """
    if not RESULTS_CSV.exists():
        print("ERROR: tracked results.csv not found: {}".format(RESULTS_CSV),
              file=sys.stderr)
        sys.exit(2)

    # parse tracked results
    labels = {MOLECULES[m]["label"]: m for m in MOLECULES}
    tracked = {m: {} for m in MOLECULES}
    with open(RESULTS_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T = int(float(row["T(K)"]))
            for label, mol in labels.items():
                tracked[mol][T] = float(row["{}_1000lnb".format(label)])

    ok = True
    worst = 0.0
    for mol in MOLECULES:
        fl = freqs[mol]["32S"]
        fh = freqs[mol]["34S"]
        for T in T_POINTS:
            recomputed = 1000.0 * math.log(calc_beta(fl, fh, T))
            diff = abs(recomputed - tracked[mol][T])
            worst = max(worst, diff)
            status = "OK" if diff <= ABS_TOL_PERMIL else "MISMATCH"
            if diff > ABS_TOL_PERMIL:
                ok = False
            print("  {:<8s} T={:>5d}  recomputed={:9.3f}  tracked={:9.3f}  |d|={:6.3f}  {}"
                  .format(MOLECULES[mol]["label"], T, recomputed, tracked[mol][T], diff, status))
        print("  {:<8s} frequency-product diagnostic: {:.6f}"
              .format(MOLECULES[mol]["label"], frequency_product_diagnostic(fl, fh)))

    print("\n  worst |d| = {:.4f} \u2030 (tolerance {:.2f} \u2030)".format(worst, ABS_TOL_PERMIL))
    if not ok:
        print("CHECK FAILED: recomputed baseline does not match tracked results.csv "
              "(scientific mismatch, not a formatting issue).", file=sys.stderr)
        sys.exit(1)
    print("CHECK PASSED: recomputed baseline matches tracked results.csv.")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Sulfur isotope (34S/32S) equilibrium fractionation "
                    "(Bigeleisen-Mayer / Urey).")
    parser.add_argument("--check", action="store_true",
                        help="read-only regression check against tracked data/results.csv")
    args = parser.parse_args()

    print("=" * 60)
    print("  Sulfur Isotope (\u00b3\u2074S/\u00b3\u00b2S) Fractionation Calculator")
    print("  Bigeleisen-Mayer theory | B3LYP 6-31G(d)/6-31+G(d) | scale={}".format(SCALE))
    print("  Frequencies: data/frequencies.csv (Gaussian-derived)")
    print("=" * 60)

    freqs = load_frequencies(FREQUENCIES_CSV)

    if args.check:
        return run_check(freqs)

    results = {}
    for mol in MOLECULES:
        fl = freqs[mol]["32S"]
        fh = freqs[mol]["34S"]
        print("\n{} ({} modes)".format(MOLECULES[mol]["label"], len(fl)))
        print("  \u00b3\u00b2S scaled frequencies: [{}]".format(
            ", ".join("{:.2f}".format(w) for w in fl)))
        print("  \u00b3\u2074S scaled frequencies: [{}]".format(
            ", ".join("{:.2f}".format(w) for w in fh)))
        shifts = [h - l for l, h in zip(fl, fh)]
        print("  isotope shifts (cm\u207b\u00b9): [{}]".format(
            ", ".join("{:.3f}".format(s) for s in shifts)))
        print("  frequency-product diagnostic: {:.6f}".format(
            frequency_product_diagnostic(fl, fh)))
        results[mol] = {}
        for T in T_POINTS:
            b = calc_beta(fl, fh, T)
            results[mol][T] = (b, 1000.0 * math.log(b))

    print("\n" + "=" * 60)
    print("  1000\u00b7ln(\u03b2) at selected temperatures (\u2030)")
    print("=" * 60)
    header = "{:>8}".format("T(K)")
    for mol in MOLECULES:
        header += "  {:>12}".format(MOLECULES[mol]["label"])
    print(header)
    print("-" * 60)
    for T in T_POINTS:
        row = "{:8.0f}".format(T)
        for mol in MOLECULES:
            row += "  {:12.3f}".format(results[mol][T][1])
        print(row)

    print("\n  Writing outputs...")
    write_results_csv(results)
    make_plots(freqs)

    print("\n  RESULTS SUMMARY (298 K)")
    for mol in MOLECULES:
        b, ln10b = results[mol][298]
        print("  {:<8s}: \u03b2 = {:.5f},  1000\u00b7ln\u03b2 = {:.2f}\u2030".format(
            MOLECULES[mol]["label"], b, ln10b))
    print("\nDone.")


if __name__ == "__main__":
    sys.exit(main())
