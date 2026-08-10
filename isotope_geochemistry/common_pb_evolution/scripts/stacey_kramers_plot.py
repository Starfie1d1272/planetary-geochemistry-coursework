#!/usr/bin/env python3
"""
Stacey & Kramers (1975) 两阶段 Pb 演化模型作图 — v3
修改：
  - 图1 图例标注母体来源 (238U/235U/232Th decay)
  - 图2 添加 4.57 Ga 初始点, 完善 3.7 Ga 转折标注
  - 高密度采样确保折点可见
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Module-relative output directory (works from any cwd)
OUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 衰变常数 (Ga^-1)
lam238 = 0.155125
lam235 = 0.98485
lam232 = 0.049475

# 初始 Pb (Canyon Diablo 陨石)
Pb206_0 = 9.307
Pb207_0 = 10.294
Pb208_0 = 29.476

T_earth = 4.57
t_break = 3.70

# 两阶段参数 (由数据反推)
mu1, mu2 = 7.20, 9.73
omega1, omega2 = 32.09, 36.91

# 阶段分界值
Pb206_break = Pb206_0 + mu1 * (np.exp(lam238 * T_earth) - np.exp(lam238 * t_break))
Pb207_break = Pb207_0 + (mu1 / 137.88) * (np.exp(lam235 * T_earth) - np.exp(lam235 * t_break))
Pb208_break = Pb208_0 + omega1 * (np.exp(lam232 * T_earth) - np.exp(lam232 * t_break))

# 高密度时间序列 (2000 点 → 折点清晰)
ages_all = np.linspace(T_earth, 0, 2000)

Pb206_all = np.zeros_like(ages_all)
Pb207_all = np.zeros_like(ages_all)
Pb208_all = np.zeros_like(ages_all)

for i, t in enumerate(ages_all):
    if t >= t_break:
        Pb206_all[i] = Pb206_0 + mu1 * (np.exp(lam238 * T_earth) - np.exp(lam238 * t))
        Pb207_all[i] = Pb207_0 + (mu1 / 137.88) * (np.exp(lam235 * T_earth) - np.exp(lam235 * t))
        Pb208_all[i] = Pb208_0 + omega1 * (np.exp(lam232 * T_earth) - np.exp(lam232 * t))
    else:
        Pb206_all[i] = Pb206_break + mu2 * (np.exp(lam238 * t_break) - np.exp(lam238 * t))
        Pb207_all[i] = Pb207_break + (mu2 / 137.88) * (np.exp(lam235 * t_break) - np.exp(lam235 * t))
        Pb208_all[i] = Pb208_break + omega2 * (np.exp(lam232 * t_break) - np.exp(lam232 * t))

# 标记点 (用户计算结果)
marker_ages = [4.0, 3.7, 3.0, 2.0, 1.0, 0]
marker_206 = [10.544, 11.152, 12.930, 15.158, 17.066, 18.699]
marker_207 = [12.313, 12.998, 14.343, 15.192, 15.509, 15.627]
marker_208 = [30.599, 31.177, 32.683, 34.745, 36.709, 38.577]

# ========== 图1: 三曲线演化图 ==========
fig1, ax1 = plt.subplots(figsize=(8, 5))

color1, color2, color3 = '#2166ac', '#d6604d', '#4dac26'

ax1.plot(ages_all, Pb206_all, color=color1, linewidth=1.5,
         label='$^{206}$Pb/$^{204}$Pb ($^{238}$U decay)')
ax1.plot(ages_all, Pb207_all, color=color2, linewidth=1.5,
         label='$^{207}$Pb/$^{204}$Pb ($^{235}$U decay)')
ax1.plot(ages_all, Pb208_all, color=color3, linewidth=1.5,
         label='$^{208}$Pb/$^{204}$Pb ($^{232}$Th decay)')

ax1.scatter(marker_ages, marker_206, color=color1, s=30, zorder=5, marker='o')
ax1.scatter(marker_ages, marker_207, color=color2, s=30, zorder=5, marker='s')
ax1.scatter(marker_ages, marker_208, color=color3, s=30, zorder=5, marker='^')

# 阶段分界线
ax1.axvline(x=t_break, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
ax1.text(t_break + 0.08, ax1.get_ylim()[1] * 0.95,
         f'{t_break} Ga\n(Stage boundary)', fontsize=8, color='gray', va='top')

ax1.set_xlabel('Age (Ga)')
ax1.set_ylabel('Pb isotope ratio')
ax1.set_xlim(T_earth, 0)
ax1.set_xticks([4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0])
ax1.legend(frameon=True, fontsize=9)
ax1.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_DIR / 'figure1_evolution.png',
            dpi=200, bbox_inches='tight')
plt.close()
print("Figure 1 saved (annotated legend, high-res).")

# ========== 图2: Pb-Pb 演化图 ==========
fig2, ax2 = plt.subplots(figsize=(7, 6))

stage1 = ages_all >= t_break
stage2 = ages_all < t_break

ax2.plot(Pb206_all[stage1], Pb207_all[stage1],
         color='#4393c3', linewidth=2, label='Stage 1 (4.57–3.70 Ga)', zorder=2)
ax2.plot(Pb206_all[stage2], Pb207_all[stage2],
         color='#d6604d', linewidth=2, label='Stage 2 (3.70–0 Ga)', zorder=2)

# 计算节点
ax2.scatter(marker_206, marker_207, color='k', s=36, zorder=5, marker='o')
ax2.scatter(marker_206, marker_207, color='white', s=16, zorder=6, marker='o')

for x, y, a in zip(marker_206, marker_207, marker_ages):
    ax2.annotate(f'{a} Ga', (x, y), textcoords='offset points',
                 xytext=(6, 6), fontsize=9)

# 标注 4.57 Ga 初始点
ax2.scatter([Pb206_0], [Pb207_0], color='#4393c3', s=50, zorder=5, marker='*',
            edgecolors='k', linewidths=0.6)
ax2.annotate('4.57 Ga\n(Initial Pb)', (Pb206_0, Pb207_0),
             textcoords='offset points', xytext=(-65, 12),
             fontsize=9, color='#4393c3', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#4393c3', lw=1.0))

# 标注 3.7 Ga 转折点
ax2.annotate('T₁ = 3.70 Ga\nStage 1 → Stage 2\n(µ: 7.20 → 9.73)',
             (Pb206_break, Pb207_break),
             textcoords='offset points', xytext=(-100, -25),
             fontsize=9, color='#333333',
             arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', fc='#ffffcf', ec='#999999', alpha=0.85))

ax2.set_xlabel('$^{206}$Pb/$^{204}$Pb')
ax2.set_ylabel('$^{207}$Pb/$^{204}$Pb')
ax2.legend(frameon=True, fontsize=10)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_DIR / 'figure2_PbPb.png',
            dpi=200, bbox_inches='tight')
plt.close()
print("Figure 2 saved (with 4.57 Ga initial point + 3.7 Ga transition).")

# ========== 验证折点 ==========
# 在 3.7 Ga 附近选点验证斜率变化
print("\nKink verification (derivative at t_break):")
# stage 1 side (approaching from above)
t_above = t_break + 1e-6
d206_s1 = -mu1 * lam238 * np.exp(lam238 * t_above)
d207_s1 = -(mu1/137.88) * lam235 * np.exp(lam235 * t_above)
# stage 2 side (approaching from below)
t_below = t_break - 1e-6
d206_s2 = -mu2 * lam238 * np.exp(lam238 * t_below)
d207_s2 = -(mu2/137.88) * lam235 * np.exp(lam235 * t_below)

print(f"  206Pb/204Pb slope (stage 1 side): {d206_s1:.4f}")
print(f"  206Pb/204Pb slope (stage 2 side): {d206_s2:.4f}")
print(f"  Ratio (s2/s1): {d206_s2/d206_s1:.3f}")
print(f"  207Pb/204Pb slope (stage 1 side): {d207_s1:.4f}")
print(f"  207Pb/204Pb slope (stage 2 side): {d207_s2:.4f}")

print("\nDone.")
