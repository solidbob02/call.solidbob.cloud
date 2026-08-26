"""server/apps — 허브(hub)와 스포크들의 컨테이너. main.py·pytest.ini·.importlinter 가 이 디렉토리를 PYTHONPATH 에 올려
각 앱이 최상위 패키지로 보이게 한다 (hub.app.dtos... 처럼 앱 이름부터 시작하는 import).

여기에는 "요청이 흐르는 길"만 둔다. 청킹·검색·리랭크·모델·평가는 ../ai/apps 다.
경계는 ../CLAUDE.md 참고. server → ai 방향 import 는 .importlinter 계약 2 가 막는다.
"""
