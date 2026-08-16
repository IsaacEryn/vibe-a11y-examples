#!/usr/bin/env python3
"""마크다운 원본에서 사이트 페이지를 생성한다.

  book/vibe-a11y/prompts/README.md          -> prompts/index.html
  book/vibe-a11y/rules/accessibility-rules.md -> rules/index.html

원본 md는 책 원고에서 생성되므로(writer 저장소의 조립 과정) 여기서는
md를 단일 소스로 삼아 HTML만 다시 만든다.

사용: python3 scripts/build-pages.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'book' / 'vibe-a11y'

HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231d4ed8'/%3E%3Ctext x='16' y='23' font-size='19' font-family='sans-serif' font-weight='700' fill='%23fff' text-anchor='middle'%3Ea%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>
<a class="skip" href="#main">본문으로 건너뛰기</a>

<header>
  <p class="topnav"><a href="../">실습 데모 목록</a></p>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</header>

<main id="main">
'''

FOOT = '''</main>

<footer>
  <p>이 페이지는 <a href="{src}">{srcname}</a>에서 생성됩니다. 내용 수정은 원본 파일에서 합니다.</p>
  <p>《바이브 코딩, 접근성까지 부탁해》 실습 데모 ·
     <a href="https://github.com/IsaacEryn/vibe-a11y-examples">GitHub 저장소</a></p>
</footer>

<script src="../assets/copy.js" defer></script>
</body>
</html>
'''


def slugify(text, seen):
    base = re.sub(r'[^0-9A-Za-z가-힣]+', '-', text).strip('-').lower() or 'item'
    slug, n = base, 2
    while slug in seen:
        slug, n = f'{base}-{n}', n + 1
    seen.add(slug)
    return slug


def snippet(title, body, slug, label, level='h3'):
    """제목 + 복사 버튼 + 코드 블록 한 덩어리."""
    return f'''<section class="snippet" id="{slug}">
  <div class="snippet-head">
    <{level}>{html.escape(title)}</{level}>
    <button type="button" class="subtle" data-copy="{slug}-text">{label}</button>
  </div>
  <pre id="{slug}-text">{html.escape(body)}</pre>
</section>
'''


def build_prompts():
    md = (SITE / 'prompts' / 'README.md').read_text()
    items = re.findall(r'^## (.+?)\n\n```text\n(.*?)\n```', md, re.S | re.M)
    seen, toc, body = set(), [], []
    for title, code in items:
        slug = slugify(title, seen)
        toc.append(f'<li><a href="#{slug}">{html.escape(title)}</a></li>')
        body.append(snippet(title, code, slug, '프롬프트 복사'))

    out = HEAD.format(
        title='복사해서 쓰는 프롬프트 모음 — 바이브 코딩, 접근성까지 부탁해',
        desc='책 본문에 등장하는 접근성 프롬프트 전문. 버튼 한 번으로 복사해 AI에게 그대로 붙여 넣으세요.',
        h1='복사해서 쓰는 프롬프트 모음',
        lede='책 본문에 등장하는 프롬프트입니다. 복사해서 쓰되, 대괄호로 표시한 부분은 프로젝트에 맞게 바꿔주세요.',
    )
    out += '''  <nav class="toc" aria-labelledby="toc-title">
    <h2 id="toc-title">이 페이지의 프롬프트</h2>
    <ul>
''' + '\n'.join('      ' + t for t in toc) + '''
    </ul>
  </nav>

  <p class="lede">복사 버튼을 누르면 결과를 소리로도 알려줍니다.
     화면 변화를 시각 외의 방법으로 전달하는 방식으로, 책 14장에서 다루는 상태 메시지의 실제 예입니다.</p>

  <p class="copy-status" role="status" aria-live="polite" id="copy-status"></p>

''' + '\n'.join(body)
    out += FOOT.format(
        src='https://github.com/IsaacEryn/vibe-a11y-examples/blob/main/book/vibe-a11y/prompts/README.md',
        srcname='prompts/README.md')
    (SITE / 'prompts' / 'index.html').write_text(out)
    return len(items)


def build_rules():
    md = (SITE / 'rules' / 'accessibility-rules.md').read_text()
    m = re.search(r'```markdown\n(.*?)```', md, re.S)
    rules = m.group(1).rstrip()
    intro = '''  <p>AI 코딩 도구가 매번 읽는 규칙 파일(CLAUDE.md, AGENTS.md, Cursor Rules 등)에
     그대로 붙여 넣으세요. 한 번 넣어두면 앞으로 만드는 모든 화면에 적용됩니다.
     각 규칙을 왜 그렇게 정했는지는 책 8장에서 다룹니다.</p>

  <p class="copy-status" role="status" aria-live="polite" id="copy-status"></p>

'''
    out = HEAD.format(
        title='접근성 기본 규칙 세트 — 바이브 코딩, 접근성까지 부탁해',
        desc='AI 규칙 파일에 붙여 넣는 웹 접근성 규칙 세트. 책 8장의 규칙 전문.',
        h1='접근성 기본 규칙 세트',
        lede='책 8장에서 만드는 규칙입니다. 프로젝트의 AI 규칙 파일에 통째로 붙여 넣으면 됩니다.',
    ) + intro + snippet('규칙 전문', rules, 'rules', '전체 복사', level='h2')
    out += FOOT.format(
        src='https://github.com/IsaacEryn/vibe-a11y-examples/blob/main/book/vibe-a11y/rules/accessibility-rules.md',
        srcname='rules/accessibility-rules.md')
    (SITE / 'rules' / 'index.html').write_text(out)
    return rules.count('\n') + 1


if __name__ == '__main__':
    print(f'prompts/index.html — 프롬프트 {build_prompts()}개')
    print(f'rules/index.html — 규칙 {build_rules()}줄')
