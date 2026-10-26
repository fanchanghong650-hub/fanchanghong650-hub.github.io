/**
 * 桜ノ詩の庭 — 全站背景层
 *
 * 说明：这里原本是 galgame 截图轮播（8 张樱之诗 CG + 1 张 AI 壁纸），
 * 因版权原因已于 2026-10-26 全部移除，改为纯 CSS 渐变（无任何图片字节）。
 *
 * 想换回图片时：把自有版权的图片放进 source/images/bg/，
 * 然后在下面的 PHOTO_URLS 里填上路径即可（不要把 URL 留空）。
 */
(function () {
  'use strict';

  // 留空 = 使用 CSS 渐变；填入自有图片路径 = 使用图片轮播
  var PHOTO_URLS = [];
  var INTERVAL_MS = 3500;

  var LIGHT_STACK = [
    'radial-gradient(900px 620px at 15% 18%, rgba(255,255,255,0.50), rgba(255,255,255,0) 62%)',
    'radial-gradient(720px 520px at 82% 12%, rgba(255,238,243,0.60), rgba(255,255,255,0) 66%)',
    'radial-gradient(820px 620px at 72% 86%, rgba(226,140,163,0.38), rgba(255,255,255,0) 70%)',
    'radial-gradient(620px 420px at 28% 92%, rgba(255,214,225,0.55), rgba(255,255,255,0) 66%)',
    'linear-gradient(170deg, #EFB0C0 0%, #F7C8D4 28%, #F9D2DC 55%, #EDB2C2 82%, #F6C6D2 100%)'
  ].join(',');

  var DARK_STACK = [
    'radial-gradient(900px 620px at 15% 18%, rgba(140,55,80,0.42), rgba(0,0,0,0) 62%)',
    'radial-gradient(720px 520px at 82% 12%, rgba(100,38,58,0.48), rgba(0,0,0,0) 66%)',
    'radial-gradient(820px 620px at 72% 86%, rgba(70,26,40,0.55), rgba(0,0,0,0) 70%)',
    'linear-gradient(170deg, #1B1014 0%, #26141A 45%, #180E12 100%)'
  ].join(',');

  var isDark = function () {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  };

  // 图层 1：纯渐变底
  var base = document.createElement('div');
  base.id = 'site-bg';
  base.style.cssText = [
    'position:fixed', 'top:0', 'left:0', 'width:100%', 'height:100%',
    'z-index:-2', 'pointer-events:none', 'background-repeat:no-repeat',
    'background-size:cover', 'transition:opacity 0.6s ease-in-out'
  ].join(';');
  base.style.backgroundImage = isDark() ? DARK_STACK : LIGHT_STACK;

  // 图层 2：照片层（PHOTO_URLS 为空时保持全透明）
  var photo = document.createElement('div');
  photo.id = 'site-bg-photo';
  photo.style.cssText = [
    'position:fixed', 'top:0', 'left:0', 'width:100%', 'height:100%',
    'z-index:-1', 'pointer-events:none', 'background-size:cover',
    'background-position:center', 'background-repeat:no-repeat',
    'transition:opacity 2s ease-in-out', 'opacity:0'
  ].join(';');

  var mount = function () {
    document.body.appendChild(base);
    document.body.appendChild(photo);
    if (PHOTO_URLS.length) startSlideshow();
  };

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);

  // 暗色模式切换时同步换渐变
  new MutationObserver(function () {
    base.style.backgroundImage = isDark() ? DARK_STACK : LIGHT_STACK;
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme', 'class']
  });

  function startSlideshow() {
    var i = 0;
    var fade = true;
    photo.style.backgroundImage = 'url(' + PHOTO_URLS[0] + ')';
    photo.style.opacity = '1';
    setInterval(function () {
      i = (i + 1) % PHOTO_URLS.length;
      photo.style.opacity = '0';
      setTimeout(function () {
        photo.style.backgroundImage = 'url(' + PHOTO_URLS[i] + ')';
        photo.style.opacity = '1';
      }, fade ? 900 : 0);
    }, INTERVAL_MS);
  }
})();
