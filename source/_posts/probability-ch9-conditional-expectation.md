---
title: 概率论第九章「条件期望」— 概率推断中最强大的工具
date: 2026-05-29 15:00:00
categories:
  - 数学
  - 概率论
tags:
  - 条件期望
  - 全期望定律
  - 全方差定律
  - Adam定律
  - Eve定律
  - Stat110
  - Blitzstein
mathjax: true
---

## 为什么第九章是"全书最重要的分水岭"

如果从全书中只挑一章来讲，应该是第九章。

前八章你学会了描述随机性——分布、联合分布、期望、方差、矩、变换。这些都是**工具**。第九章教你的是**策略**：如何把一个复杂问题，通过设定一个条件变量，拆解成你已经会做的简单问题。

> **核心洞察**：条件期望本身是一个随机变量——它随着你"知道的信息"变化。这不是一个定义技巧，而是一套完整的问题分解方法论。

本章的两大支柱——**Adam 定律**（全期望定律）和 **Eve 定律**（全方差定律）——让你能够：
- 把含有随机个数随机变量的和（如 $S_N = X_1 + \cdots + X_N$）的期望和方差化为已知量的组合
- 把总变异分解为"组内变异"和"组间变异"——这是 ANOVA 的核心思想
- 用**条件化策略**解决那些直接计算会让积分完全失控的问题

这一章也是后续所有统计推断的基础。第九章之后的每一章，你都会不断地使用 Adam's Law 和 Eve's Law。

## 前置知识

- 第三章离散随机变量（PMF、条件概率）
- 第四章期望（期望的线性、LOTUS）
- 第五章连续随机变量（条件 PDF）
- 第六章方差与协方差
- 第八章分布变换（Gamma、Poisson、指数分布的性质）

## 一、条件期望 I：给定事件

### 1.1 定义

如果 $A$ 是一个事件且 $P(A) > 0$，条件期望 $E(Y \mid A)$ 就是把条件 PDF/PMF 代入期望公式：

$$E(Y \mid A) = \begin{cases} \sum_y y \cdot P(Y=y \mid A) & \text{(离散)} \\ \int_{-\infty}^{\infty} y \cdot f_{Y|A}(y) \, dy & \text{(连续)} \end{cases}$$

其中条件 PDF 定义为 $f_{Y|A}(y) = \frac{f_Y(y)}{P(A)}$ 对 $y \in A$ 支撑（其余为 0）。

> **直觉**：就是把 Y 的世界限制到 $A$ 发生的那部分，然后在那个子世界里重新归一化，取期望。

**例子**：$X \sim \text{Expo}(\lambda)$，求 $E(X \mid X > t)$。由无记忆性，$X-t \mid X>t \sim \text{Expo}(\lambda)$，所以 $E(X \mid X>t) = t + E(X-t \mid X>t) = t + \frac{1}{\lambda}$。

### 1.2 全期望定律（事件版）

这是 LOE（Law of Total Expectation）的最简单形式：

$$E(Y) = E(Y \mid A) P(A) + E(Y \mid A^c) P(A^c)$$

推广到多个互斥事件 $A_1, \ldots, A_n$ 构成样本空间的一个划分：

$$E(Y) = \sum_{i=1}^{n} E(Y \mid A_i) P(A_i)$$

它与全概率定律的结构完全平行——你只是把每个 $P(\cdot \mid A_i)$ 换成了 $E(\cdot \mid A_i)$。

> 这是从"条件概率"到"条件期望"最自然的过渡，也是第九章推开的第一扇门。

## 二、条件期望 II：给定随机变量

### 2.1 $E(Y \mid X)$ 是一个随机变量

这是本章最重要的观念跃迁。$E(Y \mid X)$ 不是数，而是**一个以 $X$ 为自变量的函数**：

$$E(Y \mid X) = g(X), \quad \text{其中 } g(x) = E(Y \mid X=x)$$

每当 $X$ 取一个具体值 $x$，$E(Y \mid X)$ 也相应地取值 $g(x)$。因此 $E(Y \mid X)$ 与 $X$ 有相同的"分辨率"——当我们知道 $X$ 时，也就知道了 $E(Y \mid X)$。

> **直觉**：$E(Y \mid X)$ 是"根据你知道了 $X$ 之后，你对 $Y$ 期望的最佳猜测"。它不是真实的 $Y$，但它是用 $X$ 的信息能做出的**均方误差最优的预测**。

