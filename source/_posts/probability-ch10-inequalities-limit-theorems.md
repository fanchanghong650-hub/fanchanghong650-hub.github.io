---
title: 概率论第十章「不等式与极限定理」— 从概率论到统计推断的第一道门
date: 2026-05-29 08:40:00
categories:
  - 数学
  - 概率论
tags:
  - 不等式
  - 大数定律
  - 中心极限定理
  - Markov不等式
  - Chebyshev不等式
  - Jensen不等式
  - 卡方分布
  - Stat110
  - Blitzstein
mathjax: true
---

## 为什么第十章是概率论和统计学的交汇点

前十章中的大部分时间，我们都在做"正向计算"：已知分布，求概率、期望、方差。第十章首次系统地教你做**反向推断**：在不知道完整分布的情况下，用有限的矩信息来**界定**概率，或者用**极限行为**来近似复杂的抽样分布。

这一章的三条主线分别回答了三个不同层次的问题：

1. **不等式**：我只知道均值和方差，能对概率说什么？
2. **大数定律（LLN）**：当样本量趋于无穷时，样本均值的行为是什么？
3. **中心极限定理（CLT）**：标准化后的样本均值，它的**分布**趋近于什么？

> **核心洞察**：不等式给你的是**保证**（对于任意有限的 $n$），LLN 给你的是**收敛**（$n \to \infty$ 时的确定性行为），CLT 给你的是**近似分布**（$n$ 大但有限时的分布形态）。三者构成了从有限样本到渐近推断的完整链条。

掌握这三样东西，你就拥有了从数据推断总体的**第一套完整工具**。

## 前置知识

- 第四章期望与方差
- 第六章矩母函数（MGF）——CLT 的证明会用到
- 第五章连续分布（尤其是正态分布）
- 第八章 Gamma 分布（卡方分布的基础）

## 一、不等式工具箱：用矩信息界定概率

当你不完全知道一个分布的形态时，不等式让你能用**已知的矩**（如均值 $\mu$、方差 $\sigma^2$）来给出概率的**上界**。

### 1.1 Markov 不等式：最基础但最通用

设 $X$ 是一个非负随机变量。对任意 $a > 0$：

$$\boxed{P(X \geq a) \leq \frac{E(X)}{a}}$$

**证明**非常优雅：定义指示变量 $I = I(X \geq a)$。则 $aI \leq X$（因为当 $X \geq a$ 时 $aI = a \leq X$，当 $X < a$ 时 $aI = 0 \leq X$）。取期望：$aP(X \geq a) = E(aI) \leq E(X)$。$\square$

> **直觉**：如果均值只有 10，那 $X \geq 100$ 的概率不可能超过 10%。否则那 10%+ 的观测就会把均值拉得太高。

Markov 不等式唯一的前提是 $X \geq 0$（几乎必然），这是它如此通用的代价——上界通常很松，但它**永远正确**，而且极难绕过（任何更紧的界都需要额外的假设）。

### 1.2 Chebyshev 不等式：把方差也用起来

对任意随机变量 $Y$（不需要非负！）和任意 $c > 0$：

$$\boxed{P(|Y - E(Y)| \geq c) \leq \frac{\text{Var}(Y)}{c^2}}$$

**推导**：令 $X = (Y - E(Y))^2$，这是一个非负随机变量。对 $X$ 用 Markov 不等式，取 $a = c^2$：
$$P(|Y - E(Y)| \geq c) = P((Y - E(Y))^2 \geq c^2) \leq \frac{E((Y - E(Y))^2)}{c^2} = \frac{\text{Var}(Y)}{c^2}$$

> **直觉**：方差越小，分布越集中。以方差 $\sigma^2$ 为例，任何分布落在均值 $\pm k\sigma$ 之外的概率不超过 $1/k^2$。无论分布是什么形状。

Chebyshev 的界限通常也是松的，但对于**任意分布**它都成立——这已经是你能得到的最好的、只依赖方差的无分布界。

