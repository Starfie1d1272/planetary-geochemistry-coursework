"""Public-hygiene checks for the tracked public tree.

Scans tracked files only (git ls-files), so untracked local artifacts can
never leak into the check. The denylist literals in this test file itself are
excluded from the scan by design.
"""
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MAX_TRACKED_BYTES = 5 * 1024 * 1024  # 5 MiB

DENY_STRINGS = [
    "231830104", "231830008", "231830038", "231830040", "231830043",
    "231830053", "231830128", "231830133", "258354072",
    "XJZ", "MZY",
    "/Users/starfie1d", "D:\\GitHub", "D:\\Gaussian",
    "duxinyu475@gmail.com",
]

DENY_EXTENSIONS = [
    ".pdf", ".pptx", ".docx", ".xls", ".xlsx", ".xlsm",
    ".exe", ".msi", ".dmg", ".l6s", ".000",
    ".tif", ".tiff", ".fchk", ".chk", ".log",
]

DENY_PATH_PARTS = ["讲义", "PPT_for_assignment", "_Questions"]

# External raw database snapshot must not be redistributed.
DENY_FILENAMES = ["iac_exoplanet_atmospheres-20260624.csv"]


@pytest.fixture(scope="module")
def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True,
                         text=True, check=True)
    paths = [REPO / p for p in out.stdout.splitlines() if p]
    assert paths, "no tracked files found"
    return paths


def test_no_student_ids_or_personal_identifiers(tracked_files):
    for p in tracked_files:
        if p.name == "test_public_hygiene.py":
            continue
        if p.suffix in {".png", ".jpg", ".jpeg", ".gif"}:
            continue  # binary images are covered by filename scan only
        text = p.read_text(encoding="utf-8", errors="replace")
        for token in DENY_STRINGS:
            assert token not in text, f"{token!r} found in {p}"


def test_no_banned_filenames_or_paths(tracked_files):
    for p in tracked_files:
        name = p.name
        assert name not in DENY_FILENAMES, f"banned filename in tree: {p}"
        for ext in DENY_EXTENSIONS:
            assert not name.lower().endswith(ext), f"banned extension {ext}: {p}"
        for part in DENY_PATH_PARTS:
            assert part not in str(p), f"banned path part {part!r}: {p}"


def test_no_symlinks(tracked_files):
    for p in tracked_files:
        assert not p.is_symlink(), f"symlink in tracked tree: {p}"


def test_no_large_tracked_files(tracked_files):
    for p in tracked_files:
        size = p.stat().st_size
        assert size <= MAX_TRACKED_BYTES, \
            f"tracked file exceeds 5 MiB: {p} ({size} bytes)"