### 2.2 核心性质

条件期望继承了无条件期望的全部操作性质，外加一些独特的条件性质：

| 性质 | 公式 | 直觉 |
|------|------|------|
| **线性** | $E(aY_1 + bY_2 \mid X) = aE(Y_1 \mid X) + bE(Y_2 \mid X)$ | 条件不破坏线性 |
| **拿出已知** | $E(h(X)Y \mid X) = h(X)E(Y \mid X)$ | 已知 $X$ 时，$h(X)$ 被视为常数 |
| **独立性** | $E(Y \mid X) = E(Y)$ 若 $X, Y$ 独立 | 知道 $X$ 对预测 $Y$ 无帮助 |
| **套叠性** | $E(E(Y \mid X) \mid X) = E(Y \mid X)$ | 条件期望的条件期望还是它自己 |
| **常数性** | $E(c \mid X) = c$ | 已知的东西就是确定的 |

"拿出已知"（taking out what's known）是最常用也最容易忘的性质。它的逻辑是：**既然我们已经知道 $X$ 的值，那么 $X$ 的函数 $h(X)$ 就是确定的数**，可以当作常数从条件期望中提出来。

### 2.3 例子：$X, Y \sim \text{Pois}(\lambda)$ i.i.d.

- $E(X + Y \mid X) = X + E(Y \mid X) = X + \lambda$（拿出 $X$ 已知，$Y$ 独立于 $X$）
- $E(X \mid X + Y) = \frac{X+Y}{2}$（由对称性，两 i.i.d. 变量的和已知时，每个的期望是和的一半）

第二条展示了一个强大的技术：**对称性条件化**。当 $X$ 和 $Y$ 是 i.i.d. 时，给定它们的和 $S$，每个分量有相同的条件期望，从而 $E(X \mid S) = S/2$。

## 三、Adam 定律：全期望定律

### 3.1 陈述

$$\boxed{E(Y) = E\!\left(E(Y \mid X)\right)}$$

读作："$Y$ 的期望 = $Y$ 对 $X$ 的条件期望的（无条件）期望"。

证明非常简短（以连续情况为例）：

$$E(E(Y \mid X)) = \int E(Y \mid X=x) \cdot f_X(x)\,dx = \int\!\!\!\int y\, f_{Y|X}(y|x) f_X(x)\, dy\, dx = \int\!\!\!\int y\, f_{X,Y}(x,y)\, dx\, dy = E(Y)$$

### 3.2 条件化策略

Adam 定律的真正威力不是证明本身，而是它给出的**解题策略**：

> 每当 $E(Y)$ 难以直接计算时，找一个合适的条件变量 $X$，希望 $E(Y \mid X)$（以及 $E(Y \mid X)$ 的期望）更容易处理。

这是概率论中最通用的策略之一，本章的 9.6 节（Adam and Eve Examples）展示了它在多种经典场景下的应用。

### 3.3 经典例子：随机和

设 $N$ 是非负整值随机变量，$X_1, X_2, \ldots$ i.i.d. 且独立于 $N$，$S_N = \sum_{i=1}^{N} X_i$。由 Adam's Law：

$$E(S_N) = E(E(S_N \mid N)) = E(N \cdot E(X_1)) = E(N) \cdot E(X_1)$$

如果 $N$ 和 $X$ 不独立，这个公式不成立，但 Adam 定律仍然适用——只需计算 $E(S_N \mid N=n)$ 后对 $N$ 取期望。

### 3.4 条件化在两个变量上的推广

Adam 定律可以递推：

$$E(Y) = E\!\left(E(Y \mid X_1, X_2)\right) = E\!\left[E\!\left(E(Y \mid X_1, X_2) \mid X_1\right)\right]$$

这在多级分层模型中非常有用——你可以在最方便的那一层计算条件期望，再逐层取期望。

## 四、Eve 定律：全方差定律

### 4.1 陈述

$$\boxed{\text{Var}(Y) = E(\text{Var}(Y \mid X)) + \text{Var}(E(Y \mid X))}$$

- **第一项** $E(\text{Var}(Y \mid X))$：组内变异——$X$ 的分组内部 $Y$ 的随机波动
- **第二项** $\text{Var}(E(Y \mid X))$：组间变异——不同 $X$ 分组之间的均值差异

