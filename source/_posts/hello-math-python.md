---
title: Hello World - 数学与 Python 博客起步
date: 2026-05-28 15:52:40
categories:
  - 笔记
tags:
  - Python
  - Math
  - 随笔
mathjax: true
---

## 欢迎

这是我的第一篇博客文章。这个博客主要用来记录我在数学和 Python 编程方面的学习和思考。

## 数学公式测试

### 行内公式

爱因斯坦质能方程：$E = mc^2$

### 块级公式

欧拉恒等式：

$$
e^{i\pi} + 1 = 0
$$

### 矩阵

$$ \begin{bmatrix} a & b \\ c & d \end{bmatrix} \times \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} ax+by \\ cx+dy \end{bmatrix} $$

### 微积分

傅里叶变换：$$ \mathcal{F}\{f(t)\} = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt $$

### 概率论

贝叶斯定理：

$$
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
$$

## Python 代码测试

### 质数判定

```python
def is_prime(n: int) -> bool:
    """判断一个数是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# 找出100以内的所有质数
primes = [n for n in range(2, 100) if is_prime(n)]
print(f"100以内的质数: {primes}")
```

### 斐波那契数列

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """递归计算第n个斐波那契数（带缓存）"""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


for i in range(10):
    print(f"F({i}) = {fib(i)}")
```

## 结语

博客刚刚起步，后续会逐步完善。期待在这里记录更多内容。