### 1.3 Cauchy-Schwarz 不等式：乘积的界

$$\boxed{|E(XY)| \leq \sqrt{E(X^2) E(Y^2)}}$$

等号成立当且仅当 $X$ 和 $Y$ 线性相关（$P(aX = bY) = 1$ 对某 $a, b$）。

一个重要的特例：取 $Y=1$，得 $E(|X|) \leq \sqrt{E(X^2)}$，说明二阶矩存在则一阶矩也存在。

由 Cauchy-Schwarz 可以直接推出**相关系数**的范围：$|\rho| \leq 1$：
$$|\text{Cov}(X,Y)| = |E((X-\mu_X)(Y-\mu_Y))| \leq \sqrt{E((X-\mu_X)^2)E((Y-\mu_Y)^2)} = \sigma_X \sigma_Y$$

### 1.4 Jensen 不等式：凸函数和期望的次序

如果 $g$ 是**凸函数**，则：

$$\boxed{E(g(X)) \geq g(E(X))}$$

如果 $g$ 是**严格凸的**，除非 $X$ 是常数，否则是严格不等号。

> **直觉**：凸函数的"在期望处的值" $\leq$ "在值上的期望"。换言之，期望不穿过凸函数——把凸函数放在期望里面比放在外面更大。

经典例子：
- $E(X^2) \geq (E(X))^2$（$g(x) = x^2$ 是凸函数）
- $E(1/X) > 1/E(X)$ 对正的非退化 $X$（$g(x) = 1/x$ 在 $(0, \infty)$ 上是严格凸的）
- $E(\log X) \leq \log E(X)$（$g(x) = -\log x$ 是凸的，取负号）

### 1.5 不等式之间的证明链

这四个不等式存在清晰的逻辑层次：

```
Markov（最基本，只需 X ≥ 0）
  ├── Chebyshev（对 (Y-μ)² 用 Markov）
  ├── Chernoff 界（对 e^{tX} 用 Markov，再对 t 优化）
  └── Jensen（证明风格不同，不依赖 Markov）
```

> 「Markov 是"不等式之母"。几乎所有用矩来界定概率的界，最终都源自对某个非负变换后的变量使用 Markov 不等式。」

## 二、大数定律：均值如何"确定"下来

### 2.1 弱大数定律（WLLN）

设 $X_1, X_2, \ldots, X_n$ i.i.d.，均值为 $\mu$，方差为 $\sigma^2$（有限）。样本均值 $\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i$ 满足：对任意 $\varepsilon > 0$，

$$\boxed{P(|\bar{X}_n - \mu| > \varepsilon) \to 0 \quad \text{当 } n \to \infty}$$

**证明**（只需方差存在）：$E(\bar{X}_n) = \mu$，$\text{Var}(\bar{X}_n) = \sigma^2/n$。用 Chebyshev：
$$P(|\bar{X}_n - \mu| > \varepsilon) \leq \frac{\text{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2} \to 0$$

> **直觉**：样本量足够大时，样本均值和真实均值之间的任意正差距都变得几乎不可能。这证明了"用频率估计概率"的合理性。

这叫**依概率收敛**，记作 $\bar{X}_n \xrightarrow{p} \mu$。

### 2.2 强大数定律（SLLN）

比 WLLN 更强（同样的 i.i.d. 条件，仅需有限均值）：

$$\boxed{P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1}$$

这称为**几乎必然收敛**（almost sure convergence），记作 $\bar{X}_n \xrightarrow{a.s.} \mu$。

> **区别**：WLLN 说对于大的 $n$，$\bar{X}_n$ 很有可能接近 $\mu$。SLLN 说以概率 1，序列 $\bar{X}_1, \bar{X}_2, \ldots$ 最终稳定在 $\mu$ 附近且不再偏离。SLLN 保证了"一次实验中的每一次长序列"都会收敛，而 WLLN 只保证"在大量独立实验中，大多数序列会收敛"。

SLLN 的证明比 WLLN 复杂得多（需要 Borel-Cantelli 引理或 Kolmogorov 不等式），本书侧重陈述和应用。

### 2.3 LLN 为何重要

- 它解释了**频率派统计学的哲学基础**：概率是长期频率的极限
- 它为 **Monte Carlo 积分**提供理论保证：$\frac{1}{n}\sum f(X_i) \to E(f(X))$
- 它是 CLT 的前提——先确认 $\bar{X}_n$ 收敛到的那个数 $\mu$，再问 "收敛速度"和"极限分布"

## 三、中心极限定理：万物归于正态

### 3.1 定理陈述

设 $X_1, \ldots, X_n$ i.i.d.，均值为 $\mu$，方差为 $\sigma^2$（有限）。则：

$$\boxed{\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} = \frac{\sum_{i=1}^{n} X_i - n\mu}{\sqrt{n}\,\sigma} \xrightarrow{d} \mathcal{N}(0, 1)}$$

