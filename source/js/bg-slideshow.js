/**
 * 桜ノ詩の庭 — 背景图片轮播
 * Cycles background images on archive and article pages
 */
(function () {
  'use strict';

  // Run on archive, post, category, and tag pages
  var path = window.location.pathname;
  var isPost = path.match(/\/\d{4}\/\d{2}\/\d{2}\//);
  var isArchive = path.match(/\/archives\//);
  var isCategory = path.match(/\/categories\//);
  var isTag = path.match(/\/tags\//);
  if (!isPost && !isArchive && !isCategory && !isTag) return;

  var bgIndex = 0;
  var bgInterval = 8000; // 8 seconds per image

  var images = [
    '/images/bg/sakura_ai_wallpaper_pc_01.png',
    '/images/bg/' + encodeURIComponent('屏幕截图 2026-05-05 212232.png'),
    '/images/bg/' + encodeURIComponent('屏幕截图 2026-05-10 135332.png'),
    '/images/bg/' + encodeURIComponent('屏幕截图 2026-05-23 230354.png'),
    '/images/bg/' + encodeURIComponent('屏幕截图 2026-05-26 220923.png'),
  ];

  // Preload images
  var preloaded = [];
  images.forEach(function (src) {
    var img = new Image();
    img.src = src;
    preloaded.push(img);
  });

  // Create background layers for crossfade
  var layer1 = document.createElement('div');
  layer1.id = 'bg-layer-1';
  layer1.style.cssText =
    'position:fixed;top:0;left:0;width:100%;height:100%;z-index:-2;' +
    'background-size:cover;background-position:center;background-repeat:no-repeat;' +
    'transition:opacity 2s ease-in-out;opacity:1;';

  var layer2 = document.createElement('div');
  layer2.id = 'bg-layer-2';
  layer2.style.cssText =
    'position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;' +
    'background-size:cover;background-position:center;background-repeat:no-repeat;' +
    'transition:opacity 2s ease-in-out;opacity:0;';

  // Set initial background
  layer1.style.backgroundImage = 'url(' + images[0] + ')';
  document.body.appendChild(layer1);
  document.body.appendChild(layer2);

  var activeLayer = 1;

  function nextSlide() {
    bgIndex = (bgIndex + 1) % images.length;
    var nextBg = images[bgIndex];

    if (activeLayer === 1) {
      layer2.style.backgroundImage = 'url(' + nextBg + ')';
      layer2.style.opacity = '1';
      layer1.style.opacity = '0';
      activeLayer = 2;
    } else {
      layer1.style.backgroundImage = 'url(' + nextBg + ')';
      layer1.style.opacity = '1';
      layer2.style.opacity = '0';
      activeLayer = 1;
    }
  }

  setInterval(nextSlide, bgInterval);

  // Add dark overlay for readability
  var overlay = document.createElement('div');
  overlay.id = 'bg-overlay';
  overlay.style.cssText =
    'position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;' +
    'background:rgba(0,0,0,0.25);pointer-events:none;';
  document.body.appendChild(overlay);
})();
