---
title: 概率论第八章「变换」— 从旧分布到新分布的完整工具箱
date: 2026-05-29 23:30:00
categories:
  - 数学
  - 概率论
tags:
  - 变量变换
  - 卷积
  - Beta分布
  - Gamma分布
  - 次序统计量
  - 雅可比
  - Stat110
  - Blitzstein
mathjax: true
---

## 为什么第八章是"从定义到构造"的转折点

前七章你已经掌握了描述随机变量的全部语言。但如果我问你："$X \sim N(0,1)$，$Y = X^2$ 的分布是什么？"或者"两个独立的指数分布之和是什么分布？"——这些问题要求你**从已知分布构造新分布**。

这就是第八章的核心议题：**给定 $X$ 的分布和函数 $g$，如何求 $Y = g(X)$ 的分布？**

这一章给出的答案是一个完整的工具箱：

1. **变量变换公式**（Change of Variables）：把 $g$ 作用在单个随机变量上，PDF 如何缩放
2. **卷积**（Convolution）：独立随机变量之和的分布
3. **Beta 分布**：比例和概率的天然模型——"Uniform 次序统计量是什么分布？答：Beta"
4. **Gamma 分布**：等待时间的天然模型——"$n$ 个独立指数分布之和是什么分布？答：Gamma"
5. **Beta-Gamma 联系**（Bank-Post Office）：全书最漂亮的概率故事之一
6. **次序统计量**（Order Statistics）：排序后数据的分布——统计推断的基础

掌握了这些工具，你就可以从简单分布出发，用加、乘、取最大值/最小值、排序等操作构造出新的分布。这是**数学统计学的第一块基石**。

## 前置知识

- 第五章连续随机变量（PDF、CDF 的定义与关系）
- 第四章期望与方差（$E(X)$、$\text{Var}(X)$、LOTUS）
- 第六章矩母函数（MGF 的定义与基本性质）
- 基本的多元微积分（偏导数、Jacobian 行列式）

## 一、变量变换：函数作用在随机变量上

### 1.1 离散情况：平凡但重要

如果 $X$ 是离散的，$Y = g(X)$ 的分布很简单：

$$P(Y = y) = \sum_{x: g(x) = y} P(X = x)$$

就是把所有映射到 $y$ 的 $x$ 的概率加起来。这本质上和第三章的内容一致。

### 1.2 连续情况：PDF 缩放原理

连续情况更微妙。$Y = g(X)$ 的 PDF 不是简单地"把 $g$ 代入 $f_X$"。考虑一个严格单调的 $g$：

$$f_Y(y) = f_X(x) \cdot \left|\frac{dx}{dy}\right|$$

其中 $x = g^{-1}(y)$。因子 $|dx/dy|$ 是**缩放因子**：$g$ 在某处"拉伸"了 $x$ 轴，该处的概率密度必须按比例稀释；$g$ 在某处"压缩"了 $x$ 轴，概率密度就相应浓缩。

> **直觉类比**：想象 $X$ 均匀分布在 $[0, 1]$，$Y = 2X$（放大两倍）。$Y$ 分布在 $[0, 2]$，但总概率必须还是 1，所以 PDF 从 1 变成了 1/2。$|dx/dy| = |1/2| = 1/2$ 正是这个缩放因子。

**通用公式**（$g$ 不一定是单调的）：如果 $g$ 在 $y$ 处有多个原像 $x_1, x_2, \ldots$：

