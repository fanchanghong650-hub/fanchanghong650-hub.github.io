/**
 * Add body classes based on URL path for CSS targeting
 */
(function () {
  'use strict';

  function init() {
    var path = window.location.pathname;
    var body = document.body;

    if (path === '/' || path === '/index.html') {
      body.classList.add('page-home');
    } else if (path.match(/\/archives\//)) {
      body.classList.add('page-archive');
    } else if (path.match(/\/\d{4}\/\d{2}\/\d{2}\//)) {
      body.classList.add('page-post');
    } else if (path.match(/\/categories\//)) {
      body.classList.add('page-category');
    } else if (path.match(/\/tags\//)) {
      body.classList.add('page-tag');
    } else if (path.match(/\/about\//)) {
      body.classList.add('page-page');
    }
  }

  // Wait for body to exist — this script is loaded in <head>
  if (document.body) {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
