/* 화면 모드(밝게/어둡게) 선택.
 *
 * 기본값은 시스템 설정이다. 사용자가 직접 고르면 그 값을 저장해서
 * 다음에 다시 와도 고른 모드로 보인다. 저장한 값은 <html>의 data-theme
 * 속성으로 옮기고, 색은 site.css가 그 속성을 보고 바꾼다.
 *
 * 이 파일은 <head>에서 defer 없이 불러야 한다. 그래야 첫 화면이
 * 잠깐 다른 색으로 번쩍이지 않는다.
 */
(function () {
  var KEY = 'vibe-a11y-theme';
  var MODES = [['system', '시스템 설정'], ['light', '밝게'], ['dark', '어둡게']];
  var root = document.documentElement;

  // 사파리 시크릿 창이나 file:// 로 열었을 때 저장소 접근이 막히는 경우가 있다.
  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function write(value) {
    try {
      if (value === 'system') localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, value);
    } catch (e) { /* 저장만 못 할 뿐, 이번 방문 동안은 그대로 동작한다. */ }
  }

  function apply(mode) {
    if (mode === 'light' || mode === 'dark') root.setAttribute('data-theme', mode);
    else root.removeAttribute('data-theme');  // 속성이 없으면 시스템 설정을 따른다.
  }

  apply(read());

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.topnav');
    if (!nav) return;

    var label = document.createElement('label');
    label.htmlFor = 'theme-select';
    label.textContent = '화면 모드';

    var select = document.createElement('select');
    select.id = 'theme-select';
    MODES.forEach(function (mode) {
      select.appendChild(new Option(mode[1], mode[0]));
    });
    select.value = read() || 'system';
    select.addEventListener('change', function () {
      write(select.value);
      apply(select.value);
    });

    var wrap = document.createElement('span');
    wrap.className = 'theme-switch';
    wrap.append(label, select);
    nav.appendChild(wrap);
  });
})();
