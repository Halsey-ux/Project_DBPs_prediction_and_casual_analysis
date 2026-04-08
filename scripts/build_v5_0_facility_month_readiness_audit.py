from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = (
    PROJECT_ROOT
    / "data_local"
    / "V3_Chapter1_Part1_Prototype_Build"
    / "V3_facility_month_master.csv"
)
OUTPUT_DIR = (
    PROJECT_ROOT
    / "data_local"
    / "V5_Chapter1_Part1_Facility_Month_Module"
    / "V5_0"
)
SNAPSHOT_PATH = OUTPUT_DIR / "V5_0_Facility_Month_Readiness_Audit_Snapshot.md"
TZ = ZoneInfo("Asia/Hong_Kong")

TTHM_COLUMN = "tthm_mean_ug_l"
HIGH_RISK_COLUMN = "is_tthm_high_risk_month"

WATER_VARIABLES = {
    "pH": "ph_mean",
    "alkalinity": "alkalinity_mean_mg_l",
    "TOC": "toc_mean_mg_l",
    "free_chlorine": "free_chlorine_mean_mg_l",
    "total_chlorine": "total_chlorine_mean_mg_l",
}

CORE_PATTERN_VARIABLES = {
    "pH": "ph_mean",
    "alkalinity": "alkalinity_mean_mg_l",
    "TOC": "toc_mean_mg_l",
    "free_chlorine": "free_chlorine_mean_mg_l",
}


@dataclass(frozen=True)
class BaselineCandidate:
    label: str
    column: str
    candidate_role: str
    recommendation: str


