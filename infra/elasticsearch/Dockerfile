# Requirement: B-2
# 공식 Elasticsearch 이미지에는 nori(한국어 형태소 분석기)가 들어 있지 않다.
# 기획서 3.1절이 "nori(BM25) + dense_vector + RRF" 로 지정했으므로 플러그인을 넣어 굽는다.
#
# 이미지를 따로 굽는 이유: 컨테이너가 뜰 때마다 설치하면 기동이 느려지고,
# 네트워크가 없는 환경에서 실패한다.
ARG ES_VERSION=8.15.3
FROM docker.elastic.co/elasticsearch/elasticsearch:${ES_VERSION}

RUN bin/elasticsearch-plugin install --batch analysis-nori
