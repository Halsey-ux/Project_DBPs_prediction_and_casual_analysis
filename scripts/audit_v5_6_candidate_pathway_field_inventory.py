from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
V3_DIR = PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build"
V4_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V5_Chapter1_Part1_Facility_Month_Module" / "V5_6"
DOCS_DIR = PROJECT_ROOT / "docs" / "07_v5" / "13_v5_6_execution"
TZ = ZoneInfo("Asia/Hong_Kong")

INPUT_TABLES = {
    "pws_year": {
        "path": V3_DIR / "V3_pws_year_master.csv",
        "source_table": "V3_pws_year_master.csv",
        "tthm_label_columns": ("tthm_sample_weighted_mean_ug_l",),
        "haa5_label_columns": ("haa5_sample_weighted_mean_ug_l",),
    },
    "facility_month": {
        "path": V3_DIR / "V3_facility_month_master.csv",
        "source_table": "V3_facility_month_master.csv",
        "tthm_label_columns": ("tthm_mean_ug_l", "is_tthm_high_risk_month"),
        "haa5_label_columns": ("haa5_mean_ug_l", "is_haa5_high_risk_month"),
    },
    "pws_year_ml_ready": {
        "path": V4_DIR / "V4_pws_year_ml_ready.csv",
        "source_table": "V4_pws_year_ml_ready.csv",
        "tthm_label_columns": ("tthm_regulatory_exceed_label", "tthm_sample_weighted_mean_ug_l"),
        "haa5_label_columns": (),
    },
}

SUBTYPE_MECHANISM = "possible_mechanism_intensity"
SUBTYPE_MONITORING = "possible_monitoring_coverage"
SUBTYPE_QUALITY = "possible_evidence_quality"
SUBTYPE_OUTCOME = "possible_outcome_or_label"
SUBTYPE_CONTEXT = "possible_context_or_structure"
SUBTYPE_REVIEW = "needs_review"


@dataclass(frozen=True)
class PathwaySpec:
    name: str
    role: str
    training_scope: str
    review_reason: str
    exact_fields: tuple[str, ...] = ()
    prefixes: tuple[str, ...] = ()
    contains: tuple[str, ...] = ()


PATHWAYS = [
    PathwaySpec(
        name="结构背景通路",
        role="main_screening_candidate",
        training_scope="可进入主筛查准入测试，但仍需经过先验因果-语义复核。",
        review_reason="需区分风险画像变量、工程背景变量和机制变量。",
        exact_fields=(
            "system_type",
            "source_water_type",
            "retail_population_served",
            "adjusted_total_population_served",
            "state_code",
        ),
    ),
    PathwaySpec(
        name="设施复杂度通路",
        role="main_screening_candidate",
        training_scope="可进入主筛查准入测试，重点关注覆盖率、应用可得性和缺失语义。",
        review_reason="设施数、设施类型和 flow 记录更像工程背景或监测代理，不应直接解释为化学机制。",
        exact_fields=(
            "water_facility_type",
            "n_facilities_in_master",
            "n_supplying_facilities",
            "flow_record_count",
            "water_facility_type_list",
        ),
    ),
    PathwaySpec(
        name="处理工艺通路",
        role="main_screening_or_mechanistic_candidate",
        training_scope="可作为工程背景候选进入准入测试，但必须先复核缺失语义和应用可得性。",
        review_reason="处理工艺字段具有工程含义，但记录缺失可能反映制度性记录差异。",
        exact_fields=(
            "has_disinfection_process",
            "has_filtration_process",
            "has_adsorption_process",
            "has_oxidation_process",
            "has_chloramination_process",
            "has_hypochlorination_process",
            "treatment_process_record_count",
            "n_treatment_process_names",
            "n_treatment_objective_names",
            "filter_type_list",
            "treatment_process_name_list",
            "treatment_objective_name_list",
            "treatment_process_summary",
        ),
    ),
    PathwaySpec(
        name="酸碱与缓冲条件通路",
        role="optional_mechanistic_evidence_candidate",
        training_scope="适合进入可选机制证据模块准入测试，不宜直接等同于全国主筛查主力输入。",
        review_reason="需拆分 pH/alkalinity 浓度强度字段与样本数、月份数、设施数等覆盖字段。",
        prefixes=("ph_", "alkalinity_"),
    ),
    PathwaySpec(
        name="NOM/有机前体物通路",
        role="optional_mechanistic_evidence_candidate",
        training_scope="更适合高信息子样本、专题审计或 reduced dataset 机制模块。",
        review_reason="需拆分 TOC/DOC/UV254/SUVA 强度字段与监测覆盖字段。",
        prefixes=("toc_", "doc_", "uv254_", "suva_"),
    ),
    PathwaySpec(
        name="消毒剂与残余消毒剂通路",
        role="optional_mechanistic_or_future_module",
        training_scope="当前不宜直接进入广覆盖主模型，需先复核时间顺序和真实应用可得性。",
        review_reason="消毒剂字段可能接近同周期运行状态，存在时序模糊和应用可得性风险。",
        exact_fields=("plant_disinfectant_concentration_mean_mg_l", "plant_ct_value_mean"),
        prefixes=("free_chlorine_", "total_chlorine_", "chloramine_"),
    ),
    PathwaySpec(
        name="监测覆盖度与证据质量通路",
        role="evidence_quality_module_candidate",
        training_scope="优先用于证据等级、完整性和可信度判断，不应直接解释为化学机制。",
        review_reason="样本数、月份数、设施数、source_module_count 和 match quality 类字段可能是监测强度代理。",
        exact_fields=(
            "n_result_vars_available",
            "n_outcome_vars_available",
            "n_core_vars_available",
            "n_extended_vars_available",
            "n_mechanism_vars_available",
            "source_module_count",
            "match_quality_tier",
            "annual_match_quality_tier",
            "months_observed_any",
            "months_with_1plus_core_vars",
            "months_with_2plus_core_vars",
            "months_with_3plus_core_vars",
            "mean_core_vars_available_in_row",
            "max_core_vars_available_in_row",
            "n_facility_month_rows",
            "has_water_system_facility_record",
            "has_facility_plant_record",
            "has_flow_record",
            "has_treatment_process_record",
            "has_treatment_summary",
            "n_facilities_with_treatment_summary",
        ),
        contains=("missing_flag", "treatment_profile_summary"),
    ),
    PathwaySpec(
        name="结果谱系/解释候选通路",
        role="outcome_profile_or_explanation_only",
        training_scope="只做字段存在性和覆盖率盘点，不得作为同周期预测输入。",
        review_reason="结果字段、目标代理和同周期结果家族字段存在直接或间接泄露风险。",
        prefixes=("tthm_", "haa5_", "bromate_", "chlorite_"),
        exact_fields=(
            "has_tthm",
            "has_haa5",
            "is_tthm_high_risk_month",
            "is_haa5_high_risk_month",
            "tthm_regulatory_exceed_label",
            "tthm_warning_label",
        ),
    ),
    PathwaySpec(
        name="合规与纠正行动响应候选通路",
        role="audit_only_due_to_leakage_risk",
        training_scope="只做字段存在性和覆盖率盘点，时序未明确前不得作为前置预测输入。",
        review_reason="合规、违规、纠正行动和监管响应字段可能是事后信息或目标代理。",
        contains=("compliance", "violation", "corrective", "action", "response", "enforcement"),
    ),
]


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(f"输入表不存在或为空：{path}")
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)


