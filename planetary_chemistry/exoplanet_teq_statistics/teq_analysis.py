import sys
import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Module-relative paths: figures are always written to the module's figures/
# directory, regardless of the cwd the script is invoked from.
# ---------------------------------------------------------------------------
MODULE_DIR = Path(__file__).resolve().parent
FIG_DIR = MODULE_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# The raw IAC ExoAtmospheres download is NOT redistributed with this
# repository (external database snapshot; see README.md for provenance).
# The script therefore requires the user to supply the dataset; it never
# silently substitutes other data.
parser = argparse.ArgumentParser(
    description="Equilibrium-temperature statistics from the IAC ExoAtmospheres "
                "database (coursework analysis).")
parser.add_argument("--csv", type=Path, required=True,
                    help="Path to the IAC ExoAtmospheres CSV download "
                         "(required; the dataset is not redistributed with this repository)")
args = parser.parse_args()

csv_path = args.csv
if not csv_path.exists():
    print(f"ERROR: input CSV not found: {csv_path}", file=sys.stderr)
    print("Input dataset is not redistributed with this repository.", file=sys.stderr)
    print("See README.md for data provenance and expected input schema/path.", file=sys.stderr)
    sys.exit(1)

df = pd.read_csv(csv_path, sep=';', quotechar='"')

# 1. 按行星名去重，避免同一颗行星因多篇观测记录被重复计数
planets = df.drop_duplicates(subset=['name']).copy()

# 2. 提取 Teq 并去掉缺失值
sub = planets[['name', 'temp_calculated', 'type', 'radius', 'mass']].copy()
sub['temp_calculated'] = pd.to_numeric(sub['temp_calculated'], errors='coerce')
sub = sub.dropna(subset=['temp_calculated'])

teq = sub['temp_calculated'].values

# 3. 基本统计
print("N =", len(teq))
print("min =", np.min(teq))
print("max =", np.max(teq))
print("mean =", np.mean(teq))
print("median =", np.median(teq))
print("Q1, Q3 =", np.percentile(teq, [25, 75]))

# 4. 分箱统计
bins = [0, 500, 1000, 1500, 2000, 2500, 4000]
cats = pd.cut(sub['temp_calculated'], bins=bins, right=False)
count_by_bin = sub.groupby(cats).size()
frac_by_bin = count_by_bin / len(sub) * 100
print(pd.DataFrame({"count": count_by_bin, "percent": frac_by_bin.round(1)}))

# 5. 直方图
plt.figure(figsize=(7.2, 5.2))
bins_hist = np.arange(0, 4050, 150)
plt.hist(teq, bins=bins_hist, edgecolor='black')
plt.xlabel("Equilibrium temperature Teq (K)")
plt.ylabel("Number of planets")
plt.title("Distribution of Teq in the IAC ExoAtmospheres database")
plt.tight_layout()
plt.savefig(FIG_DIR / "teq_histogram.png", dpi=300)

# 6. CDF
x = np.sort(teq)
y = np.arange(1, len(x) + 1) / len(x)
plt.figure(figsize=(7.2, 5.2))
plt.plot(x, y)
plt.xlabel("Equilibrium temperature Teq (K)")
plt.ylabel("Cumulative fraction")
plt.title("CDF of Teq")
plt.tight_layout()
plt.savefig(FIG_DIR / "teq_cdf.png", dpi=300)

# 7. Teq–radius 散点图
mask = sub['radius'].notna()
plt.figure(figsize=(7.2, 5.2))
plt.scatter(sub.loc[mask, 'temp_calculated'],
            pd.to_numeric(sub.loc[mask, 'radius'], errors='coerce'),
            s=20, alpha=0.7)
plt.xlabel("Equilibrium temperature Teq (K)")
plt.ylabel("Planet radius (R_earth)")
plt.title("Teq vs planet radius")
plt.tight_layout()
plt.savefig(FIG_DIR / "teq_radius.png", dpi=300)
