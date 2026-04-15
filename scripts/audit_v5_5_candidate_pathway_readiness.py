from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
V3_DIR = PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build"
FACILITY_MONTH_PATH = V3_DIR / "V3_facility_month_master.csv"
PWS_YEAR_PATH = V3_DIR / "V3_pws_year_master.csv"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V5_Chapter1_Part1_Facility_Month_Module" / "V5_5"
TZ = ZoneInfo("Asia/Hong_Kong")

TTHM_FACILITY_LABEL = "is_tthm_high_risk_month"
HAA5_FACILITY_LABEL = "is_haa5_high_risk_month"
TTHM_YEAR_LABEL = "v5_5_tthm_high_risk_audit_label"
HAA5_YEAR_LABEL = "v5_5_haa5_high_risk_audit_label"
TTHM_YEAR_VALUE = "tthm_sample_weighted_mean_ug_l"
HAA5_YEAR_VALUE = "haa5_sample_weighted_mean_ug_l"

ROLE_MAIN = "main_screening_candidate"
ROLE_MECHANISM = "optional_mechanistic_evidence_candidate"
ROLE_QUALITY = "evidence_quality_module_candidate"
ROLE_EXPLANATION = "outcome_profile_or_explanation_only"
ROLE_EXPLORATORY = "exploratory_future_module"
ROLE_DEFER = "defer_or_exclude"


@dataclass(frozen=True)
class PathwaySpec:
    name: str
    candidate_role: str
    application_availability_judgement: str
    leakage_risk_level: str
    leakage_risk_note: str
    mechanism_or_regulatory_interpretation: str
    next_step_recommendation: str
    exact_fields: tuple[str, ...] = ()
    prefixes: tuple[str, ...] = ()


