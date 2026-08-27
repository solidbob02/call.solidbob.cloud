-- CallGuard PostgreSQL 스키마 — db/generate_schema_docs.py에서 자동 생성.
-- 이 파일을 직접 고치지 말고 generate_schema_docs.py의 TABLES를 고친 뒤 다시 생성할 것.

-- 고객 — F-3(반복 문의 연결)이 참조하는 안정적 식별자. 2026-08-26 도메인 4종 확정 이전엔 통신 전용 `subscriber`(+`plan`/체납·분실신고 플래그)였으나, 그 필드들은 폐기된 명의변경 처리유형(TERM-5.3, 지금은 존재하지 않는 문서 ID)에만 쓰였고 4개 도메인(금융보험·다산콜센터·쇼핑·질병관리본부) 중 어디에도 대응하는 개념이 없어 제거했다 (`_project/decisions/006-db-스키마-도메인-정리.md`)
CREATE TABLE "customer" (
    "customer_id" VARCHAR(40) NOT NULL,
    "first_seen_at" TIMESTAMPTZ NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    PRIMARY KEY ("customer_id")
);
COMMENT ON COLUMN "customer"."customer_id" IS '해시/난수 — 실명 저장 안 함, 도메인 공통';

-- 상담원 마스터 — 부록B H-4/H-5 리스크(감시 도구화)는 UI·집계 노출 문제이지 call.agent_id 존재 자체의 문제가 아니므로 최소 식별자만 둔다
CREATE TABLE "agent" (
    "agent_id" VARCHAR(20) NOT NULL,
    "display_name" VARCHAR(30) NOT NULL,
    "team" VARCHAR(30) NULL,
    PRIMARY KEY ("agent_id")
);

-- 통화 — D-1·D-2 결과(summary_text·inquiry_type)를 1:1이라 병합(역정규화)
CREATE TABLE "call" (
    "call_id" VARCHAR(40) NOT NULL,
    "domain" VARCHAR(30) NOT NULL,
    "customer_id" VARCHAR(40) NULL,
    "agent_id" VARCHAR(20) NULL,
    "started_at" TIMESTAMPTZ NOT NULL,
    "ended_at" TIMESTAMPTZ NULL,
    "channel_count" SMALLINT NOT NULL,
    "stt_engine" VARCHAR(30) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "summary_text" TEXT NULL,
    "inquiry_type" VARCHAR(30) NULL,
    PRIMARY KEY ("call_id"),
    CHECK ("domain" IN ('finance','dasan','shopping','health')),
    FOREIGN KEY ("customer_id") REFERENCES "customer"("customer_id"),
    FOREIGN KEY ("agent_id") REFERENCES "agent"("agent_id")
);
COMMENT ON COLUMN "call"."domain" IS '4개 데모 도메인 — 검색·F-2 라우팅 기준([1.4절](/docs/01/))';
COMMENT ON COLUMN "call"."channel_count" IS 'V1 확인: 전부 1(모노)';
COMMENT ON COLUMN "call"."summary_text" IS 'D-1, 통화 후 생성';
COMMENT ON COLUMN "call"."inquiry_type" IS 'D-2, 통화 후 생성';

-- 전사 세그먼트 — 발화 1건 = 1행 (1NF: 통화 전체를 한 칸에 몰아넣지 않음)
CREATE TABLE "transcript_segment" (
    "segment_id" BIGINT NOT NULL,
    "call_id" VARCHAR(40) NOT NULL,
    "speaker" VARCHAR(30) NOT NULL,
    "text" TEXT NOT NULL,
    "is_final" BOOLEAN NOT NULL,
    "utterance_end_ms" INT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("segment_id"),
    CHECK ("speaker" IN ('customer','agent')),
    FOREIGN KEY ("call_id") REFERENCES "call"("call_id")
);
COMMENT ON COLUMN "transcript_segment"."text" IS '마스킹 완료본만 — 원문 저장 금지 (SEC-1)';