$$f_Y(y) = \sum_{i} \frac{f_X(x_i)}{|g'(x_i)|}, \quad \text{其中 } g(x_i) = y$$

### 1.3 二维情况与 Jacobian

对于随机向量 $(X, Y)$ 到 $(U, V) = (g_1(X,Y), g_2(X,Y))$：

$$f_{U,V}(u,v) = f_{X,Y}(x,y) \cdot \left|\det \frac{\partial(x,y)}{\partial(u,v)}\right|$$

或者更方便的形式：

$$f_{U,V}(u,v) \cdot \left|\det \frac{\partial(u,v)}{\partial(x,y)}\right| = f_{X,Y}(x,y)$$

Jacobian 行列式的绝对值度量了变换在每一点带来的"面积缩放"。

> **实践中常用的一招**：如果直接求 $\partial(u,v)/\partial(x,y)$ 比求逆 Jacobian 容易，就用后一个公式，然后用 $f_{U,V} = f_{X,Y} / |\det(\partial(u,v)/\partial(x,y))|$ 来计算。

## 二、卷积：独立随机变量之和的分布

### 2.1 卷积公式的推导

设 $X$ 和 $Y$ **独立**，$T = X + Y$。如何求 $T$ 的分布？

**直觉先于公式**：$T = t$ 可以来自许多种 $(X, Y)$ 的组合——$X = x$ 且 $Y = t-x$，对所有可能的 $x$。因为 $X$ 和 $Y$ 独立，每种组合的概率/密度是乘积。对所有可能的 $x$ 求和/积分：

**离散**：$P(T = t) = \sum_x P(X = x) \cdot P(Y = t - x)$

**连续**：$f_T(t) = \int_{-\infty}^{\infty} f_X(x) \cdot f_Y(t - x) \, dx$

这就是**卷积**。它在信号处理、图像处理、深度学习中无处不在——但这里的直觉很简单：枚举所有相加得到 $t$ 的方式。

> **卷积的对称性**：$f_X * f_Y = f_Y * f_X$。你可以固定 $x$ 用 $t-x$ 确定 $Y$，也可以固定 $y$ 用 $t-y$ 确定 $X$。两种方式给出相同的答案。

### 2.2 卷积 vs MGF：两种计算独立和的策略

卷积给出**精确的**分布公式，但积分可能很麻烦。MGF 更巧妙地解决了同一问题：

$$M_{X+Y}(t) = M_X(t) \cdot M_Y(t)$$

如果乘积的 MGF 恰好是某个已知分布的 MGF，那你就直接知道 $X+Y$ 服从什么分布——不需要积分。这就是第六章 MGF 的实践价值。但 MGF 不总是存在（比如 Cauchy 分布），这时就必须用卷积。

## 三、Beta 分布：比例的天然模型

### 3.1 Beta 的定义与故事

**PDF**：对 $0 < x < 1$：

$$f(x) = \frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)} x^{a-1} (1-x)^{b-1}, \quad a > 0, b > 0$$

归一化常数中的 Beta 函数：$B(a,b) = \frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$。

**Bank-Post Office 故事**：这是 Beta 分布最重要的直觉。

- 银行（Bank）：$X \sim \text{Gamma}(a, \lambda)$——等待 $a$ 次事件的总时间
- 邮局（Post Office）：$Y \sim \text{Gamma}(b, \lambda)$——等待 $b$ 次事件的**独立**总时间
- 总等待时间 $T = X + Y \sim \text{Gamma}(a+b, \lambda)$
- 在总时间中，银行所占的**比例** $W = X / (X+Y) \sim \text{Beta}(a, b)$

最精彩的部分：**$W$ 与 $T$ 独立。** 知道总等待时间不影响银行所占比例的分布——这是一个深刻的概率事实。

**关键性质**：
- $E[\text{Beta}(a,b)] = \frac{a}{a+b}$——这正是"银行时间的期望比例"，直觉完美吻合
- $\text{Beta}(1,1) = \text{Unif}(0,1)$——没有任何偏向的比例
- $\text{Beta}(a,b)$ 和 $\text{Beta}(b,a)$ 关于 $x=0.5$ 镜像对称

### 3.2 Beta 与二项分布的共轭关系

如果把 Beta 作为 $p$ 的先验分布（$p \sim \text{Beta}(a,b)$），观测到 $k$ 次成功和 $n-k$ 次失败后，后验分布是 $\text{Beta}(a+k, b+n-k)$。Beta 的 $a$ 和 $b$ 就像"伪计数"——$a-1$ 次先验成功，$b-1$ 次先验失败。这是贝叶斯统计中最优雅的共轭关系之一。

## 四、Gamma 分布：等待时间的天然模型

### 4.1 Gamma 的定义与故事

**PDF**：对 $x > 0$：

$$f(x) = \frac{\lambda^a}{\Gamma(a)} x^{a-1} e^{-\lambda x}, \quad a > 0, \lambda > 0$$

其中 $\Gamma(a) = \int_0^\infty t^{a-1} e^{-t} dt$。

