# 桜ノ詩の庭 · 源码仓库

这是 [fanchanghong650-hub.github.io](https://fanchanghong650-hub.github.io) 的 Hexo 源码分支。

## 分支怎么分工

| 分支 | 内容 | 谁写 |
| --- | --- | --- |
| `source` | Hexo 源码（配置、主题、文章 Markdown） | 我 |
| `main` | 构建产物（HTML/CSS/JS），GitHub Pages 直接托管 | 只由 Actions 写 |

**不要手动改 `main`。** 每次往 `source` 推送，GitHub Actions 会自动构建并把结果推回 `main`，Pages 随后刷新。

## 写一篇文章

在 `source/_posts/` 下新建 `英文短横线文件名.md`，模板：

```markdown
---
title: 文章标题
date: 2026-10-26 20:00:00
categories:
  - 数学
tags:
  - 概率论
---

正文……
```

保存后 `git add . && git commit -m "post: 标题" && git push` 到 `source` 分支即可，两三分钟后线上可见。

文件名只影响 URL（`https://fanchanghong650-hub.github.io/年/月/日/文件名/`），标题和文件名不必一致。

### 公式

MathJax 已全局开启，行内 `$...$`、行间 `$$...$$` 直接用。不要用反引号包公式。

### 图片

放进 `source/images/`，正文里写 `![](/images/文件名.png)`。

## 本地预览

本机（macOS）需要先装好依赖：

```bash
cd ~/blog
export PATH=/usr/local/bin:$PATH                 # node 在这里
export HTTPS_PROXY=http://127.0.0.1:7897         # 装依赖要走代理
npm install --cache /tmp/npm-cache               # ~/.npm 权限坏过，绕开它
```

预览：

```bash
export PATH=/usr/local/bin:$PATH
npx hexo server      # 打开 http://localhost:4000
```

只构建不预览：

```bash
npx hexo generate    # 产物在 public/
```

## 已知环境坑

- 直连 `github.com` 会失败：`git config http.version HTTP/1.1` + `git config http.proxy http://127.0.0.1:7897`（本仓库已配好）。
- `raw.githubusercontent.com` 不可达，取文件用 `api.github.com`。
- `~/.npm` 里有 root 所有的文件，npm 要加 `--cache /tmp/npm-cache`。
- 不要在别处的旧副本上跑 `hexo g -d`：会把旧文章推回来覆盖 `main`。唯一真相是这个 `source` 分支。