这正是 ANOVA（方差分析）的核心结构。整本统计教材中关于"总变异 = 组内变异 + 组间变异"的讨论，都源自这一个公式。

### 4.2 证明

令 $g(X) = E(Y \mid X)$。用 Adam 定律：

$$\begin{aligned} E(\text{Var}(Y \mid X)) &= E(E(Y^2 \mid X) - g(X)^2) = E(Y^2) - E(g(X)^2) \\ \text{Var}(g(X)) &= E(g(X)^2) - (E(g(X)))^2 = E(g(X)^2) - (E(Y))^2 \end{aligned}$$

两式相加：$E(Y^2) - (E(Y))^2 = \text{Var}(Y)$。$\square$

### 4.3 理解 Eve 定律

> 如果你用 $X$ 来预测 $Y$，预测值为 $E(Y \mid X)$，那么：
> - $\text{Var}(E(Y \mid X))$ 衡量的是**预测值本身的波动**（预测在不同 $X$ 下变多少）
> - $E(\text{Var}(Y \mid X))$ 衡量的是**预测误差的大小**（知道 $X$ 后还剩多少不确定性）

如果把 $X$ 想成"组标签"（如性别、年龄段），那么 $\text{Var}(E(Y\mid X))$ 就是组均值之间的差距，$E(\text{Var}(Y\mid X))$ 就是组内个体的差异。

### 4.4 经典例子：随机和的方差

在 $S_N = \sum_{i=1}^{N} X_i$ 中，用 Eve 定律：

$$\text{Var}(S_N) = E(N) \cdot \text{Var}(X_1) + \text{Var}(N) \cdot (E(X_1))^2$$

这个公式拆解了随机和方差的**两个来源**：每个 $X_i$ 自身的不确定性 + $N$ 的不确定性。当 $n$ 固定时（$\text{Var}(N)=0$），公式退回 $\text{Var}(S_n) = n \,\text{Var}(X_1)$。

## 五、条件期望的几何直觉（简述）

在 $L^2$ 空间中（所有方差有限的随机变量构成的内积空间），条件期望 $E(Y \mid X)$ 是 $Y$ 到**所有 $X$ 的函数构成的子空间**上的**正交投影**。

这意味着：
- $E(Y \mid X)$ 是所有 $h(X)$ 形式的函数中使均方误差 $E[(Y - h(X))^2]$ 最小的那个
- 残差 $Y - E(Y \mid X)$ 与任意 $X$ 的函数**不相关**

这解释了为什么 $E(Y \mid X)$ 被称为"最佳预测"——它在 MSE 意义下最小化了用 $X$ 预测 $Y$ 的误差。

虽然本书将这一节标注为选学（9.4*），但这个投影视角是连接概率论与统计推断（回归分析）的关键桥梁。

## 概念全景图

```
                    条件期望  E(Y|X)
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    给定事件 E(Y|A)   给定 r.v. E(Y|X)   给定多变量 E(Y|X₁,...,Xₙ)
          │              │              │
          └──────┬───────┘              │
                 │                      │
           全期望定律            Eve 定律（全方差）
           Adam's Law:          Var(Y) = E(Var(Y|X))
           E(Y) = E(E(Y|X))            + Var(E(Y|X))
                 │                      │
          ┌──────┴──────┐        ┌──────┴──────┐
          │             │        │             │
     随机和的期望    条件策略   组内变异      组间变异
     E(Sₙ) = E(N)E(X₁)        (ANOVA 基础)
                 │                      │
                 └──────────┬───────────┘
                            │
                    概率推断的基础工具
                  （回归、贝叶斯、抽样理论）
```

## 精选习题

### 第一组：条件期望基础

**题 1（教材 9.2 | 睡梦中的邮件）**

Fred 睡觉时收到 $X$ 封正常邮件和 $Y$ 封垃圾邮件。$X \sim \text{Pois}(10)$、$Y \sim \text{Pois}(40)$ 且相互独立。醒来后发现共有 30 封新邮件。给定这个信息，正常邮件的期望数量是多少？

**▼ 答案与解析**

给定 $X+Y=30$。由于 $X$ 和 $Y$ 是独立的 Poisson 变量，$X \mid X+Y=30 \sim \text{Bin}(30, \frac{10}{10+40}) = \text{Bin}(30, \frac{1}{5})$。

