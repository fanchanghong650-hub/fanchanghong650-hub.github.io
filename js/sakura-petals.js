/**
 * 櫻ノ詩 — 樱花飘落动画 (性能优化版)
 * Canvas-based cherry blossom petal effect
 *
 * 优化要点：
 * - 帧率限制到 ~30fps（视觉无差异，GPU 负担减半）
 * - alpha 预烘焙到颜色值（消除 globalAlpha 合成开销）
 * - 利用 ellipse() 原生旋转参数，消除 ctx.save/restore
 * - 花瓣数量从 45 降至 36
 * - resize 添加 debounce
 * - devicePixelRatio 上限 2x（高分屏避免 3x 渲染）
 */
(function () {
  'use strict';

  function createSakura() {
    if (document.getElementById('sakura-canvas')) return;

    var canvas = document.createElement('canvas');
    canvas.id = 'sakura-canvas';
    canvas.style.cssText =
      'position:fixed;top:0;left:0;z-index:99999;pointer-events:none;width:100%;height:100%;' +
      'will-change:transform;';
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d', { alpha: true });
    var dpr = Math.min(window.devicePixelRatio || 1, 2); // Cap at 2x
    var width, height;

    function resizeCanvas() {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resizeCanvas();

    var petals = [];
    var maxPetals = 36;

    // Alpha 已预烘焙到颜色值 — 无需 globalAlpha
    var colors = [
      'rgba(242,167,181,0.80)',
      'rgba(250,218,221,0.70)',
      'rgba(232,138,154,0.60)',
      'rgba(255,220,225,0.80)',
      'rgba(245,180,190,0.70)',
      'rgba(255,235,238,0.75)',
    ];

    function Petal() {
      this.x = Math.random() * width;
      this.y = Math.random() * -height;
      this.size = Math.random() * 12 + 6;
      this.speedY = Math.random() * 0.8 + 0.4;
      this.speedX = Math.random() * 0.6 - 0.3;
      this.rotation = Math.random() * Math.PI * 2;
      this.rotationSpeed = (Math.random() - 0.5) * 0.02;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      // 叶脉线颜色（alpha 预烘焙）
      this.veinAlpha = 0.2 + Math.random() * 0.2;
      this.wobbleSpeed = Math.random() * 0.003 + 0.001;
      this.phase = Math.random() * Math.PI * 2;
    }

    Petal.prototype.update = function () {
      this.y += this.speedY;
      this.x += this.speedX + Math.sin(this.y * this.wobbleSpeed + this.phase) * 0.5;
      this.rotation += this.rotationSpeed;

      if (this.y > height + 30) {
        this.y = -30;
        this.x = Math.random() * width;
      }
      if (this.x > width + 30) this.x = -30;
      if (this.x < -30) this.x = width + 30;
    };

    Petal.prototype.draw = function (ctx) {
      var s = this.size;

      // 使用 ellipse() 的原生旋转参数，无需 save/translate/rotate/restore
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, s * 0.6, s * 0.35, this.rotation, 0, Math.PI * 2);
      ctx.fill();

      // 叶脉（颜色在构造时预计算，避免每帧字符串拼接）
      if (!this._veinColor) {
        this._veinColor = 'rgba(255,255,255,' + this.veinAlpha.toFixed(2) + ')';
      }
      ctx.strokeStyle = this._veinColor;
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      var hw = Math.cos(this.rotation) * s * 0.5;
      var hh = Math.sin(this.rotation) * s * 0.5;
      ctx.moveTo(this.x - hw, this.y - hh);
      ctx.lineTo(this.x + hw, this.y + hh);
      ctx.stroke();
    };

    // 初始花瓣分布在屏幕各处
    for (var i = 0; i < maxPetals; i++) {
      var p = new Petal();
      p.y = Math.random() * height;
      petals.push(p);
    }

    // 帧率限制 ~30fps
    var FPS = 30;
    var frameInterval = 1000 / FPS;
    var lastTime = 0;

    function animate(timestamp) {
      requestAnimationFrame(animate);

      var elapsed = timestamp - lastTime;
      if (elapsed < frameInterval) return;
      lastTime = timestamp - (elapsed % frameInterval);

      ctx.clearRect(0, 0, width, height);
      for (var i = 0; i < petals.length; i++) {
        petals[i].update();
        petals[i].draw(ctx);
      }
    }

    requestAnimationFrame(animate);

    // Debounced resize
    var resizeTimer;
    window.addEventListener(
      'resize',
      function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resizeCanvas, 200);
      },
      { passive: true }
    );
  }

  if (document.readyState === 'complete') {
    createSakura();
  } else {
    window.addEventListener('load', createSakura);
  }
})();