-- C-5 마스킹 이벤트 — 세그먼트당 여러 개 가능해 분리 (1NF)
CREATE TABLE "masking_event" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "segment_id" BIGINT NOT NULL,
    "pattern" VARCHAR(4) NOT NULL,
    "span_start" INT NOT NULL,
    "span_end" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("segment_id") REFERENCES "transcript_segment"("segment_id")
);
COMMENT ON COLUMN "masking_event"."pattern" IS 'P1~P7';

-- C-1~C-4 위반 유형 카탈로그 — 팀 교차검증(팀원 ERD)에서 반영: suggestion이 C-4(권장 대체 표현 제시) 요구사항의 실제 저장 위치
CREATE TABLE "compliance_rule" (
    "rule_code" VARCHAR(4) NOT NULL,
    "label" VARCHAR(50) NOT NULL,
    "default_severity" VARCHAR(30) NOT NULL,
    "suggestion" VARCHAR(200) NULL,
    PRIMARY KEY ("rule_code"),
    CHECK ("default_severity" IN ('high','medium','low'))
);
COMMENT ON COLUMN "compliance_rule"."rule_code" IS 'C-1~C-4';
COMMENT ON COLUMN "compliance_rule"."suggestion" IS '도메인별 MANUAL 문서의 1.4절(권장 대체 표현), 예: FIN-MANUAL-1.4';

-- C-1~C-4 위반 탐지 — D-4(놓친 위반 표현 누적)의 원천 데이터
CREATE TABLE "compliance_flag" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "segment_id" BIGINT NOT NULL,
    "rule_code" VARCHAR(4) NOT NULL,
    "phrase" VARCHAR(200) NOT NULL,
    "confidence" REAL NULL,
    "detected_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("segment_id") REFERENCES "transcript_segment"("segment_id"),
    FOREIGN KEY ("rule_code") REFERENCES "compliance_rule"("rule_code")
);

-- 지식베이스 문서 조항 — 실제 본문은 Elasticsearch, 여기는 참조 무결성·관리용 메타데이터. recommendation_card·closure가 참조하므로 그 앞에 정의해야 FK 생성 순서가 맞는다
CREATE TABLE "document" (
    "document_id" VARCHAR(30) NOT NULL,
    "doc_type" VARCHAR(30) NOT NULL,
    "chapter" VARCHAR(20) NULL,
    "clause" VARCHAR(20) NULL,
    "title" VARCHAR(100) NOT NULL,
    "source_path" VARCHAR(200) NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("document_id"),
    CHECK ("doc_type" IN ('TERM','MANUAL','POLICY'))
);
COMMENT ON COLUMN "document"."document_id" IS '도메인 접두어 포함, 예: FIN-TERM-3.2';
COMMENT ON COLUMN "document"."source_path" IS 'knowledge-base/ 내 경로';

-- 추천 트리거 이벤트 — 카드 목록은 recommendation_card로 분리 (1NF)
CREATE TABLE "recommendation" (
    "recommendation_id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "call_id" VARCHAR(40) NOT NULL,
    "trigger_at_ms" INT NOT NULL,
    "internal_latency_ms" INT NULL,
    "e2e_latency_ms" INT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("recommendation_id"),
    FOREIGN KEY ("call_id") REFERENCES "call"("call_id")
);

-- 추천 카드 — 트리거 1건이 카드 여러 개를 낼 수 있어 분리 (1NF)
CREATE TABLE "recommendation_card" (
    "card_id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "recommendation_id" BIGINT NOT NULL,
    "source_doc_id" VARCHAR(30) NULL,
    "title" VARCHAR(100) NOT NULL,
    "summary" TEXT NOT NULL,
    "similarity_score" REAL NULL,
    "rank" SMALLINT NOT NULL,
    PRIMARY KEY ("card_id"),
    FOREIGN KEY ("recommendation_id") REFERENCES "recommendation"("recommendation_id"),
    FOREIGN KEY ("source_doc_id") REFERENCES "document"("document_id")
);
COMMENT ON COLUMN "recommendation_card"."source_doc_id" IS 'B-6: 근거 없으면 NULL';
COMMENT ON COLUMN "recommendation_card"."title" IS '생성 모델 출력 — document.title과 다를 수 있음';

