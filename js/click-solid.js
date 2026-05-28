/**
 * 桜ノ詩の庭 — Click transparent panel to solidify
 */
(function () {
  'use strict';

  function init() {
    var isArchive = document.body.classList.contains('page-archive');
    var isPost = document.body.classList.contains('page-post');
    var isCategory = document.body.classList.contains('page-category');
    var isTag = document.body.classList.contains('page-tag');
    if (!isArchive && !isPost && !isCategory && !isTag) return;

    function makeClickable(panel) {
      if (!panel) return;
      panel.addEventListener('click', function (e) {
        if (e.target.closest('a') || e.target.closest('pre') ||
            e.target.closest('button') || e.target.closest('input') ||
            e.target.closest('code') || e.target.closest('img')) {
          return;
        }
        panel.classList.toggle('solid');
      });
    }

    // Main content panel
    if (isArchive) makeClickable(document.getElementById('archive'));
    if (isPost) makeClickable(document.getElementById('article-container'));
    if (isCategory || isTag) makeClickable(document.getElementById('page'));

    // Sidebar cards
    var cards = document.querySelectorAll('#aside-content .card-widget');
    for (var i = 0; i < cards.length; i++) {
      (function (card) {
        card.addEventListener('click', function (e) {
          if (e.target.closest('a')) return;
          card.classList.toggle('solid');
        });
      })(cards[i]);
    }
  }

  if (document.readyState === 'complete') init();
  else window.addEventListener('load', init);
})();
