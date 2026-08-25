-- CallGuard MySQL 스키마 — db/generate_schema_docs.py에서 자동 생성.
-- 이 파일을 직접 고치지 말고 generate_schema_docs.py의 TABLES를 고친 뒤 다시 생성할 것.

-- 요금제 — 3NF: plan_name·월정액을 subscriber에 중복 저장하지 않고 여기서 참조
CREATE TABLE plan (
    plan_code VARCHAR(20) NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    monthly_fee INT NOT NULL COMMENT '원',
    data_allowance_gb INT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (plan_code)
);

-- 가입자 — F-2(명의변경 제한 사유)·F-3(반복 문의 연결)가 참조하는 안정적 식별자
CREATE TABLE subscriber (
    subscriber_id VARCHAR(40) NOT NULL COMMENT '해시/난수 — 실명 저장 안 함',
    plan_code VARCHAR(20) NULL,
    joined_at DATETIME NOT NULL,
    arrears_flag BOOLEAN NOT NULL COMMENT '요금 체납 중 — TERM-5.3',
    lost_report_flag BOOLEAN NOT NULL COMMENT '분실·도난 신고 중 — TERM-5.3',
    status VARCHAR(20) NOT NULL,
    PRIMARY KEY (subscriber_id),
    FOREIGN KEY (plan_code) REFERENCES plan(plan_code)
);

-- 상담원 마스터 — 부록B H-4/H-5 리스크(감시 도구화)는 UI·집계 노출 문제이지 call.agent_id 존재 자체의 문제가 아니므로 최소 식별자만 둔다
CREATE TABLE agent (
    agent_id VARCHAR(20) NOT NULL,
    display_name VARCHAR(30) NOT NULL,
    team VARCHAR(30) NULL,
    PRIMARY KEY (agent_id)
);

-- 통화 — D-1·D-2 결과(summary_text·inquiry_type)를 1:1이라 병합(역정규화)
CREATE TABLE call (
    call_id VARCHAR(40) NOT NULL,
    subscriber_id VARCHAR(40) NULL,
    agent_id VARCHAR(20) NULL,
    started_at DATETIME NOT NULL,
    ended_at DATETIME NULL,
    channel_count TINYINT NOT NULL COMMENT 'V1 확인: 전부 1(모노)',
    stt_engine VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL,
    summary_text TEXT NULL COMMENT 'D-1, 통화 후 생성',
    inquiry_type VARCHAR(30) NULL COMMENT 'D-2, 통화 후 생성',
    PRIMARY KEY (call_id),
    FOREIGN KEY (subscriber_id) REFERENCES subscriber(subscriber_id),
    FOREIGN KEY (agent_id) REFERENCES agent(agent_id)
);

-- 전사 세그먼트 — 발화 1건 = 1행 (1NF: 통화 전체를 한 칸에 몰아넣지 않음)
CREATE TABLE transcript_segment (
    segment_id BIGINT NOT NULL,
    call_id VARCHAR(40) NOT NULL,
    speaker ENUM('customer','agent') NOT NULL,
    text TEXT NOT NULL COMMENT '마스킹 완료본만 — 원문 저장 금지 (SEC-1)',
    is_final BOOLEAN NOT NULL,
    utterance_end_ms INT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (segment_id),
    FOREIGN KEY (call_id) REFERENCES call(call_id)
);

-- C-5 마스킹 이벤트 — 세그먼트당 여러 개 가능해 분리 (1NF)
CREATE TABLE masking_event (
    id BIGINT NOT NULL,
    segment_id BIGINT NOT NULL,
    pattern VARCHAR(4) NOT NULL COMMENT 'P1~P7',
    span_start INT NOT NULL,
    span_end INT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (segment_id) REFERENCES transcript_segment(segment_id)
);

-- C-1~C-4 위반 유형 카탈로그 — 팀 교차검증(팀원 ERD)에서 반영: suggestion이 C-4(권장 대체 표현 제시) 요구사항의 실제 저장 위치
CREATE TABLE compliance_rule (
    rule_code VARCHAR(4) NOT NULL COMMENT 'C-1~C-4',
    label VARCHAR(50) NOT NULL,
    default_severity ENUM('high','medium','low') NOT NULL,
    suggestion VARCHAR(200) NULL COMMENT 'MANUAL-1.4 권장 대체 표현',
    PRIMARY KEY (rule_code)
);

-- C-1~C-4 위반 탐지 — D-4(놓친 위반 표현 누적)의 원천 데이터
CREATE TABLE compliance_flag (
    id BIGINT NOT NULL,
    segment_id BIGINT NOT NULL,
    rule_code VARCHAR(4) NOT NULL,
    phrase VARCHAR(200) NOT NULL,
    confidence FLOAT NULL,
    detected_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (segment_id) REFERENCES transcript_segment(segment_id),
    FOREIGN KEY (rule_code) REFERENCES compliance_rule(rule_code)
);

-- 지식베이스 문서 조항 — 실제 본문은 Elasticsearch, 여기는 참조 무결성·관리용 메타데이터. recommendation_card·closure가 참조하므로 그 앞에 정의해야 FK 생성 순서가 맞는다
CREATE TABLE document (
    document_id VARCHAR(30) NOT NULL COMMENT '예: TERM-3.2',
    doc_type ENUM('TERM','MANUAL','POLICY') NOT NULL,
    chapter VARCHAR(20) NULL,
    clause VARCHAR(20) NULL,
    title VARCHAR(100) NOT NULL,
    source_path VARCHAR(200) NOT NULL COMMENT 'knowledge-base/ 내 경로',
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (document_id)
);