-- 카드 채택·무시 기록 (E-1) — 상담원이 추천을 실제로 썼는지. recommendation_card에 컬럼을 더하지 않고 분리한 이유: 피드백은 카드 내용과 다른 사실이고 자체 시각을 갖는다. 카드 하나에 이벤트가 여러 번 붙을 수 있어(채택→취소) 이력이 남아야 한다 — masking_event·compliance_flag와 같은 이벤트 테이블 패턴. ⚠ 상담원 단위로 집계해 점수·순위를 만들지 않는다(부록 A-1) — 카드 품질을 재는 데이터다
CREATE TABLE "card_feedback" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "card_id" BIGINT NOT NULL,
    "action" VARCHAR(30) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("id"),
    CHECK ("action" IN ('adopted','ignored')),
    FOREIGN KEY ("card_id") REFERENCES "recommendation_card"("card_id")
);

-- F-2 종결 판정 — evidence 필드를 역정규화(POLICY 문서 참고)해 하나의 넓은 표로 관리. F-2는 종결형 처리가 있는 금융보험·쇼핑에만 적용된다([1.4절](/docs/01/)) — 다산콜센터·질병관리본부는 안내형 업무라 이 테이블에 행이 생기지 않는다
CREATE TABLE "closure" (
    "closure_id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "call_id" VARCHAR(40) NOT NULL,
    "closure_type" VARCHAR(30) NOT NULL,
    "reason" VARCHAR(100) NULL,
    "중도해지수수료_안내" BOOLEAN NULL,
    "약정혜택소멸_안내" BOOLEAN NULL,
    "고객확인_기록" BOOLEAN NULL,
    "사고경위_확인" BOOLEAN NULL,
    "귀책여부_확인" BOOLEAN NULL,
    "환불금액_안내" BOOLEAN NULL,
    "환불기간_안내" BOOLEAN NULL,
    "상품상태_확인" BOOLEAN NULL,
    "교환가능_확인" BOOLEAN NULL,
    "재고_확인" BOOLEAN NULL,
    "verdict" VARCHAR(30) NOT NULL,
    "source_doc_id" VARCHAR(30) NULL,
    "decided_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("closure_id"),
    CHECK ("closure_type" IN ('상품해지','보상','반품','교환')),
    CHECK ("verdict" IN ('approved','blocked')),
    FOREIGN KEY ("call_id") REFERENCES "call"("call_id"),
    FOREIGN KEY ("source_doc_id") REFERENCES "document"("document_id")
);
COMMENT ON COLUMN "closure"."closure_id" IS 'append-only: UPDATE 없이 INSERT만 (F-4)';
COMMENT ON COLUMN "closure"."closure_type" IS '상품해지·보상=금융보험, 반품·교환=쇼핑';
COMMENT ON COLUMN "closure"."중도해지수수료_안내" IS '상품해지 전용(금융보험) — FIN-POLICY-CLOSE-1';
COMMENT ON COLUMN "closure"."약정혜택소멸_안내" IS '상품해지 전용(금융보험) — FIN-POLICY-CLOSE-1';
COMMENT ON COLUMN "closure"."고객확인_기록" IS '상품해지 전용(금융보험) — FIN-POLICY-CLOSE-1';
COMMENT ON COLUMN "closure"."사고경위_확인" IS '보상 전용(금융보험) — FIN-POLICY-COMPENSATE-1';
COMMENT ON COLUMN "closure"."귀책여부_확인" IS '보상 전용(금융보험) — FIN-POLICY-COMPENSATE-1';
COMMENT ON COLUMN "closure"."환불금액_안내" IS '반품 전용(쇼핑) — SHOP-POLICY-RETURN-1';
COMMENT ON COLUMN "closure"."환불기간_안내" IS '반품 전용(쇼핑) — SHOP-POLICY-RETURN-1';
COMMENT ON COLUMN "closure"."상품상태_확인" IS '반품 전용(쇼핑) — SHOP-POLICY-RETURN-1';
COMMENT ON COLUMN "closure"."교환가능_확인" IS '교환 전용(쇼핑) — SHOP-POLICY-EXCHANGE-1';
COMMENT ON COLUMN "closure"."재고_확인" IS '교환 전용(쇼핑) — SHOP-POLICY-EXCHANGE-1';

