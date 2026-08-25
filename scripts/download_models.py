"""모델 가중치를 data/README.md와 같은 방식으로 models/ 아래에 받아둔다.
크기가 커서 커밋 대상이 아니다 (.gitignore 참고). 필요할 때 다시 실행하면 된다."""

import os
from huggingface_hub import snapshot_download

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

TARGETS = [
    # (허깅페이스 repo id, 로컬 폴더명, 용도)
    ("jhgan/ko-sroberta-multitask", "ko-sroberta-multitask", "임베딩 — B-2 하이브리드 검색 dense_vector"),
    ("beomi/KcELECTRA-base", "kcelectra-base", "컴플라이언스 분류기 베이스 — C-1~C-4 파인튜닝 대상"),
    ("monologg/koelectra-base-v3-naver-ner", "koelectra-ner", "NER — C-5 마스킹 P6(인명)·P7(주소)"),
    ("EleutherAI/polyglot-ko-1.3b", "polyglot-ko-1.3b", "카드 요약 생성 — B-4, MPS(Apple M5) 기준 소형 시작점"),
]

for repo_id, local_name, purpose in TARGETS:
    dest = os.path.join(MODELS_DIR, local_name)
    print(f"\n=== {repo_id} -> models/{local_name} ({purpose}) ===")
    snapshot_download(repo_id=repo_id, local_dir=dest)
    print(f"완료: {dest}")

print("\n전체 다운로드 완료")
