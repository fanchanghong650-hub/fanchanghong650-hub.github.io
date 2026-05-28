---
title: 博客编辑操作指南
date: 2026-05-28 20:00:00
categories: 文档
tags: [指南, Hexo, 博客]
---

## 项目总览

本博客使用 **Hexo 8.x** 静态网站生成器，主题为 **Butterfly 5.x**，部署在 **GitHub Pages**。

```
C:\blog\
├── _config.yml              # 主配置文件（网站标题、作者、URL、部署）
├── _config.butterfly.yml    # 主题配置文件（头像、导航、颜色、功能开关）
├── source\                  # 网站源文件（你编辑的所有内容都在这里）
│   ├── _posts\              # 博客文章（.md 文件）
│   ├── about\index.md       # "关于"页面
│   ├── categories\index.md  # 分类页面
│   ├── tags\index.md        # 标签页面
│   ├── css\custom.css       # 自定义样式（背景、颜色、面板效果）
│   ├── js\                  # 自定义脚本
│   │   ├── bg-slideshow.js  # 背景图片轮播
│   │   ├── sakura-petals.js # 樱花飘落动画
│   │   ├── body-class.js    # 页面类型标记
│   │   └── click-solid.js   # 点击面板变实心
│   └── images\bg\           # 背景图片存放处
├── scaffolds\               # 文章模板
├── themes\butterfly\        # 主题文件（一般不需要改）
├── public\                  # 生成的静态网站（自动生成，不要手动编辑）
├── node_modules\            # npm 依赖（自动管理）
└── package.json             # 项目依赖清单
```

### 修改是否自动同步？

- **本地预览** (`hexo server`)：修改 `source/` 下的文件会自动刷新。修改 `_config.yml` 或 `_config.butterfly.yml` 需要重启 `hexo server`。
- **线上网站**：本地修改后，需要执行 `hexo clean; hexo generate; hexo deploy` 才能部署到 GitHub Pages。线上不会自动同步。

---

## 一、发布文章

### 创建新文章

在终端中执行：

```bash
cd C:\blog
hexo new post "你的文章标题"
```

这会自动在 `source\_posts\` 下创建一个 `.md` 文件，文件名格式为 `你的文章标题.md`。

也可以直接在 `source\_posts\` 下手动创建 `.md` 文件，但必须包含 **Front Matter**（见下文）。

### 文章 Front Matter

每篇文章开头必须包含以下元数据：

```yaml
---
title: 文章标题
date: 2026-05-28 20:00:00
categories: [分类1, 子分类2]   # 支持多级分类
tags: [标签1, 标签2, 标签3]     # 支持多个标签
---
```

`hexo new` 命令会自动生成 `title` 和 `date`，你只需要补充 `categories` 和 `tags`。

### 文章正文

使用 Markdown 语法编写（参考本站的另一篇「Markdown 语法参考」）。

### 发布流程

```bash
cd C:\blog
hexo clean        # 清除缓存
hexo generate     # 生成静态文件（可简写为 hexo g）
hexo deploy       # 部署到 GitHub Pages（可简写为 hexo d）
```

也可以合并为：`hexo clean; hexo generate; hexo deploy`

> 注意：使用 PowerShell 时必须用分号 `;` 分隔命令，不能用 `&&`。

### 草稿

如果文章还没写完，可以创建为草稿：

```bash
hexo new draft "草稿标题"
```

草稿保存在 `source\_drafts\`，不会发布。完成后用以下命令发布：

```bash
hexo publish draft "草稿标题"
```

---

## 二、替换背景图片

### 背景图片位置

所有背景图片存放在 `C:\blog\source\images\bg\`。

当前使用的 9 张背景图片（定义在 `bg-slideshow.js` 的 `images` 数组中）：
1. `sakura_ai_wallpaper_pc_01.png`
2. `屏幕截图 2026-05-05 212232.png`
3. `屏幕截图 2026-05-10 135332.png`
4. `屏幕截图 2026-05-23 230354.png`
5. `屏幕截图 2026-05-26 220923.png`
6. `屏幕截图 2026-05-05 213723.png`
7. `屏幕截图 2026-05-05 214857.png`
8. `屏幕截图 2026-05-17 224053.png`
9. `屏幕截图 2026-05-23 112138.png`

### 替换步骤

1. 将新图片放入 `C:\blog\source\images\bg\`
2. 编辑 `C:\blog\source\js\bg-slideshow.js`
3. 在 `images` 数组中增删条目。例如：

```javascript
var images = [
  '/images/bg/你的新图片1.png',
  '/images/bg/你的新图片2.png',
  '/images/bg/你的新图片3.png',
];
```

> **注意**：文件名含中文时，需要用 `encodeURIComponent()` 包裹文件名部分，否则浏览器可能无法加载。格式为：
> ```javascript
> '/images/bg/' + encodeURIComponent('中文文件名.png')
> ```

4. 图片数量没有限制，轮播脚本会自动适应
5. 如果要调整切换间隔，修改 `bgInterval` 的值（单位毫秒，当前 3500 = 3.5秒）
6. 重新部署：`hexo clean; hexo generate; hexo deploy`

### 添加更多或更少背景图

- **增加图片**：在数组中添加新行，格式为 `'/images/bg/文件名.png',`
- **减少图片**：删除对应的行
- 轮播会自动适应图片数量

---

## 三、更改网站配色

所有自定义颜色定义在 `C:\blog\source\css\custom.css`。

### 主要颜色变量

在 `custom.css` 文件的第 13-18 行，`:root` 块中：

```css
:root {
  --sakura-pink: #F2A7B5;        /* 主粉色 */
  --sakura-dark: #E88A9A;         /* 深粉色（链接悬停、强调） */
  --sakura-light: #FADADD;        /* 浅粉色（选中文字背景） */
  --panel-transparent: rgba(255, 255, 255, 0.22);  /* 半透明面板 */
  --panel-solid: rgba(255, 250, 251, 0.93);         /* 实心面板 */
}
```

修改这些变量的值即可改变全局配色。例如换为蓝色系：

```css
:root {
  --sakura-pink: #7BA3D6;
  --sakura-dark: #5A8AC5;
  --sakura-light: #D0E3FA;
  --panel-transparent: rgba(255, 255, 255, 0.22);
  --panel-solid: rgba(245, 249, 255, 0.93);
}
```

### 主题色配置

在 `C:\blog\_config.butterfly.yml` 中搜索 `theme_color`，可以设置主题级的颜色：

```yaml
theme_color:
  main: "#F2A7B5"            # 主题色
  paginator: "#F2A7B5"       # 分页按钮色
  button_hover: "#E88A9A"    # 按钮悬停色
  text_selection: "#FADADD"  # 文字选中色
  link_color: "#E88A9A"      # 链接色