"$\xrightarrow{d}$" 表示**依分布收敛**（convergence in distribution）——CDF 逐点收敛到标准正态的 CDF $\Phi$。

> **三条深层洞见**：
> 1. **极限分布不依赖于原始分布**：无论 $X_i$ 是离散、连续、偏态还是对称，标准化后的样本均值在大样本下都近似正态。
> 2. **$\sqrt{n}$ 的缩放是精确的**：缩小得比 $\sqrt{n}$ 慢则发散（方差爆炸），缩小得比 $\sqrt{n}$ 快则退化为常数（LLN）。$\sqrt{n}$ 恰好"停住"了随机性。
> 3. **CLT 给出了"收敛速度"**：$|\bar{X}_n - \mu|$ 的量级是 $O_P(1/\sqrt{n})$。

### 3.2 二项分布的正态近似

经典应用：$X \sim \text{Bin}(n, p)$。由 CLT（$X$ 是 $n$ 个 i.i.d. Bernoulli 之和）：

$$\frac{X - np}{\sqrt{np(1-p)}} \;\dot\sim\; \mathcal{N}(0, 1)$$

**连续性校正**（continuity correction）：由于 $X$ 是离散的而正态是连续的，计算 $P(a \leq X \leq b)$ 时用：
$$P(a \leq X \leq b) \approx \Phi\!\left(\frac{b + 0.5 - np}{\sqrt{npq}}\right) - \Phi\!\left(\frac{a - 0.5 - np}{\sqrt{npq}}\right)$$

经验规则：当 $np \geq 10$ 且 $n(1-p) \geq 10$ 时，正态近似通常是可以接受的。当 $p$ 非常接近 0 或 1 时，Poisson 近似可能更好。

### 3.3 MGF 证明（梗概）

假设 MGF $M(t)$ 在 $t=0$ 附近存在。不失一般性，设 $\mu=0, \sigma=1$（否则标准化）。令 $S_n = \sum_{i=1}^{n} X_i$：

$$M_{S_n / \sqrt{n}}(t) = E(e^{t S_n / \sqrt{n}}) = [M(t / \sqrt{n})]^n$$

取对数并做 Taylor 展开（用到 $M'(0) = E(X) = 0$，$M''(0) = E(X^2) = 1$）：
$$\log M_{S_n / \sqrt{n}}(t) = n \log M(t / \sqrt{n}) = n \left[\frac{t^2}{2n} + o\!\left(\frac{1}{n}\right)\right] \to \frac{t^2}{2}$$

而 $t^2/2$ 正是 $\mathcal{N}(0,1)$ 的对数 MGF。由 MGF 的唯一性，极限分布为 $\mathcal{N}(0,1)$。

## 四、卡方分布与 t 分布：CLT 的衍生分布

第二版在 10.4 节新增了这两个在统计推断中至关重要的分布。

### 4.1 卡方分布（Chi-Square）

若 $Z_1, \ldots, Z_n \sim \mathcal{N}(0,1)$ i.i.d.，则：