def first_existing_mask(df: pd.DataFrame, columns: tuple[str, ...]) -> pd.Series:
    for column in columns:
        if column in df.columns:
            return df[column].notna()
    return pd.Series(False, index=df.index)


def pct(value: object) -> str:
    if pd.isna(value):
        return "不适用"
    return f"{float(value) * 100:.2f}%"


def fmt_int(value: object) -> str:
    if pd.isna(value):
        return "不适用"
    return f"{int(value):,}"


def compact_number(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def sample_values(series: pd.Series, limit: int = 5) -> str:
    values: list[str] = []
    for value in series.dropna():
        text = compact_number(value).strip()
        if text and text not in values:
            values.append(text)
        if len(values) >= limit:
            break
    return "; ".join(values)


def infer_field_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    return "categorical_or_text"


def field_matches_spec(field_name: str, spec: PathwaySpec) -> tuple[bool, str]:
    lower_name = field_name.lower()
    if field_name in spec.exact_fields:
        return True, "exact"
    if any(lower_name.startswith(prefix) for prefix in spec.prefixes):
        return True, "prefix"
    if any(token in lower_name for token in spec.contains):
        return True, "contains"
    return False, ""


def matched_pathways(field_name: str) -> list[tuple[PathwaySpec, str]]:
    matches: list[tuple[PathwaySpec, str]] = []
    for spec in PATHWAYS:
        matched, matched_by = field_matches_spec(field_name, spec)
        if matched:
            matches.append((spec, matched_by))
    if any(spec.name == "结果谱系/解释候选通路" for spec, _ in matches):
        return [match for match in matches if match[0].name == "结果谱系/解释候选通路"]
    if any(spec.name == "合规与纠正行动响应候选通路" for spec, _ in matches):
        return [match for match in matches if match[0].name == "合规与纠正行动响应候选通路"]
    return matches


def pathway_guess(field_name: str) -> str:
    matches = matched_pathways(field_name)
    if not matches:
        return "未归类字段"
    return "; ".join(spec.name for spec, _ in matches)


def name_pattern(field_name: str) -> str:
    matches = matched_pathways(field_name)
    if not matches:
        return "unmatched"
    return "; ".join(matched_by for _, matched_by in matches)


def preliminary_subtype(field_name: str, pathway_name: str) -> str:
    lower_name = field_name.lower()
    if pathway_name in {"结果谱系/解释候选通路", "合规与纠正行动响应候选通路"}:
        return SUBTYPE_OUTCOME
    if (
        "match_quality" in lower_name
        or "available" in lower_name
        or "source_module_count" in lower_name
        or "missing_flag" in lower_name
        or lower_name in {"months_observed_any", "n_facility_month_rows"}
    ):
        return SUBTYPE_QUALITY
    if any(
        token in lower_name
        for token in ("sample_count", "n_samples", "months_with", "facility_month_count", "n_facilities", "record_count")
    ):
        return SUBTYPE_MONITORING
    if pathway_name in {"结构背景通路", "设施复杂度通路", "处理工艺通路"}:
        return SUBTYPE_CONTEXT
    if any(token in lower_name for token in ("mean", "median", "max", "p90", "ct_value", "concentration")):
        return SUBTYPE_MECHANISM
    return SUBTYPE_REVIEW


def field_remark(field_name: str, pathway_name: str, subtype: str) -> str:
    if pathway_name == "结果谱系/解释候选通路":
        return "结果或目标代理字段；本轮仅盘点，不得作为同周期预测输入。"
    if pathway_name == "合规与纠正行动响应候选通路":
        return "疑似事后监管响应或目标代理字段；需时序和泄露复核。"
    if subtype == SUBTYPE_QUALITY:
        return "证据质量或监测覆盖字段；可用于可信度分层，不宜直接解释为化学机制。"
    if subtype == SUBTYPE_MONITORING:
        return "样本数、月份数、设施数或记录数类字段；需与机制强度字段拆分。"
    if "chlorine" in field_name or "disinfectant" in field_name or "ct_value" in field_name:
        return "消毒剂相关字段；需复核时间顺序、运行状态接近性和应用可得性。"
    return "候选通路字段；本轮仅代表数据可用性审计，不代表最终字段准入。"


def preliminary_use_note(pathway_name: str, subtype: str, layer: str, haa5_available_n: int) -> str:
    if pathway_name == "结果谱系/解释候选通路":
        return "仅用于结果谱系盘点或解释，不作为同周期预测输入。"
    if pathway_name == "合规与纠正行动响应候选通路":
        return "仅用于后续泄露风险和时序复核。"
    if subtype == SUBTYPE_QUALITY:
        return "优先用于证据质量、完整性或可信度分层。"
    if layer == "pws_year_ml_ready" and haa5_available_n == 0:
        return "该 V4 对照表当前仅有 TTHM 主线标签，不能用于 HAA5 对齐结论。"
    return "可作为候选字段继续进入准入事实审计；是否入模需后续复核。"


def needs_causal_review(pathway_name: str, subtype: str) -> bool:
    if pathway_name in {"结果谱系/解释候选通路", "合规与纠正行动响应候选通路"}:
        return True
    return subtype in {SUBTYPE_MECHANISM, SUBTYPE_MONITORING, SUBTYPE_QUALITY, SUBTYPE_REVIEW}


def build_inventory(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, df in tables.items():
        total_n = len(df)
        source_table = INPUT_TABLES[layer]["source_table"]
        for field_name in df.columns:
            series = df[field_name]
            non_missing_n = int(series.notna().sum())
            guess = pathway_guess(field_name)
            rows.append(
                {
                    "layer": layer,
                    "source_table": source_table,
                    "field_name": field_name,
                    "field_type": infer_field_type(series),
                    "non_missing_n": non_missing_n,
                    "total_n": total_n,
                    "non_missing_rate": non_missing_n / total_n if total_n else 0.0,
                    "unique_n": int(series.nunique(dropna=True)),
                    "example_values": sample_values(series),
                    "name_pattern": name_pattern(field_name),
                    "is_known_candidate_field": guess != "未归类字段",
                    "candidate_pathway_guess": guess,
                    "remarks": "全字段 inventory 自动盘点；字段准入仍需后续复核。",
                }
            )
    return pd.DataFrame(rows)


def build_field_label_alignment(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, df in tables.items():
        total_n = len(df)
        tthm_mask = first_existing_mask(df, INPUT_TABLES[layer]["tthm_label_columns"])
        haa5_mask = first_existing_mask(df, INPUT_TABLES[layer]["haa5_label_columns"])
        tthm_available_n = int(tthm_mask.sum())
        haa5_available_n = int(haa5_mask.sum())
        for field_name in df.columns:
            series = df[field_name]
            field_mask = series.notna()
            non_missing_n = int(field_mask.sum())
            guess = pathway_guess(field_name)
            primary_pathway = guess.split("; ")[0]
            subtype = preliminary_subtype(field_name, primary_pathway)
            tthm_overlap = int((field_mask & tthm_mask).sum())
            haa5_overlap = int((field_mask & haa5_mask).sum())
            rows.append(
                {
                    "layer": layer,
                    "field_name": field_name,
                    "candidate_pathway_guess": guess,
                    "non_missing_n": non_missing_n,
                    "total_n": total_n,
                    "non_missing_rate": non_missing_n / total_n if total_n else 0.0,
                    "tthm_label_available_n": tthm_available_n,
                    "field_and_tthm_label_n": tthm_overlap,
                    "field_and_tthm_label_rate": tthm_overlap / total_n if total_n else 0.0,
                    "haa5_label_available_n": haa5_available_n,
                    "field_and_haa5_label_n": haa5_overlap,
                    "field_and_haa5_label_rate": haa5_overlap / total_n if total_n else 0.0,
                    "preliminary_use_note": preliminary_use_note(primary_pathway, subtype, layer, haa5_available_n),
                    "needs_causal_semantic_review": needs_causal_review(primary_pathway, subtype),
                }
            )
    return pd.DataFrame(rows)


def pathway_fields_for_layer(df: pd.DataFrame, spec: PathwaySpec) -> list[tuple[str, str, bool]]:
    fields: list[tuple[str, str, bool]] = []
    seen: set[str] = set()
    for field in spec.exact_fields:
        if field not in seen:
            fields.append((field, "exact", field in df.columns))
            seen.add(field)
    for field in df.columns:
        if field in seen:
            continue
        lower_field = field.lower()
        if any(lower_field.startswith(prefix) for prefix in spec.prefixes):
            fields.append((field, "prefix", True))
            seen.add(field)
        elif any(token in lower_field for token in spec.contains):
            fields.append((field, "contains", True))
            seen.add(field)
    return fields


def build_pathway_field_map(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, df in tables.items():
        total_n = len(df)
        tthm_mask = first_existing_mask(df, INPUT_TABLES[layer]["tthm_label_columns"])
        haa5_mask = first_existing_mask(df, INPUT_TABLES[layer]["haa5_label_columns"])
        for spec in PATHWAYS:
            for field_name, matched_by, exists in pathway_fields_for_layer(df, spec):
                if exists:
                    field_mask = df[field_name].notna()
                    non_missing_n = int(field_mask.sum())
                    non_missing_rate = non_missing_n / total_n if total_n else 0.0
                    tthm_overlap = int((field_mask & tthm_mask).sum())
                    haa5_overlap = int((field_mask & haa5_mask).sum())
                    subtype = preliminary_subtype(field_name, spec.name)
                    remarks = field_remark(field_name, spec.name, subtype)
                else:
                    non_missing_n = 0
                    non_missing_rate = 0.0
                    tthm_overlap = 0
                    haa5_overlap = 0
                    subtype = SUBTYPE_REVIEW
                    remarks = "字段未出现在当前层级输入表中。"
                rows.append(
                    {
                        "layer": layer,
                        "pathway_name": spec.name,
                        "field_name": field_name,
                        "matched_by": matched_by,
                        "field_exists": exists,
                        "non_missing_n": non_missing_n,
                        "non_missing_rate": non_missing_rate,
                        "field_and_tthm_label_n": tthm_overlap,
                        "field_and_haa5_label_n": haa5_overlap,
                        "preliminary_field_subtype": subtype,
                        "remarks": remarks,
                    }
                )
    return pd.DataFrame(rows)


def summarize_field_rates(field_rows: pd.DataFrame, limit: int = 5) -> tuple[str, str]:
    existing = field_rows.loc[field_rows["field_exists"] == True].copy()
    if existing.empty:
        return "", ""
    existing = existing.sort_values(["non_missing_rate", "non_missing_n", "field_name"], ascending=[False, False, True])
    top = [f"{row.field_name}({pct(row.non_missing_rate)})" for row in existing.head(limit).itertuples(index=False)]
    low = [f"{row.field_name}({pct(row.non_missing_rate)})" for row in existing.tail(limit).itertuples(index=False)]
    return "; ".join(top), "; ".join(low)


def build_internal_coverage_summary(tables: dict[str, pd.DataFrame], field_map: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, df in tables.items():
        total_n = len(df)
        tthm_mask = first_existing_mask(df, INPUT_TABLES[layer]["tthm_label_columns"])
        haa5_mask = first_existing_mask(df, INPUT_TABLES[layer]["haa5_label_columns"])
        for spec in PATHWAYS:
            pathway_rows = field_map.loc[(field_map["layer"] == layer) & (field_map["pathway_name"] == spec.name)]
            existing_fields = [
                field for field in pathway_rows.loc[pathway_rows["field_exists"] == True, "field_name"].tolist()
                if field in df.columns
            ]
            any_mask = df[existing_fields].notna().any(axis=1) if existing_fields else pd.Series(False, index=df.index)
            top_fields, low_fields = summarize_field_rates(pathway_rows)
            tthm_overlap = int((any_mask & tthm_mask).sum())
            haa5_overlap = int((any_mask & haa5_mask).sum())
            rows.append(
                {
                    "layer": layer,
                    "pathway_name": spec.name,
                    "field_count": int(len(pathway_rows)),
                    "fields_existing_n": int(len(existing_fields)),
                    "any_field_non_missing_n": int(any_mask.sum()),
                    "any_field_non_missing_rate": int(any_mask.sum()) / total_n if total_n else 0.0,
                    "top_coverage_fields": top_fields,
                    "low_coverage_fields": low_fields,
                    "possible_mechanism_fields_n": int((pathway_rows["preliminary_field_subtype"] == SUBTYPE_MECHANISM).sum()),
                    "possible_monitoring_coverage_fields_n": int((pathway_rows["preliminary_field_subtype"] == SUBTYPE_MONITORING).sum()),
                    "tthm_label_overlap_n": tthm_overlap,
                    "tthm_label_overlap_rate": tthm_overlap / total_n if total_n else 0.0,
                    "haa5_label_overlap_n": haa5_overlap,
                    "haa5_label_overlap_rate": haa5_overlap / total_n if total_n else 0.0,
                }
            )
    return pd.DataFrame(rows)


def feasibility_note(spec: PathwaySpec, complete_rate: float, partial1_rate: float, tthm_overlap_n: int) -> str:
    if spec.name in {"结果谱系/解释候选通路", "合规与纠正行动响应候选通路"}:
        return "仅限盘点和泄露复核，不进入预测输入。"
    if complete_rate >= 0.3 and tthm_overlap_n > 1000:
        return "完整组合样本基础较好，可进入后续模型准入测试。"
    if partial1_rate >= 0.1 and tthm_overlap_n > 1000:
        return "完整组合不足，但 partial-case 或子组合审计仍有基础。"
    return "完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。"


def build_complete_partial_summary(tables: dict[str, pd.DataFrame], field_map: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, df in tables.items():
        total_n = len(df)
        tthm_mask = first_existing_mask(df, INPUT_TABLES[layer]["tthm_label_columns"])
        haa5_mask = first_existing_mask(df, INPUT_TABLES[layer]["haa5_label_columns"])
        for spec in PATHWAYS:
            pathway_rows = field_map.loc[(field_map["layer"] == layer) & (field_map["pathway_name"] == spec.name)]
            existing_fields = [
                field for field in pathway_rows.loc[pathway_rows["field_exists"] == True, "field_name"].tolist()
                if field in df.columns
            ]
            candidate_count = len(existing_fields)
            if existing_fields:
                non_missing_count = df[existing_fields].notna().sum(axis=1)
                complete_mask = non_missing_count == candidate_count
                partial1_mask = non_missing_count >= 1
                partial2_mask = non_missing_count >= 2 if candidate_count >= 2 else None
                partial3_mask = non_missing_count >= 3 if candidate_count >= 3 else None
            else:
                complete_mask = pd.Series(False, index=df.index)
                partial1_mask = pd.Series(False, index=df.index)
                partial2_mask = None
                partial3_mask = None
            complete_n = int(complete_mask.sum())
            partial1_n = int(partial1_mask.sum())
            partial2_n = int(partial2_mask.sum()) if partial2_mask is not None else pd.NA
            partial3_n = int(partial3_mask.sum()) if partial3_mask is not None else pd.NA
            complete_rate = complete_n / total_n if total_n else 0.0
            partial1_rate = partial1_n / total_n if total_n else 0.0
            rows.append(
                {
                    "layer": layer,
                    "pathway_name": spec.name,
                    "candidate_field_count": candidate_count,
                    "complete_case_n_all_candidate_fields": complete_n,
                    "complete_case_rate_all_candidate_fields": complete_rate,
                    "partial_case_n_at_least_1": partial1_n,
                    "partial_case_rate_at_least_1": partial1_rate,
                    "partial_case_n_at_least_2": partial2_n,
                    "partial_case_rate_at_least_2": partial2_n / total_n if total_n and partial2_mask is not None else pd.NA,
                    "partial_case_n_at_least_3": partial3_n,
                    "partial_case_rate_at_least_3": partial3_n / total_n if total_n and partial3_mask is not None else pd.NA,
                    "tthm_overlap_complete_case_n": int((complete_mask & tthm_mask).sum()),
                    "haa5_overlap_complete_case_n": int((complete_mask & haa5_mask).sum()),
                    "training_feasibility_note": feasibility_note(
                        spec,
                        complete_rate,
                        partial1_rate,
                        int((complete_mask & tthm_mask).sum()),
                    ),
                }
            )
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame, columns: list[str], max_rows: int | None = None) -> str:
    view = df.loc[:, columns].copy()
    if max_rows is not None:
        view = view.head(max_rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for _, row in view.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if column.endswith("_rate"):
                values.append(pct(value))
            elif column.endswith("_n") or column in {"rows", "columns", "field_count", "candidate_field_count", "fields_existing_n"}:
                values.append(fmt_int(value))
            else:
                values.append(str(value).replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def inventory_layer_summary(inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for layer, group in inventory.groupby("layer", sort=False):
        rows.append(
            {
                "layer": layer,
                "field_count": int(len(group)),
                "high_coverage_fields_n": int((group["non_missing_rate"] >= 0.8).sum()),
                "medium_coverage_fields_n": int(((group["non_missing_rate"] >= 0.2) & (group["non_missing_rate"] < 0.8)).sum()),
                "low_coverage_fields_n": int((group["non_missing_rate"] < 0.2).sum()),
                "known_candidate_fields_n": int(group["is_known_candidate_field"].sum()),
            }
        )
    return pd.DataFrame(rows)


def input_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "layer": layer,
                "source_table": INPUT_TABLES[layer]["source_table"],
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "tthm_label_available_n": int(first_existing_mask(df, INPUT_TABLES[layer]["tthm_label_columns"]).sum()),
                "haa5_label_available_n": int(first_existing_mask(df, INPUT_TABLES[layer]["haa5_label_columns"]).sum()),
            }
            for layer, df in tables.items()
        ]
    )


def top_alignment(alignment: pd.DataFrame, layer: str, label: str, limit: int = 8) -> pd.DataFrame:
    rate_col = f"field_and_{label}_label_rate"
    n_col = f"field_and_{label}_label_n"
    cols = ["layer", "field_name", "candidate_pathway_guess", "non_missing_rate", n_col, rate_col]
    return (
        alignment.loc[(alignment["layer"] == layer) & (alignment[n_col] > 0), cols]
        .sort_values([rate_col, n_col, "field_name"], ascending=[False, False, True])
        .head(limit)
    )


def write_report(
    inventory: pd.DataFrame,
    alignment: pd.DataFrame,
    internal_summary: pd.DataFrame,
    complete_summary: pd.DataFrame,
    layer_summary: pd.DataFrame,
    inputs: pd.DataFrame,
) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    pws_internal = internal_summary.loc[internal_summary["layer"] == "pws_year"]
    facility_internal = internal_summary.loc[internal_summary["layer"] == "facility_month"]
    pws_complete = complete_summary.loc[complete_summary["layer"] == "pws_year"]
    facility_complete = complete_summary.loc[complete_summary["layer"] == "facility_month"]

    report = [
        "# V5.6 候选通路字段盘点与覆盖审计执行报告",
        "",
        f"更新时间：{now_text()}（Asia/Hong_Kong）",
        "",
        "## 1. 本轮任务定位",
        "",
        "本轮 `V5.6` 是数据认识补全和候选通路字段审计，不是正式建模，也不是最终主筛查特征组冻结。本轮只回答当前派生主表中有哪些字段、字段覆盖率如何、字段与 `TTHM/HAA5` 标签能否对齐、候选通路内部覆盖结构如何，以及 complete-case / partial-case 样本基础是否足以支撑后续准入测试。",
        "",
        "本轮没有训练树模型、boosting 模型、超参数搜索模型或投票模型；原始 SYR4 数据未被原位修改。",
        "",
        "## 2. 输入数据说明",
        "",
        md_table(inputs, ["layer", "source_table", "rows", "columns", "tthm_label_available_n", "haa5_label_available_n"]),
        "",
        "`V4_pws_year_ml_ready.csv` 只作为 V4 主线字段对照表使用。该表当前没有 `HAA5` 标签，因此其 HAA5 对齐结果不用于判断 HAA5 可训练性。",
        "",
        "## 3. 全字段 inventory 总结",
        "",
        md_table(layer_summary, ["layer", "field_count", "high_coverage_fields_n", "medium_coverage_fields_n", "low_coverage_fields_n", "known_candidate_fields_n"]),
        "",
        "高覆盖字段按非缺失率 `>=80%` 统计，中覆盖字段为 `20%-80%`，低覆盖字段为 `<20%`。这些只是数据完整性口径，不代表字段一定可入模。全字段明细见本地 `V5_6_all_field_inventory.csv`。",
        "",
        "## 4. 候选通路字段展开",
        "",
        "本轮按 V5.5 的候选通路框架继续展开，并额外盘点结果谱系/解释候选通路与合规/纠正行动响应候选通路。字段展开明细见本地 `V5_6_candidate_pathway_field_map.csv`。",
        "",
        "第三层 `PWS-year` 通路覆盖摘要：",
        "",
        md_table(pws_internal, ["layer", "pathway_name", "fields_existing_n", "any_field_non_missing_n", "any_field_non_missing_rate", "tthm_label_overlap_n", "tthm_label_overlap_rate", "haa5_label_overlap_n", "haa5_label_overlap_rate"]),
        "",
        "第二层 `facility-month` 通路覆盖摘要：",
        "",
        md_table(facility_internal, ["layer", "pathway_name", "fields_existing_n", "any_field_non_missing_n", "any_field_non_missing_rate", "tthm_label_overlap_n", "tthm_label_overlap_rate", "haa5_label_overlap_n", "haa5_label_overlap_rate"]),
        "",
        "## 5. 字段-Y 对齐总结",
        "",
        "字段-Y 对齐表中的重叠率采用“字段非缺失且标签可定义的行数 / 该层级总行数”口径。它不是字段预测能力，也不是因果效应。",
        "",
        "第三层 `PWS-year` 与 `TTHM` 标签重叠较高的字段：",
        "",
        md_table(top_alignment(alignment, "pws_year", "tthm"), ["layer", "field_name", "candidate_pathway_guess", "non_missing_rate", "field_and_tthm_label_n", "field_and_tthm_label_rate"]),
        "",
        "第三层 `PWS-year` 与 `HAA5` 标签重叠较高的字段：",
        "",
        md_table(top_alignment(alignment, "pws_year", "haa5"), ["layer", "field_name", "candidate_pathway_guess", "non_missing_rate", "field_and_haa5_label_n", "field_and_haa5_label_rate"]),
        "",
        "第二层 `facility-month` 的标签对齐受同月同设施观测重叠约束明显更强，NOM、消毒剂和处理工艺字段虽有机制意义，但与同周期 `TTHM/HAA5` 的直接重叠样本明显有限。",
        "",
        "## 6. 通路内部覆盖结构",
        "",
        "通路内部覆盖结构显示：结构背景、设施复杂度和证据质量通路的“任意字段覆盖率”较高；水质机制类通路往往由少数强度字段和大量样本数、月份数、设施数类覆盖字段共同组成。后续不能把这些覆盖字段直接解释为化学机制。",
        "",
        md_table(internal_summary, ["layer", "pathway_name", "field_count", "fields_existing_n", "top_coverage_fields", "low_coverage_fields", "possible_mechanism_fields_n", "possible_monitoring_coverage_fields_n"]),
        "",
        "## 7. complete-case / partial-case 可训练性",
        "",
        "complete-case 表示通路内所有候选字段在同一行全部非缺失；partial-case 表示至少有 1、2 或 3 个候选字段非缺失。对字段数少于阈值的通路，对应 partial-case 指标标注为不适用。",
        "",
        "第三层 `PWS-year` complete/partial-case：",
        "",
        md_table(pws_complete, ["layer", "pathway_name", "candidate_field_count", "complete_case_n_all_candidate_fields", "complete_case_rate_all_candidate_fields", "partial_case_n_at_least_1", "partial_case_rate_at_least_1", "partial_case_n_at_least_2", "partial_case_rate_at_least_2", "partial_case_n_at_least_3", "partial_case_rate_at_least_3", "tthm_overlap_complete_case_n", "haa5_overlap_complete_case_n", "training_feasibility_note"]),
        "",
        "第二层 `facility-month` complete/partial-case：",
        "",
        md_table(facility_complete, ["layer", "pathway_name", "candidate_field_count", "complete_case_n_all_candidate_fields", "complete_case_rate_all_candidate_fields", "partial_case_n_at_least_1", "partial_case_rate_at_least_1", "partial_case_n_at_least_2", "partial_case_rate_at_least_2", "partial_case_n_at_least_3", "partial_case_rate_at_least_3", "tthm_overlap_complete_case_n", "haa5_overlap_complete_case_n", "training_feasibility_note"]),
        "",
        "当前没有正式 train / validation / test split 审计。本轮输出的是未切分总体审计；split 口径下的正负样本基础应在下一轮模型准入测试或特征冻结前补做。",
        "",
        "## 8. 当前能确定的结论",
        "",
        "- `PWS-year` 结构背景通路和设施复杂度通路具备较好的数据覆盖基础，可进入后续主筛查准入测试，但仍需先验因果-语义复核。",
        "- `PWS-year` 酸碱与缓冲条件通路有中等覆盖和一定标签重叠基础，更适合可选机制证据模块或高信息子样本测试。",
        "- `NOM/有机前体物通路` 与 `消毒剂与残余消毒剂通路` 机制意义较强，但完整组合覆盖和标签重叠不足，不宜直接承担全国主筛查主力输入。",
        "- 监测覆盖度与证据质量字段覆盖稳定，但它们主要服务证据等级和可信度判断，不应解释为导致 DBP 的化学机制因素。",
        "- 结果谱系、同周期目标代理、合规/违规、纠正行动和监管响应类字段只能用于字段存在性、解释或泄露风险审计，不能作为前置预测输入。",
        "",
        "## 9. 当前不能确定的结论",
        "",
        "- 本轮不判断任何字段的最终模型准入。",
        "- 本轮不判断任何候选通路的最终因果效应。",
        "- 本轮不判断任何字段或通路是否带来稳定模型增量性能。",
        "- 本轮不冻结最终主筛查输入组。",
        "",
        "## 10. 术语解释与读法说明",
        "",
        "- 非缺失率：表示某个字段在某张表中有有效记录的比例。例如 `PWS-year` 结构背景字段几乎全覆盖，说明这些字段数据较完整；但非缺失率高只代表可用基础好，不代表一定适合作为模型输入。",
        "- 字段-Y 重叠率：表示某个字段非缺失且目标标签 `TTHM` 或 `HAA5` 同时可用的样本比例。例如消毒剂字段具有机制意义，但在第三层与 `TTHM/HAA5` 标签的重叠样本较少，因此不能直接承担广覆盖主筛查主力输入。",
        "- 通路覆盖率：本报告中的通路覆盖率主要指“任意字段覆盖率”，即通路内至少一个字段非缺失的样本比例；它不同于完整组合覆盖率。",
        "- complete-case：表示某个候选特征组合中的所有候选字段在同一行全部非缺失。如果 complete-case 样本很少，整条通路不适合直接作为完整特征组训练。",
        "- partial-case：表示某条通路中只有部分字段可用。partial-case 可以支持单字段、子组合、缺失指示、分层建模或专题审计，但不能等同于完整通路可训练。",
        "- 候选通路：当前按解释机制、监管语义和字段名称临时组织出来的字段集合，不是最终因果通路，也不是最终模型特征组。",
        "- 字段准入：指某个字段是否允许进入后续模型或解释模块。它需要综合覆盖率、字段-Y 对齐、时间顺序、泄露风险、解释语义、稳定性和增量价值，而不是只看一个指标。",
        "- 泄露风险：指字段可能直接或间接包含目标结果、同周期结果、监管响应或后验信息，使模型训练时“偷看答案”。例如 `tthm_*`、`haa5_*`、合规/违规和纠正行动字段都必须先做泄露复核。",
        "",
        "结合本轮输出，三个典型读法是：第一，结构背景和设施复杂度通路覆盖率高，但仍要判断它们是风险画像变量、工程背景变量还是机制变量；第二，NOM 通路更接近机制解释，但覆盖率和字段-Y 重叠不足，不应直接承担全国主筛查主力输入；第三，监测覆盖度、样本数、设施数和 match quality 类字段可能对风险识别有帮助，但更可能属于证据质量或监测强度变量。",
        "",
        "## 11. 后续先验因果-语义分析待复核清单",
        "",
        "- 所有 `tthm_*`、`haa5_*`、`has_tthm`、`has_haa5` 和高风险标签字段。",
        "- 所有样本数、月份数、设施数、记录数、`source_module_count`、`match_quality_tier`、`annual_match_quality_tier` 和缺失标记字段。",
        "- 所有合规、违规、纠正行动和监管响应类字段；当前主表中未发现明显字段，也应在后续原始模块审计中保留该类检查。",
        "- 所有消毒剂与残余消毒剂字段，尤其是 `free_chlorine_*`、`total_chlorine_*`、`chloramine_*`、`plant_disinfectant_concentration_mean_mg_l` 和 `plant_ct_value_mean`。",
        "- NOM 通路中的 `toc/doc/uv254/suva` 强度字段与样本数、月份数、设施数覆盖字段的拆分。",
        "- 酸碱通路中的 `ph/alkalinity` 强度字段与样本数、月份数、设施数覆盖字段的拆分。",
        "",
        "## 12. 下一步建议",
        "",
        "下一步应先进入先验因果-语义分析，围绕泄露风险、时间顺序、应用可得性、机制强度字段与监测覆盖字段的拆分进行复核。完成该复核后，再进入主筛查特征组冻结和 split 口径下的模型准入测试。",
        "",
        "## 13. 结论提醒",
        "",
        "本轮的“可用”“覆盖较好”“对齐较好”只代表数据审计意义上的可用基础，不等于已经证明该字段有预测价值、因果作用或稳定模型增量。",
    ]

    (DOCS_DIR / "V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Report.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    decision = [
        "# V5.6 通路数据可用性决策摘要",
        "",
        f"更新时间：{now_text()}（Asia/Hong_Kong）",
        "",
        "## 1. 决策定位",
        "",
        "本摘要只给出数据可用性层面的下一步建议，不冻结最终模型输入，也不判断因果效应。",
        "",
        "## 2. 通路级建议",
        "",
        md_table(complete_summary, ["layer", "pathway_name", "candidate_field_count", "complete_case_n_all_candidate_fields", "complete_case_rate_all_candidate_fields", "partial_case_n_at_least_1", "partial_case_rate_at_least_1", "tthm_overlap_complete_case_n", "haa5_overlap_complete_case_n", "training_feasibility_note"]),
        "",
        "## 3. 建议",
        "",
        "- 主筛查准入测试优先从 `PWS-year` 结构背景通路和设施复杂度通路开始。",
        "- 处理工艺通路可以保留为可审计工程背景候选，但需要先复核缺失语义。",
        "- 酸碱与缓冲条件通路优先进入可选机制证据模块。",
        "- NOM 与消毒剂相关通路暂按专题审计或高信息子样本候选处理。",
        "- 证据质量通路服务证据等级和可信度，不应作为化学机制解释。",
    ]
    (DOCS_DIR / "V5_6_Pathway_Data_Availability_Decision_Summary.md").write_text(
        "\n".join(decision) + "\n",
        encoding="utf-8",
    )

    todo = [
        "# V5.6 后续先验因果-语义复核清单",
        "",
        f"更新时间：{now_text()}（Asia/Hong_Kong）",
        "",
        "## 1. 必须复核的字段类型",
        "",
        "- `TTHM/HAA5` 结果字段、目标代理字段、高风险标签字段和同周期结果谱系字段。",
        "- 样本数、月份数、设施数、记录数、覆盖度、`source_module_count`、`match_quality` 和缺失标记字段。",
        "- 合规、违规、纠正行动、监管响应类字段；即使当前 V3/V4 主表未显式出现，也应在后续原始模块审计中保留检查。",
        "- 消毒剂与残余消毒剂字段，重点复核时间顺序、同周期运行状态接近性和预测时可获得性。",
        "- NOM 与酸碱通路中机制强度字段和监测覆盖字段的拆分。",
        "",
        "## 2. 建议复核顺序",
        "",
        "1. 先排除或隔离所有结果字段、标签字段、合规/纠正行动字段。",
        "2. 再将样本数、月份数、设施数、match quality 类字段归入证据质量或覆盖强度层。",
        "3. 最后复核水质机制强度字段的时间顺序、应用可得性和是否适合进入主筛查或机制模块。",
        "",
        "## 3. 预期产出",
        "",
        "- 一份字段准入/暂缓/仅证据质量/仅解释的决策表。",
        "- 一份主筛查特征组冻结候选清单。",
        "- 一份可选机制证据模块候选清单。",
    ]
    (DOCS_DIR / "V5_6_Causal_Semantic_Review_Todo_List.md").write_text(
        "\n".join(todo) + "\n",
        encoding="utf-8",
    )


def write_outputs(
    tables: dict[str, pd.DataFrame],
    inventory: pd.DataFrame,
    alignment: pd.DataFrame,
    field_map: pd.DataFrame,
    internal_summary: pd.DataFrame,
    complete_summary: pd.DataFrame,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(OUTPUT_DIR / "V5_6_all_field_inventory.csv", index=False, encoding="utf-8-sig")
    alignment.to_csv(OUTPUT_DIR / "V5_6_field_label_alignment.csv", index=False, encoding="utf-8-sig")
    field_map.to_csv(OUTPUT_DIR / "V5_6_candidate_pathway_field_map.csv", index=False, encoding="utf-8-sig")
    internal_summary.to_csv(
        OUTPUT_DIR / "V5_6_pathway_internal_coverage_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )
    complete_summary.to_csv(
        OUTPUT_DIR / "V5_6_pathway_complete_partial_case_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    layer_summary = inventory_layer_summary(inventory)
    inputs = input_summary(tables)
    payload = {
        "generated_at": now_text(),
        "task": "V5.6 Candidate Pathway Field Inventory And Coverage Audit",
        "input_tables": inputs.to_dict(orient="records"),
        "output_dir": str(OUTPUT_DIR),
        "docs_dir": str(DOCS_DIR),
        "layer_field_inventory_summary": layer_summary.to_dict(orient="records"),
        "pathway_internal_coverage_summary": internal_summary.to_dict(orient="records"),
        "pathway_complete_partial_case_summary": complete_summary.to_dict(orient="records"),
        "notes": [
            "本轮未训练任何模型。",
            "本轮标签重叠率仅表示字段非缺失且目标标签可定义的审计重叠，不代表预测能力。",
            "V4_pws_year_ml_ready.csv 仅作为 TTHM 主线字段对照表；不用于 HAA5 可训练性判断。",
        ],
    }
    (OUTPUT_DIR / "V5_6_candidate_pathway_field_inventory_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report(inventory, alignment, internal_summary, complete_summary, layer_summary, inputs)


def main() -> None:
    tables = {layer: read_table(config["path"]) for layer, config in INPUT_TABLES.items()}
    inventory = build_inventory(tables)
    alignment = build_field_label_alignment(tables)
    field_map = build_pathway_field_map(tables)
    internal_summary = build_internal_coverage_summary(tables, field_map)
    complete_summary = build_complete_partial_summary(tables, field_map)
    write_outputs(tables, inventory, alignment, field_map, internal_summary, complete_summary)

    print("Completed V5.6 candidate pathway field inventory and coverage audit")
    for layer, df in tables.items():
        print(f"{layer}: rows={len(df):,}, columns={len(df.columns):,}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Docs dir: {DOCS_DIR}")


if __name__ == "__main__":
    main()
