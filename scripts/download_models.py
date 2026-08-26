"""모델 가중치를 data/README.md와 같은 방식으로 models/ 아래에 받아둔다.
크기가 커서 커밋 대상이 아니다 (.gitignore 참고). 필요할 때 다시 실행하면 된다.

생성 모델(B-4)은 여기 없다 — 2026-08-26 exaone3.5:2.4b(Ollama 서빙)로 교체되면서
`ollama pull exaone3.5:2.4b`로 받는다(HuggingFace snapshot_download 대상 아님).
`_project/decisions/009-생성모델-EXAONE-Ollama-확정.md` 참고. 기존
`EleutherAI/polyglot-ko-1.3b`는 목록에서 뺐다(로컬에 남아 있으면 지워도 된다).

컴플라이언스 분류기·NER 베이스는 아직 교체를 결정하지 않았다 — 후보와 판단 재료는
`jekyll/open-items.markdown` 참고."""

import os
from huggingface_hub import snapshot_download

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

TARGETS = [
    # (허깅페이스 repo id, 로컬 폴더명, 용도)
    ("jhgan/ko-sroberta-multitask", "ko-sroberta-multitask", "임베딩 — B-2 하이브리드 검색 dense_vector"),
    ("beomi/KcELECTRA-base", "kcelectra-base", "컴플라이언스 분류기 베이스 — C-1~C-4 파인튜닝 대상 (교체 검토 중)"),
    ("monologg/koelectra-base-v3-naver-ner", "koelectra-ner", "NER — C-5 마스킹 P6(인명)·P7(주소) (교체 검토 중)"),
]

for repo_id, local_name, purpose in TARGETS:
    dest = os.path.join(MODELS_DIR, local_name)
    print(f"\n=== {repo_id} -> models/{local_name} ({purpose}) ===")
    snapshot_download(repo_id=repo_id, local_dir=dest)
    print(f"완료: {dest}")

print("\n전체 다운로드 완료")