BASELINE_CANDIDATES = [
    BaselineCandidate("month", "month", "baseline_core", "保留为二层 baseline 的基础季节字段"),
    BaselineCandidate("state_code", "state_code", "baseline_core", "保留为结构背景字段"),
    BaselineCandidate("system_type", "system_type", "baseline_core", "保留为系统类型字段"),
    BaselineCandidate("source_water_type", "source_water_type", "baseline_core", "保留为原水类型字段"),
    BaselineCandidate("retail_population_served", "retail_population_served", "baseline_core", "保留为规模字段"),
    BaselineCandidate(
        "adjusted_total_population_served",
        "adjusted_total_population_served",
        "baseline_core",
        "保留为调整后规模字段",
    ),
    BaselineCandidate(
        "has_treatment_summary",
        "has_treatment_summary",
        "baseline_core",
        "保留为 treatment 可用性指示字段",
    ),
    BaselineCandidate(
        "water_facility_type",
        "water_facility_type",
        "conditional_baseline",
        "可作为条件性 baseline 候选，但不能作为第一版必选字段",
    ),
    BaselineCandidate(
        "has_disinfection_process",
        "has_disinfection_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
    BaselineCandidate(
        "has_filtration_process",
        "has_filtration_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
    BaselineCandidate(
        "has_adsorption_process",
        "has_adsorption_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
    BaselineCandidate(
        "has_oxidation_process",
        "has_oxidation_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
    BaselineCandidate(
        "has_chloramination_process",
        "has_chloramination_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
    BaselineCandidate(
        "has_hypochlorination_process",
        "has_hypochlorination_process",
        "pause_from_baseline",
        "当前覆盖过低，不建议进入第一版 baseline",
    ),
]

BASELINE_SETS = {
    "baseline_core": [
        TTHM_COLUMN,
        "month",
        "state_code",
        "system_type",
        "source_water_type",
        "retail_population_served",
        "adjusted_total_population_served",
        "has_treatment_summary",
    ],
    "baseline_core_plus_water_facility_type": [
        TTHM_COLUMN,
        "month",
        "state_code",
        "system_type",
        "source_water_type",
        "water_facility_type",
        "retail_population_served",
        "adjusted_total_population_served",
        "has_treatment_summary",
    ],
    "baseline_core_plus_disinfection_flag": [
        TTHM_COLUMN,
        "month",
        "state_code",
        "system_type",
        "source_water_type",
        "retail_population_served",
        "adjusted_total_population_served",
        "has_treatment_summary",
        "has_disinfection_process",
    ],
    "baseline_core_plus_all_treatment_flags": [
        TTHM_COLUMN,
        "month",
        "state_code",
        "system_type",
        "source_water_type",
        "retail_population_served",
        "adjusted_total_population_served",
        "has_treatment_summary",
        "has_disinfection_process",
        "has_filtration_process",
        "has_adsorption_process",
        "has_oxidation_process",
        "has_chloramination_process",
        "has_hypochlorination_process",
    ],
}

REQUIRED_COMPLETE_CASE_COMBOS = [
    ("TTHM + pH", [TTHM_COLUMN, WATER_VARIABLES["pH"]]),
    ("TTHM + alkalinity", [TTHM_COLUMN, WATER_VARIABLES["alkalinity"]]),
    ("TTHM + TOC", [TTHM_COLUMN, WATER_VARIABLES["TOC"]]),
    ("TTHM + free_chlorine", [TTHM_COLUMN, WATER_VARIABLES["free_chlorine"]]),
    ("TTHM + total_chlorine", [TTHM_COLUMN, WATER_VARIABLES["total_chlorine"]]),
    (
        "TTHM + pH + alkalinity",
        [TTHM_COLUMN, WATER_VARIABLES["pH"], WATER_VARIABLES["alkalinity"]],
    ),
    (
        "TTHM + pH + alkalinity + TOC",
        [TTHM_COLUMN, WATER_VARIABLES["pH"], WATER_VARIABLES["alkalinity"], WATER_VARIABLES["TOC"]],
    ),
    (
        "TTHM + pH + alkalinity + TOC + free_chlorine",
        [
            TTHM_COLUMN,
            WATER_VARIABLES["pH"],
            WATER_VARIABLES["alkalinity"],
            WATER_VARIABLES["TOC"],
            WATER_VARIABLES["free_chlorine"],
        ],
    ),
    (
        "TTHM + pH + alkalinity + TOC + total_chlorine",
        [
            TTHM_COLUMN,
            WATER_VARIABLES["pH"],
            WATER_VARIABLES["alkalinity"],
            WATER_VARIABLES["TOC"],
            WATER_VARIABLES["total_chlorine"],
        ],
    ),
]

ADDITIONAL_COMPLETE_CASE_COMBOS = [
    (
        "TTHM + pH + free_chlorine",
        [TTHM_COLUMN, WATER_VARIABLES["pH"], WATER_VARIABLES["free_chlorine"]],
    ),
    (
        "TTHM + pH + total_chlorine",
        [TTHM_COLUMN, WATER_VARIABLES["pH"], WATER_VARIABLES["total_chlorine"]],
    ),
    (
        "TTHM + pH + alkalinity + free_chlorine",
        [
            TTHM_COLUMN,
            WATER_VARIABLES["pH"],
            WATER_VARIABLES["alkalinity"],
            WATER_VARIABLES["free_chlorine"],
        ],
    ),
    (
        "TTHM + pH + alkalinity + total_chlorine",
        [
            TTHM_COLUMN,
            WATER_VARIABLES["pH"],
            WATER_VARIABLES["alkalinity"],
            WATER_VARIABLES["total_chlorine"],
        ],
    ),
    (
        "TTHM + pH + alkalinity + free_chlorine + total_chlorine",
        [
            TTHM_COLUMN,
            WATER_VARIABLES["pH"],
            WATER_VARIABLES["alkalinity"],
            WATER_VARIABLES["free_chlorine"],
            WATER_VARIABLES["total_chlorine"],
        ],
    ),
]


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_source() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"未找到输入文件：{INPUT_PATH}")

    required_columns = {
        "month",
        TTHM_COLUMN,
        HIGH_RISK_COLUMN,
        "match_quality_tier",
    }
    required_columns.update(WATER_VARIABLES.values())
    required_columns.update(candidate.column for candidate in BASELINE_CANDIDATES)

    return pd.read_csv(
        INPUT_PATH,
        usecols=sorted(required_columns),
        encoding="utf-8-sig",
        low_memory=False,
        dtype={
            "state_code": "string",
            "system_type": "string",
            "source_water_type": "string",
            "water_facility_type": "string",
            "match_quality_tier": "string",
        },
    )


def build_candidate_variable_coverage_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows_total = len(df)
    tthm_mask = df[TTHM_COLUMN].notna()
    tthm_rows = int(tthm_mask.sum())
    rows: list[dict[str, object]] = []

    for label, column in WATER_VARIABLES.items():
        non_missing_rows = int(df[column].notna().sum())
        overlap_mask = tthm_mask & df[column].notna()
        overlap_rows = int(overlap_mask.sum())
        overlap_positive_rows = int(df.loc[overlap_mask, HIGH_RISK_COLUMN].fillna(0).sum())
        rows.append(
            {
                "variable_label": label,
                "column_name": column,
                "non_missing_rows_total": non_missing_rows,
                "non_missing_rate_total": non_missing_rows / rows_total if rows_total else 0.0,
                "tthm_overlap_rows": overlap_rows,
                "tthm_overlap_rate_within_tthm_rows": overlap_rows / tthm_rows if tthm_rows else 0.0,
                "tthm_overlap_rate_within_variable_rows": overlap_rows / non_missing_rows if non_missing_rows else 0.0,
                "high_risk_positive_rows_in_overlap": overlap_positive_rows,
                "high_risk_positive_rate_in_overlap": (
                    overlap_positive_rows / overlap_rows if overlap_rows else 0.0
                ),
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["tthm_overlap_rows", "non_missing_rows_total"],
        ascending=[False, False],
    )


def build_pairwise_overlap_summary(df: pd.DataFrame) -> pd.DataFrame:
    tthm_rows = int(df[TTHM_COLUMN].notna().sum())
    rows: list[dict[str, object]] = []
    for label, column in WATER_VARIABLES.items():
        mask = df[[TTHM_COLUMN, column]].notna().all(axis=1)
        overlap_rows = int(mask.sum())
        positive_rows = int(df.loc[mask, HIGH_RISK_COLUMN].fillna(0).sum())
        rows.append(
            {
                "combo_name": f"TTHM + {label}",
                "variable_label": label,
                "combo_columns": f"{TTHM_COLUMN}, {column}",
                "complete_case_rows": overlap_rows,
                "complete_case_rate_within_tthm_rows": overlap_rows / tthm_rows if tthm_rows else 0.0,
                "high_risk_positive_rows": positive_rows,
                "high_risk_positive_rate": positive_rows / overlap_rows if overlap_rows else 0.0,
            }
        )
    return pd.DataFrame(rows).sort_values("complete_case_rows", ascending=False)


def build_complete_case_summary(df: pd.DataFrame) -> pd.DataFrame:
    tthm_rows = int(df[TTHM_COLUMN].notna().sum())
    rows: list[dict[str, object]] = []
    all_combos = [
        *[(name, columns, True) for name, columns in REQUIRED_COMPLETE_CASE_COMBOS],
        *[(name, columns, False) for name, columns in ADDITIONAL_COMPLETE_CASE_COMBOS],
    ]

    for combo_name, columns, is_required in all_combos:
        mask = df[columns].notna().all(axis=1)
        complete_case_rows = int(mask.sum())
        positive_rows = int(df.loc[mask, HIGH_RISK_COLUMN].fillna(0).sum())
        rows.append(
            {
                "combo_name": combo_name,
                "is_required_by_v5_0_prompt": int(is_required),
                "n_variables_including_tthm": len(columns),
                "complete_case_rows": complete_case_rows,
                "complete_case_rate_within_tthm_rows": (
                    complete_case_rows / tthm_rows if tthm_rows else 0.0
                ),
                "high_risk_positive_rows": positive_rows,
                "high_risk_positive_rate": positive_rows / complete_case_rows if complete_case_rows else 0.0,
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["n_variables_including_tthm", "complete_case_rows"],
        ascending=[True, False],
    )


def describe_core_pattern(row: pd.Series) -> str:
    observed = [label for label, column in CORE_PATTERN_VARIABLES.items() if bool(row[column])]
    return "none" if not observed else " + ".join(observed)


def build_core_pattern_summary(df: pd.DataFrame) -> pd.DataFrame:
    tthm_df = df.loc[df[TTHM_COLUMN].notna()].copy()
    for column in CORE_PATTERN_VARIABLES.values():
        tthm_df[column] = tthm_df[column].notna()
    tthm_df["pattern_name"] = tthm_df[list(CORE_PATTERN_VARIABLES.values())].apply(
        describe_core_pattern,
        axis=1,
    )

    summary = (
        tthm_df.groupby("pattern_name", dropna=False)
        .agg(
            complete_case_rows=(HIGH_RISK_COLUMN, "size"),
            high_risk_positive_rows=(HIGH_RISK_COLUMN, lambda series: int(series.fillna(0).sum())),
        )
        .reset_index()
    )
    total_rows = int(summary["complete_case_rows"].sum())
    summary["complete_case_rate_within_tthm_rows"] = summary["complete_case_rows"] / total_rows if total_rows else 0.0
    summary["high_risk_positive_rate"] = summary["high_risk_positive_rows"] / summary["complete_case_rows"]
    return summary.sort_values("complete_case_rows", ascending=False)


def build_baseline_candidate_summary(df: pd.DataFrame) -> pd.DataFrame:
    tthm_df = df.loc[df[TTHM_COLUMN].notna()].copy()
    tthm_rows = int(len(tthm_df))
    rows: list[dict[str, object]] = []

    for candidate in BASELINE_CANDIDATES:
        series = tthm_df[candidate.column]
        non_missing_rows = int(series.notna().sum())
        rows.append(
            {
                "field_label": candidate.label,
                "column_name": candidate.column,
                "candidate_role": candidate.candidate_role,
                "tthm_non_missing_rows": non_missing_rows,
                "tthm_non_missing_rate": non_missing_rows / tthm_rows if tthm_rows else 0.0,
                "n_unique_non_missing_values": int(series.dropna().nunique()),
                "recommendation": candidate.recommendation,
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["candidate_role", "tthm_non_missing_rate", "field_label"],
        ascending=[True, False, True],
    )


def build_baseline_set_readiness(df: pd.DataFrame) -> pd.DataFrame:
    tthm_rows = int(df[TTHM_COLUMN].notna().sum())
    rows: list[dict[str, object]] = []

    for set_name, columns in BASELINE_SETS.items():
        mask = df[columns].notna().all(axis=1)
        ready_rows = int(mask.sum())
        positive_rows = int(df.loc[mask, HIGH_RISK_COLUMN].fillna(0).sum())
        rows.append(
            {
                "baseline_set_name": set_name,
                "columns": ", ".join(columns),
                "ready_rows": ready_rows,
                "ready_rate_within_tthm_rows": ready_rows / tthm_rows if tthm_rows else 0.0,
                "high_risk_positive_rows": positive_rows,
                "high_risk_positive_rate": positive_rows / ready_rows if ready_rows else 0.0,
            }
        )

    return pd.DataFrame(rows).sort_values("ready_rows", ascending=False)


def build_match_quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    tthm_df = df.loc[df[TTHM_COLUMN].notna()].copy()
    total_rows = int(len(tthm_df))
    summary = (
        tthm_df.groupby("match_quality_tier", dropna=False)
        .agg(
            rows=(HIGH_RISK_COLUMN, "size"),
            high_risk_positive_rows=(HIGH_RISK_COLUMN, lambda series: int(series.fillna(0).sum())),
        )
        .reset_index()
        .rename(columns={"match_quality_tier": "tier_name"})
    )
    summary["share_within_tthm_rows"] = summary["rows"] / total_rows if total_rows else 0.0
    summary["high_risk_positive_rate"] = summary["high_risk_positive_rows"] / summary["rows"]
    return summary.sort_values("rows", ascending=False)


def build_recommendation_summary(
    complete_case_df: pd.DataFrame,
    baseline_set_df: pd.DataFrame,
) -> pd.DataFrame:
    lookup = complete_case_df.set_index("combo_name")
    baseline_lookup = baseline_set_df.set_index("baseline_set_name")

    rows = [
        {
            "stage_name": "V5.1",
            "recommended_action": "proceed",
            "recommended_chain": "baseline_core",
            "evidence_rows": int(baseline_lookup.loc["baseline_core", "ready_rows"]),
            "evidence_positive_rows": int(baseline_lookup.loc["baseline_core", "high_risk_positive_rows"]),
            "judgement": "二层 baseline 可围绕稳定结构字段和 treatment 可用性指示字段启动。",
        },
        {
            "stage_name": "V5.2",
            "recommended_action": "proceed",
            "recommended_chain": "baseline + pH + alkalinity",
            "evidence_rows": int(lookup.loc["TTHM + pH + alkalinity", "complete_case_rows"]),
            "evidence_positive_rows": int(lookup.loc["TTHM + pH + alkalinity", "high_risk_positive_rows"]),
            "judgement": "在所有二层水质双变量组合中，pH + alkalinity 与 TTHM 的重合度最高，适合作为第一轮正式增强。",
        },
        {
            "stage_name": "V5.3",
            "recommended_action": "hold_for_now",
            "recommended_chain": "baseline + pH + alkalinity + TOC",
            "evidence_rows": int(lookup.loc["TTHM + pH + alkalinity + TOC", "complete_case_rows"]),
            "evidence_positive_rows": int(
                lookup.loc["TTHM + pH + alkalinity + TOC", "high_risk_positive_rows"]
            ),
            "judgement": "TOC 在真正二层下的 strict complete-case 只剩极少样本，当前更适合作为 reduced dataset 专题候选，而不是立即进入正式主链。",
        },
        {
            "stage_name": "free_chlorine",
            "recommended_action": "pause_formal_chain",
            "recommended_chain": "baseline + pH + alkalinity + free_chlorine",
            "evidence_rows": int(
                lookup.loc["TTHM + pH + alkalinity + free_chlorine", "complete_case_rows"]
            ),
            "evidence_positive_rows": int(
                lookup.loc["TTHM + pH + alkalinity + free_chlorine", "high_risk_positive_rows"]
            ),
            "judgement": "虽然比 TOC 链保留更多 complete-case，但总体覆盖仍不足 1%，不适合作为正式主链下一步。",
        },
        {
            "stage_name": "total_chlorine",
            "recommended_action": "pause_formal_chain",
            "recommended_chain": "baseline + pH + alkalinity + total_chlorine",
            "evidence_rows": int(
                lookup.loc["TTHM + pH + alkalinity + total_chlorine", "complete_case_rows"]
            ),
            "evidence_positive_rows": int(
                lookup.loc["TTHM + pH + alkalinity + total_chlorine", "high_risk_positive_rows"]
            ),
            "judgement": "总氯整体覆盖更弱，只适合作为第二层小范围专题变量候选。",
        },
    ]

    return pd.DataFrame(rows)


def pct_text(value: float) -> str:
    return f"{value * 100:.2f}%"


def build_snapshot_markdown(
    candidate_df: pd.DataFrame,
    complete_case_df: pd.DataFrame,
    baseline_set_df: pd.DataFrame,
    recommendation_df: pd.DataFrame,
) -> str:
    baseline_core = baseline_set_df.loc[
        baseline_set_df["baseline_set_name"] == "baseline_core"
    ].iloc[0]
    stage_v52 = recommendation_df.loc[recommendation_df["stage_name"] == "V5.2"].iloc[0]
    stage_v53 = recommendation_df.loc[recommendation_df["stage_name"] == "V5.3"].iloc[0]
    required_df = complete_case_df.loc[complete_case_df["is_required_by_v5_0_prompt"] == 1].copy()

    lines = [
        "# V5.0 Facility-Month Readiness Audit 本地摘要",
        "",
        f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
        f"- 输入文件：`{INPUT_PATH}`",
        f"- 输出目录：`{OUTPUT_DIR}`",
        "",
        "## 1. 当前最重要的结论",
        "",
        f"- `baseline_core` 可用行数为 `{int(baseline_core['ready_rows']):,}`，占 `TTHM` 月样本的 `{pct_text(float(baseline_core['ready_rate_within_tthm_rows']))}`。",  # noqa: E501
        f"- 第一轮正式增强最稳妥的链条仍是 `baseline + pH + alkalinity`，对应 complete-case 行数为 `{int(stage_v52['evidence_rows']):,}`。",  # noqa: E501
        f"- `baseline + pH + alkalinity + TOC` 当前只剩 `{int(stage_v53['evidence_rows'])}` 行 complete-case，暂不建议直接进入正式主链。",  # noqa: E501
        "- `free_chlorine` 与 `total_chlorine` 都不适合作为当前第二层正式主链变量，应先暂停。",
        "",
        "## 2. 候选变量覆盖率",
        "",
        "| 变量 | 总体非缺失行数 | 总体非缺失率 | 与 TTHM 重合行数 | TTHM 内重合率 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for _, row in candidate_df.iterrows():
        lines.append(
            f"| `{row['variable_label']}` | {int(row['non_missing_rows_total']):,} | "
            f"{pct_text(float(row['non_missing_rate_total']))} | {int(row['tthm_overlap_rows']):,} | "
            f"{pct_text(float(row['tthm_overlap_rate_within_tthm_rows']))} |"
        )

    lines.extend(
        [
            "",
            "## 3. 必做 complete-case 检查",
            "",
            "| 组合 | 行数 | TTHM 内比例 | 高风险正例数 |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for _, row in required_df.iterrows():
        lines.append(
            f"| `{row['combo_name']}` | {int(row['complete_case_rows']):,} | "
            f"{pct_text(float(row['complete_case_rate_within_tthm_rows']))} | "
            f"{int(row['high_risk_positive_rows']):,} |"
        )

    lines.extend(
        [
            "",
            "## 4. 当前建议",
            "",
        ]
    )

    for _, row in recommendation_df.iterrows():
        lines.append(
            f"- `{row['stage_name']}`：`{row['recommended_action']}`，"
            f"`{row['recommended_chain']}`，证据行为 `{int(row['evidence_rows']):,}`。"
        )
        lines.append(f"  说明：{row['judgement']}")

    return "\n".join(lines) + "\n"


def write_csv(df: pd.DataFrame, file_name: str) -> Path:
    output_path = OUTPUT_DIR / file_name
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def main() -> None:
    ensure_output_dir()
    source_df = read_source()

    candidate_df = build_candidate_variable_coverage_summary(source_df)
    pairwise_df = build_pairwise_overlap_summary(source_df)
    complete_case_df = build_complete_case_summary(source_df)
    core_pattern_df = build_core_pattern_summary(source_df)
    baseline_candidate_df = build_baseline_candidate_summary(source_df)
    baseline_set_df = build_baseline_set_readiness(source_df)
    match_quality_df = build_match_quality_summary(source_df)
    recommendation_df = build_recommendation_summary(complete_case_df, baseline_set_df)

    output_paths = [
        write_csv(candidate_df, "v5_0_facility_month_candidate_variable_coverage.csv"),
        write_csv(pairwise_df, "v5_0_facility_month_pairwise_overlap_summary.csv"),
        write_csv(complete_case_df, "v5_0_facility_month_complete_case_summary.csv"),
        write_csv(core_pattern_df, "v5_0_facility_month_core_pattern_summary.csv"),
        write_csv(baseline_candidate_df, "v5_0_facility_month_baseline_candidate_summary.csv"),
        write_csv(baseline_set_df, "v5_0_facility_month_baseline_set_readiness.csv"),
        write_csv(match_quality_df, "v5_0_facility_month_match_quality_summary.csv"),
        write_csv(recommendation_df, "v5_0_facility_month_recommendation_summary.csv"),
    ]

    SNAPSHOT_PATH.write_text(
        build_snapshot_markdown(
            candidate_df=candidate_df,
            complete_case_df=complete_case_df,
            baseline_set_df=baseline_set_df,
            recommendation_df=recommendation_df,
        ),
        encoding="utf-8",
    )

    print("Completed V5.0 facility-month readiness audit")
    for path in output_paths:
        print(f"Wrote: {path}")
    print(f"Wrote: {SNAPSHOT_PATH}")
    print(candidate_df.to_string(index=False))
    print(complete_case_df.to_string(index=False))
    print(baseline_set_df.to_string(index=False))
    print(recommendation_df.to_string(index=False))


if __name__ == "__main__":
    main()
