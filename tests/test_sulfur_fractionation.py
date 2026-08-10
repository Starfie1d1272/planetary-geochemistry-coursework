"""Scientific regression tests for the sulfur isotope fractionation module."""
import csv
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "isotope_geochemistry" / "sulfur_fractionation" / "scripts"))
import isotope_fractionation as sf  # noqa: E402

MODULE = Path(__file__).resolve().parents[1] / "isotope_geochemistry" / "sulfur_fractionation"

# Canonical rounded 298 K values in the publication layer.
BASELINE_298K = {"H2S": 11.033, "SO2": 41.124, "SO4_2-": 66.567}
TOL_PERMIL = 0.01

# Frequency-product diagnostic convention R_f = prod(nu_34S / nu_32S),
# locked from the tracked Gaussian-derived dataset (heavy/light convention).
DIAGNOSTIC = {"H2S": 0.997320, "SO2": 0.972770, "SO4_2-": 0.941830}
DIAG_TOL = 1e-6


@pytest.fixture(scope="module")
def freqs():
    return sf.load_frequencies(MODULE / "data" / "frequencies.csv")


def test_physical_mode_counts(freqs):
    """H2S: 3 modes, SO2: 3 modes, SO4^2-: 9 modes — degenerate modes must
    not be removed by value-deduplication."""
    for mol, n in sf.N_MODES.items():
        for iso in ("32S", "34S"):
            assert len(freqs[mol][iso]) == n, f"{mol}/{iso} must have {n} physical modes"


def test_298k_baseline(freqs):
    for mol, expected in BASELINE_298K.items():
        ln10b = 1000.0 * math.log(sf.calc_beta(freqs[mol]["32S"], freqs[mol]["34S"], 298))
        assert abs(ln10b - expected) <= TOL_PERMIL, \
            f"{mol} 298K baseline: {ln10b:.3f} vs expected {expected:.3f}"


def test_frequency_product_diagnostic_convention(freqs):
    """Lock the heavy/light convention R_f = prod(nu(34S)/nu(32S)) of the
    frequency-product diagnostic (first-order self-consistency check)."""
    for mol, expected in DIAGNOSTIC.items():
        got = sf.frequency_product_diagnostic(freqs[mol]["32S"], freqs[mol]["34S"])
        assert abs(got - expected) <= DIAG_TOL, \
            f"{mol} diagnostic {got:.6f} != expected {expected:.6f} " \
            f"(R_f = prod(nu_34S / nu_32S))"


def test_tracked_results_consistency(freqs):
    """Recompute from frequencies.csv and compare against tracked results.csv
    at every tracked temperature point."""
    labels = {sf.MOLECULES[m]["label"]: m for m in sf.MOLECULES}
    tracked = {m: {} for m in sf.MOLECULES}
    with open(MODULE / "data" / "results.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T = int(float(row["T(K)"]))
            for label, mol in labels.items():
                tracked[mol][T] = float(row[f"{label}_1000lnb"])
    for mol in sf.MOLECULES:
        for T, ref in tracked[mol].items():
            recomputed = 1000.0 * math.log(sf.calc_beta(freqs[mol]["32S"], freqs[mol]["34S"], T))
            assert abs(recomputed - ref) <= TOL_PERMIL, \
                f"{mol} at {T} K: recomputed {recomputed:.3f} vs tracked {ref:.3f}"
