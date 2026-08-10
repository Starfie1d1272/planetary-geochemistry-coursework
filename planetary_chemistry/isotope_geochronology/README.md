# Problem 2
> Coursework artifact · Nanjing University · 2026  
> Original course module: Planetary Chemistry · HW2 · isotope geochronology

**学生姓名：** 杜鑫宇

---

## 1. 月球样品的 Bi 分析

### 1.1 物理背景与已知参数

首先列出并查阅所需的参数：

*   **样本总质量**：$m = 20 \times 10^{-3} \text{ g}$
*   **目标元素质量分数**：$c = 3 \times 10^{-9}$
*   **反应堆最大中子通量**：$\Phi = 5 \times 10^{14} \text{ neutrons}/(\text{cm}^2\cdot\text{s})$
*   **计划辐照时间**：$t_i = 5.0 \text{ d}$
*   **探测器测量效率**：$\epsilon = 25\%$
*   **目标检测下限**：$5 \text{ cpm}$

自然界中铋为单同位素元素，丰度为 100%，因此靶核均为 $^{209}\text{Bi}$，其相对原子质量 $M \approx 208.98 \text{ g/mol}$，阿伏伽德罗常数 $N_A \approx 6.022 \times 10^{23} \text{ mol}^{-1}$。

由题目所给条件，$^{209}\text{Bi}$ 俘获热中子后由两个不同的中子俘获截面生成两个不同的能量态。其中长寿命亚稳态 $^{210m}\text{Bi}$ 的截面为 10 mb，但因其半衰期长达 $3 \times 10^6 \text{ a}$，在 5 天的实验周期内衰变极少，对短时探测计数无有效贡献，故不予考虑。生成 $^{210}\text{Bi}$ 基态的反应截面为 $\sigma = 24 \text{ mb} = 24 \times 10^{-27} \text{ cm}^2$。目标核素 $^{210}\text{Bi}$ 基态的半衰期 $T_{1/2} = 5.01 \text{ d}$。

### 1.2 理论公式与推导

首先计算样本中靶核 $^{209}\text{Bi}$ 的原子总数 $N_0$：
$$
N_0 = \frac{m \cdot c}{M} N_A
$$

辐照结束时刻，生成的 $^{210}\text{Bi}$ 放射性活度 $A_0$ 由活化方程给出：
$$
A_0 = N_0 \Phi \sigma (1 - e^{-\lambda t_i})
$$
式中 $\lambda = \frac{\ln 2}{T_{1/2}}$ 为衰变常数，$(1 - e^{-\lambda t_i})$ 为活化饱和因子。

为与题目要求的计数率标准进行对比，需将活度单位自国际单位制 Bq（次/秒，dps）转换为每分钟衰变数（dpm），再结合探测效率 $\epsilon$ 求出仪器的预期计数率 $R$（cpm）：
$$
A_0 (\text{dpm}) = A_0 (\text{Bq}) \times 60
$$
$$
R = A_0 (\text{dpm}) \times \epsilon
$$

### 1.3 计算与结果

将数值代入，计算得到 $^{210}\text{Bi}$ 的活度 $A_0 = 1.0359 \text{ Bq}$，对应的计数率为 $R = 15.5392 \text{ cpm}$。这个数值远大于题目要求的下限 $5 \text{ cpm}$，因此我们可以达到题目的要求。

## 2. 正氢与仲氢

### 2.1 物理背景与已知参数

由题，主要已知物理量与常数如下：

*   **氢气转动惯量**：$I = 0.046 \times 10^{-46} \text{ kg}\cdot\text{m}^2$
*   **环境温度**：$T = 300 \text{ K}$
*   **氢气分子对称数**：$\sigma = 2$
*   **普朗克常数**：$h \approx 6.626 \times 10^{-34} \text{ J}\cdot\text{s}$
*   **玻尔兹曼常数**：$k \approx 1.381 \times 10^{-23} \text{ J/K}$

### 2.2 理论公式与推导

由转动能级公式 $\varepsilon_J = \frac{h^2}{8\pi^2 I} J(J+1)$，可定义分子的转动特征温度 $\Theta_{rot}$：
$$
\Theta_{rot} = \frac{h^2}{8\pi^2 I k}
$$

当不考虑核自旋与奇偶能级分裂，且满足高温近似（$T \gg \Theta_{rot}$）时，总的转动配分函数为：
$$
q_{rot} = \frac{T}{\sigma \Theta_{rot}}
$$