**Poisson 过程故事**：在速率为 $\lambda$ 的 Poisson 过程中，$\text{Gamma}(a, \lambda)$ 是等待**第 $a$ 次**事件发生所需的总时间。

- $a$（形状参数）——你要等几次事件
- $\lambda$（速率参数）——事件发生的频率

**特殊情形**：
- $\text{Gamma}(1, \lambda) = \text{Expo}(\lambda)$——等到第 1 次事件的时间就是指数分布
- $\text{Gamma}(n, \lambda)$（$n$ 为整数）= $n$ 个独立 $\text{Expo}(\lambda)$ 之和——等到 $n$ 次事件 = 一次一次地等

**关键性质**：
- $E[\text{Gamma}(a,\lambda)] = a/\lambda$——平均每次等 $1/\lambda$，等 $a$ 次就是 $a/\lambda$
- 独立 Gamma 之和（同 $\lambda$）：$X \sim \text{Gamma}(a,\lambda), Y \sim \text{Gamma}(b,\lambda)$ 独立 $\Rightarrow$ $X+Y \sim \text{Gamma}(a+b,\lambda)$
- MGF：$M(t) = (\frac{\lambda}{\lambda - t})^a$，$t < \lambda$

> **为什么要区分 Gamma 和 Exponential？** 指数分布是一个事件的时间，Gamma 是 $a$ 个事件的时间。单用指数分布无法描述"下一个事故/下一个顾客"的等待时间分布——你需要 Gamma 来累积。

## 五、Beta-Gamma 联系与次序统计量

### 5.1 Bank-Post Office 的深层含义

Beta-Gamma 联系的核心结论：

$$X \sim \text{Gamma}(a,\lambda), Y \sim \text{Gamma}(b,\lambda) \text{ 独立} \Rightarrow \frac{X}{X+Y} \sim \text{Beta}(a,b) \perp X+Y$$

这个结果有三个重要推论：
1. **Beta 可以来自 Gamma 的比值**——Beta 是"比例分布"
2. **比值的分布与总和独立**——这是 Gamma 的独特性质
3. **MGF 的分解**：独立和 $\Leftrightarrow$ MGF 乘积。Gamma 的 MGF 乘积仍然是 Gamma 的 MGF

### 5.2 次序统计量：排序后的分布

从 i.i.d. $X_1, \ldots, X_n$ 中抽取样本，排序得 $X_{(1)} \leq X_{(2)} \leq \cdots \leq X_{(n)}$。

**核心结果**：对于 $U_1, \ldots, U_n$ i.i.d. $\text{Unif}(0,1)$：

$$U_{(j)} \sim \text{Beta}(j, n-j+1)$$

**直觉**：$U_{(j)}$ 把 $[0,1]$ 分成了 $j$ 个"小于"和 $n-j$ 个"大于"的部分。Beta 的参数 $j$ 和 $n-j+1$ 反映了这种"分割比例"。

由此可以直接得到次序统计量的期望：

$$E[U_{(j)}] = \frac{j}{n+1}$$

这些点均分 $[0,1]$——$n$ 个均匀随机点的次序统计量，其期望恰好把 $[0,1]$ 分成 $n+1$ 个等份。

**一般分布的次序统计量**：对于一般分布 $F$：

$$f_{X_{(j)}}(x) = n \binom{n-1}{j-1} f(x) [F(x)]^{j-1} [1-F(x)]^{n-j}$$

三项分别对应：选取哪个作为第 $j$ 个 $\times$ 在前 $j-1$ 个中选 $j-1$ 个 $\times$ PDF $\times$ $j-1$ 个小于 $\times$ $n-j$ 个大于。

## 六、概念全景图

```
                         变换 (Transformations)
                               |
          ┌────────────────────┼────────────────────┐
          |                    |                     |
    一元变量变换            卷积 (Convolution)      Beta & Gamma
    Y = g(X)               T = X + Y (独立)        (两个新分布族)
          |                    |                     |
    ┌─────┴─────┐        ┌────┴────┐          ┌─────┴─────┐
    |           |        |         |          |           |
  离散: 求和   连续:    离散卷积   连续卷积    Beta(a,b)  Gamma(a,λ)
  P(g(X)=y)   f_Y(y)=  P(T=t)=   f_T(t)=   (比例分布)  (等待时间)
  =ΣP(X=x)   f_X(x)·  ΣP(X=x)· ∫f_X(x)·       |           |
             |dx/dy|  P(Y=t-x)  f_Y(t-x)dx     |     ┌─────┴─────┐
                      = MGF乘积法              |     |           |
                                              Bank-Post    Gamma(1,λ)
                                              Office:      = Expo(λ)
                                         X/(X+Y)~Beta(a,b) Gamma(n,λ)
                                         ⟂ X+Y             = n个Expo和
                                              |
                                        次序统计量 U_(j)
                                        ~ Beta(j, n-j+1)
```

