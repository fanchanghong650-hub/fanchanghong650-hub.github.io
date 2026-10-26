# 桜ノ詩の庭 · 源码仓库

这是 [fanchanghong650-hub.github.io](https://fanchanghong650-hub.github.io) 的 Hexo 源码分支。

本地位置：`学习资料/博客/`（Obsidian vault 内，可直接编辑）

## 分支怎么分工

| 分支 | 内容 | 谁写 |
| --- | --- | --- |
| `source` | Hexo 源码（配置、主题、文章 Markdown） | 我 |
| `main` | 构建产物（HTML/CSS/JS），GitHub Pages 直接托管 | 只由 Actions 写 |

**不要手动改 `main`。** 每次往 `source` 推送，GitHub Actions 自动构建并把结果推回 `main`，Pages 随后刷新。

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

也可以命令行生成骨架：`npx hexo new "文章标题"`。

写完推上去：

```bash
cd "学习资料/博客"
git add -A && git commit -m "post: 标题" && git push
```

两三分钟后线上可见，进度看 https://github.com/fanchanghong650-hub/fanchanghong650-hub.github.io/actions

文件名只影响 URL（`https://fanchanghong650-hub.github.io/年/月/日/文件名/`），标题和文件名不必一致。

### 公式

MathJax 已全局开启，行内 `$...$`、行间 `$$...$$` 直接用。**不要用反引号包公式。**

### 图片

图片放 `source/images/`，正文写 `![](/images/文件名.png)`。

这样网站上 100% 正确；在 Obsidian 里这张图会显示不出来（Obsidian 把 `/` 当 vault 根），这是正常现象，不影响发布。

`source/images/bg/` 里原本有 22MB 的首页轮播壁纸（8 张樱之诗 CG 截图 + 1 张 AI 壁纸），**2026-10-26 因版权原因已全部移除**，本地备份在 `~/Pictures/樱之诗CG/`。现在背景由 `source/js/bg.js` 的纯 CSS 渐变提供；想换回图片就把自有版权的图放进 `source/images/bg/` 并填 `bg.js` 顶部的 `PHOTO_URLS`。

## 本地预览

**不要在 vault 里跑 `npm install`** —— `node_modules` 有十几万个小文件，iCloud 会同步到崩溃。要预览就复制一份到临时目录：

```bash
export PATH=/usr/local/bin:$PATH
export HTTPS_PROXY=http://127.0.0.1:7897

rsync -a --exclude .git --exclude public --exclude node_modules \
  "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/学习资料/博客/" /tmp/blog-preview/

cd /tmp/blog-preview
npm install --cache /tmp/npm-cache     # ~/.npm 权限坏过，绕开它
npx hexo server                        # http://localhost:4000
```

日常不预览也行：写完推送，构建结果看 Actions 页面。

## 已知环境坑

- 直连 `github.com` 会失败：需要 `git config http.version HTTP/1.1` + `git config http.proxy http://127.0.0.1:7897`。
- `raw.githubusercontent.com` 不可达，取文件用 `api.github.com`。
- `~/.npm` 里有 root 所有的文件，npm 必须加 `--cache /tmp/npm-cache`。
- **不要在旧副本上跑 `hexo g -d`**：会把旧文章推回 `main` 覆盖线上。唯一真相是这个 `source` 分支。
