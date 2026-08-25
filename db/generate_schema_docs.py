# Requirement: 아키텍처(MySQL 스키마), ERD 문서화
"""CallGuard MySQL 스키마를 한 군데(TABLES)에 정의하고, 여기서
schema.sql(DDL)과 docs/erd.dot(ERD 소스)을 같이 생성한다. 스키마를 고칠 땐 이
파일만 고치고 다시 실행하면 SQL과 ERD가 항상 같은 정의를 가리키게 된다.

실행:
    .venv/bin/python db/generate_schema_docs.py

(graphviz의 `dot`이 설치돼 있으면 ERD.png까지 자동으로 렌더링하고, 지킬이 보여줄 수
있게 jekyll/assets/erd/ERD.png로도 복사한다. `brew install graphviz`로 설치.)
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
DOCS_DIR = DB_DIR / "docs"
JEKYLL_ERD_ASSET = DB_DIR.parent / "jekyll" / "assets" / "erd" / "ERD.png"


@dataclass
class Column:
    name: str
    sql_type: str
    key: str = ""  # "PK" | "FK" | ""
    fk_ref: str | None = None  # "table.column"
    nullable: bool = True
    note: str = ""
    # 식별 관계(True) — 자식이 부모 없이는 존재 의미가 없는 약한 개체(transcript_segment,
    # masking_event 등). 비식별 관계(False, 기본값) — 부모는 참조/분류 대상일 뿐 자식은
    # 독립적 정체성을 가짐(subscriber→plan, recommendation_card→document 등).
    # 모든 테이블이 서로게이트 PK를 쓰므로 물리적으로 부모 PK가 자식 PK에 포함되는
    # "진짜" 식별 관계는 없다 — 여기서는 개념적 강한 종속(약한 개체) 여부를 표시한다.
    identifying: bool = False


@dataclass
class Table:
    name: str
    comment: str
    columns: list[Column] = field(default_factory=list)
    cluster: str = ""


TABLES: list[Table] = [
    Table(
        "plan", "요금제 — 3NF: plan_name·월정액을 subscriber에 중복 저장하지 않고 여기서 참조",
        cluster="가입자",
        columns=[
            Column("plan_code", "VARCHAR(20)", "PK", nullable=False),
            Column("plan_name", "VARCHAR(50)", nullable=False),
            Column("monthly_fee", "INT", nullable=False, note="원"),
            Column("data_allowance_gb", "INT"),
            Column("created_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "subscriber", "가입자 — F-2(명의변경 제한 사유)·F-3(반복 문의 연결)가 참조하는 안정적 식별자",
        cluster="가입자",
        columns=[
            Column("subscriber_id", "VARCHAR(40)", "PK", nullable=False, note="해시/난수 — 실명 저장 안 함"),
            Column("plan_code", "VARCHAR(20)", "FK", "plan.plan_code"),
            Column("joined_at", "DATETIME", nullable=False),
            Column("arrears_flag", "BOOLEAN", nullable=False, note="요금 체납 중 — TERM-5.3"),
            Column("lost_report_flag", "BOOLEAN", nullable=False, note="분실·도난 신고 중 — TERM-5.3"),
            Column("status", "VARCHAR(20)", nullable=False),
        ],
    ),
    Table(
        "agent", "상담원 마스터 — 부록B H-4/H-5 리스크(감시 도구화)는 UI·집계 노출 문제이지 "
        "call.agent_id 존재 자체의 문제가 아니므로 최소 식별자만 둔다",
        cluster="가입자",
        columns=[
            Column("agent_id", "VARCHAR(20)", "PK", nullable=False),
            Column("display_name", "VARCHAR(30)", nullable=False),
            Column("team", "VARCHAR(30)"),
        ],
    ),
    Table(
        "call", "통화 — D-1·D-2 결과(summary_text·inquiry_type)를 1:1이라 병합(역정규화)",
        cluster="통화",
        columns=[
            Column("call_id", "VARCHAR(40)", "PK", nullable=False),
            Column("subscriber_id", "VARCHAR(40)", "FK", "subscriber.subscriber_id"),
            Column("agent_id", "VARCHAR(20)", "FK", "agent.agent_id"),
            Column("started_at", "DATETIME", nullable=False),
            Column("ended_at", "DATETIME"),
            Column("channel_count", "TINYINT", nullable=False, note="V1 확인: 전부 1(모노)"),
            Column("stt_engine", "VARCHAR(30)", nullable=False),
            Column("status", "VARCHAR(20)", nullable=False),
            Column("summary_text", "TEXT", note="D-1, 통화 후 생성"),
            Column("inquiry_type", "VARCHAR(30)", note="D-2, 통화 후 생성"),
        ],
    ),
    Table(
        "transcript_segment", "전사 세그먼트 — 발화 1건 = 1행 (1NF: 통화 전체를 한 칸에 몰아넣지 않음)",
        cluster="통화",
        columns=[
            Column("segment_id", "BIGINT", "PK", nullable=False),
            Column("call_id", "VARCHAR(40)", "FK", "call.call_id", nullable=False, identifying=True),
            Column("speaker", "ENUM('customer','agent')", nullable=False),
            Column("text", "TEXT", nullable=False, note="마스킹 완료본만 — 원문 저장 금지 (SEC-1)"),
            Column("is_final", "BOOLEAN", nullable=False),
            Column("utterance_end_ms", "INT"),
            Column("created_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "masking_event", "C-5 마스킹 이벤트 — 세그먼트당 여러 개 가능해 분리 (1NF)",
        cluster="통화",
        columns=[
            Column("id", "BIGINT", "PK", nullable=False),
            Column("segment_id", "BIGINT", "FK", "transcript_segment.segment_id", nullable=False, identifying=True),
            Column("pattern", "VARCHAR(4)", nullable=False, note="P1~P7"),
            Column("span_start", "INT", nullable=False),
            Column("span_end", "INT", nullable=False),
            Column("created_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "compliance_rule", "C-1~C-4 위반 유형 카탈로그 — 팀 교차검증(팀원 ERD)에서 반영: "
        "suggestion이 C-4(권장 대체 표현 제시) 요구사항의 실제 저장 위치",
        cluster="통화",
        columns=[
            Column("rule_code", "VARCHAR(4)", "PK", nullable=False, note="C-1~C-4"),
            Column("label", "VARCHAR(50)", nullable=False),
            Column("default_severity", "ENUM('high','medium','low')", nullable=False),
            Column("suggestion", "VARCHAR(200)", note="MANUAL-1.4 권장 대체 표현"),
        ],
    ),
    Table(
        "compliance_flag", "C-1~C-4 위반 탐지 — D-4(놓친 위반 표현 누적)의 원천 데이터",
        cluster="통화",
        columns=[
            Column("id", "BIGINT", "PK", nullable=False),
            Column("segment_id", "BIGINT", "FK", "transcript_segment.segment_id", nullable=False, identifying=True),
            Column("rule_code", "VARCHAR(4)", "FK", "compliance_rule.rule_code", nullable=False),
            Column("phrase", "VARCHAR(200)", nullable=False),
            Column("confidence", "FLOAT"),
            Column("detected_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "document", "지식베이스 문서 조항 — 실제 본문은 Elasticsearch, 여기는 참조 무결성·관리용 메타데이터. "
        "recommendation_card·closure가 참조하므로 그 앞에 정의해야 FK 생성 순서가 맞는다",
        cluster="문서",
        columns=[
            Column("document_id", "VARCHAR(30)", "PK", nullable=False, note="예: TERM-3.2"),
            Column("doc_type", "ENUM('TERM','MANUAL','POLICY')", nullable=False),
            Column("chapter", "VARCHAR(20)"),
            Column("clause", "VARCHAR(20)"),
            Column("title", "VARCHAR(100)", nullable=False),
            Column("source_path", "VARCHAR(200)", nullable=False, note="knowledge-base/ 내 경로"),
            Column("updated_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "recommendation", "추천 트리거 이벤트 — 카드 목록은 recommendation_card로 분리 (1NF)",
        cluster="추천",
        columns=[
            Column("recommendation_id", "BIGINT", "PK", nullable=False),
            Column("call_id", "VARCHAR(40)", "FK", "call.call_id", nullable=False, identifying=True),
            Column("trigger_at_ms", "INT", nullable=False),
            Column("internal_latency_ms", "INT"),
            Column("e2e_latency_ms", "INT"),
            Column("created_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "recommendation_card", "추천 카드 — 트리거 1건이 카드 여러 개를 낼 수 있어 분리 (1NF)",
        cluster="추천",
        columns=[
            Column("card_id", "BIGINT", "PK", nullable=False),
            Column("recommendation_id", "BIGINT", "FK", "recommendation.recommendation_id", nullable=False, identifying=True),
            Column("source_doc_id", "VARCHAR(30)", "FK", "document.document_id", note="B-6: 근거 없으면 NULL"),
            Column("title", "VARCHAR(100)", nullable=False, note="생성 모델 출력 — document.title과 다를 수 있음"),
            Column("summary", "TEXT", nullable=False),
            Column("similarity_score", "FLOAT"),
            Column("rank", "TINYINT", nullable=False),
        ],
    ),
    Table(
        "closure", "F-2 종결 판정 — evidence 필드를 역정규화(POLICY 문서 참고)해 하나의 넓은 표로 관리",
        cluster="종결",
        columns=[
            Column("closure_id", "BIGINT", "PK", nullable=False, note="append-only: UPDATE 없이 INSERT만 (F-4)"),
            Column("call_id", "VARCHAR(40)", "FK", "call.call_id", nullable=False, identifying=True),
            Column("closure_type", "ENUM('해지','명의변경','보상')", nullable=False),
            Column("reason", "VARCHAR(100)"),
            Column("위약금_안내", "BOOLEAN", note="해지 전용 — POLICY-CANCEL-1"),
            Column("잔여할부_안내", "BOOLEAN", note="해지 전용 — POLICY-CANCEL-1"),
            Column("고객확인_기록", "BOOLEAN", note="해지 전용 — POLICY-CANCEL-1"),
            Column("본인확인_수단", "BOOLEAN", note="명의변경 전용 — POLICY-CHANGE-1"),
            Column("요청경위_확인", "BOOLEAN", note="명의변경 전용 — POLICY-CHANGE-1"),
            Column("사유_근거", "BOOLEAN", note="보상 전용 — POLICY-REFUND-1"),
            Column("승인권한_확인", "BOOLEAN", note="보상 전용 — POLICY-REFUND-1"),
            Column("verdict", "ENUM('approved','blocked')", nullable=False),
            Column("source_doc_id", "VARCHAR(30)", "FK", "document.document_id"),
            Column("decided_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "follow_up_action", "D-3 후속조치 항목 — 통화 1건에 여러 개 가능해 분리 (1NF)",
        cluster="후속처리",
        columns=[
            Column("id", "BIGINT", "PK", nullable=False),
            Column("call_id", "VARCHAR(40)", "FK", "call.call_id", nullable=False, identifying=True),
            Column("action_text", "VARCHAR(200)", nullable=False),
            Column("status", "VARCHAR(20)", nullable=False),
            Column("created_at", "DATETIME", nullable=False),
        ],
    ),
    Table(
        "knowledge_gap", "D-4 공백 리포트 — B/C/F 세 모듈의 실패 사례를 한 곳에 누적",
        cluster="후속처리",
        columns=[
            Column("id", "BIGINT", "PK", nullable=False),
            Column("module", "ENUM('B','C','F')", nullable=False),
            Column("description", "VARCHAR(300)", nullable=False),
            Column("call_id", "VARCHAR(40)", "FK", "call.call_id"),
            Column("segment_id", "BIGINT", "FK", "transcript_segment.segment_id"),
            Column("closure_id", "BIGINT", "FK", "closure.closure_id"),
            Column("created_at", "DATETIME", nullable=False),
            Column("status", "ENUM('open','resolved')", nullable=False),
        ],
    ),
    Table(
        "eval_run", "평가 실행 배치 — 6.2절 '여러 번 실행한 값 중 최저치 고정'을 위해 실행 단위로 분리",
        cluster="평가",
        columns=[
            Column("run_id", "BIGINT", "PK", nullable=False),
            Column("golden_set_version", "VARCHAR(10)", nullable=False),
            Column("git_commit", "VARCHAR(40)"),
            Column("error_rate", "FLOAT", nullable=False, note="4.2절 STT 오류 주입률 0.00~0.20, 팀 교차검증 반영"),
            Column("executed_at", "DATETIME", nullable=False),
            Column("executed_by", "VARCHAR(30)"),
        ],
    ),
    Table(
        "eval_result", "평가 결과 상세 — 실행 1건이 지표 여러 개를 내므로 분리 (1NF)",
        cluster="평가",
        columns=[
            Column("id", "BIGINT", "PK", nullable=False),
            Column("run_id", "BIGINT", "FK", "eval_run.run_id", nullable=False, identifying=True),
            Column("module", "VARCHAR(10)", nullable=False, note="B/C/C-5/F-2 등"),
            Column("metric_name", "VARCHAR(40)", nullable=False),
            Column("metric_value", "FLOAT", nullable=False),
            Column("passed_absolute_rule", "BOOLEAN", note="C-5·F-2만 해당, 그 외 NULL"),
        ],
    ),
    Table(
        "resource_center", "G-2 지역 자원 연계 — 조건부(여유 시) 모듈, 스키마만 선반영",
        cluster="G-2(조건부)",
        columns=[
            Column("center_id", "BIGINT", "PK", nullable=False),
            Column("name", "VARCHAR(100)", nullable=False),
            Column("category", "ENUM('정신건강복지센터','자살예방센터')", nullable=False),
            Column("address", "VARCHAR(200)", nullable=False),
            Column("region", "VARCHAR(30)", nullable=False),
            Column("phone", "VARCHAR(20)"),
            Column("operating_hours", "VARCHAR(50)"),
            Column("is_active", "BOOLEAN", nullable=False, note="폐지·이전 기관 반환 0건 검증용"),
        ],
    ),
]


def to_sql(tables: list[Table]) -> str:
    lines = [
        "-- CallGuard MySQL 스키마 — db/generate_schema_docs.py에서 자동 생성.",
        "-- 이 파일을 직접 고치지 말고 generate_schema_docs.py의 TABLES를 고친 뒤 다시 생성할 것.",
        "",
    ]
    for t in tables:
        lines.append(f"-- {t.comment}")
        lines.append(f"CREATE TABLE {t.name} (")
        col_lines = []
        fk_lines = []
        pk_col = None
        for c in t.columns:
            null_sql = "NOT NULL" if not c.nullable else "NULL"
            comment_sql = f" COMMENT '{c.note}'" if c.note else ""
            col_lines.append(f"    {c.name} {c.sql_type} {null_sql}{comment_sql}")
            if c.key == "PK":
                pk_col = c.name
            if c.key == "FK" and c.fk_ref:
                ref_table, ref_col = c.fk_ref.split(".")
                fk_lines.append(
                    f"    FOREIGN KEY ({c.name}) REFERENCES {ref_table}({ref_col})"
                )
        if pk_col:
            col_lines.append(f"    PRIMARY KEY ({pk_col})")
        col_lines.extend(fk_lines)
        lines.append(",\n".join(col_lines))
        lines.append(");")
        lines.append("")
    return "\n".join(lines)


def to_dot(tables: list[Table]) -> str:
    clusters: dict[str, list[Table]] = {}
    for t in tables:
        clusters.setdefault(t.cluster, []).append(t)

    lines = [
        "digraph CallGuardERD {",
        '  rankdir=LR;',
        '  graph [fontname="Helvetica", nodesep=0.7, ranksep=1.3, splines=polyline];',
        '  node [fontname="Helvetica", shape=plain];',
        '  edge [fontname="Helvetica", fontsize=11, arrowtail=tee, arrowhead=crow, dir=both, color="#555555"];',
        "",
    ]

    for cluster_name, cluster_tables in clusters.items():
        lines.append(f'  subgraph "cluster_{cluster_name}" {{')
        lines.append(f'    label="{cluster_name}"; style=rounded; color="#cccccc"; fontname="Helvetica"; fontsize=13;')
        for t in cluster_tables:
            rows = [
                f'<TR><TD BGCOLOR="#2f6fed" COLSPAN="3"><FONT COLOR="white"><B>{t.name}</B></FONT></TD></TR>'
            ]
            for c in t.columns:
                key_label = ""
                if c.key == "PK":
                    key_label = "<B><U>PK</U></B>"
                elif c.key == "FK":
                    key_label = "<I>FK</I>"
                name_html = f"<B>{c.name}</B>" if c.key == "PK" else c.name
                rows.append(
                    f'<TR><TD ALIGN="LEFT">{key_label}</TD>'
                    f'<TD ALIGN="LEFT">{name_html}</TD>'
                    f'<TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#666666">{c.sql_type}</FONT></TD></TR>'
                )
            label = (
                '<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
                + "".join(rows)
                + "</TABLE>>"
            )
            lines.append(f'    "{t.name}" [label={label}];')
        lines.append("  }")
        lines.append("")

    for t in tables:
        for c in t.columns:
            if c.key == "FK" and c.fk_ref:
                ref_table = c.fk_ref.split(".")[0]
                # 실선 = 식별 관계(자식이 부모 없이는 존재 의미가 없는 약한 개체)
                # 점선 = 비식별 관계(부모는 참조·분류 대상일 뿐, 자식은 독립적 정체성을 가짐)
                style = "solid" if c.identifying else "dashed"
                kind_label = "식별" if c.identifying else "비식별"
                lines.append(
                    f'  "{ref_table}" -> "{t.name}" '
                    f'[label="  1:N ({c.name}, {kind_label})", style={style}];'
                )

    # 범례 — 실선/점선 구분을 다이어그램 안에서 바로 확인할 수 있게 정적 라벨 노드로 둔다
    # (레이아웃 엔진이 계산할 필요 없는 고정 텍스트라 크래시 위험이 없다).
    legend_rows = [
        '<TR><TD COLSPAN="2" BGCOLOR="#2f6fed"><FONT COLOR="white"><B>범례</B></FONT></TD></TR>',
        '<TR><TD ALIGN="LEFT">━━━━━━</TD>'
        '<TD ALIGN="LEFT">식별 관계 — 자식이 부모 없이는 존재 의미가 없는 약한 개체<BR/>'
        '(transcript_segment, masking_event, recommendation_card 등)</TD></TR>',
        '<TR><TD ALIGN="LEFT">┄┄┄┄┄┄</TD>'
        '<TD ALIGN="LEFT">비식별 관계 — 참조·분류 대상. 자식이 독립적 정체성을 가짐<BR/>'
        '(subscriber→plan, recommendation_card→document 등)</TD></TR>',
        '<TR><TD ALIGN="LEFT">──▷</TD><TD ALIGN="LEFT">까마귀발 = N쪽(자식 여러 행)</TD></TR>',
        '<TR><TD ALIGN="LEFT">──┤</TD><TD ALIGN="LEFT">막대 = 1쪽(부모 1행)</TD></TR>',
    ]
    legend_label = (
        '<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5">'
        + "".join(legend_rows)
        + "</TABLE>>"
    )
    lines.append(f'  "legend" [label={legend_label}, shape=plain];')

    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DB_DIR / "schema.sql").write_text(to_sql(TABLES), encoding="utf-8")
    (DOCS_DIR / "erd.dot").write_text(to_dot(TABLES), encoding="utf-8")
    print(f"생성 완료: {DB_DIR / 'schema.sql'}")
    print(f"생성 완료: {DOCS_DIR / 'erd.dot'}")
    print(f"테이블 수: {len(TABLES)}")

    if shutil.which("dot") is None:
        print("graphviz(dot)가 없어 ERD.png는 못 만들었다 — `brew install graphviz` 후 다시 실행할 것.")
        return

    erd_png = DOCS_DIR / "ERD.png"
    subprocess.run(["dot", "-Tpng", str(DOCS_DIR / "erd.dot"), "-o", str(erd_png)], check=True)
    print(f"생성 완료: {erd_png}")

    JEKYLL_ERD_ASSET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(erd_png, JEKYLL_ERD_ASSET)
    print(f"복사 완료: {JEKYLL_ERD_ASSET} (지킬 docs/16 페이지가 여기서 읽는다)")


if __name__ == "__main__":
    main()