## 七、精选习题

### 第一组：变量变换与卷积（题 1-3）

**题 1（教材 Ch8 | 1D 变量变换）** 设 $X \sim N(0,1)$，求 $Y = X^2$ 的分布。

**▼ 答案与解析**

$g(x) = x^2$ 不是单调的。对 $y > 0$，方程 $x^2 = y$ 有两个解：$x = \sqrt{y}$ 和 $x = -\sqrt{y}$。在每个解处 $|g'(x)| = |2x| = 2\sqrt{y}$。

变量变换公式给出：

$$f_Y(y) = \frac{f_X(\sqrt{y})}{|2\sqrt{y}|} + \frac{f_X(-\sqrt{y})}{|-2\sqrt{y}|} = \frac{1}{\sqrt{2\pi}} \frac{e^{-y/2}}{2\sqrt{y}} + \frac{1}{\sqrt{2\pi}} \frac{e^{-y/2}}{2\sqrt{y}}$$

$$= \frac{1}{\sqrt{2\pi}} \frac{1}{\sqrt{y}} e^{-y/2}, \quad y > 0$$

这正是 $\text{Gamma}(1/2, 1/2)$ 的 PDF——也就是自由度为 1 的**卡方分布** $\chi^2_{(1)}$。

**洞察**：正态分布的平方是卡方分布——这是统计推断中最基础的变换之一。非单调的 $g$ 需要把所有原像的概率密度加起来。

**训练点**：非单调 1D 变量变换、卡方分布的定义。

---

**题 2（SP9-1(a) | Beta 对称性的变换证明）** 设 $B \sim \text{Beta}(a,b)$。利用变量变换公式证明 $1 - B \sim \text{Beta}(b,a)$。

**▼ 答案与解析**

令 $W = 1 - B = g(B)$。$B = g^{-1}(W) = 1 - W$，$|dB/dW| = |-1| = 1$。

由变量变换公式：

$$f_W(w) = f_B(1-w) \cdot |{-1}| = \frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)} (1-w)^{a-1} w^{b-1}$$

这正是 $\text{Beta}(b,a)$ 的 PDF（注意 $a$ 和 $b$ 交换了位置）。

**直觉解释**：$B$ 是"成功的比例"（先验有 $a$ 次伪成功和 $b$ 次伪失败）。那 $1-B$ 就是"失败的比例"——自然是 $\text{Beta}(b,a)$。变量变换从数学上确认了这个直觉。

**洞察**：$\text{Beta}(a,b)$ 和 $\text{Beta}(b,a)$ 是关于 $x=0.5$ 的镜像。当 $a=b$ 时，Beta 关于 0.5 对称。

**训练点**：1D 变量变换、Beta PDF 的识别、概率直觉与计算的双向验证。

---

**题 3（教材 Ch8 | 独立指数和的卷积）** 设 $X, Y$ 独立同分布于 $\text{Expo}(\lambda)$。用卷积公式求 $T = X + Y$ 的 PDF。

**▼ 答案与解析**

对独立连续随机变量：
$$f_T(t) = \int_0^t f_X(x) f_Y(t-x) dx = \int_0^t \lambda e^{-\lambda x} \cdot \lambda e^{-\lambda(t-x)} dx$$
$$= \lambda^2 e^{-\lambda t} \int_0^t 1 \, dx = \lambda^2 t e^{-\lambda t}, \quad t > 0$$

这正是 $\text{Gamma}(2, \lambda)$ 的 PDF（形状参数 $a=2$）。推广：$n$ 个独立 $\text{Expo}(\lambda)$ 之和 $\sim \text{Gamma}(n, \lambda)$。