$$\boxed{V = \sum_{i=1}^{n} Z_i^2 \sim \chi^2_{(n)}}$$

$n$ 称为**自由度**（degrees of freedom）。$\chi^2_{(n)}$ 是 Gamma 分布的特例：$\chi^2_{(n)} = \text{Gamma}(n/2, 1/2)$。

> **直觉**：$n$ 个独立标准正态的平方和。在回归分析中，残差平方和（除以 $\sigma^2$）就服从卡方分布——这是所有 F 检验和 t 检验的基础。

关键性质：
- $E(V) = n$，$\text{Var}(V) = 2n$
- 若 $V \sim \chi^2_{(n)}$ 且 $W \sim \chi^2_{(m)}$ 独立，则 $V+W \sim \chi^2_{(n+m)}$

### 4.2 Student's t 分布

若 $Z \sim \mathcal{N}(0,1)$，$V \sim \chi^2_{(n)}$，且 $Z, V$ 独立，则：

$$\boxed{T = \frac{Z}{\sqrt{V / n}} \sim t_{(n)}}$$

> **直觉**：t 分布是"当你不知道总体方差，用样本方差代替时"产生的分布。分母中的 $\sqrt{V/n}$ 引入了额外的随机性，使得 t 分布的尾部比正态更重——反映了用估计量代替参数的代价。

当 $n \to \infty$ 时，$t_{(n)} \to \mathcal{N}(0,1)$（因为 $V/n \xrightarrow{p} 1$）。对于 $n \geq 30$，正态近似通常足够好。

## 概念全景图

```
              概率推断的三大支柱
                     │
     ┌───────────────┼───────────────┐
     │               │               │
  不等式          大数定律        中心极限定理
  (Ch 10.1)       (Ch 10.2)        (Ch 10.3)
     │               │               │
     │               │               │
  ┌──┴──┐      ┌────┴────┐     ┌────┴────┐
  │     │      │         │     │         │
Markov Chebyshev WLLN    SLLN   CLT    衍生分布
  │     │      │         │     │    (χ², Student's t)
  │     │      │         │     │         │
  └──┬──┘      └────┬────┘     └────┬────┘
     │              │              │
     有限 n 的保证   n→∞ 的收敛    n 大时的分布近似
     "保底"        "收敛到哪里"    "怎么收敛"
                     │              │
                     └──────┬───────┘
                            │
                    统计推断的数学基础
                  （置信区间、假设检验）
```

## 精选习题

### 第一组：不等式

**题 1（SP10-2.2 | Jensen 不等式的两个应用）**

设 $X$ 是正的、非常数的随机变量。用 Jensen 不等式证明：
- (a) $E(1/X) > 1 / E(X)$
- (b) $E(X/Y) \cdot E(Y/X) > 1$，其中 $X, Y$ 是 i.i.d. 正随机变量。

**▼ 答案与解析**

**(a)** $g(x) = 1/x$ 在 $(0, \infty)$ 上严格凸（二阶导数 $g''(x) = 2/x^3 > 0$）。由 Jensen 不等式（严格版本，因 $X$ 非常数）：
$$E(1/X) > 1 / E(X)$$

**(b)** 由于 $X$ 和 $Y$ 是 i.i.d.，由对称性 $E(X/Y) = E(Y/X)$。将 Jensen 不等式用于 $g(x) = -\log x$（凸函数）：
$$E(\log(X/Y)) = E(\log X - \log Y) = 0 < \log E(X/Y)$$

但由 Jensen，$\log E(X/Y) > E(\log(X/Y)) = 0$，因此 $E(X/Y) > 1$。同理 $E(Y/X) > 1$。两者相乘得 $E(X/Y)E(Y/X) > 1$。

**洞察**：比值期望天然地大于 1——即使 $X$ 和 $Y$ 同分布且对称。这与直觉"比值应该围绕 1"形成了微妙的对比：Jensen 告诉我们 $E(X/Y) \neq 1/E(Y/X)$，因为 $1/x$ 的凸性在条件期望中制造了系统偏差。

