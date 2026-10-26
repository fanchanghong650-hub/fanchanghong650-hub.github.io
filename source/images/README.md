# 图片目录

文章里要用的图片放这里，正文写：

```markdown
![](/images/你的文件名.png)
```

这样网站上 100% 正确。（在 Obsidian 里会显示不出来，因为 Obsidian 把 `/` 当 vault 根，这是正常现象，不影响发布。）

## 关于背景图

这个目录下原本有 `bg/`，装着 8 张 galgame 截图和 1 张 AI 壁纸，共 22MB，用作首页轮播背景。
**2026-10-26 已全部移除**（版权原因），本地备份在 `~/Pictures/樱之诗CG/`。

现在站点背景由 `source/js/bg.js` 里的纯 CSS 渐变提供，不占体积。

如果想换回图片背景：把**自有版权**的图片放进 `source/images/bg/`，然后在 `source/js/bg.js` 顶部的 `PHOTO_URLS` 里填上路径即可。
