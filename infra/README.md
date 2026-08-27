# infra/

로컬 개발 인프라. **팀원 누구나 같은 명령으로 같은 상태**를 만들 수 있게 두는 곳이다.

> ⚠ 운영(AWS) 인프라는 정성윤 담당이다([7.1절](/docs/07/)). 이 폴더는 **로컬 개발용**이고,
> 여기 있는 값으로 운영을 띄우지 않는다.

## MySQL

```bash
cd infra
docker compose up -d          # 최초 기동 시 ../db/schema.sql 이 자동 적용된다
docker compose ps             # 상태 확인 (healthy 가 될 때까지 30초쯤 걸린다)
docker compose logs -f mysql  # 기동 로그
docker compose down           # 정지 — 데이터는 남는다
docker compose down -v        # 정지 + 데이터 삭제 — 스키마를 다시 적용할 때
```

### `.env` 에 넣을 값

컨테이너가 뜨면 저장소 루트 `.env` 에 아래를 채운다. **`.env` 는 커밋되지 않는다**(SEC-2).

```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB_NAME=callguard
MYSQL_USER=callguard
MYSQL_PASSWORD=callguard-dev
DATABASE_URL=mysql://callguard:callguard-dev@127.0.0.1:3306/callguard
```

이 값들이 있어야 `server/` 의 전사 저장이 로그 어댑터 대신 **MySQL 리포지토리**로 떨어진다
(`hub/dependencies/transcript_record_provider.py` 가 `mysql_configured` 를 본다).

### 값을 바꾸고 싶으면

`infra/.env` 를 만든다(gitignore 대상). compose 가 그걸 먼저 읽는다.

```
MYSQL_PORT=3307          # 다른 MySQL 이 3306 을 쓰고 있을 때
MYSQL_PASSWORD=...
```

## 스키마를 고쳤을 때

`db/schema.sql` 은 **최초 기동(빈 볼륨)일 때만** 적용된다. 이미 뜬 컨테이너에는 반영되지 않는다.

```bash
docker compose down -v && docker compose up -d
```

로컬 데이터가 날아가므로, 마이그레이션 도구를 도입하기 전까지는 이 방식이다.
스키마 변경은 [팀 승인 사안](/backlog/w1-db-schema/)이다.

## 검증

```bash
docker compose exec mysql mysql -ucallguard -pcallguard-dev callguard -e "SHOW TABLES;"
cd ../server && ../.venv/bin/python -m pytest -m integration
```

## 왜 utf8mb4 인가

한글이 들어간다. 그리고 [7.3절](/docs/07/)이 마스킹 구간(`span`)을 **문자(코드포인트) 오프셋**으로
정했으므로, DB 도 문자 기준으로 다뤄야 프론트·백이 어긋나지 않는다.