**洞察**：$t$ 的积分上限从 $\infty$ 变成了 $t$——因为 $X > t$ 时 $Y = t-X < 0$ 不可能（指数分布支撑在正半轴）。这是含支撑约束的卷积的核心技巧。

**训练点**：卷积公式的运用、积分限的处理、Gamma 与指数和的关系。

---

### 第二组：Beta 与 Gamma 分布（题 4-6）

**题 4（SP9-2 | Gamma 可加性的三种证明）** 设 $X \sim \text{Gamma}(a,\lambda)$ 和 $Y \sim \text{Gamma}(b,\lambda)$ 独立（$a,b$ 为整数）。用以下三种方法证明 $X + Y \sim \text{Gamma}(a+b, \lambda)$：

(a) 基于 Poisson 过程的"故事证明"

(b) 基于 MGF 的计算证明

**▼ 答案与解析**

(a) **故事证明**：在速率为 $\lambda$ 的 Poisson 过程中，$X$ 是等待第 $a$ 次事件的时间，$Y$ 是之后等待第 $b$ 次事件的时间。它们发生在过程的不重叠区间上，因此独立。$X+Y$ 是等待第 $a+b$ 次事件的时间——正是 $\text{Gamma}(a+b, \lambda)$。

(b) **MGF 证明**：$\text{Gamma}(a,\lambda)$ 的 MGF 为 $M(t) = (1 - t/\lambda)^{-a}$（$t < \lambda$）。

$$M_{X+Y}(t) = M_X(t) M_Y(t) = \left(1 - \frac{t}{\lambda}\right)^{-a} \left(1 - \frac{t}{\lambda}\right)^{-b} = \left(1 - \frac{t}{\lambda}\right)^{-(a+b)}$$

这正是 $\text{Gamma}(a+b, \lambda)$ 的 MGF。由 MGF 的唯一性，$X+Y \sim \text{Gamma}(a+b, \lambda)$。

**洞察**：故事证明不需要任何积分——它把 Gamma 分布嵌入到 Poisson 过程的物理直觉中。这是概率论中最优雅的证明方式之一。MGF 证明同样简洁：乘积的 MGF = MGF 的乘积。

**训练点**：Poisson 过程与 Gamma 的联系、MGF 乘积法则、多种证明方法的对比。

---

**题 5（教材 Ch8 | Beta 的矩）** 设 $B \sim \text{Beta}(a,b)$。

(a) 计算 $E(B)$ 和 $E(B^2)$。

(b) 由此求 $\text{Var}(B)$。

**▼ 答案与解析**

(a) 利用 Bank-Post Office 故事：$B = \frac{X}{X+Y}$，其中 $X \sim \text{Gamma}(a,\lambda), Y \sim \text{Gamma}(b,\lambda)$ 独立，且 $B \perp X+Y$。

$$E(B)(a+b)/\lambda = E(B) \cdot E(X+Y) = E(B(X+Y)) = E(X) = a/\lambda$$

所以 $E(B) = \frac{a}{a+b}$。类似地：

$$E(B^2) = E\left[\left(\frac{X}{X+Y}\right)^2\right]$$

利用 $B \perp X+Y$，$E(B^2) \cdot E[(X+Y)^2] = E(X^2)$。计算 $E[(X+Y)^2] = \text{Var}(X+Y) + [E(X+Y)]^2 = \frac{a+b}{\lambda^2} + \frac{(a+b)^2}{\lambda^2} = \frac{(a+b)(a+b+1)}{\lambda^2}$。而 $E(X^2) = \frac{a(a+1)}{\lambda^2}$。

$$E(B^2) = \frac{a(a+1)}{(a+b)(a+b+1)}$$

(b)

$$\text{Var}(B) = E(B^2) - [E(B)]^2 = \frac{a(a+1)}{(a+b)(a+b+1)} - \frac{a^2}{(a+b)^2}$$

化简得：

$$\text{Var}(B) = \frac{ab}{(a+b)^2(a+b+1)}$$

**洞察**：$a$ 和 $b$ 越大，方差越小——先验信息越多，不确定性越小。当 $a=b=1$（均匀分布）时，$\text{Var} = 1/12$，和 $\text{Unif}(0,1)$ 一致。

**训练点**：Bank-Post Office 独立性的应用、条件期望替代直接积分、Beta 矩的计算技巧。

---

