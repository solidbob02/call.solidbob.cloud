#!/usr/bin/env python3
"""빌드된 지킬 사이트의 내부 링크가 실제 페이지를 가리키는지 검사한다.

파일 이름이나 소제목을 바꾸면 링크가 조용히 깨진다. 빌드는 통과하므로
사람이 클릭해 보기 전까지 아무도 모른다. 이 검사가 그걸 잡는다.

  사용:  python3 scripts/check_site_links.py [사이트_경로]
         (기본값: jekyll/_site)

  종료 코드:  0 = 깨진 링크 없음, 1 = 있음
"""

from __future__ import annotations

import glob
import os
import re
import sys
import urllib.parse

# 링크 검사 대상에서 제외 — 지킬이 만들지 않는 정적 자산·피드
SKIP_PREFIXES = ("/assets",)
SKIP_SUFFIXES = (".xml", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".ico")


def main(site_dir: str) -> int:
    if not os.path.isdir(site_dir):
        print(f"사이트 디렉터리가 없습니다: {site_dir}")
        print("먼저 `cd jekyll && bundle exec jekyll build` 를 실행하십시오.")
        return 1

    pages = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)
    anchors: dict[str, set[str]] = {}
    for page in pages:
        html = open(page, encoding="utf-8").read()
        anchors[page] = set(re.findall(r'id="([^"]+)"', html))

    broken: list[tuple[str, str, str]] = []
    for page in pages:
        html = open(page, encoding="utf-8").read()
        # 절대 경로(/...) 링크만 본다. 외부 링크(https://)는 검사 범위 밖이다.
        for path, frag in re.findall(r'href="(/[^"#]*)(#[^"]*)?"', html):
            if path.startswith(SKIP_PREFIXES) or path.endswith(SKIP_SUFFIXES):
                continue
            target = site_dir + path
            candidate = target if target.endswith(".html") else os.path.join(target, "index.html")
            rel = os.path.relpath(page, site_dir)
            if not os.path.exists(candidate):
                broken.append((rel, path + frag, "페이지 없음"))
            elif frag:
                name = urllib.parse.unquote(frag[1:])
                if name not in anchors.get(candidate, set()):
                    broken.append((rel, path + frag, "앵커 없음"))

    print(f"검사한 페이지: {len(pages)}")
    print(f"깨진 내부 링크: {len(broken)}")
    for src, link, why in broken:
        print(f"  {src} → {link}  ({why})")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "jekyll/_site"))
