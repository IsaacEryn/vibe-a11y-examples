/* 복사 버튼.
 *
 * 복사 결과를 화면에도 보여주고 role="status" 영역에도 넣는다.
 * 색이나 아이콘만으로 알리지 않고 텍스트로 전달하는 것이 요점이다.
 */
(function () {
  var status = document.getElementById('copy-status');

  function announce(message) {
    if (!status) return;
    status.textContent = '';
    // 같은 문구를 연속으로 복사해도 다시 읽히도록 한 번 비운 뒤 넣는다.
    window.setTimeout(function () { status.textContent = message; }, 60);
    window.clearTimeout(announce.timer);
    announce.timer = window.setTimeout(function () { status.textContent = ''; }, 6000);
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-copy]');
    if (!button) return;

    var source = document.getElementById(button.getAttribute('data-copy'));
    if (!source) return;

    var heading = button.closest('.snippet').querySelector('h2, h3');
    var label = heading ? heading.textContent.trim() : '내용';

    navigator.clipboard.writeText(source.textContent).then(function () {
      announce(label + ' 복사됨');
    }, function () {
      announce('복사하지 못했습니다. 아래 내용을 직접 선택해 복사해주세요.');
    });
  });
})();