**训练点**：识别凸函数、Jensen 不等式的严格性条件。

---

**题 2（SP10-2.3 | Chebyshev 与最小样本量）**

设 $X_1, \ldots, X_n$ i.i.d.，均值为 $\mu$，方差为 $\sigma^2$。希望样本均值 $\bar{X}_n$ 落在 $\mu \pm 2\sigma/\sqrt{n}$ 范围内的概率至少为 99%。用 Chebyshev 不等式求所需的最小 $n$。

**▼ 答案与解析**

由 Chebyshev（令 $c = 2\sigma/\sqrt{n}$）：
$$P(|\bar{X}_n - \mu| \geq \frac{2\sigma}{\sqrt{n}}) \leq \frac{\text{Var}(\bar{X}_n)}{(2\sigma/\sqrt{n})^2} = \frac{\sigma^2/n}{4\sigma^2/n} = \frac{1}{4}$$

因此 $P(|\bar{X}_n - \mu| < 2\sigma/\sqrt{n}) \geq 1 - 1/4 = 0.75$。这个概率与 $n$ 无关——Chebyshev 永远给出 75%。

等等，那题目要求 99% 怎么办？将 $c$ 参数化为 $k\sigma/\sqrt{n}$：
$$P(|\bar{X}_n - \mu| \geq \frac{k\sigma}{\sqrt{n}}) \leq \frac{1}{k^2}$$

要 $1 - 1/k^2 \geq 0.99$，需 $1/k^2 \leq 0.01$，即 $k \geq 10$。

所以范围需要是 $\mu \pm 10\sigma/\sqrt{n}$。此时 Chebyshev 保证概率 $\geq 99$%。

当 $n \geq 25$ 时，$10\sigma/\sqrt{25} = 2\sigma$，即 $\bar{X}_{25}$ 以 99% 概率落在 $\mu \pm 2\sigma$ 内。

（注：如果用 CLT 代替 Chebyshev——在 $n$ 大时成立——$k=10$ 对应的概率是 $\Phi(10) - \Phi(-10) \approx 1$，远优于 99%。但 Chebyshev 在**任何** $n$ 下都成立，不需要渐近近似。）

**洞察**：Chebyshev 给出的是"无分布"的保守界。真实分布若接近正态，CLT 会给出更紧的界，但 Chebyshev 的好处是它对任何分布都无条件成立。

**训练点**：Chebyshev 不等式的应用、无分布界与渐近界的区别。

---

**题 3（SP10-2.4 | 用 Jensen 证明 AM-GM 不等式）**

用概率方法证明算术-几何平均不等式：对正数 $x_1, \ldots, x_n$，
$$(x_1 x_2 \cdots x_n)^{1/n} \leq \frac{x_1 + x_2 + \cdots + x_n}{n}$$

**▼ 答案与解析**

构造一个随机变量 $X$，以等概率 $1/n$ 取每个 $x_i$。则：
$$E(X) = \frac{1}{n}\sum_{i=1}^{n} x_i \quad \text{（算术平均）}$$

对 $g(x) = \log x$（凹函数！）用 Jensen：
$$E(\log X) \leq \log(E(X))$$

而 $E(\log X) = \frac{1}{n}\sum_{i=1}^{n} \log x_i = \log((\prod x_i)^{1/n})$（对数的几何平均）。代入：
$$\log((x_1 \cdots x_n)^{1/n}) \leq \log\!\left(\frac{1}{n}\sum x_i\right)$$

取指数即得 AM-GM。

**洞察**：看似纯代数的不等式，在概率论的框架中只是一个均匀分布的 Jensen 不等式。这是概率论"跨域攻击"的美妙例子——用一个概率构造就把代数问题转化成了期望操作。

**训练点**：概率构造、凹函数与 Jensen 的方向。

---

### 第二组：大数定律

**题 4（SP11-4 | 和之比收敛于参数之比）**