这是 Poisson 分布的经典性质：两个独立 Poisson 的条件分布是二项分布，概率与各自的速率成比例。

因此 $E(X \mid X+Y=30) = 30 \times \frac{1}{5} = 6$。

**洞察**：给定独立 Poisson 之和的条件下，每个分量的行为就像从总数中按速率比例独立抽取的 Bernoulli 试验。

**训练点**：条件分布的性质、Poisson 分解。

---

**题 2（SP10-4 / 教材 9.31 | 垃圾邮件的到达时间）**

电子邮件以 i.i.d. $\text{Expo}(\lambda)$ 的间隔到达。每封邮件以概率 $p$ 是非垃圾邮件（$q=1-p$ 是垃圾邮件），独立于到达过程。设 $X$ 为第一封非垃圾邮件的到达时间。求 $E(X)$ 和 $\text{Var}(X)$。

**▼ 答案与解析**

令 $N$ 为第一封非垃圾邮件出现前的总邮件数（包含第一封非垃圾邮件本身）。$N-1 \sim \text{Geom}(p)$，即 $P(N=n) = pq^{n-1}$ 对 $n \geq 1$。

给定 $N=n$，$X = \sum_{i=1}^{n} X_i$，其中各 $X_i \sim \text{Expo}(\lambda)$ i.i.d.。

**求期望**：用 Adam 定律，
$$E(X) = E(E(X \mid N)) = E\left(\frac{N}{\lambda}\right) = \frac{E(N)}{\lambda} = \frac{1/p}{\lambda} = \frac{1}{p\lambda}$$

**求方差**：用 Eve 定律，
$$\text{Var}(X) = E(\text{Var}(X \mid N)) + \text{Var}(E(X \mid N)) = E\left(\frac{N}{\lambda^2}\right) + \text{Var}\left(\frac{N}{\lambda}\right) = \frac{1}{p\lambda^2} + \frac{1-p}{p^2\lambda^2} = \frac{1}{p^2\lambda^2}$$

**洞察**：有趣的一点是 $X \sim \text{Expo}(p\lambda)$——第一封非垃圾邮件的到达时间仍然服从指数分布，只是速率被"稀释"了。这是 Poisson 过程随机稀释（thinning）性质的直接推论。

**训练点**：Adam 定律 + Eve 定律的联合使用，Poisson 过程稀释。

---

**题 3（教材 9.11 | 硬币序列中的模式：HT vs HH）**

抛掷一枚公平硬币（$p=1/2$）。
- (a) 求首次出现"HT"模式所需的期望抛掷次数。
- (b) 求首次出现"HH"模式所需的期望抛掷次数。

**▼ 答案与解析**

**(a) 期望抛掷次数直到 HT**：令 $w_{HT}$ 为期望值。条件化于第一次抛掷：
- 若第一次是 T（概率 1/2）：T 对 HT 无贡献，从第二次重新开始，期望增加 $1 + w_{HT}$
- 若第一次是 H（概率 1/2）：此时若再来 T 则完成，若再来 H 则还在 H 状态。令 $w_{T}$ 为"当前处于已有一个 H"时还需等待的期望次数。由无记忆性，$w_T = (1/2)(1) + (1/2)(1 + w_T)$，解得 $w_T = 2$。所以从 H 开始的总期望是 $1 + w_T = 3$

因此 $w_{HT} = \frac{1}{2}(1 + w_{HT}) + \frac{1}{2} \cdot 3$，解得 $w_{HT} = 4$。

**(b) 期望抛掷次数直到 HH**：令 $w_{HH}$ 为期望值。同样条件化第一次抛掷：
- 若第一次 T（概率 1/2）：从第二次重新开始，$1 + w_{HH}$
- 若第一次 H（概率 1/2）：从 H 状态出发，需要等第二个 H。令 $w_H$ 为当前已有一个 H 时还需等待的期望次数。$w_H = \frac{1}{2}(1) + \frac{1}{2}(1 + w_{HH})$（因为若再来 T，所有进度清零！）

故 $w_{HH} = \frac{1}{2}(1 + w_{HH}) + \frac{1}{2}(1 + w_H) = \frac{1}{2}(1 + w_{HH}) + \frac{1}{2}\left(1 + \frac{1}{2} + \frac{1}{2}(1 + w_{HH})\right)$