```

### 其他可改的颜色

`custom.css` 中还有以下颜色可以修改：

| 位置 | 用途 |
|------|------|
| `#nav` background | 导航栏背景 |
| `blockquote` border-left | 引用块左边框颜色 |
| `#pagination .page-number.current` | 分页当前页按钮 |
| `.tag-cloud-list a` | 标签云文字颜色 |
| `::-webkit-scrollbar-thumb` | 滚动条颜色 |
| `#toc .toc-link.active` | 目录激活项颜色 |
| `::selection` | 选中文字颜色 |

---

## 四、更换头像和图标

### 头像

编辑 `C:\blog\_config.butterfly.yml`，找到 `avatar` 部分：

```yaml
avatar:
  img: /img/butterfly-icon.png   # 改为你的头像路径
  effect: false
```

建议将头像图片放到 `C:\blog\source\images\` 下，然后配置为：

```yaml
avatar:
  img: /images/avatar.jpg
```

### 网站图标（Favicon）

同一文件中找到 `favicon`：

```yaml
favicon: /img/favicon.png
```

将你的 favicon 图片放到 `C:\blog\source\images\`，改为：

```yaml
favicon: /images/favicon.ico
```

---

## 五、更改网站文字

### 网站标题、副标题、作者名

编辑 `C:\blog\_config.yml`：

```yaml
title: 桜ノ詩の庭              # 网站标题
subtitle: '桜の花びらが舞う庭で'  # 副标题
description: '记录数学思考与编程笔记 — 桜色の個人ブログ'  # 网站描述
author: Fam_RiverBird          # 作者名
keywords: blog, math, python, acg, 数学, Python  # SEO关键词
```

### 首页打字机副标题

编辑 `C:\blog\_config.butterfly.yml`，搜索 `subtitle`：

```yaml
subtitle:
  enable: true
  effect: true    # 打字机效果
  source: 3       # 3 = 使用自定义文字；改为 false 则使用 _config.yml 的 subtitle
  sub:
    - 桜の花びらが舞う庭で
    - 風が運ぶ、遠い記憶の欠片
    - 知識は花のように、そっと咲き誇る
    - 白昼夢の中、桜は永遠に散らない