设 $X_1, X_2, \ldots$ i.i.d. 正随机变量，均值为 2。设 $Y_1, Y_2, \ldots$ i.i.d. 正随机变量，均值为 3。证明：
$$\frac{X_1 + \cdots + X_n}{Y_1 + \cdots + Y_n} \to \frac{2}{3} \quad \text{以概率 1}$$

$X_i$ 和 $Y_j$ 是否独立是否影响结论？

**▼ 答案与解析**

由 SLLN（每个序列各自）：
$$\frac{1}{n}\sum_{i=1}^{n} X_i \to 2 \;\; \text{a.s.}, \quad \frac{1}{n}\sum_{i=1}^{n} Y_i \to 3 \;\; \text{a.s.}$$

两个几乎必然收敛的事件同时发生的概率也是 1。因此：
$$\frac{\sum X_i}{\sum Y_i} = \frac{\frac{1}{n}\sum X_i}{\frac{1}{n}\sum Y_i} \to \frac{2}{3} \quad \text{a.s.}$$

$X_i$ 和 $Y_j$ 之间**不需要独立**。SLLN 在每个序列内部单独成立（只要每个序列自己的元素是 i.i.d.），序列之间的相关性不影响各自收敛到各自的极限。两个极限之比就是 2/3。

**洞察**："i.i.d."的条件是对序列内部而言的，序列之间可以任意依赖——LLN 对此毫不在意。这是 LLN 强度的一个重要体现。

**训练点**：SLLN 的基本应用、独立性与收敛条件的关系。

---

**题 5（SP11-5 | Monte Carlo 积分）**

设 $f$ 是定义在 $[a,b]$ 上、满足 $0 \leq f(x) \leq c$ 的函数。在矩形 $[a, b] \times [0, c]$ 中均匀地、独立地抽取 $n$ 个点 $(X_i, Y_i)$。如何用这些点来估计 $\int_a^b f(x)\,dx$？用 LLN 证明这个方法的一致性。

**▼ 答案与解析**

对于每个点 $(X_i, Y_i)$，定义指示变量：
$$I_i = I(Y_i \leq f(X_i))$$

即该点落在曲线 $y = f(x)$ 下方的指示。由于点在矩形内均匀分布：
$$P(I_i = 1) = \frac{\text{曲线下方面积}}{\text{矩形面积}} = \frac{\int_a^b f(x)\,dx}{c(b-a)}$$

因此估计：
$$\hat{I} = c(b-a) \cdot \frac{1}{n}\sum_{i=1}^{n} I_i$$

由 SLLN，$\frac{1}{n}\sum I_i \to P(I_1 = 1) = \frac{\int_a^b f(x)\,dx}{c(b-a)}$ a.s.，故 $\hat{I} \to \int_a^b f(x)\,dx$ a.s.

**洞察**：这是 Monte Carlo 积分的理论基础。不需要解析地计算积分——只需要生成随机点，统计落在曲线下方的比例。在高维积分中，这是唯一可行的方法。

**训练点**：LLN 在 Monte Carlo 方法中的应用、概率构造。

---

### 第三组：中心极限定理

**题 6（SP11-1 | CLT 蕴含 WLLN 吗？）**

给出一个直观论证：为什么中心极限定理"蕴含"弱大数定律（忽略收敛形式的不同）。然后简要说明两者的收敛形式有何不同。

**▼ 答案与解析**

**直观论证**：CLT 说：
$$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

这意味着对于大的 $n$，$\bar{X}_n$ 近似分布为 $\mathcal{N}(\mu, \sigma^2/n)$。方差 $\sigma^2/n \to 0$，因此 $\bar{X}_n$ 的分布越来越集中到 $\mu$ 附近——这正是 WLLN 的结论。