PATHWAYS = [
    PathwaySpec(
        name="结构背景通路",
        candidate_role=ROLE_MAIN,
        application_availability_judgement="high_prior_availability：系统类型、水源类型、服务人口和州别通常可在预测前获得。",
        leakage_risk_level="low",
        leakage_risk_note="不包含同周期 DBP 结果字段，主要为系统背景与规模信息。",
        mechanism_or_regulatory_interpretation="反映系统规模、水源类型、州别和基础监管背景，适合承担广覆盖主筛查输入。",
        next_step_recommendation="enter_model_admission_test",
        exact_fields=(
            "system_type",
            "source_water_type",
            "retail_population_served",
            "adjusted_total_population_served",
            "state_code",
        ),
    ),
    PathwaySpec(
        name="处理工艺通路",
        candidate_role=ROLE_MAIN,
        application_availability_judgement="medium_to_high_prior_availability：处理工艺摘要来自系统/设施背景表，理论上可前置获得，但部分字段覆盖取决于 treatment 表记录完整性。",
        leakage_risk_level="low",
        leakage_risk_note="不包含同周期 DBP 结果字段；工艺记录可作为前置结构信息，但需保留缺失语义。",
        mechanism_or_regulatory_interpretation="反映消毒、过滤、吸附、氧化和工艺记录丰富度，可作为主筛查或机制增强候选。",
        next_step_recommendation="enter_model_admission_test",
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
        ),
    ),
    PathwaySpec(
        name="设施复杂度通路",
        candidate_role=ROLE_MAIN,
        application_availability_judgement="medium_prior_availability：设施类型、设施数量、供水设施数量和 flow 记录多来自设施/处理背景，可前置使用但覆盖不均。",
        leakage_risk_level="low",
        leakage_risk_note="不包含 DBP 结果字段；主要是设施结构复杂度代理。",
        mechanism_or_regulatory_interpretation="反映系统内部设施构成与供水复杂度，适合与结构背景合并为广覆盖筛查输入。",
        next_step_recommendation="enter_model_admission_test",
        exact_fields=(
            "water_facility_type",
            "n_facilities_in_master",
            "n_supplying_facilities",
            "flow_record_count",
            "water_facility_type_list",
        ),
    ),
    PathwaySpec(
        name="NOM/有机前体物通路",
        candidate_role=ROLE_MECHANISM,
        application_availability_judgement="low_to_medium_prior_availability：TOC 覆盖相对可用，DOC/UV254/SUVA 多为高信息子样本或专题变量。",
        leakage_risk_level="low",
        leakage_risk_note="不包含同周期 DBP 结果字段；属于水质机制变量，但不能替代结果标签。",
        mechanism_or_regulatory_interpretation="反映有机前体物和芳香性等 DBP 生成潜势相关信息，机制意义强但覆盖率通常限制其主筛查用途。",
        next_step_recommendation="audit_more_before_modeling",
        prefixes=("toc_", "doc_", "uv254_", "suva_"),
    ),
    PathwaySpec(
        name="酸碱与缓冲条件通路",
        candidate_role=ROLE_MECHANISM,
        application_availability_judgement="medium_prior_availability：pH 和 alkalinity 是常见水质变量，可在高信息样本中前置获得。",
        leakage_risk_level="low",
        leakage_risk_note="不包含同周期 DBP 结果字段；属于机制支撑变量。",
        mechanism_or_regulatory_interpretation="反映反应条件与缓冲环境，适合作为可选机制证据模块。",
        next_step_recommendation="enter_model_admission_test",
        prefixes=("ph_", "alkalinity_"),
    ),
    PathwaySpec(
        name="消毒剂与残余消毒剂通路",
        candidate_role=ROLE_MECHANISM,
        application_availability_judgement="low_to_medium_prior_availability：残余消毒剂覆盖不均，厂内消毒剂浓度与 CT 值更依赖处理记录完整性。",
        leakage_risk_level="medium",
        leakage_risk_note="不属于同目标 DBP 结果，但可能与同周期运行状态接近；正式建模前需进一步确认时间顺序。",
        mechanism_or_regulatory_interpretation="反映消毒剂暴露和运行条件，机制意义强，但覆盖率、时序和真实可得性决定其只能作为可选模块候选。",
        next_step_recommendation="audit_more_before_modeling",
        exact_fields=("plant_disinfectant_concentration_mean_mg_l", "plant_ct_value_mean"),
        prefixes=("free_chlorine_", "total_chlorine_", "chloramine_"),
    ),
    PathwaySpec(
        name="监测覆盖度与证据质量通路",
        candidate_role=ROLE_QUALITY,
        application_availability_judgement="high_internal_availability：这些字段可由已观测数据完整性派生，适合用于证据等级和可信度判断。",
        leakage_risk_level="medium",
        leakage_risk_note="覆盖度变量反映监测强度和数据完整性，不能解释为 DBP 化学生成机制；若直接入预测需避免用结果可得性代理目标。",
        mechanism_or_regulatory_interpretation="用于证据质量、适用范围和完整性分级，不应被写成导致 DBP 高风险的化学机制因素。",
        next_step_recommendation="use_for_evidence_quality_only",
        exact_fields=(
            "n_result_vars_available",
            "n_outcome_vars_available",
            "n_core_vars_available",
            "n_extended_vars_available",
            "n_mechanism_vars_available",
            "source_module_count",
            "match_quality_tier",
            "annual_match_quality_tier",
            "months_with_1plus_core_vars",
            "months_with_2plus_core_vars",
            "months_with_3plus_core_vars",
        ),
    ),
]

FUTURE_MODULES = [
    {
        "module_name": "单项 THM 与单项 HAA 组分",
        "recommended_framework_role": ROLE_EXPLANATION,
        "next_step_recommendation": "use_for_explanation_only",
        "reason": "同周期同目标家族组分存在直接目标泄露风险，不得作为同周期 TTHM/HAA5 预测输入。",
    },
    {
        "module_name": "bromate/chlorite",
        "recommended_framework_role": ROLE_EXPLANATION,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "更适合作为结果谱系或副产物共现解释模块，需先做字段存在性、覆盖率和时序审计。",
    },
    {
        "module_name": "微生物相关模块",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "可能反映消毒需求或微生物控制背景，但尚未完成字段、覆盖率和泄露边界审计。",
    },
    {
        "module_name": "ADWR compliance",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "合规信息可能是事后监管响应或结果代理，时序未明确前不得作为前置预测输入。",
    },
    {
        "module_name": "corrective actions",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "纠正行动通常具有事后响应属性，需先审计时间顺序和目标泄露风险。",
    },
    {
        "module_name": "cryptobinning",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "专题属性强，需先限定为字段存在性与覆盖率盘点。",
    },
    {
        "module_name": "phasechem",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "广义水化学背景可作为后续专题候选，本轮不重新整合原始模块。",
    },
    {
        "module_name": "rads",
        "recommended_framework_role": ROLE_EXPLORATORY,
        "next_step_recommendation": "defer_to_future_raw_module_audit",
        "reason": "与 DBP 机制关系不直接，本轮只列为后续原始模块覆盖率审计候选。",
    },
]


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def read_csv_header(path: Path) -> list[str]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    return list(pd.read_csv(path, nrows=0, encoding="utf-8-sig").columns)