```

修改 `sub` 列表中的文字即可更改首页显示的句子。

### "关于"页面

编辑 `C:\blog\source\about\index.md`，直接修改正文内容。

### 导航菜单文字

导航菜单的文字来自主题的语言文件，但菜单项名称在 `_config.butterfly.yml` 中配置：

```yaml
menu:
  Home: / || fas fa-home
  Archives: /archives/ || fas fa-archive
  Categories: /categories/ || fas fa-folder
  Tags: /tags/ || fas fa-tags
  About: /about/ || fas fa-heart
```

格式：`显示名称: 链接 || 图标`

- 添加新菜单项：新增一行
- 删除菜单项：删除对应行
- 修改显示文字：改冒号前面的文字

如需深度修改导航文字（如 Archives → 归档），需编辑 `C:\blog\themes\butterfly\languages\zh-CN.yml`。

### 页脚信息

编辑 `C:\blog\_config.butterfly.yml`，搜索 `footer` 部分。可以自定义版权信息等。

---

## 六、本地预览

在部署到线上之前，建议先在本地预览效果：

```bash
cd C:\blog
hexo server
```

然后在浏览器打开 `http://localhost:4000`。

- 修改 `source/` 下的文件会自动刷新
- 修改 `_config.yml` 或 `_config.butterfly.yml` 后需要重启 `hexo server`（按 Ctrl+C 停止，再重新运行）

常用预览命令：
```bash
hexo server -p 5000    # 使用 5000 端口
hexo server --draft    # 预览草稿
```

---

## 七、部署到 GitHub Pages

### 完整部署流程

```bash
cd C:\blog
git add -A
git commit -m "描述你的修改"
git push -u origin main
hexo clean; hexo generate; hexo deploy
```

### 部署原理

1. `git push` 将源代码推送到 GitHub 仓库的 main 分支（备份源码）
2. `hexo deploy` 将生成的静态网站推送到同一仓库的 main 分支（GitHub Pages 读取这个分支）
3. 网站地址：`https://fanchanghong650-hub.github.io`

### 线上与本地同步

这个博客可以一直存在，只要 GitHub Pages 服务不停止，你的仓库不被删除。

> **重要**：每次本地修改后，必须执行 `hexo clean; hexo generate; hexo deploy` 才能让线上网站更新。修改不会自动同步。

---

## 八、文件操作速查表

| 你想要的操作 | 编辑的文件 | 是否需要部署 |
|-------------|-----------|-------------|
| 发布新文章 | `source\_posts\xxx.md` | 是 |
| 修改"关于"页面 | `source\about\index.md` | 是 |
| 更改背景图片 | `source\images\bg\` + `source\js\bg-slideshow.js` | 是 |
| 更改网站配色 | `source\css\custom.css` | 是 |
| 更改头像 | `_config.butterfly.yml` → avatar | 是 |
| 更改网站标题/作者名 | `_config.yml` → title/author | 是 |
| 更改首页副标题 | `_config.butterfly.yml` → subtitle | 是 |
| 更改导航菜单 | `_config.butterfly.yml` → menu | 是 |
| 添加/删除页面 | `source\` 下创建或删除文件夹 | 是 |
| 调整樱花动画 | `source\js\sakura-petals.js` | 是 |
| 调整面板透明度 | `source\css\custom.css` | 是 |
| 更改 favicon | `_config.butterfly.yml` → favicon | 是 |

> 所有需要部署的操作，都执行：`hexo clean; hexo generate; hexo deploy`

---

## 九、常见问题

### Q: hexo deploy 失败，提示 "Repository not found"
A: 检查 `_config.yml` 中 `deploy.repo` 是否与你的 GitHub 仓库地址完全一致。

### Q: 修改了 CSS/JS 但线上没变化
A: 浏览器可能缓存了旧文件。按 Ctrl+Shift+R 强制刷新，或在部署前执行 `hexo clean`。

### Q: 如何删除文章
A: 直接删除 `source\_posts\` 下对应的 `.md` 文件，然后重新部署。

### Q: 图片不显示
A: 确认图片路径以 `/images/` 开头（对应 `source\images\` 目录），且文件名（包括中文）完全正确。

### Q: 这个博客能永久存在吗
A: 只要你不删除 GitHub 仓库，并且 GitHub Pages 服务不停止，博客就永久在线。建议定期备份 `C:\blog` 文件夹。