更严格地：对任意 $\varepsilon > 0$，
$$P(|\bar{X}_n - \mu| > \varepsilon) = P\left(\frac{|\bar{X}_n - \mu|}{\sigma / \sqrt{n}} > \frac{\varepsilon \sqrt{n}}{\sigma}\right) \approx 2\left(1 - \Phi\!\left(\frac{\varepsilon \sqrt{n}}{\sigma}\right)\right) \to 0$$

（但这只是一个近似论证，因为在 CLT 的收敛意义上不能直接这样代换。）

**收敛形式的不同**：
- WLLN：**依概率收敛**——$P(|\bar{X}_n - \mu| > \varepsilon) \to 0$。只关心概率是否趋于 0。
- CLT：**依分布收敛**——CDF 逐点收敛。不仅告诉我们 $\bar{X}_n - \mu \to 0$，还告诉我们**缩放后的分布形态**趋于正态。

**洞察**：CLT 比 WLLN 更强，因为它给出了收敛的"速率"（$O(1/\sqrt{n})$）和"渐近分布"（正态）。但如果只关心一致性（估计量是否一致），LLN 通常就足够了。CLT 用于构建置信区间。

**训练点**：不同收敛模式的区别和层次关系。

---

**题 7（SP11-2 | Poisson 的正态近似与 Stirling 公式）**

- (a) 解释为什么 $\text{Pois}(n)$ 在 $n$ 大时近似于正态分布，并给出近似的正态参数。
- (b) 用 (a) 加上连续性校正，给出 Stirling 公式 $n! \approx \sqrt{2\pi n}\,(n/e)^n$ 的启发式推导。

**▼ 答案与解析**

**(a)** $\text{Pois}(n)$ 是 $n$ 个独立的 $\text{Pois}(1)$ 之和。由 CLT，标准化后收敛到 $\mathcal{N}(0,1)$：
$$\frac{N - n}{\sqrt{n}} \;\dot\sim\; \mathcal{N}(0, 1)$$

因此 $\text{Pois}(n) \;\dot\sim\; \mathcal{N}(n, n)$。**注意**：这里我们利用了 Poisson 的可加性——$n$ 个独立的 $\text{Pois}(1)$ 之和 = $\text{Pois}(n)$。

**(b)** 对 $N \sim \text{Pois}(n)$，其 PMF 在 $n$ 处的值为：
$$P(N = n) = e^{-n} \frac{n^n}{n!}$$

用一个 $\mathcal{N}(n, n)$ 的 PDF 加上连续性校正来近似：
$$P(N = n) \approx \int_{n-0.5}^{n+0.5} \frac{1}{\sqrt{2\pi n}} e^{-(x-n)^2/(2n)}\,dx \approx \frac{1}{\sqrt{2\pi n}} \cdot 1$$

因此：
$$e^{-n} \frac{n^n}{n!} \approx \frac{1}{\sqrt{2\pi n}} \implies n! \approx \sqrt{2\pi n}\,(n/e)^n$$

**洞察**：Stirling 公式——一个纯分析的组合恒等式——可以从概率的 CLT 中"跌出来"。这是 CLT 作为"万能近似器"的又一个惊艳展示。Poisson 被用作"中转站"：它既能表示为 i.i.d. 之和（适用 CLT），又有整洁的 PMF 形式（嵌入 $n!$）。

**训练点**：CLT 的创造性应用、Poisson 的双重角色。

---

**题 8（SP11-3 | Student-t 和的 CLT）**

设 $T_1, T_2, \ldots$ 是 i.i.d. 的 Student-t 随机变量，自由度为 $m \geq 3$。求常数 $a_n$ 和 $b_n$（用 $m$ 和 $n$ 表示）使得：
$$a_n (T_1 + T_2 + \cdots + T_n - b_n) \xrightarrow{d} \mathcal{N}(0, 1)$$

**▼ 答案与解析**

由于 $T_i$ i.i.d.，标准的 CLT 适用。需要 $E(T_i)$ 和 $\text{Var}(T_i)$。