-- D-3 후속조치 항목 — 통화 1건에 여러 개 가능해 분리 (1NF)
CREATE TABLE "follow_up_action" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "call_id" VARCHAR(40) NOT NULL,
    "action_text" VARCHAR(200) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("call_id") REFERENCES "call"("call_id")
);

-- D-4 공백 리포트 — B/C/F 세 모듈의 실패 사례를 한 곳에 누적
CREATE TABLE "knowledge_gap" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "module" VARCHAR(30) NOT NULL,
    "description" VARCHAR(300) NOT NULL,
    "call_id" VARCHAR(40) NULL,
    "segment_id" BIGINT NULL,
    "closure_id" BIGINT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "status" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("id"),
    CHECK ("module" IN ('B','C','F')),
    CHECK ("status" IN ('open','resolved')),
    FOREIGN KEY ("call_id") REFERENCES "call"("call_id"),
    FOREIGN KEY ("segment_id") REFERENCES "transcript_segment"("segment_id"),
    FOREIGN KEY ("closure_id") REFERENCES "closure"("closure_id")
);

-- 평가 실행 배치 — 6.2절 '여러 번 실행한 값 중 최저치 고정'을 위해 실행 단위로 분리
CREATE TABLE "eval_run" (
    "run_id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "golden_set_version" VARCHAR(10) NOT NULL,
    "git_commit" VARCHAR(40) NULL,
    "error_rate" REAL NOT NULL,
    "executed_at" TIMESTAMPTZ NOT NULL,
    "executed_by" VARCHAR(30) NULL,
    PRIMARY KEY ("run_id")
);
COMMENT ON COLUMN "eval_run"."error_rate" IS '4.2절 STT 오류 주입률 0.00~0.20, 팀 교차검증 반영';

-- 평가 결과 상세 — 실행 1건이 지표 여러 개를 내므로 분리 (1NF)
CREATE TABLE "eval_result" (
    "id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "run_id" BIGINT NOT NULL,
    "module" VARCHAR(10) NOT NULL,
    "metric_name" VARCHAR(40) NOT NULL,
    "metric_value" REAL NOT NULL,
    "passed_absolute_rule" BOOLEAN NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("run_id") REFERENCES "eval_run"("run_id")
);
COMMENT ON COLUMN "eval_result"."module" IS 'B/C/C-5/F-2 등';
COMMENT ON COLUMN "eval_result"."passed_absolute_rule" IS 'C-5·F-2만 해당, 그 외 NULL';

-- G-2 지역 자원 연계 — 조건부(여유 시) 모듈, 스키마만 선반영
CREATE TABLE "resource_center" (
    "center_id" BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "category" VARCHAR(30) NOT NULL,
    "address" VARCHAR(200) NOT NULL,
    "region" VARCHAR(30) NOT NULL,
    "phone" VARCHAR(20) NULL,
    "operating_hours" VARCHAR(50) NULL,
    "is_active" BOOLEAN NOT NULL,
    PRIMARY KEY ("center_id"),
    CHECK ("category" IN ('정신건강복지센터','자살예방센터'))
);
COMMENT ON COLUMN "resource_center"."is_active" IS '폐지·이전 기관 반환 0건 검증용';