由题目条件，正氢和仲氢的配分函数（忽略高阶微小项，各取前三项求和）分别为：
$$
q_{rot, \text{ortho}} = 3 \sum_{J=1,3,5} (2J+1)e^{-J(J+1)\Theta_{rot}/T}
$$
$$
q_{rot, \text{para}} = \sum_{J=0,2,4} (2J+1)e^{-J(J+1)\Theta_{rot}/T}
$$
$300 \text{ K}$ 下正氢与仲氢的平衡比例即为二者各自配分函数之比。

### 2.3 计算与结果

代入各项参数，计算 $\text{H}_2$ 的转动特征温度与近似配分函数：
$$
\Theta_{rot} = \frac{(6.626 \times 10^{-34})^2}{8\pi^2 \times (0.046 \times 10^{-46}) \times (1.381 \times 10^{-23})} \approx 87.53 \text{ K}
$$
$$
q_{rot, \text{approx}} = \frac{300}{2 \times 87.53} \approx 1.714
$$

分别计算 $300 \text{ K}$ 下正氢与仲氢配分函数前三项并求和：
*   **正氢配分函数（$J=1, 3, 5$）**：
    $$
    q_{rot, \text{ortho}} \approx 9e^{-2(87.53)/300} + 21e^{-12(87.53)/300} + 33e^{-30(87.53)/300} \approx 5.021 + 0.633 + 0.005 = 5.659
    $$
*   **仲氢配分函数（$J=0, 2, 4$）**：
    $$
    q_{rot, \text{para}} \approx 1e^{0} + 5e^{-6(87.53)/300} + 9e^{-20(87.53)/300} \approx 1.000 + 0.868 + 0.026 = 1.894
    $$

最终计算 $300 \text{ K}$ 下正氢与仲氢的平衡比例：
$$
\frac{q_{rot, \text{ortho}}}{q_{rot, \text{para}}} = \frac{5.659}{1.894} \approx 2.988
$$

**结论**：$\text{H}_2$ 分子的转动特征温度为 **$87.53 \text{ K}$**；由高温近似公式计算得到的转动配分函数为 **$1.714$**。在 $300 \text{ K}$ 下，精确计算得到的正氢配分函数为 **$5.659$**，仲氢为 **$1.894$**，此时正氢和仲氢的平衡比例约为 **$2.99 : 1$**（可见在室温下，其平衡比例已极度逼近核自旋简并度的高温极限理论值 $3:1$）。

## 3. 合成氨反应

### 3.1 物理背景与已知参数

查阅 NIST Chemistry WebBook，提取合成氨反应中各气态物质（$\text{N}_2$, $\text{H}_2$, $\text{NH}_3$）的基础热力学数据。在标准状态（$298.15 \text{ K}, 1 \text{ bar}$）下，各物质的标准摩尔生成焓（$\Delta_f H^\circ$）与标准摩尔熵（$S^\circ$）如下：
*   $\text{N}_2(g)$: $\Delta_f H^\circ_{298} = 0 \text{ kJ/mol}, \quad S^\circ_{298} = 191.61 \text{ J/(mol}\cdot\text{K)}$
*   $\text{H}_2(g)$: $\Delta_f H^\circ_{298} = 0 \text{ kJ/mol}, \quad S^\circ_{298} = 130.68 \text{ J/(mol}\cdot\text{K)}$
*   $\text{NH}_3(g)$: $\Delta_f H^\circ_{298} = -45.90 \text{ kJ/mol}, \quad S^\circ_{298} = 192.77 \text{ J/(mol}\cdot\text{K)}$

为计算 $500 \text{ }^\circ\text{C}$（$773.15 \text{ K}$）下的热力学性质，提取适用于该温度区间的 Shomate 经验方程系数。理想气体常数 $R = 8.314 \text{ J/(mol}\cdot\text{K)}$。
Shomate 方程参数表（针对包含 $773.15 \text{ K}$ 的温度区间）：
*   $\text{N}_2(g)$ ($500-2000 \text{ K}$): $A=19.5058, B=19.8870, C=-8.5985, D=1.3698, E=0.5276, F=-4.9352, G=212.3900, H=0.0$
*   $\text{H}_2(g)$ ($298-1000 \text{ K}$): $A=33.0662, B=-11.3634, C=11.4328, D=-2.7729, E=-0.1586, F=-9.9808, G=172.7080, H=0.0$
*   $\text{NH}_3(g)$ ($298-1400 \text{ K}$): $A=19.9956, B=49.7712, C=-15.3760, D=1.9212, E=0.1892, F=-53.3067, G=203.8591, H=-45.8981$