def resolve_fields(columns: list[str], spec: PathwaySpec) -> list[str]:
    resolved: list[str] = []
    for field in spec.exact_fields:
        if field not in resolved:
            resolved.append(field)
    for prefix in spec.prefixes:
        for column in columns:
            if column.startswith(prefix) and column not in resolved:
                resolved.append(column)
    return resolved


def required_facility_columns() -> list[str]:
    header = read_csv_header(FACILITY_MONTH_PATH)
    required = {
        "pwsid",
        "water_facility_id",
        "year",
        "month",
        TTHM_FACILITY_LABEL,
        HAA5_FACILITY_LABEL,
        "tthm_mean_ug_l",
        "haa5_mean_ug_l",
        "tthm_n_samples",
        "haa5_n_samples",
    }
    for spec in PATHWAYS:
        required.update(resolve_fields(header, spec))
    return sorted(column for column in required if column in header)


def read_facility_month() -> pd.DataFrame:
    if not FACILITY_MONTH_PATH.exists() or FACILITY_MONTH_PATH.stat().st_size == 0:
        raise FileNotFoundError(f"未找到可用的第二层主表：{FACILITY_MONTH_PATH}")
    return pd.read_csv(
        FACILITY_MONTH_PATH,
        encoding="utf-8-sig",
        usecols=required_facility_columns(),
        low_memory=False,
    )


def first_non_missing(series: pd.Series) -> object:
    values = series.dropna()
    return values.iloc[0] if not values.empty else pd.NA


def unique_join(series: pd.Series) -> object:
    values = sorted({str(value) for value in series.dropna() if str(value).strip()})
    return "; ".join(values) if values else pd.NA


def weighted_mean(group: pd.DataFrame, value_column: str, weight_column: str) -> float | pd.NA:
    valid = group[[value_column, weight_column]].dropna()
    if valid.empty:
        return pd.NA
    weight_sum = valid[weight_column].sum()
    if weight_sum and weight_sum > 0:
        return float((valid[value_column] * valid[weight_column]).sum() / weight_sum)
    return float(valid[value_column].mean())


def weighted_mean_by_group(
    df: pd.DataFrame,
    group_keys: list[str],
    value_column: str,
    weight_column: str,
    output_column: str,
) -> pd.DataFrame:
    valid = df.loc[df[value_column].notna(), group_keys + [value_column, weight_column]].copy()
    if valid.empty:
        return pd.DataFrame(columns=group_keys + [output_column])
    weights = valid[weight_column].fillna(1)
    weights = weights.mask(weights <= 0, 1)
    valid["_weighted_value"] = valid[value_column] * weights
    valid["_weight"] = weights
    grouped = valid.groupby(group_keys, dropna=False, sort=False)[["_weighted_value", "_weight"]].sum()
    grouped[output_column] = grouped["_weighted_value"] / grouped["_weight"]
    return grouped[[output_column]].reset_index()