**题 6（教材 Ch8 | Gamma 与 Exponential 的关系）** 速率为 $\lambda$ 的 Poisson 过程中，设 $T_1, T_2, T_3$ 为前三次事件的到达时间。

(a) 求 $T_1, T_2, T_3$ 的联合分布。

(b) 求 $T_3$ 的边际分布。

(c) 设 $X_1 = T_1, X_2 = T_2 - T_1, X_3 = T_3 - T_2$（到达间隔）。$X_1, X_2, X_3$ 的分布是什么？它们是否独立？

**▼ 答案与解析**

(a) Poisson 过程的性质：在 $[t, t+dt]$ 区间内有一次事件的概率为 $\lambda dt$。对于 $0 < t_1 < t_2 < t_3$：

$$f(t_1, t_2, t_3) = \lambda e^{-\lambda t_1} \cdot \lambda e^{-\lambda(t_2 - t_1)} \cdot \lambda e^{-\lambda(t_3 - t_2)} = \lambda^3 e^{-\lambda t_3}$$

三段的指数密度相乘，因为过程在不相交区间上是独立的。

(b) $T_3$ 是第三次事件的到达时间。由 Gamma 的 Poisson 过程故事：$T_3 \sim \text{Gamma}(3, \lambda)$。PDF：$f_{T_3}(t) = \frac{\lambda^3}{2} t^2 e^{-\lambda t}$，$t > 0$。

(c) 到达间隔 $X_i$ 独立同分布于 $\text{Expo}(\lambda)$。联合分布 $f(x_1,x_2,x_3) = \lambda^3 e^{-\lambda(x_1+x_2+x_3)}$（注意常数项，与 (a) 对比）。

**洞察**：Poisson 过程的到达间隔是 i.i.d. Exponential。这个性质**等价于** Poisson 过程的定义——事件以恒定速率独立地发生。

**训练点**：Poisson 过程的联合分布、Gamma 作为"第 $a$ 次等待时间"的故事、到达间隔的 i.i.d. 性质。

---

### 第三组：Beta-Gamma 联系与次序统计量（题 7-8）

**题 7（SP9-3 | Bank-Post Office：比值与总和的独立性）** 设 $X \sim \text{Gamma}(a,\lambda)$，$Y \sim \text{Gamma}(b,\lambda)$ 独立。判断 $\frac{X}{Y}$ 是否与 $X+Y$ 独立，并说明理由。

**▼ 答案与解析**

**是独立的。** 由 Bank-Post Office 故事：$W = \frac{X}{X+Y} \sim \text{Beta}(a,b)$，且 $W \perp X+Y$。

注意到 $\frac{X}{Y} = \frac{X/(X+Y)}{Y/(X+Y)} = \frac{W}{1-W}$ 是 $W$ 的**函数**（严格单调递增：$w \mapsto w/(1-w)$）。因为 $W \perp X+Y$，任何 $W$ 的函数也与 $X+Y$ 独立。所以 $\frac{X}{Y} \perp X+Y$。

**举个反直觉的例子**：如果 $X$ 是等 3 封邮件的时间，$Y$ 是等 5 封邮件的时间（同速率），那么比值 $X/Y$ 的分布与总等待时间 $X+Y$ 毫无关系——知道总时间长短不改变"第一个占了多久"的相对信息。

**洞察**：$W \perp X+Y$ 是概率论中最深刻的独立关系之一。比值独立于总和——这在正态分布中不成立，是 Gamma 分布独有的性质。

**训练点**：Bank-Post Office 独立性的应用、函数的独立性传递。

---

**题 8（SP9-OS-1 | Uniform 次序统计量是 Beta）** 设 $U_1, U_2, \ldots, U_n$ i.i.d. $\text{Unif}(0,1)$，$U_{(j)}$ 是第 $j$ 个次序统计量。

(a) 推导 $U_{(j)}$ 的 PDF。

(b) 识别 $U_{(j)}$ 服从什么分布，并求 $E[U_{(j)}]$。

**▼ 答案与解析**

(a) 思路：$U_{(j)} \in [t, t+dt]$ 意味着有一个 $U_i$ 恰好落在 $[t, t+dt]$（概率约 $dt$），$j-1$ 个小于 $t$，$n-j$ 个大于 $t$。哪个 $U_i$ 是第 $j$ 个？有 $n$ 种选择；哪 $j-1$ 个小于它？有 $\binom{n-1}{j-1}$ 种选择。

