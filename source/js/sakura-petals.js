/**
 * 櫻ノ詩 — 樱花飘落动画
 * Canvas-based cherry blossom petal effect
 */
(function () {
  'use strict';

  function createSakura() {
    if (document.getElementById('sakura-canvas')) return;

    var canvas = document.createElement('canvas');
    canvas.id = 'sakura-canvas';
    canvas.style.cssText =
      'position:fixed;top:0;left:0;z-index:99999;pointer-events:none;width:100%;height:100%;';
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d');
    var width = (canvas.width = window.innerWidth);
    var height = (canvas.height = window.innerHeight);
    var petals = [];
    var maxPetals = 45;

    // 樱之诗配色 — 淡粉到白色
    var colors = [
      'rgba(242,167,181,0.8)',
      'rgba(250,218,221,0.7)',
      'rgba(232,138,154,0.6)',
      'rgba(255,220,225,0.8)',
      'rgba(245,180,190,0.7)',
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
      this.opacity = Math.random() * 0.4 + 0.4;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.wobble = Math.random() * 40 + 20;
      this.wobbleSpeed = Math.random() * 0.003 + 0.001;
      this.phase = Math.random() * Math.PI * 2;
    }

    Petal.prototype.update = function () {
      this.y += this.speedY;
      this.x += this.speedX + Math.sin(this.y * this.wobbleSpeed + this.phase) * 0.5;
      this.rotation += this.rotationSpeed;

      // Reset when out of view
      if (this.y > height + 30) {
        this.y = -30;
        this.x = Math.random() * width;
      }
      if (this.x > width + 30) this.x = -30;
      if (this.x < -30) this.x = width + 30;
    };

    Petal.prototype.draw = function (ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.globalAlpha = this.opacity;

      // Draw a simple petal shape
      var s = this.size;
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.ellipse(0, 0, s * 0.6, s * 0.35, 0, 0, Math.PI * 2);
      ctx.fill();

      // Petal vein
      ctx.strokeStyle = 'rgba(255,255,255,0.3)';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(-s * 0.5, 0);
      ctx.lineTo(s * 0.5, 0);
      ctx.stroke();

      ctx.restore();
    };

    // Create initial petals
    for (var i = 0; i < maxPetals; i++) {
      var p = new Petal();
      p.y = Math.random() * height; // Start spread across screen
      petals.push(p);
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);
      for (var i = 0; i < petals.length; i++) {
        petals[i].update();
        petals[i].draw(ctx);
      }
      requestAnimationFrame(animate);
    }

    animate();

    // Resize handler
    window.addEventListener(
      'resize',
      function () {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      },
      { passive: true }
    );
  }

  // Start after page load for better performance
  if (document.readyState === 'complete') {
    createSakura();
  } else {
    window.addEventListener('load', createSakura);
  }
})();
