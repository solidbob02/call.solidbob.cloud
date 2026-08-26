"""ai/apps — 검색·모델·평가 모듈의 컨테이너. pytest.ini·.importlinter 가 이 디렉토리와
../server/apps 를 함께 PYTHONPATH 에 올린다.

../server/apps 를 올리는 이유: evaluation 이 hub 의 포트·DTO(계약)를 import 한다.
계약은 server 가 정의하고 여기서 구현·채점한다 — 의존 방향은 ai → server 한쪽뿐이다.
경계는 ../CLAUDE.md 참고.
"""