$$f_{U_{(j)}}(t) = n \binom{n-1}{j-1} \cdot 1 \cdot t^{j-1} \cdot (1-t)^{n-j}$$

$$= \frac{n!}{(j-1)!(n-j)!} t^{j-1} (1-t)^{n-j}$$

(b) 这恰好是 $\text{Beta}(j, n-j+1)$ 的 PDF（因子 $\frac{n!}{(j-1)!(n-j)!} = \frac{\Gamma(n+1)}{\Gamma(j)\Gamma(n-j+1)} = \frac{1}{B(j, n-j+1)}$）。

因此 $U_{(j)} \sim \text{Beta}(j, n-j+1)$，且：

$$E[U_{(j)}] = \frac{j}{n+1}$$

$n$ 个均匀点的次序统计量，期望值恰好把 $[0,1]$ 平分成 $n+1$ 份——简洁且优雅。

**洞察**：次序统计量将 Uniform 和 Beta 联系起来——这是非参数统计（如经验 CDF、分位数估计）的数学基础。任何连续分布的次序统计量都可以通过概率积分变换 $F^{-1}(U_{(j)})$ 得到。

**训练点**：次序统计量 PDF 的推导、Beta PDF 的识别、组合概率的直觉。

---

## 八、本章核心脉络

本章可以看作一个"分布构造工具箱"，三个层次递进：

**第一层（一元变换）**：变量变换公式 $f_Y(y) = f_X(x) \cdot |dx/dy|$ 是构造新分布最基本的操作。它告诉你：把随机变量塞进一个函数，PDF 按导数的绝对值缩放。如果函数不是单调的，把所有原像的贡献加起来。

**第二层（和—Gamma—卷积）**：独立和是最自然的构造方式。卷积公式是对此的精确描述。当分量都是指数分布时，和就是 Gamma——而 Gamma 的灵活性（通过调节 $a$ 和 $\lambda$）使它成为正的连续量最通用的模型。MGF 方法通常比卷积积分更快。

**第三层（比例与排序—Beta—次序统计量）**：Bank-Post Office 故事把 Gamma 比值变成 Beta，次序统计量把 Uniform 的排序版本变成 Beta。两者都指向 Beta 分布的核心角色——它是"比例/概率的分布"。Beta 是贝叶斯推断中比例参数的共轭先验——这不是巧合，而是 Beta 的数学本质决定的。

**如果你只从这一章带走三样东西：**

1. **变量变换公式**：$f_Y(y) = f_X(x) \cdot |dx/dy|$——忘掉导数因子是初学者最常见的错误。导数的绝对值度量了 $g$ 在该点的"拉伸"程度。

2. **Bank-Post Office 故事**：$X \sim \text{Gamma}(a,\lambda), Y \sim \text{Gamma}(b,\lambda)$ 独立 $\Rightarrow$ $X/(X+Y) \sim \text{Beta}(a,b) \perp X+Y$。这个结论在全书各处被反复使用——从 Beta 的矩到次序统计量，它是最便捷的推导路径。

3. **$U_{(j)} \sim \text{Beta}(j, n-j+1)$**：次序统计量连接了"排序"和 Beta 分布。用它可以直接求出分位数的分布、经验 CDF 的方差——是数理统计最根本的工具之一。

## 参考文献

1. **教材**：Blitzstein, J. K. & Hwang, J. (2019). *Introduction to Probability* (2nd ed.). CRC Press. Chapter 8: Transformations.
2. **Stat 110 课程录像**：Lecture 22（Transformations and Convolutions）、Lecture 23（Beta Distribution）、Lecture 24（Gamma Distribution）、Lecture 25（Beta-Gamma Connections and Order Statistics）。可在 YouTube 搜索 "Harvard Stat 110"。
3. **Stat 110 Strategic Practice 9**：Beta and Gamma Distributions + Order Statistics。包含本文题 2, 4, 7, 8 的完整解答。
4. **补充参考**：Casella, G. & Berger, R. (2002). *Statistical Inference* (2nd ed.). Duxbury. Chapter 5: Properties of a Random Sample（次序统计量的系统处理）。