解得 $w_{HH} = 6$。

**洞察**：$\mathbb{E}(W_{HH}) = 6 > 4 = \mathbb{E}(W_{HT})$。HH 比 HT 慢的原因在于两者的"失败后状态"不同：HT 失败（出现 HH）后还剩一个 H 可以利用；HH 失败（出现 HT）后一切归零。这是一个经典的第一次经过时间（first-passage time）问题。

**训练点**：第一次经过分析、条件化策略。

---

### 第二组：Eve 定律与条件方差

**题 4（SP10-2 / 教材 9.18 | 证明 Eve 定律）**

证明全方差定律：
$$\text{Var}(Y) = E(\text{Var}(Y \mid X)) + \text{Var}(E(Y \mid X))$$

**▼ 答案与解析**

令 $g(X) = E(Y \mid X)$。

第一项的展开：
$$E(\text{Var}(Y \mid X)) = E\!\left[E(Y^2 \mid X) - (E(Y \mid X))^2\right] = E(E(Y^2 \mid X)) - E(g(X)^2) = E(Y^2) - E(g(X)^2)$$

最后一步用了 Adam 定律：$E(E(Y^2 \mid X)) = E(Y^2)$。

第二项的展开（用方差定义 + Adam 定律）：
$$\text{Var}(g(X)) = E(g(X)^2) - (E(g(X)))^2 = E(g(X)^2) - (E(Y))^2$$

其中 $E(g(X)) = E(E(Y \mid X)) = E(Y)$ 再次用了 Adam 定律。

两式相加：$(E(Y^2) - E(g(X)^2)) + (E(g(X)^2) - (E(Y))^2) = E(Y^2) - (E(Y))^2 = \text{Var}(Y)$。$\square$

**洞察**：Eve 定律的证明几乎完全依赖 Adam 定律。如果你理解了 Adam 定律，Eve 定律只是一个代数量身定做的应用。这也是为什么这两个定律总是配对出现。

**训练点**：条件期望的代数操作、从 Adam 到 Eve 的逻辑链。

---

**题 5（SP10-5 / 教材 9.24 | 两种硬币的混合）**

有两枚外观相同的硬币：一枚正面概率 $p_1$，另一枚正面概率 $p_2$。随机选择一枚（概率各 $1/2$），抛掷 $n$ 次。设 $X$ 为正面次数。求 $E(X)$ 和 $\text{Var}(X)$。

**▼ 答案与解析**

设 $I$ 为指示选到 $p_1$ 硬币的随机变量（Bernoulli，参数 $1/2$）。

条件化于 $I$：
- 若 $I=1$：$X \sim \text{Bin}(n, p_1)$，期望 $np_1$，方差 $np_1(1-p_1)$
- 若 $I=0$：$X \sim \text{Bin}(n, p_2)$，期望 $np_2$，方差 $np_2(1-p_2)$

**期望**（Adam 定律）：
$$E(X) = E(E(X \mid I)) = \frac{1}{2}np_1 + \frac{1}{2}np_2 = \frac{n}{2}(p_1 + p_2)$$

**方差**（Eve 定律）：
$$E(\text{Var}(X \mid I)) = \frac{1}{2}np_1(1-p_1) + \frac{1}{2}np_2(1-p_2)$$

$$E(X \mid I) = I \cdot np_1 + (1-I) \cdot np_2 = np_2 + n(p_1-p_2)I$$

$$\text{Var}(E(X \mid I)) = n^2(p_1-p_2)^2 \cdot \text{Var}(I) = n^2(p_1-p_2)^2 \cdot \frac{1}{4}$$

因此：
$$\text{Var}(X) = \frac{1}{2}\!\left[np_1(1-p_1) + np_2(1-p_2)\right] + \frac{n^2}{4}(p_1 - p_2)^2$$

**洞察**：如果 $p_1 = p_2$，第二项消失，$X \sim \text{Bin}(n, p_1)$。如果 $p_1 \neq p_2$，第二项是正的——$X$ **不是**二项分布，即使它的期望和某个二项分布相同。这是混合分布不等于其组成部分的经典例子。

**训练点**：Eve 定律在混合模型中的应用、混合分布不等于简单分布。

---

**题 6（SP10-3 / 教材 9.23 | 残差的性质）**