### 3.2 理论公式与推导

合成氨反应的化学方程式为：$N_2(g) + 3H_2(g) \rightleftharpoons 2NH_3(g)$

标准状态（$298.15 \text{ K}$）下，反应的标准摩尔焓变与熵变为：
$$ \Delta_r H^\circ_{298} = \sum \nu_i \Delta_f H^\circ_{i,298} $$
$$ \Delta_r S^\circ_{298} = \sum \nu_i S^\circ_{i,298} $$

对于任意温度 $T$ 的高温状态，需结合 Shomate 经验方程计算焓差 $[H^\circ(T) - H^\circ(298.15)]$ 及绝对熵 $S^\circ(T)$（式中 $t = T/1000$）：
$$ H^\circ - H^\circ_{298.15}= A t + \frac{B t^2}{2} + \frac{C t^3}{3} + \frac{D t^4}{4} - \frac{E}{t} + F - H $$
$$ S^\circ = A \ln(t) + B t + \frac{C t^2}{2} + \frac{D t^3}{3} - \frac{E}{2t^2} + G $$
进而求得目标温度下的 $\Delta_r H^\circ_T$ 与 $\Delta_r S^\circ_T$：
$$ \Delta_r H^\circ_T = \Delta_r H^\circ_{298} + \sum \nu_i [H^\circ_i(T) - H^\circ_{i}(298.15)] $$
$$ \Delta_r S^\circ_T = \sum \nu_i S^\circ_{i}(T) $$

反应的标准吉布斯自由能变及平衡常数 $K$ 的关系为：
$$ \Delta_r G^\circ_T = \Delta_r H^\circ_T - T\Delta_r S^\circ_T $$
$$ K = \exp\left(-\frac{\Delta_r G^\circ_T}{RT}\right) $$

### 3.3 计算与结果

(1) 标准状态（$298.15 \text{ K}$）下的计算

将 $298.15 \text{ K}$ 的基础数据代入公式，得：
*   $\Delta_r H^\circ_{298} = 2(-45.90) - (0 + 3 \times 0) = -91.80 \text{ kJ/mol}$
*   $\Delta_r S^\circ_{298} = 2(192.77) - (191.61 + 3 \times 130.68) = -198.11 \text{ J/(mol}\cdot\text{K)}$
*   $\Delta_r G^\circ_{298} = -91800 - 298.15 \times (-198.11) = -32733.5 \text{ J/mol}$
计算得出平衡常数 **$K_{298} \approx 5.43 \times 10^5$**。由于 $K_{298} \gg 1$ 且 $\Delta_r G^\circ < 0$，该反应在标准状态下具有极强的自发正向趋势。因此，氨气在标准状态下具有高度热力学稳定性，不会倾向于分解。

(2) 合成氨通常条件（$773.15 \text{ K}$）下的计算

利用 Shomate 方程参数及 $t = 0.77315$，计算各物质在 $773.15 \text{ K}$ 的焓差与绝对熵：
*   $\text{N}_2(g)$: 焓差 $= 14.20 \text{ kJ/mol}, \quad S^\circ_{773} = 219.95 \text{ J/(mol}\cdot\text{K)}$
*   $\text{H}_2(g)$: 焓差 $= 13.91 \text{ kJ/mol}, \quad S^\circ_{773} = 158.54 \text{ J/(mol}\cdot\text{K)}$
*   $\text{NH}_3(g)$: 焓差 $= 20.48 \text{ kJ/mol}, \quad S^\circ_{773} = 232.74 \text{ J/(mol}\cdot\text{K)}$

代入反应物与产物的化学计量数，求得高温下反应的总热力学量：
*   $\Delta_r H^\circ_{773} = -91.80 +[2(20.48) - (14.20 + 3 \times 13.91)] = -106.77 \text{ kJ/mol}$
*   $\Delta_r S^\circ_{773} = 2(232.74) - (219.95 + 3 \times 158.54) = -230.09 \text{ J/(mol}\cdot\text{K)}$
*   $\Delta_r G^\circ_{773} = -106770 - 773.15 \times (-230.09) = 71124.5 \text{ J/mol}$
计算得出高温平衡常数 **$K_{773} \approx 1.56 \times 10^{-5}$**。由于 $K_{773} \ll 1$ 且 $\Delta_r G^\circ > 0$，在 $500 \text{ }^\circ\text{C}$ 下热力学平衡极大地倾向于反应物，合成反应不再自发。