对于 $t_{(m)}$ 分布（$m \geq 3$）：
- $E(T_i) = 0$（对称分布，$m > 1$ 时存在）
- $\text{Var}(T_i) = \frac{m}{m-2}$（$m > 2$ 时存在）

由 CLT（Lindberg-Levy）：
$$\frac{\sum_{i=1}^{n} T_i - n \cdot 0}{\sqrt{n \cdot \frac{m}{m-2}}} = \sqrt{\frac{m-2}{mn}} \sum_{i=1}^{n} T_i \xrightarrow{d} \mathcal{N}(0, 1)$$

因此：
$$b_n = 0, \quad a_n = \sqrt{\frac{m-2}{mn}}$$

**洞察**：CLT 对任何有有限二阶矩的 i.i.d. 序列都成立——包括 t 分布这样的厚尾分布。答案中 $a_n \propto 1/\sqrt{n}$ 是符合直觉的（样本均值的精度按 $1/\sqrt{n}$ 提升）。而 $\sqrt{(m-2)/m} < 1$ 反映了 t 分布的额外分散性——自由度越小，这个缩放因子越小。

**训练点**：CLT 标准化公式、t 分布的矩、$\xrightarrow{d}$ 记号的熟练使用。

---

## 本章核心脉络

### 三个层次

1. **不等式（有限样本）**：在只知道矩信息时给出概率的**上界**。Markov 是母不等式，Chebyshev 是它最著名的推论。Jensen 和 Cauchy-Schwarz 补充了期望操作中的不等式关系。

2. **大数定律（渐近确定性）**：样本量趋于无穷时，随机性消失——样本均值**确定性地**收敛于总体均值。WLLN 给依概率收敛，SLLN 给几乎必然收敛。它解释了我们为什么能用频率估计概率、能用 Monte Carlo 积分。

3. **中心极限定理（渐近分布）**：$\sqrt{n}$ 缩放后的样本均值**以正态分布为极限**。它告诉我们的不只是"收敛到哪"，而是"波动有多大、呈什么分布"——这是构建置信区间和假设检验的核心依据。

### 如果你只从这一章带走三样东西

1. **Markov 不等式** $P(X \geq a) \leq E(X)/a$ 是一切概率界的源头。记住它的前提（$X \geq 0$）和证明（$aI \leq X$），你就能随时重新导出 Chebyshev 和 Chernoff。

2. **CLT 让正态分布无处不在**。样本均值——无论原始分布是什么——在大样本下近似正态。这是统计学中一切"正态近似"和"$z$ 检验"的最终保障。

3. **LLN、CLT、不等式解决不同的问题**。LLN 解决"能不能"（一致性），CLT 解决"精度如何"（渐近分布），不等式解决"最坏情况"（有限样本保底）。选哪个工具，取决于你的问题在哪个层面上。

## 参考文献

1. **教材**：Blitzstein, J. K. & Hwang, J. (2019). *Introduction to Probability* (2nd ed.). CRC Press. Chapter 10: Inequalities and Limit Theorems (pp. 457–496).

2. **Stat 110 课程录像**：
   - Lecture 28: Inequalities（Markov、Chebyshev、Cauchy-Schwarz、Jensen）
   - Lecture 29: Law of Large Numbers and Central Limit Theorem（WLLN、SLLN、CLT、Monte Carlo 积分）
   - 以上录像可在 YouTube 搜索 "Harvard Stat 110 Lecture 28/29"

3. **Stat 110 Strategic Practice**：
   - SP10 第 2 节（Inequalities）：4 道不等式习题
   - SP11（Law of Large Numbers & Central Limit Theorem）：5 道 LLN/CLT 习题
   - 含详细解答，可在 Harvard Stat 110 课程网站获取

4. **补充参考**：
   - Ross, S. (2019). *A First Course in Probability* (10th ed.). Pearson. Chapter 8: Limit Theorems.
   - 卡方分布和 t 分布的深入讨论见 Casella, G. & Berger, R. L. (2002). *Statistical Inference* (2nd ed.). Duxbury. Chapters 5 and 8.