-- 추천 트리거 이벤트 — 카드 목록은 recommendation_card로 분리 (1NF)
CREATE TABLE recommendation (
    recommendation_id BIGINT NOT NULL,
    call_id VARCHAR(40) NOT NULL,
    trigger_at_ms INT NOT NULL,
    internal_latency_ms INT NULL,
    e2e_latency_ms INT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (recommendation_id),
    FOREIGN KEY (call_id) REFERENCES call(call_id)
);

-- 추천 카드 — 트리거 1건이 카드 여러 개를 낼 수 있어 분리 (1NF)
CREATE TABLE recommendation_card (
    card_id BIGINT NOT NULL,
    recommendation_id BIGINT NOT NULL,
    source_doc_id VARCHAR(30) NULL COMMENT 'B-6: 근거 없으면 NULL',
    title VARCHAR(100) NOT NULL COMMENT '생성 모델 출력 — document.title과 다를 수 있음',
    summary TEXT NOT NULL,
    similarity_score FLOAT NULL,
    rank TINYINT NOT NULL,
    PRIMARY KEY (card_id),
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(recommendation_id),
    FOREIGN KEY (source_doc_id) REFERENCES document(document_id)
);

-- F-2 종결 판정 — evidence 필드를 역정규화(POLICY 문서 참고)해 하나의 넓은 표로 관리
CREATE TABLE closure (
    closure_id BIGINT NOT NULL COMMENT 'append-only: UPDATE 없이 INSERT만 (F-4)',
    call_id VARCHAR(40) NOT NULL,
    closure_type ENUM('해지','명의변경','보상') NOT NULL,
    reason VARCHAR(100) NULL,
    위약금_안내 BOOLEAN NULL COMMENT '해지 전용 — POLICY-CANCEL-1',
    잔여할부_안내 BOOLEAN NULL COMMENT '해지 전용 — POLICY-CANCEL-1',
    고객확인_기록 BOOLEAN NULL COMMENT '해지 전용 — POLICY-CANCEL-1',
    본인확인_수단 BOOLEAN NULL COMMENT '명의변경 전용 — POLICY-CHANGE-1',
    요청경위_확인 BOOLEAN NULL COMMENT '명의변경 전용 — POLICY-CHANGE-1',
    사유_근거 BOOLEAN NULL COMMENT '보상 전용 — POLICY-REFUND-1',
    승인권한_확인 BOOLEAN NULL COMMENT '보상 전용 — POLICY-REFUND-1',
    verdict ENUM('approved','blocked') NOT NULL,
    source_doc_id VARCHAR(30) NULL,
    decided_at DATETIME NOT NULL,
    PRIMARY KEY (closure_id),
    FOREIGN KEY (call_id) REFERENCES call(call_id),
    FOREIGN KEY (source_doc_id) REFERENCES document(document_id)
);

-- D-3 후속조치 항목 — 통화 1건에 여러 개 가능해 분리 (1NF)
CREATE TABLE follow_up_action (
    id BIGINT NOT NULL,
    call_id VARCHAR(40) NOT NULL,
    action_text VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (call_id) REFERENCES call(call_id)
);

-- D-4 공백 리포트 — B/C/F 세 모듈의 실패 사례를 한 곳에 누적
CREATE TABLE knowledge_gap (
    id BIGINT NOT NULL,
    module ENUM('B','C','F') NOT NULL,
    description VARCHAR(300) NOT NULL,
    call_id VARCHAR(40) NULL,
    segment_id BIGINT NULL,
    closure_id BIGINT NULL,
    created_at DATETIME NOT NULL,
    status ENUM('open','resolved') NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (call_id) REFERENCES call(call_id),
    FOREIGN KEY (segment_id) REFERENCES transcript_segment(segment_id),
    FOREIGN KEY (closure_id) REFERENCES closure(closure_id)
);

-- 평가 실행 배치 — 6.2절 '여러 번 실행한 값 중 최저치 고정'을 위해 실행 단위로 분리
CREATE TABLE eval_run (
    run_id BIGINT NOT NULL,
    golden_set_version VARCHAR(10) NOT NULL,
    git_commit VARCHAR(40) NULL,
    error_rate FLOAT NOT NULL COMMENT '4.2절 STT 오류 주입률 0.00~0.20, 팀 교차검증 반영',
    executed_at DATETIME NOT NULL,
    executed_by VARCHAR(30) NULL,
    PRIMARY KEY (run_id)
);

-- 평가 결과 상세 — 실행 1건이 지표 여러 개를 내므로 분리 (1NF)
CREATE TABLE eval_result (
    id BIGINT NOT NULL,
    run_id BIGINT NOT NULL,
    module VARCHAR(10) NOT NULL COMMENT 'B/C/C-5/F-2 등',
    metric_name VARCHAR(40) NOT NULL,
    metric_value FLOAT NOT NULL,
    passed_absolute_rule BOOLEAN NULL COMMENT 'C-5·F-2만 해당, 그 외 NULL',
    PRIMARY KEY (id),
    FOREIGN KEY (run_id) REFERENCES eval_run(run_id)
);

-- G-2 지역 자원 연계 — 조건부(여유 시) 모듈, 스키마만 선반영
CREATE TABLE resource_center (
    center_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category ENUM('정신건강복지센터','자살예방센터') NOT NULL,
    address VARCHAR(200) NOT NULL,
    region VARCHAR(30) NOT NULL,
    phone VARCHAR(20) NULL,
    operating_hours VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL COMMENT '폐지·이전 기관 반환 0건 검증용',
    PRIMARY KEY (center_id)
);
