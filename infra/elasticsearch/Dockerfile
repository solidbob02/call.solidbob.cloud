# Requirement: B-2
# 공식 Elasticsearch 이미지에는 nori(한국어 형태소 분석기)가 들어 있지 않다.
# 기획서 3.1절이 "nori(BM25) + dense_vector + RRF" 로 지정했으므로 플러그인을 넣어 굽는다.
#
# 이미지를 따로 굽는 이유: 컨테이너가 뜰 때마다 설치하면 기동이 느려지고,
# 네트워크가 없는 환경에서 실패한다.
#
# ⚠ 버전을 바꾸면 `ai/requirements.txt` 의 클라이언트도 같이 바꿔야 한다.
#    9.x 클라이언트는 8.x 서버에 붙지 않는다 — 실측:
#    `BadRequestError(400, 'media_type_header_exception', ... Accept version must be
#     either version 8 or 7, but found 9)`. 접속 자체가 거부된다.
ARG ES_VERSION=9.5.1
FROM docker.elastic.co/elasticsearch/elasticsearch:${ES_VERSION}

RUN bin/elasticsearch-plugin install --batch analysis-nori
