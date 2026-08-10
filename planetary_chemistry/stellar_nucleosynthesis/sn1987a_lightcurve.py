import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 定义常数与衰变率
# ==========================================
t_half_ni = 5.9
t_half_co = 77.3

lam_ni = np.log(2) / t_half_ni
lam_co = np.log(2) / t_half_co

# ==========================================
# 2. 提前计算公式中的各项系数 (用于打印最终公式)
# ==========================================
# 形状函数 S(t) = lam_ni * exp(-lam_ni*t) + factor * (exp(-lam_co*t) - exp(-lam_ni*t))
# 合并同类项后: S(t) = (lam_ni - factor) * exp(-lam_ni*t) + factor * exp(-lam_co*t)

factor = (lam_ni * lam_co) / (lam_ni - lam_co)
C_Ni = lam_ni - factor  # Ni 衰变项的最终系数
C_Co = factor           # Co 衰变项的最终系数

# 计算 500 天时的形状函数值 S(500)
t_norm = 500
S_500 = C_Ni * np.exp(-lam_ni * t_norm) + C_Co * np.exp(-lam_co * t_norm)

# 计算对数截距 log_K
log_K = 40.45 - np.log10(S_500)

# ==========================================
# 3. 打印最终的数值公式给你的作业本！
# ==========================================
print("\n" + "="*50)
print("根据 Python 自动推算，你可以将以下公式抄写在作业上：\n")
print(f"1. 衰变常数: λ_Ni = {lam_ni:.5f} d^-1,  λ_Co = {lam_co:.5f} d^-1")
print(f"2. 归一化常数: log_K = {log_K:.4f}")
print("\n最终用于绘图的数值光变曲线公式为：")
print(f"log L(t) = {log_K:.4f} + log10[ {C_Ni:.5f} * exp(-{lam_ni:.5f} * t) + {C_Co:.5f} * exp(-{lam_co:.5f} * t) ]")
print("="*50 + "\n")

# ==========================================
# 4. 矩阵运算生成曲线数据
# ==========================================
t = np.linspace(0, 800, 1000)
S_t = C_Ni * np.exp(-lam_ni * t) + C_Co * np.exp(-lam_co * t)
log_L = log_K + np.log10(S_t)

# ==========================================
# 5. 绘图出图
# ==========================================
plt.figure(figsize=(10, 6), dpi=150)
plt.plot(t, log_L, color='red', linewidth=2, label='Theoretical: ${}^{56}$Ni $\\rightarrow$ ${}^{56}$Co $\\rightarrow$ ${}^{56}$Fe')
plt.scatter(500, 40.45, color='blue', s=60, zorder=5, label='Normalization Point (500d, 40.45)')

plt.xlim(0, 800)
plt.ylim(38.5, 43.5)
plt.title('SN 1987A Theoretical Light Curve (Pure Radioactive Decay)', fontsize=14, pad=15)
plt.xlabel('Days since Core Collapse', fontsize=12)
plt.ylabel('log L (erg/s)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()