def build_pws_year_from_facility_month(facility_df: pd.DataFrame) -> pd.DataFrame:
    group_keys = ["pwsid", "year"]
    grouped = facility_df.groupby(group_keys, dropna=False, sort=False)

    all_candidate_fields = set()
    for spec in PATHWAYS:
        all_candidate_fields.update(resolve_fields(list(facility_df.columns), spec))

    base_df = grouped.size().rename("n_facility_month_rows").reset_index()

    first_fields = [
        "state_code",
        "system_type",
        "source_water_type",
        "retail_population_served",
        "adjusted_total_population_served",
        "has_disinfection_process",
        "has_filtration_process",
        "has_adsorption_process",
        "has_oxidation_process",
        "has_chloramination_process",
        "has_hypochlorination_process",
        "filter_type_list",
        "match_quality_tier",
        "plant_disinfectant_concentration_mean_mg_l",
        "plant_ct_value_mean",
        "water_facility_type",
    ]
    sum_fields = [
        "treatment_process_record_count",
        "n_treatment_process_names",
        "n_treatment_objective_names",
        "flow_record_count",
        "n_supplying_facilities",
        "n_result_vars_available",
        "n_core_vars_available",
        "n_extended_vars_available",
        "n_mechanism_vars_available",
        "source_module_count",
    ]

    first_existing = [field for field in first_fields if field in facility_df.columns and field in all_candidate_fields]
    if first_existing:
        base_df = base_df.merge(grouped[first_existing].first().reset_index(), on=group_keys, how="left")

    sum_existing = [field for field in sum_fields if field in facility_df.columns and field in all_candidate_fields]
    if sum_existing:
        max_df = grouped[sum_existing].max().reset_index()
        base_df = base_df.merge(max_df, on=group_keys, how="left")

    if "water_facility_id" in facility_df.columns:
        facility_count_df = grouped["water_facility_id"].nunique(dropna=True).rename("n_facilities_in_master").reset_index()
        base_df = base_df.merge(facility_count_df, on=group_keys, how="left")

    if "water_facility_type" in facility_df.columns:
        facility_type_list_df = (
            grouped["water_facility_type"]
            .agg(unique_join)
            .rename("water_facility_type_list")
            .reset_index()
        )
        base_df = base_df.merge(facility_type_list_df, on=group_keys, how="left")

    sample_columns = [column for column in facility_df.columns if column.endswith("_n_samples")]
    for sample_column in sample_columns:
        output_column = sample_column.replace("_n_samples", "_sample_count")
        sample_df = grouped[sample_column].sum(min_count=1).rename(output_column).reset_index()
        base_df = base_df.merge(sample_df, on=group_keys, how="left")

    for mean_column in [column for column in facility_df.columns if "_mean" in column]:
        prefix, suffix = mean_column.split("_mean", 1)
        sample_column = f"{prefix}_n_samples"
        output_column = f"{prefix}_sample_weighted_mean{suffix}"
        if sample_column in facility_df.columns:
            mean_df = weighted_mean_by_group(facility_df, group_keys, mean_column, sample_column, output_column)
        else:
            mean_df = grouped[mean_column].mean().rename(output_column).reset_index()
        base_df = base_df.merge(mean_df, on=group_keys, how="left")

    if TTHM_YEAR_VALUE in base_df.columns:
        base_df[TTHM_YEAR_LABEL] = pd.Series(pd.NA, index=base_df.index, dtype="Int64")
        mask = base_df[TTHM_YEAR_VALUE].notna()
        base_df.loc[mask, TTHM_YEAR_LABEL] = (base_df.loc[mask, TTHM_YEAR_VALUE] >= 80.0).astype("Int64")
    if HAA5_YEAR_VALUE in base_df.columns:
        base_df[HAA5_YEAR_LABEL] = pd.Series(pd.NA, index=base_df.index, dtype="Int64")
        mask = base_df[HAA5_YEAR_VALUE].notna()
        base_df.loc[mask, HAA5_YEAR_LABEL] = (base_df.loc[mask, HAA5_YEAR_VALUE] >= 60.0).astype("Int64")

    if "n_core_vars_available" in facility_df.columns:
        for threshold in [1, 2, 3]:
            month_df = (
                facility_df.assign(_core_threshold=(facility_df["n_core_vars_available"] >= threshold).astype(int))
                .groupby(group_keys, dropna=False, sort=False)["_core_threshold"]
                .sum()
                .rename(f"months_with_{threshold}plus_core_vars")
                .reset_index()
            )
            base_df = base_df.merge(month_df, on=group_keys, how="left")
        base_df["annual_match_quality_tier"] = pd.NA
        base_df.loc[base_df["n_core_vars_available"] >= 3, "annual_match_quality_tier"] = "3plus_core_vars"
        base_df.loc[
            (base_df["n_core_vars_available"] >= 2) & (base_df["n_core_vars_available"] < 3),
            "annual_match_quality_tier",
        ] = "2plus_core_vars"
        base_df.loc[
            (base_df["n_core_vars_available"] >= 1) & (base_df["n_core_vars_available"] < 2),
            "annual_match_quality_tier",
        ] = "1plus_core_vars"

    return base_df