对于有有限方差的随机变量 $X$ 和 $Y$，定义残差 $W = Y - E(Y \mid X)$。
- (a) 证明 $E(W) = 0$ 和 $E(W \mid X) = 0$。
- (b) 额外假设 $W \mid X \sim N(0, X^2)$ 且 $X \sim N(0, 1)$，求 $\text{Var}(W)$。

**▼ 答案与解析**

**(a)** 由 Adam 定律：$E(W) = E(Y - E(Y \mid X)) = E(Y) - E(E(Y \mid X)) = E(Y) - E(Y) = 0$。

条件化于 $X$：$E(W \mid X) = E(Y - E(Y \mid X) \mid X) = E(Y \mid X) - E(Y \mid X) = 0$。

**(b)** 用 Eve 定律：
$$\text{Var}(W) = E(\text{Var}(W \mid X)) + \text{Var}(E(W \mid X))$$

由 (a)，$E(W \mid X) = 0$，故第二项为 0。已知 $\text{Var}(W \mid X) = X^2$，所以：
$$\text{Var}(W) = E(X^2) = E(X^2) = \text{Var}(X) + (E(X))^2 = 1 + 0 = 1$$

（因为 $X \sim N(0,1)$，所以 $E(X^2) = \text{Var}(X) = 1$。）

**洞察**：$E(W \mid X) = 0$ 说明在知道 $X$ 之后，残差的条件期望为零——这意味着 $E(Y \mid X)$ 是 $Y$ 的无偏预测。随后 Eve 定律优雅地将条件方差转化为无条件方差。

**训练点**：Adam 定律的代数操作、条件方差与无条件方差的转化。

---

### 第三组：条件期望与对称性

**题 7（教材 9.15 | i.i.d. 变量加权和的条件期望）**

设 $X_1, X_2, \ldots, X_n$ i.i.d.，样本均值为 $\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i$。对于常数 $w_1, \ldots, w_n$ 满足 $\sum_{i=1}^{n} w_i = 1$，求：
$$E(w_1 X_1 + \cdots + w_n X_n \mid \bar{X}_n)$$

**▼ 答案与解析**

由对称性：给定 $\bar{X}_n$（即给定 $\sum X_i$），所有 $X_i$ 有相同的条件分布。因此：
$$E(X_1 \mid \bar{X}_n) = E(X_2 \mid \bar{X}_n) = \cdots = E(X_n \mid \bar{X}_n)$$

将这些条件期望相加：
$$E\left(\sum_{i=1}^{n} X_i \;\middle|\; \bar{X}_n\right) = n \cdot E(X_1 \mid \bar{X}_n)$$

但左边就是 $\sum_{i=1}^{n} X_i = n\bar{X}_n$（条件已知时可以"拿出"），所以：
$$n\bar{X}_n = n \cdot E(X_1 \mid \bar{X}_n) \implies E(X_1 \mid \bar{X}_n) = \bar{X}_n$$

因此：
$$E\left(\sum_{i=1}^{n} w_i X_i \;\middle|\; \bar{X}_n\right) = \sum_{i=1}^{n} w_i E(X_i \mid \bar{X}_n) = \sum_{i=1}^{n} w_i \cdot \bar{X}_n = \bar{X}_n$$

**洞察**：任意权重和的 i.i.d. 条件期望等于样本均值本身——只要权重之和为 1。这是对称性条件化最精美的应用之一：给定总和时，每个分量的条件期望都相同，等于总和的 $1/n$。

**训练点**：对称性 + 条件期望、拿出已知的技巧。

---

**题 8（教材 9.17 | 室友对）**

$2n$ 名学生被分成 $n$ 对室友。每人以概率 $p$ 独立地选一门课。设 $X$ 为选课总人数，$Y$ 为两人都选课的室友对数。求 $E(Y \mid X)$ 和 $E(Y)$。

**▼ 答案与解析**

**(a) 求 $E(Y \mid X)$**：给定 $X = k$（恰好 $k$ 人选课），$k$ 人均匀分布在 $2n$ 人中。

对于任意一对特定的室友，两人都选课的概率（给定 $X=k$）等于从 $2n$ 人中选 $k$ 人的超几何概率：
$$P(\text{该对都选} \mid X=k) = \frac{\binom{2n-2}{k-2}}{\binom{2n}{k}} = \frac{k(k-1)}{2n(2n-1)}$$

