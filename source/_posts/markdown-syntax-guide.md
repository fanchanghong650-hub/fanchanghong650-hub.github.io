---
title: Markdown 语法参考
date: 2026-05-28 20:01:00
categories: 文档
tags: [Markdown, 参考, 写作]
mathjax: true
---

本文档涵盖本博客写作中常用的 Markdown 语法，方便随时查阅。

---

## 一、基础语法

### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
```

一级标题通常留给文章标题（Front Matter 中的 `title`），正文从二级标题开始。

### 段落和换行

直接写文字就是段落。段落之间空一行。

同一段落内换行，在行末加两个空格后回车。  
像这样。

### 强调

```markdown
**粗体文字**
*斜体文字*
***粗斜体***
~~删除线~~
<u>下划线</u>
```

效果：**粗体文字** *斜体文字* ***粗斜体*** ~~删除线~~ <u>下划线</u>

### 列表

无序列表：

```markdown
- 项目一
- 项目二
  - 嵌套项目（前面缩进两个空格）
  - 嵌套项目二
- 项目三
```

有序列表：

```markdown
1. 第一步
2. 第二步
3. 第三步
```

### 引用

```markdown
> 这是一段引用
> 可以多行
>
> 空一行引用中间有间距
```

> 这是一段引用
> 可以多行

嵌套引用：

```markdown
> 外层引用
>> 内层引用
```

### 分割线

```markdown
---
或
***
```

---

### 链接

```markdown
[链接文字](https://example.com)
[带标题的链接](https://example.com "鼠标悬停显示的文字")
<https://example.com>    # 直接显示URL
```

### 图片

```markdown
![替代文字](/images/bg/图片名.png)
![替代文字](https://example.com/image.jpg)
```

本博客中引用本地图片的路径前缀为 `/images/`，对应项目中的 `source\images\` 文件夹。

---

## 二、代码

### 行内代码

用反引号包裹：`` `print("hello")` `` → `print("hello")`

### 代码块

用三个反引号包裹，并指定语言：

````markdown
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
````

效果：

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

常用语言标识：`python` `javascript` `bash` `cpp` `java` `html` `css` `json` `yaml` `markdown` `latex`

### 行内代码中显示反引号

用双反引号包裹：`` `` ` `` ``

---

## 三、表格

```markdown
| 左对齐 | 居中对齐 | 右对齐 |
|:-------|:--------:|-------:|
| 内容   | 内容     | 内容   |
| 数据   | 数据     | 数据   |
```

| 左对齐 | 居中对齐 | 右对齐 |
|:-------|:--------:|-------:|
| 内容   | 内容     | 内容   |
| 数据   | 数据     | 数据   |

> 冒号在左边 = 左对齐，在两边 = 居中，在右边 = 右对齐

---

## 四、数学公式（MathJax）

本博客已启用 MathJax。在 Front Matter 中添加 `mathjax: true` 即可在文章中使用公式。

### 行内公式

用 `$` 包裹：

```latex
$E = mc^2$
$e^{i\pi} + 1 = 0$
```

效果：$E = mc^2$ 和 $e^{i\pi} + 1 = 0$

### 独立公式（块级）

用 `$$` 包裹：

```latex
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

效果：

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

### 常用 LaTeX 命令速查

| 语法 | 效果 | 说明 |
|------|------|------|
| `x^2` | $x^2$ | 上标 |
| `x_n` | $x_n$ | 下标 |
| `\frac{a}{b}` | $\frac{a}{b}$ | 分数 |
| `\sqrt{x}` | $\sqrt{x}$ | 平方根 |
| `\sqrt[n]{x}` | $\sqrt[n]{x}$ | n次根 |
| `\sum_{i=1}^n` | $\sum_{i=1}^n$ | 求和 |
| `\prod_{i=1}^n` | $\prod_{i=1}^n$ | 累乘 |
| `\int_a^b` | $\int_a^b$ | 积分 |
| `\lim_{x \to \infty}` | $\lim_{x \to \infty}$ | 极限 |
| `\alpha \beta \gamma` | $\alpha \beta \gamma$ | 希腊字母 |
| `\pi \theta \lambda` | $\pi \theta \lambda$ | 希腊字母 |
| `\sin \cos \tan` | $\sin \cos \tan$ | 三角函数 |
| `\log \ln` | $\log \ln$ | 对数 |
| `\infty` | $\infty$ | 无穷 |
| `\partial` | $\partial$ | 偏导 |
| `\nabla` | $\nabla$ | 梯度 |
| `\cdot \times \div` | $\cdot \times \div$ | 运算符 |
| `\pm \mp` | $\pm \mp$ | 正负 |
| `\leq \geq \neq` | $\leq \geq \neq$ | 比较 |
| `\approx \equiv` | $\approx \equiv$ | 约等/恒等 |
| `\forall \exists` | $\forall \exists$ | 全称/存在 |
| `\in \subset \subseteq` | $\in \subset \subseteq$ | 集合 |
| `\cup \cap` | $\cup \cap$ | 并集/交集 |
| `\emptyset` | $\emptyset$ | 空集 |
| `\mathbb{R}` | $\mathbb{R}$ | 实数集 |
| `\mathbf{A}` | $\mathbf{A}$ | 粗体矩阵 |
| `\text{文字}` | $\text{文字}$ | 公式中插入文字 |
| `\quad` | （空格） | 公式内空格 |
| `\to` 或 `\rightarrow` | $\to$ | 箭头 |
| `\Rightarrow` | $\Rightarrow$ | 推导箭头 |
| `\begin{cases}...\end{cases}` | — | 分段函数 |
| `\begin{bmatrix}...\end{bmatrix}` | — | 矩阵 |
| `\begin{aligned}...\end{aligned}` | — | 多行对齐 |

---

## 五、Hexo Front Matter

每篇 Hexo 文章开头必须包含 Front Matter（用 `---` 包裹的 YAML 块）：

```yaml
---
title: 文章标题
date: 2026-05-28 20:00:00
categories: [主分类, 子分类]
tags: [标签1, 标签2, 标签3]
mathjax: true       # 可选：启用数学公式
---
```

### 支持的字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 文章标题 |
| `date` | 是 | 发布日期，格式 `YYYY-MM-DD HH:mm:ss` |
| `categories` | 否 | 分类，支持多级：`[一级, 二级]` |
| `tags` | 否 | 标签列表：`[tag1, tag2]` |
| `mathjax` | 否 | 设为 `true` 以启用数学公式 |
| `updated` | 否 | 更新日期 |
| `description` | 否 | 文章摘要 |
| `top_img` | 否 | 文章顶部大图 |
| `cover` | 否 | 文章封面图 |
| `comments` | 否 | 设为 `false` 禁用评论 |

### 分类和标签的写法

单分类单标签：
```yaml
categories: 技术
tags: Python
```

多分类（子分类）：
```yaml
categories: [技术, Python]
```

多标签（二选一写法均可）：
```yaml
tags:
  - Python
  - 数学
  - 教程
# 或
tags: [Python, 数学, 教程]
```

---

## 六、实用技巧

### 在 Markdown 中使用 HTML

Markdown 支持直接嵌入 HTML：

```html
<details>
<summary>点击展开</summary>
隐藏的内容在这里。
</details>
```

### 任务列表

```markdown
- [x] 已完成任务
- [ ] 待完成任务
- [ ] 另一个待办
```

### 脚注

```markdown
这里有一个脚注[^1]

[^1]: 这是脚注的内容。
```

### 转义字符

如果需要在正文中显示 Markdown 特殊符号（如 `*` `_` `#` `` ` `` 等），在符号前加反斜杠 `\`：

```markdown
\*这不是斜体\*
\# 这不是标题
```

### 高亮文字（本主题支持）

本博客支持使用 `{#label}` 语法高亮文字：

```markdown
这是 {% label 重点文字 red %}
这是 {% label 提示文字 blue %}
这是 {% label 成功文字 green %}
```

颜色可选：`default` `blue` `pink` `red` `purple` `orange` `green`

---

## 七、完整文章示例

```markdown
---
title: 我的新文章
date: 2026-05-28 20:00:00
categories: [技术, Python]
tags: [Python, 数学, 教程]
mathjax: true
---

## 引言

这是一段**引言**文字。

## 代码示例

```python
def hello():
    print("Hello, World!")
```

## 数学示例

行内公式 $x^2 + y^2 = z^2$，以及独立公式：

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## 总结

以上就是完整示例。
```

---

## 参考资料

- [Markdown 官方教程](https://www.markdownguide.com/)
- [Hexo 官方文档](https://hexo.io/docs/)
- [Butterfly 主题文档](https://butterfly.js.org/)
- [MathJax 文档](https://docs.mathjax.org/)
- [LaTeX 数学符号列表](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols)