def read_or_build_pws_year(facility_df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    if PWS_YEAR_PATH.exists() and PWS_YEAR_PATH.stat().st_size > 0:
        return pd.read_csv(PWS_YEAR_PATH, encoding="utf-8-sig", low_memory=False), "V3_pws_year_master.csv"
    return build_pws_year_from_facility_month(facility_df), "derived_from_V3_facility_month_master_due_to_empty_V3_pws_year_master"


def infer_field_type(series: pd.Series | None) -> str:
    if series is None:
        return "missing_field"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    return "categorical_or_text"


def build_field_coverage(layer: str, df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    total_n = len(df)
    columns = list(df.columns)
    for spec in PATHWAYS:
        for field in resolve_fields(columns, spec):
            exists = field in df.columns
            series = df[field] if exists else None
            non_missing_n = int(series.notna().sum()) if series is not None else 0
            rows.append(
                {
                    "layer": layer,
                    "pathway_name": spec.name,
                    "field_name": field,
                    "field_exists": bool(exists),
                    "non_missing_n": non_missing_n,
                    "total_n": total_n,
                    "non_missing_rate": non_missing_n / total_n if total_n else 0.0,
                    "field_type": infer_field_type(series),
                    "candidate_role": spec.candidate_role,
                    "leakage_risk_note": spec.leakage_risk_note,
                    "remarks": build_field_remark(layer, field, exists),
                }
            )
    return pd.DataFrame(rows)


def build_field_remark(layer: str, field: str, exists: bool) -> str:
    if not exists:
        return "字段未出现在当前层级审计表中。"
    if field.startswith(("tthm_", "haa5_")) or field in {TTHM_YEAR_LABEL, HAA5_YEAR_LABEL}:
        return "该字段属于结果或审计标签，不应作为同周期预测输入。"
    if "match_quality" in field or "available" in field or field.startswith("months_with_"):
        return "证据质量/覆盖度字段，仅用于完整性和可信度判断。"
    if layer == "pws_year" and field in {"n_facilities_in_master", "water_facility_type_list"}:
        return "第三层审计中该字段可由第二层按 pwsid-year 上卷得到。"
    return "可作为本轮候选通路字段审计。"


def label_mask(df: pd.DataFrame, label_column: str, fallback_value_column: str, threshold: float) -> pd.Series:
    if fallback_value_column in df.columns:
        return df[fallback_value_column].notna()
    if label_column in df.columns:
        return df[label_column].notna()
    return pd.Series(False, index=df.index)


def build_pathway_summary(layer: str, df: pd.DataFrame) -> pd.DataFrame:
    total_n = len(df)
    rows: list[dict[str, object]] = []

    if layer == "facility_month":
        tthm_mask = label_mask(df, TTHM_FACILITY_LABEL, "tthm_mean_ug_l", 80.0)
        haa5_mask = label_mask(df, HAA5_FACILITY_LABEL, "haa5_mean_ug_l", 60.0)
    else:
        tthm_mask = label_mask(df, TTHM_YEAR_LABEL, TTHM_YEAR_VALUE, 80.0)
        haa5_mask = label_mask(df, HAA5_YEAR_LABEL, HAA5_YEAR_VALUE, 60.0)

    columns = list(df.columns)
    for spec in PATHWAYS:
        existing_fields = [field for field in resolve_fields(columns, spec) if field in df.columns]
        if existing_fields:
            any_mask = df[existing_fields].notna().any(axis=1)
        else:
            any_mask = pd.Series(False, index=df.index)
        any_n = int(any_mask.sum())
        tthm_overlap = int((any_mask & tthm_mask).sum())
        haa5_overlap = int((any_mask & haa5_mask).sum())
        rows.append(
            {
                "layer": layer,
                "pathway_name": spec.name,
                "candidate_fields": ", ".join(existing_fields),
                "fields_existing_n": len(existing_fields),
                "any_field_non_missing_n": any_n,
                "total_n": total_n,
                "any_field_non_missing_rate": any_n / total_n if total_n else 0.0,
                "tthm_label_overlap_n": tthm_overlap,
                "tthm_label_overlap_rate": tthm_overlap / total_n if total_n else 0.0,
                "haa5_label_overlap_n": haa5_overlap,
                "haa5_label_overlap_rate": haa5_overlap / total_n if total_n else 0.0,
                "application_availability_judgement": spec.application_availability_judgement,
                "leakage_risk_level": spec.leakage_risk_level,
                "mechanism_or_regulatory_interpretation": spec.mechanism_or_regulatory_interpretation,
                "recommended_framework_role": decide_role(spec, layer, any_n / total_n if total_n else 0.0),
                "next_step_recommendation": decide_next_step(spec, layer, any_n / total_n if total_n else 0.0),
            }
        )
    return pd.DataFrame(rows)


def decide_role(spec: PathwaySpec, layer: str, coverage_rate: float) -> str:
    if spec.candidate_role == ROLE_QUALITY:
        return ROLE_QUALITY
    if spec.name in {"结构背景通路", "处理工艺通路", "设施复杂度通路"}:
        return ROLE_MAIN if coverage_rate >= 0.3 or layer == "pws_year" else ROLE_MECHANISM
    if spec.name == "酸碱与缓冲条件通路":
        return ROLE_MECHANISM if coverage_rate >= 0.05 else ROLE_EXPLORATORY
    if spec.name in {"NOM/有机前体物通路", "消毒剂与残余消毒剂通路"}:
        return ROLE_MECHANISM if coverage_rate >= 0.05 else ROLE_EXPLORATORY
    return spec.candidate_role


def decide_next_step(spec: PathwaySpec, layer: str, coverage_rate: float) -> str:
    if spec.candidate_role == ROLE_QUALITY:
        return "use_for_evidence_quality_only"
    if spec.name in {"结构背景通路", "处理工艺通路", "设施复杂度通路"}:
        return "enter_model_admission_test" if coverage_rate >= 0.3 else "audit_more_before_modeling"
    if spec.name == "酸碱与缓冲条件通路":
        return "enter_model_admission_test" if coverage_rate >= 0.05 else "audit_more_before_modeling"
    if spec.name in {"NOM/有机前体物通路", "消毒剂与残余消毒剂通路"}:
        return "audit_more_before_modeling" if coverage_rate >= 0.05 else "defer_to_future_raw_module_audit"
    return spec.next_step_recommendation


def build_future_module_table() -> pd.DataFrame:
    return pd.DataFrame(FUTURE_MODULES)


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_outputs(
    field_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    future_df: pd.DataFrame,
    input_notes: dict[str, object],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    field_df.to_csv(OUTPUT_DIR / "V5_5_candidate_field_coverage.csv", index=False, encoding="utf-8-sig")
    summary_df.to_csv(
        OUTPUT_DIR / "V5_5_candidate_pathway_readiness_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )
    future_df.to_csv(OUTPUT_DIR / "V5_5_future_raw_module_boundary_notes.csv", index=False, encoding="utf-8-sig")

    summary_records = summary_df.to_dict(orient="records")
    payload = {
        "generated_at": now_text(),
        "input_notes": input_notes,
        "output_dir": str(OUTPUT_DIR),
        "pathway_summary": summary_records,
        "future_raw_module_boundary_notes": future_df.to_dict(orient="records"),
    }
    (OUTPUT_DIR / "V5_5_candidate_pathway_readiness_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    facility_df = read_facility_month()
    pws_year_df, pws_year_source = read_or_build_pws_year(facility_df)

    facility_field_df = build_field_coverage("facility_month", facility_df)
    pws_year_field_df = build_field_coverage("pws_year", pws_year_df)
    field_df = pd.concat([pws_year_field_df, facility_field_df], ignore_index=True)

    facility_summary_df = build_pathway_summary("facility_month", facility_df)
    pws_year_summary_df = build_pathway_summary("pws_year", pws_year_df)
    summary_df = pd.concat([pws_year_summary_df, facility_summary_df], ignore_index=True)

    future_df = build_future_module_table()
    input_notes = {
        "facility_month_input": str(FACILITY_MONTH_PATH),
        "facility_month_rows": int(len(facility_df)),
        "pws_year_requested_input": str(PWS_YEAR_PATH),
        "pws_year_input_status": pws_year_source,
        "pws_year_rows": int(len(pws_year_df)),
        "pws_year_label_note": "若第三层原始标签列不可用，则 V5.5 仅为覆盖率审计临时按 TTHM>=80 ug/L、HAA5>=60 ug/L 定义高风险标签，不作为新增预测特征。",
    }

    write_outputs(field_df, summary_df, future_df, input_notes)

    print("Completed V5.5 candidate pathway readiness audit")
    print(f"Facility-month rows: {len(facility_df):,}")
    print(f"PWS-year rows: {len(pws_year_df):,}")
    print(f"PWS-year input status: {pws_year_source}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