由线性：
$$E(Y \mid X=k) = n \cdot \frac{k(k-1)}{2n(2n-1)} = \frac{k(k-1)}{2(2n-1)}$$

因此：
$$E(Y \mid X) = \frac{X(X-1)}{2(2n-1)}$$

**(b) 求 $E(Y)$**：用 Adam 定律：
$$E(Y) = E(E(Y \mid X)) = \frac{E(X^2) - E(X)}{2(2n-1)}$$

$X \sim \text{Bin}(2n, p)$，故 $E(X) = 2np$，$E(X^2) = \text{Var}(X) + (E(X))^2 = 2np(1-p) + (2np)^2$。

代入：
$$E(Y) = \frac{2np(1-p) + 4n^2p^2 - 2np}{2(2n-1)} = \frac{4n^2p^2 - 2np^2}{2(2n-1)} = np^2$$

（经过化简后得到 $E(Y) = np^2$。）

**洞察**：虽然每个室友对的选择不是独立的（给定 $X$ 后是相关事件），但线性仍然成立。而且最终 $E(Y) = np^2$ 令人愉悦——恰好等于"如果各对独立时"的期望。这说明无条件的期望 $E(Y)$ 不受室友配对这一依赖结构的影响。

**训练点**：条件化于总数后的超几何分布、Adam 定律与线性性质的配合。

---

## 本章核心脉络

### 三个层次

1. **技术层面**：$E(Y \mid A)$（给定事件）$\to$ $E(Y \mid X)$（给定 r.v.）$\to$ Adam 定律 $\to$ Eve 定律。这四个概念构成了一条逻辑链，后一个以前一个为基础。

2. **策略层面**：条件化是将复杂问题拆解为简单问题的**通用策略**。选定合适的条件变量 $X$ 之后，先计算 $E(Y \mid X)$（此时 $X$ 被视为已知），再对 $X$ 取期望（用 Adam 定律）。同样的策略也适用于方差（用 Eve 定律）。

3. **观念层面**：$E(Y \mid X)$ 是 $Y$ 的**最佳 MSE 预测**。它不再是传统的"期望一个数"，而是一个**信息敏感的函数**——你知道了多少，条件期望就回应多少。这是从概率论到统计推断（以及贝叶斯方法）的概念桥梁。

### 如果你只从这一章带走三样东西

1. **$E(Y \mid X)$ 是随机变量**，不是数。它是 $X$ 的函数，代表"知道了 $X$ 之后对 $Y$ 的最佳预测"。

2. **Adam 定律** $E(Y) = E(E(Y \mid X))$ 和 **Eve 定律** $\text{Var}(Y) = E(\text{Var}(Y \mid X)) + \text{Var}(E(Y \mid X))$ 是全书最重要的两个计算工具。掌握它们，就能处理从随机和到分层模型的一切。

3. **条件化是一种策略，不是一个公式**。面对复杂问题时问自己："如果我知道了一个关键变量 $X$ 的值，这个问题的答案会变得多简单？"如果答案变得简单，那就应该条件化于 $X$。

## 参考文献

1. **教材**：Blitzstein, J. K. & Hwang, J. (2019). *Introduction to Probability* (2nd ed.). CRC Press. Chapter 9: Conditional Expectation (pp. 415–451).

2. **Stat 110 课程录像**：
   - Lecture 25: Order Statistics and Conditional Expectation（末尾部分开始涉及条件期望）
   - Lecture 26: Conditional Expectation Continued（Two Envelope Paradox、HT vs HH、$E(Y|X)$ 作为随机变量）
   - Lecture 27: Conditional Expectation Given an R.V.（Adam's Law、Eve's Law 的完整呈现）
   - 以上录像可在 YouTube 搜索 "Harvard Stat 110 Lecture 25/26/27"

3. **Stat 110 Strategic Practice 10**：Conditional Expectation & Conditional Variance（SP10 第 1 节），含 5 道完整的条件期望和条件方差习题及详细解答。可在 Harvard Stat 110 课程网站获取。

4. **补充参考**：
   - Ross, S. (2019). *A First Course in Probability* (10th ed.). Pearson. Chapter 7: Properties of Expectation —— 提供了条件期望的另一种处理方式。
   - 习题 3 的模式分析参考 Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*, Vol. 1. Wiley. Chapter on recurrent events.
