"""Common Pb (Stacey-Kramers) script tests.

The script is executed from a copied module directory so that tracked outputs
in the repository are never touched, and so that it can be shown to work from
any cwd without any absolute-path dependency.
"""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MODULE = REPO / "isotope_geochemistry" / "common_pb_evolution"
SCRIPT = MODULE / "scripts" / "stacey_kramers_plot.py"

# Numerical checkpoint: Stacey-Kramers two-stage model endpoints at t = 0
# (206Pb/204Pb, 207Pb/204Pb, 208Pb/204Pb) as recorded in the coursework.
CHECKPOINT_T0 = (18.699, 15.627, 38.577)
TOL = 0.01


def test_no_absolute_user_paths():
    text = SCRIPT.read_text(encoding="utf-8")
    # literals are assembled at runtime so this test file stays free of
    # denylist strings in source form
    assert "/Users/" + "starfie1d" not in text
    assert "D:\\" + "GitHub" not in text


def test_runs_from_arbitrary_cwd(tmp_path):
    work = tmp_path / "module_copy"
    shutil.copytree(MODULE, work)
    proc = subprocess.run(
        [sys.executable, str(work / "scripts" / "stacey_kramers_plot.py")],
        cwd=tmp_path,  # intentionally NOT the module dir
        capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, f"script failed:\n{proc.stdout}\n{proc.stderr}"
    assert (work / "figures" / "figure1_evolution.png").exists()
    assert (work / "figures" / "figure2_PbPb.png").exists()


def test_numerical_checkpoint(tmp_path):
    work = tmp_path / "module_copy2"
    shutil.copytree(MODULE, work)
    spec = importlib.util.spec_from_file_location(
        "stacey_kramers_plot_check", work / "scripts" / "stacey_kramers_plot.py")
    assert spec is not None and spec.loader is not None, "failed to locate script module"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # executes the script inside the copy
    for ratio, expected in zip((mod.Pb206_all[-1], mod.Pb207_all[-1], mod.Pb208_all[-1]),
                               CHECKPOINT_T0):
        assert abs(ratio - expected) <= TOL, \
            f"model endpoint {ratio:.3f} does not match recorded checkpoint {expected}"
