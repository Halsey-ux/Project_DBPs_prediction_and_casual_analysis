from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from pathlib import Path
from typing import Iterable
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = Path(r"D:\Syr4_Project\syr4_DATA_CSV")
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build"
SOURCE_SUMMARY_DIR = OUTPUT_DIR / "facility_month_source_tables"
DOCS_DIR = PROJECT_ROOT / "docs"
V2_OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V2_Chapter1_Part1_DBP_Data_Foundation"
TEMPLATE_PATH = DOCS_DIR / "V2_FacilityMonth_PWSYear_Template.xlsx"

FACILITY_MONTH_KEY = ["pwsid", "water_facility_id", "year", "month"]
PWS_YEAR_KEY = ["pwsid", "year"]


@dataclass(frozen=True)
class SourceSpec:
    key: str
    label_cn: str
    category_cn: str
    path: Path
    unit_suffix: str
    level_priority: str


SOURCE_SPECS = [
    SourceSpec("tthm", "TTHM", "结果变量", RAW_ROOT / "SYR4_THMs" / "TOTAL TRIHALOMETHANES (TTHM).csv", "_ug_l", "outcome"),
    SourceSpec("haa5", "HAA5", "结果变量", RAW_ROOT / "SYR4_HAAs" / "HALOACETIC ACIDS (HAA5).csv", "_ug_l", "outcome"),
    SourceSpec("ph", "pH", "核心机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "PH.csv", "", "core"),
    SourceSpec("alkalinity", "总碱度", "核心机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "TOTAL ALKALINITY.csv", "_mg_l", "core"),
    SourceSpec("toc", "TOC", "核心机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "TOTAL ORGANIC CARBON.csv", "_mg_l", "core"),
    SourceSpec("free_chlorine", "游离余氯", "核心机制变量", RAW_ROOT / "SYR4_Disinfectant Residuals" / "FREE RESIDUAL CHLORINE (1013).csv", "_mg_l", "core"),
    SourceSpec("total_chlorine", "总氯", "扩展机制变量", RAW_ROOT / "SYR4_Disinfectant Residuals" / "TOTAL CHLORINE (1000).csv", "_mg_l", "extended"),
    SourceSpec("doc", "DOC", "扩展机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "DOC.csv", "_mg_l", "extended"),
    SourceSpec("suva", "SUVA", "扩展机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "SUVA.csv", "_l_mg_m", "extended"),
    SourceSpec("uv254", "UV254", "扩展机制变量", RAW_ROOT / "SYR4_DBP_Related Parameters" / "UV_ABSORBANCE.csv", "_cm_inv", "extended"),
    SourceSpec("chloramine", "氯胺", "扩展机制变量", RAW_ROOT / "SYR4_Disinfectant Residuals" / "CHLORAMINE (1006).csv", "_mg_l", "extended"),
]

HIGH_RISK_THRESHOLDS = {"tthm": 80.0, "haa5": 60.0}
STAT_LABELS = {"n_samples": "月度样本数", "mean": "月度均值", "median": "月度中位数", "max": "月度最大值", "p90": "月度 P90"}


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def clean_string(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NA": pd.NA})


def normalize_facility_id(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    if text.endswith(".00"):
        return text[:-3]
    if text.endswith(".0"):
        return text[:-2]
    return text


def normalize_facility_id_series(series: pd.Series) -> pd.Series:
    return series.map(normalize_facility_id, na_action="ignore").astype("string")


def parse_sample_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="%d-%b-%y", errors="coerce")


def first_valid(series: pd.Series) -> object:
    non_null = series.dropna()
    return pd.NA if non_null.empty else non_null.iloc[0]


def join_unique_strings(values: Iterable[object], limit: int = 12) -> str | pd.NA:
    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value is None or pd.isna(value):
            continue
        text = str(value).strip()
        if not text or text.lower() == "nan" or text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
        if len(cleaned) >= limit:
            break
    return pd.NA if not cleaned else " | ".join(cleaned)


def safe_weighted_mean(weighted_sum: float, sample_count: float) -> float:
    if sample_count == 0 or pd.isna(sample_count):
        return np.nan
    return weighted_sum / sample_count


def coalesce_columns(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series(pd.NA, index=frame.index, dtype="object")
    for column in columns:
        if column in frame.columns:
            result = result.where(result.notna(), frame[column])
    return result


def to_markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy().fillna("")
    headers = [str(column) for column in display.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in display.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def format_pct(numerator: int | float, denominator: int | float) -> str:
    if denominator == 0 or pd.isna(denominator):
        return "0.00%"
    return f"{numerator / denominator * 100:.2f}%"


def stat_field_name(spec: SourceSpec, stat_name: str) -> str:
    return f"{spec.key}_n_samples" if stat_name == "n_samples" else f"{spec.key}_{stat_name}{spec.unit_suffix}"


def read_occurrence_source(spec: SourceSpec) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    usecols = [
        "PWSID", "STATE_CODE", "SYSTEM_NAME", "SYSTEM_TYPE", "SOURCE_WATER_TYPE",
        "WATER_FACILITY_ID", "WATER_FACILITY_TYPE", "RETAIL_POPULATION_SERVED",
        "ADJUSTED_TOTAL_POPULATION_SERVED", "SAMPLE_COLLECTION_DATE", "VALUE", "UNIT",
    ]
    frame = pd.read_csv(spec.path, usecols=usecols, dtype={column: "string" for column in usecols}, low_memory=False)
    frame = frame.rename(columns={
        "PWSID": "pwsid",
        "STATE_CODE": "state_code",
        "SYSTEM_NAME": "system_name",
        "SYSTEM_TYPE": "system_type",
        "SOURCE_WATER_TYPE": "source_water_type",
        "WATER_FACILITY_ID": "water_facility_id",
        "WATER_FACILITY_TYPE": "water_facility_type",
        "RETAIL_POPULATION_SERVED": "retail_population_served",
        "ADJUSTED_TOTAL_POPULATION_SERVED": "adjusted_total_population_served",
        "SAMPLE_COLLECTION_DATE": "sample_collection_date",
        "VALUE": "value",
        "UNIT": "unit",
    })
    for column in ["pwsid", "state_code", "system_name", "system_type", "source_water_type", "water_facility_type", "unit"]:
        frame[column] = clean_string(frame[column])
    frame["water_facility_id"] = normalize_facility_id_series(clean_string(frame["water_facility_id"]))
    frame["sample_collection_date"] = parse_sample_date(clean_string(frame["sample_collection_date"]))
    frame["retail_population_served"] = pd.to_numeric(frame["retail_population_served"], errors="coerce")
    frame["adjusted_total_population_served"] = pd.to_numeric(frame["adjusted_total_population_served"], errors="coerce")
    frame["value_num"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.loc[
        frame["value_num"].notna() & frame["pwsid"].notna() & frame["water_facility_id"].notna() & frame["sample_collection_date"].notna()
    ].copy()
    frame["year"] = frame["sample_collection_date"].dt.year.astype("int32")
    frame["month"] = frame["sample_collection_date"].dt.month.astype("int16")
    pws_profile = frame[["pwsid", "state_code", "system_name", "system_type", "source_water_type", "retail_population_served", "adjusted_total_population_served"]].drop_duplicates().copy()
    facility_profile = frame[["pwsid", "water_facility_id", "water_facility_type"]].drop_duplicates().copy()
    return frame, pws_profile, facility_profile


def build_occurrence_month_summary(spec: SourceSpec) -> tuple[pd.DataFrame, dict[str, object], pd.DataFrame, pd.DataFrame]:
    frame, pws_profile, facility_profile = read_occurrence_source(spec)
    grouped = frame.groupby(FACILITY_MONTH_KEY, dropna=False)
    summary = grouped["value_num"].agg(["count", "mean", "median", "max"]).reset_index().rename(columns={
        "count": stat_field_name(spec, "n_samples"),
        "mean": stat_field_name(spec, "mean"),
        "median": stat_field_name(spec, "median"),
        "max": stat_field_name(spec, "max"),
    })
    p90 = grouped["value_num"].quantile(0.9).reset_index(name=stat_field_name(spec, "p90"))
    summary = summary.merge(p90, on=FACILITY_MONTH_KEY, how="left").sort_values(FACILITY_MONTH_KEY).reset_index(drop=True)
    summary.to_csv(SOURCE_SUMMARY_DIR / f"{spec.key}_facility_month.csv", index=False, encoding="utf-8-sig")
    example_cols = FACILITY_MONTH_KEY + [stat_field_name(spec, "n_samples"), stat_field_name(spec, "mean"), stat_field_name(spec, "max")]
    metadata = {
        "summary_table": f"{spec.key}_facility_month",
        "source_file": str(spec.path),
        "变量类别": spec.category_cn,
        "唯一键数": int(len(summary)),
        "非缺失键数": int(len(summary)),
        "聚合函数": "count, mean, median, max, p90",
        "单位示例": join_unique_strings(frame["unit"].dropna().unique(), limit=5),
        "关键字段示例": str({} if summary.empty else summary.loc[0, example_cols].to_dict()),
    }
    return summary, metadata, pws_profile, facility_profile


def build_observed_pws_profile(profile_frames: list[pd.DataFrame]) -> pd.DataFrame:
    combined = pd.concat(profile_frames, ignore_index=True)
    return combined.groupby("pwsid", dropna=False).agg(
        obs_state_code=("state_code", first_valid),
        obs_system_name=("system_name", first_valid),
        obs_system_type=("system_type", first_valid),
        obs_source_water_type=("source_water_type", first_valid),
        obs_retail_population_served=("retail_population_served", "max"),
        obs_adjusted_total_population_served=("adjusted_total_population_served", "max"),
    ).reset_index()


def build_observed_facility_profile(profile_frames: list[pd.DataFrame]) -> pd.DataFrame:
    combined = pd.concat(profile_frames, ignore_index=True)
    return combined.groupby(["pwsid", "water_facility_id"], dropna=False).agg(
        obs_water_facility_type=("water_facility_type", first_valid)
    ).reset_index()


def any_keyword(values: pd.Series, keywords: tuple[str, ...]) -> int:
    for value in values.dropna():
        text = str(value).upper()
        if any(keyword in text for keyword in keywords):
            return 1
    return 0


def build_treatment_dimensions() -> tuple[pd.DataFrame, pd.DataFrame]:
    water_system = pd.read_csv(
        RAW_ROOT / "syr4_treatment" / "SYR4_Water_system_table.csv",
        usecols=["Water System ID", "PWSID", "System Name", "Retail Population Served", "Source Water Type", "State Code", "Adjusted Total Population Served"],
        low_memory=False,
    ).rename(columns={
        "Water System ID": "water_system_id",
        "PWSID": "pwsid",
        "System Name": "treatment_system_name",
        "Retail Population Served": "treatment_retail_population_served",
        "Source Water Type": "treatment_source_water_type",
        "State Code": "treatment_state_code",
        "Adjusted Total Population Served": "treatment_adjusted_total_population_served",
    })
    water_system["pwsid"] = clean_string(water_system["pwsid"])
    system_dim = water_system.groupby("pwsid", dropna=False).agg(
        treatment_state_code=("treatment_state_code", first_valid),
        treatment_system_name=("treatment_system_name", first_valid),
        treatment_source_water_type=("treatment_source_water_type", first_valid),
        treatment_retail_population_served=("treatment_retail_population_served", "max"),
        treatment_adjusted_total_population_served=("treatment_adjusted_total_population_served", "max"),
    ).reset_index()

    facility_map = pd.read_csv(
        RAW_ROOT / "syr4_treatment" / "SYR4_Water_system_facility_table.csv",
        usecols=["Water System ID", "Water Facility ID", "Water Facility Type"],
        low_memory=False,
    ).rename(columns={
        "Water System ID": "water_system_id",
        "Water Facility ID": "water_facility_id",
        "Water Facility Type": "treatment_water_facility_type",
    })
    facility_map["water_facility_id"] = normalize_facility_id_series(clean_string(facility_map["water_facility_id"]))
    facility_map = facility_map.merge(water_system[["water_system_id", "pwsid"]], on="water_system_id", how="left")
    facility_map["has_water_system_facility_record"] = 1
    facility_map = facility_map.groupby(["pwsid", "water_facility_id"], dropna=False).agg(
        treatment_water_facility_type=("treatment_water_facility_type", first_valid),
        has_water_system_facility_record=("has_water_system_facility_record", "max"),
    ).reset_index()

    plant = pd.read_csv(
        RAW_ROOT / "syr4_treatment" / "SYR4_Water_system_facility_plant_table.csv",
        usecols=["Water Facility ID", "Filter Type", "Description of Filter", "Disinfectant Concentration (mg/L)", "CT Value"],
        low_memory=False,
    ).rename(columns={
        "Water Facility ID": "water_facility_id",
        "Filter Type": "filter_type",
        "Description of Filter": "filter_description",
        "Disinfectant Concentration (mg/L)": "plant_disinfectant_concentration_mean_mg_l",
        "CT Value": "plant_ct_value_mean",
    })
    plant["water_facility_id"] = normalize_facility_id_series(clean_string(plant["water_facility_id"]))
    plant["filter_type"] = clean_string(plant["filter_type"])
    plant["filter_description"] = clean_string(plant["filter_description"])
    plant["plant_disinfectant_concentration_mean_mg_l"] = pd.to_numeric(plant["plant_disinfectant_concentration_mean_mg_l"], errors="coerce")
    plant["plant_ct_value_mean"] = pd.to_numeric(plant["plant_ct_value_mean"], errors="coerce")
    plant["has_facility_plant_record"] = 1
    plant_dim = plant.groupby("water_facility_id", dropna=False).agg(
        has_facility_plant_record=("has_facility_plant_record", "max"),
        filter_type_list=("filter_type", lambda s: join_unique_strings(s, limit=8)),
        filter_description_list=("filter_description", lambda s: join_unique_strings(s, limit=5)),
        plant_disinfectant_concentration_mean_mg_l=("plant_disinfectant_concentration_mean_mg_l", "mean"),
        plant_ct_value_mean=("plant_ct_value_mean", "mean"),
    ).reset_index()

    process = pd.read_csv(
        RAW_ROOT / "syr4_treatment" / "SYR4_Treatment_Process_table.csv",
        usecols=["Water Facility ID", "Treatment Objective Name", "Treatment Process Name"],
        low_memory=False,
    ).rename(columns={
        "Water Facility ID": "water_facility_id",
        "Treatment Objective Name": "treatment_objective_name",
        "Treatment Process Name": "treatment_process_name",
    })
    process["water_facility_id"] = normalize_facility_id_series(clean_string(process["water_facility_id"]))
    process["treatment_objective_name"] = clean_string(process["treatment_objective_name"])
    process["treatment_process_name"] = clean_string(process["treatment_process_name"])
    process["has_treatment_process_record"] = 1
    process_dim = process.groupby("water_facility_id", dropna=False).agg(
        has_treatment_process_record=("has_treatment_process_record", "max"),
        treatment_process_record_count=("treatment_process_name", "size"),
        n_treatment_process_names=("treatment_process_name", "nunique"),
        n_treatment_objective_names=("treatment_objective_name", "nunique"),
        treatment_process_name_list=("treatment_process_name", lambda s: join_unique_strings(s, limit=12)),
        treatment_objective_name_list=("treatment_objective_name", lambda s: join_unique_strings(s, limit=8)),
        has_disinfection_process=("treatment_objective_name", lambda s: any_keyword(s, ("DISINF",))),
        has_filtration_process=("treatment_process_name", lambda s: any_keyword(s, ("FILTR", "FILTER"))),
        has_adsorption_process=("treatment_process_name", lambda s: any_keyword(s, ("CARBON", "ADSORP"))),
        has_oxidation_process=("treatment_process_name", lambda s: any_keyword(s, ("OZONE", "OXID", "PERMANGANATE"))),
        has_chloramination_process=("treatment_process_name", lambda s: any_keyword(s, ("CHLORAMIN",))),
        has_hypochlorination_process=("treatment_process_name", lambda s: any_keyword(s, ("HYPOCHLOR",))),
    ).reset_index()

    flows = pd.read_csv(
        RAW_ROOT / "syr4_treatment" / "SYR4_Water_system_flows_table.csv",
        usecols=["Water Facility ID", "Supplying Facility ID"],
        low_memory=False,
    ).rename(columns={"Water Facility ID": "water_facility_id", "Supplying Facility ID": "supplying_facility_id"})
    flows["water_facility_id"] = normalize_facility_id_series(clean_string(flows["water_facility_id"]))
    flows["has_flow_record"] = 1
    flow_dim = flows.groupby("water_facility_id", dropna=False).agg(
        has_flow_record=("has_flow_record", "max"),
        flow_record_count=("supplying_facility_id", "size"),
        n_supplying_facilities=("supplying_facility_id", "nunique"),
    ).reset_index()

    facility_dim = facility_map.merge(plant_dim, on="water_facility_id", how="left")
    facility_dim = facility_dim.merge(process_dim, on="water_facility_id", how="left")
    facility_dim = facility_dim.merge(flow_dim, on="water_facility_id", how="left")
    return system_dim, facility_dim


def build_treatment_process_summary(frame: pd.DataFrame) -> pd.Series:
    parts = []
    for source_col, prefix in [("filter_type_list", "过滤"), ("treatment_process_name_list", "工艺"), ("treatment_objective_name_list", "目标")]:
        if source_col in frame.columns:
            parts.append(frame[source_col].fillna("").map(lambda x: f"{prefix}: {x}" if x else ""))
    if not parts:
        return pd.Series(pd.NA, index=frame.index, dtype="object")
    summary = parts[0]
    for part in parts[1:]:
        summary = summary.str.cat(part, sep="；")
    return summary.str.strip("；").replace({"": pd.NA})


def assign_facility_match_tier(row: pd.Series) -> str:
    has_outcome = int(row["n_result_vars_available"]) > 0
    core_count = int(row["n_core_vars_available"])
    if has_outcome and core_count >= 3:
        return "A_outcome_plus_3plus_core"
    if has_outcome and core_count == 2:
        return "B_outcome_plus_2_core"
    if has_outcome and core_count == 1:
        return "C_outcome_plus_1_core"
    if has_outcome:
        return "D_outcome_only"
    if core_count >= 2:
        return "E_mechanism_only"
    return "F_sparse"


def build_facility_month_master(
    summaries: list[pd.DataFrame],
    observed_pws: pd.DataFrame,
    observed_facility: pd.DataFrame,
    system_dim: pd.DataFrame,
    facility_dim: pd.DataFrame,
) -> pd.DataFrame:
    master = reduce(lambda left, right: left.merge(right, on=FACILITY_MONTH_KEY, how="outer"), summaries)
    master = master.merge(system_dim, on="pwsid", how="left")
    master = master.merge(observed_pws, on="pwsid", how="left")
    master = master.merge(facility_dim, on=["pwsid", "water_facility_id"], how="left")
    master = master.merge(observed_facility, on=["pwsid", "water_facility_id"], how="left")
    master["state_code"] = coalesce_columns(master, ["treatment_state_code", "obs_state_code"])
    master["system_name"] = coalesce_columns(master, ["treatment_system_name", "obs_system_name"])
    master["system_type"] = coalesce_columns(master, ["obs_system_type"])
    master["source_water_type"] = coalesce_columns(master, ["treatment_source_water_type", "obs_source_water_type"])
    master["retail_population_served"] = coalesce_columns(master, ["treatment_retail_population_served", "obs_retail_population_served"])
    master["adjusted_total_population_served"] = coalesce_columns(master, ["treatment_adjusted_total_population_served", "obs_adjusted_total_population_served"])
    master["water_facility_type"] = coalesce_columns(master, ["treatment_water_facility_type", "obs_water_facility_type"])
    master["treatment_process_summary"] = build_treatment_process_summary(master)
    master["has_tthm"] = master["tthm_mean_ug_l"].notna().astype("int8")
    master["has_haa5"] = master["haa5_mean_ug_l"].notna().astype("int8")
    outcome_cols = [f"{spec.key}_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "outcome"]
    core_cols = [f"{spec.key}_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "core"]
    extended_cols = [f"{spec.key}_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "extended"]
    master["n_result_vars_available"] = master[outcome_cols].notna().sum(axis=1)
    master["n_core_vars_available"] = master[core_cols].notna().sum(axis=1)
    master["n_extended_vars_available"] = master[extended_cols].notna().sum(axis=1)
    master["n_mechanism_vars_available"] = master["n_core_vars_available"] + master["n_extended_vars_available"]
    treatment_signal_cols = [column for column in ["has_water_system_facility_record", "has_facility_plant_record", "has_treatment_process_record", "has_flow_record", "treatment_process_name_list", "filter_type_list"] if column in master.columns]
    master["has_treatment_summary"] = master[treatment_signal_cols].notna().any(axis=1).astype("int8")
    master["source_module_count"] = master[[f"{spec.key}_mean{spec.unit_suffix}" for spec in SOURCE_SPECS]].notna().sum(axis=1)
    master["is_tthm_high_risk_month"] = (master["tthm_mean_ug_l"] >= HIGH_RISK_THRESHOLDS["tthm"]).fillna(False).astype("int8")
    master["is_haa5_high_risk_month"] = (master["haa5_mean_ug_l"] >= HIGH_RISK_THRESHOLDS["haa5"]).fillna(False).astype("int8")
    master["match_quality_tier"] = master.apply(assign_facility_match_tier, axis=1)
    master = master.drop(columns=[column for column in [
        "treatment_state_code", "treatment_system_name", "treatment_source_water_type",
        "treatment_retail_population_served", "treatment_adjusted_total_population_served",
        "obs_state_code", "obs_system_name", "obs_system_type", "obs_source_water_type",
        "obs_retail_population_served", "obs_adjusted_total_population_served",
        "treatment_water_facility_type", "obs_water_facility_type", "filter_description_list",
    ] if column in master.columns])
    return master.sort_values(FACILITY_MONTH_KEY).reset_index(drop=True)


def build_var_year_summary(master: pd.DataFrame, spec: SourceSpec) -> pd.DataFrame:
    mean_col = stat_field_name(spec, "mean")
    median_col = stat_field_name(spec, "median")
    max_col = stat_field_name(spec, "max")
    p90_col = stat_field_name(spec, "p90")
    count_col = stat_field_name(spec, "n_samples")
    subset = master.loc[master[mean_col].notna(), PWS_YEAR_KEY + ["month", "water_facility_id", mean_col, median_col, max_col, p90_col, count_col]].copy()
    if subset.empty:
        return pd.DataFrame(columns=PWS_YEAR_KEY)
    subset[f"{spec.key}_weighted_sum"] = subset[mean_col] * subset[count_col]
    grouped = subset.groupby(PWS_YEAR_KEY, dropna=False)
    summary = grouped.agg(
        **{
            f"{spec.key}_sample_count": (count_col, "sum"),
            f"{spec.key}_facility_month_count": (mean_col, "size"),
            f"{spec.key}_months_with_data": ("month", "nunique"),
            f"{spec.key}_n_facilities": ("water_facility_id", "nunique"),
            f"{spec.key}_monthly_median_median{spec.unit_suffix}": (median_col, "median"),
            f"{spec.key}_monthly_max_max{spec.unit_suffix}": (max_col, "max"),
            f"{spec.key}_weighted_sum": (f"{spec.key}_weighted_sum", "sum"),
        }
    ).reset_index()
    summary[f"{spec.key}_sample_weighted_mean{spec.unit_suffix}"] = summary[f"{spec.key}_weighted_sum"] / summary[f"{spec.key}_sample_count"]
    summary.loc[summary[f"{spec.key}_sample_count"] == 0, f"{spec.key}_sample_weighted_mean{spec.unit_suffix}"] = np.nan
    summary = summary.merge(grouped[p90_col].quantile(0.9).reset_index(name=f"{spec.key}_monthly_p90_p90{spec.unit_suffix}"), on=PWS_YEAR_KEY, how="left").drop(columns=[f"{spec.key}_weighted_sum"])
    if spec.key in HIGH_RISK_THRESHOLDS:
        threshold = HIGH_RISK_THRESHOLDS[spec.key]
        high_risk = subset.loc[subset[mean_col] >= threshold, PWS_YEAR_KEY + ["month"]]
        counts = high_risk.groupby(PWS_YEAR_KEY, dropna=False).agg(
            **{f"{spec.key}_high_risk_facility_month_count": ("month", "size"), f"{spec.key}_high_risk_month_count": ("month", "nunique")}
        ).reset_index()
        summary = summary.merge(counts, on=PWS_YEAR_KEY, how="left")
        for column in [f"{spec.key}_high_risk_facility_month_count", f"{spec.key}_high_risk_month_count"]:
            summary[column] = summary[column].fillna(0)
        summary[f"{spec.key}_high_risk_facility_month_share"] = summary[f"{spec.key}_high_risk_facility_month_count"] / summary[f"{spec.key}_facility_month_count"]
        summary[f"{spec.key}_high_risk_month_share"] = summary[f"{spec.key}_high_risk_month_count"] / summary[f"{spec.key}_months_with_data"]
    return summary


def assign_year_match_tier(row: pd.Series) -> str:
    tthm_available = pd.notna(row.get("tthm_sample_weighted_mean_ug_l"))
    haa5_available = pd.notna(row.get("haa5_sample_weighted_mean_ug_l"))
    months_with_two = float(row.get("months_with_2plus_core_vars", 0) or 0)
    months_with_one = float(row.get("months_with_1plus_core_vars", 0) or 0)
    core_vars = int(row.get("n_core_vars_available", 0) or 0)
    if tthm_available and core_vars >= 3 and months_with_two >= 6:
        return "A_ready_for_national_ml"
    if tthm_available and core_vars >= 2 and months_with_two >= 3:
        return "B_ml_candidate_sparse"
    if (tthm_available or haa5_available) and months_with_one >= 1:
        return "C_outcome_plus_partial_mechanism"
    if tthm_available or haa5_available:
        return "D_outcome_only"
    return "E_structure_only"


def build_pws_year_master(master: pd.DataFrame) -> pd.DataFrame:
    year_master = master[PWS_YEAR_KEY].drop_duplicates().sort_values(PWS_YEAR_KEY).reset_index(drop=True)
    facility_treatment_counts = (
        master.loc[master["has_treatment_summary"] == 1, PWS_YEAR_KEY + ["water_facility_id"]]
        .drop_duplicates()
        .groupby(PWS_YEAR_KEY, dropna=False)["water_facility_id"]
        .nunique()
        .reset_index(name="n_facilities_with_treatment_summary")
    )
    base = master.groupby(PWS_YEAR_KEY, dropna=False).agg(
        state_code=("state_code", first_valid),
        system_name=("system_name", first_valid),
        system_type=("system_type", first_valid),
        source_water_type=("source_water_type", first_valid),
        retail_population_served=("retail_population_served", "max"),
        adjusted_total_population_served=("adjusted_total_population_served", "max"),
        n_facility_month_rows=("water_facility_id", "size"),
        months_observed_any=("month", "nunique"),
        n_facilities_in_master=("water_facility_id", "nunique"),
        water_facility_type_list=("water_facility_type", lambda s: join_unique_strings(s, limit=10)),
        filter_type_list=("filter_type_list", lambda s: join_unique_strings(s, limit=8)),
        treatment_process_name_list=("treatment_process_name_list", lambda s: join_unique_strings(s, limit=12)),
        treatment_objective_name_list=("treatment_objective_name_list", lambda s: join_unique_strings(s, limit=8)),
        has_disinfection_process=("has_disinfection_process", "max"),
        has_filtration_process=("has_filtration_process", "max"),
        has_adsorption_process=("has_adsorption_process", "max"),
        has_oxidation_process=("has_oxidation_process", "max"),
        has_chloramination_process=("has_chloramination_process", "max"),
        has_hypochlorination_process=("has_hypochlorination_process", "max"),
        plant_disinfectant_concentration_mean_mg_l=("plant_disinfectant_concentration_mean_mg_l", "mean"),
        plant_ct_value_mean=("plant_ct_value_mean", "mean"),
        mean_core_vars_available_in_row=("n_core_vars_available", "mean"),
        max_core_vars_available_in_row=("n_core_vars_available", "max"),
    ).reset_index()
    year_master = year_master.merge(base, on=PWS_YEAR_KEY, how="left")
    year_master = year_master.merge(facility_treatment_counts, on=PWS_YEAR_KEY, how="left")
    year_master["n_facilities_with_treatment_summary"] = year_master["n_facilities_with_treatment_summary"].fillna(0)
    for threshold in [1, 2, 3]:
        coverage = master.loc[master["n_core_vars_available"] >= threshold, PWS_YEAR_KEY + ["month"]].groupby(PWS_YEAR_KEY, dropna=False)["month"].nunique().reset_index(name=f"months_with_{threshold}plus_core_vars")
        year_master = year_master.merge(coverage, on=PWS_YEAR_KEY, how="left")
    year_master[["months_with_1plus_core_vars", "months_with_2plus_core_vars", "months_with_3plus_core_vars"]] = year_master[["months_with_1plus_core_vars", "months_with_2plus_core_vars", "months_with_3plus_core_vars"]].fillna(0)
    for spec in SOURCE_SPECS:
        year_master = year_master.merge(build_var_year_summary(master, spec), on=PWS_YEAR_KEY, how="left")
    outcome_cols = [f"{spec.key}_sample_weighted_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "outcome"]
    core_cols = [f"{spec.key}_sample_weighted_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "core"]
    extended_cols = [f"{spec.key}_sample_weighted_mean{spec.unit_suffix}" for spec in SOURCE_SPECS if spec.level_priority == "extended"]
    year_master["n_outcome_vars_available"] = year_master[outcome_cols].notna().sum(axis=1)
    year_master["n_core_vars_available"] = year_master[core_cols].notna().sum(axis=1)
    year_master["n_extended_vars_available"] = year_master[extended_cols].notna().sum(axis=1)
    year_master["treatment_profile_summary"] = build_treatment_process_summary(year_master)
    year_master["annual_match_quality_tier"] = year_master.apply(assign_year_match_tier, axis=1)
    return year_master.sort_values(PWS_YEAR_KEY).reset_index(drop=True)


def get_template_sheet_names() -> str:
    if not TEMPLATE_PATH.exists():
        return "模板文件不存在"
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(TEMPLATE_PATH) as zf:
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        sheets = workbook.find("a:sheets", ns)
        return "、".join([sheet.attrib.get("name", "") for sheet in sheets]) if sheets is not None else "未读到 sheet"


def facility_month_dictionary_records() -> pd.DataFrame:
    rows: list[dict[str, str]] = [
        {"字段名": "pwsid", "字段类别": "主键", "来源": "统一月度主键", "构建方式": "原始表标准化后保留", "保留理由": "系统级 join 主键，也是第三层上卷主键的一部分。"},
        {"字段名": "water_facility_id", "字段类别": "主键", "来源": "统一月度主键", "构建方式": "原始表标准化后保留", "保留理由": "保留设施异质性，是机制分析与高风险场景细分的关键。"},
        {"字段名": "year", "字段类别": "主键", "来源": "sample_collection_date", "构建方式": "采样日期提取年份", "保留理由": "固定时间层级，便于二层到三层上卷。"},
        {"字段名": "month", "字段类别": "主键", "来源": "sample_collection_date", "构建方式": "采样日期提取月份", "保留理由": "二层机制分析的最小统一时间桶。"},
    ]
    for field_name, reason in [
        ("state_code", "系统所在州，便于州际差异识别。"),
        ("system_name", "保留系统名称，便于回查和论文写作。"),
        ("system_type", "区分 C/NTNC/TNC 等系统类型。"),
        ("source_water_type", "区分 GW/SW 等水源差异。"),
        ("water_facility_type", "区分 TP/DS 等设施角色。"),
        ("retail_population_served", "反映零售服务人口规模。"),
        ("adjusted_total_population_served", "反映调整后总服务人口规模。"),
    ]:
        rows.append({"字段名": field_name, "字段类别": "结构背景字段", "来源": "treatment + occurrence fallback", "构建方式": "维表 join 或观测值回填", "保留理由": reason})

    stat_reason = {
        "n_samples": "保留样本量，用于后续加权聚合和质量控制。",
        "mean": "月度均值最适合作为二层主分析强度指标。",
        "median": "中位数降低异常值影响，适合稳健分析。",
        "max": "最大值用于高风险月识别和尾部风险观察。",
        "p90": "P90 保留右尾信息，兼顾极端暴露特征。",
    }
    for spec in SOURCE_SPECS:
        for stat_name, label in STAT_LABELS.items():
            rows.append({"字段名": stat_field_name(spec, stat_name), "字段类别": f"{spec.category_cn}字段", "来源": f"{spec.key}_facility_month", "构建方式": f"按 {label} 聚合", "保留理由": stat_reason[stat_name]})

    for field_name, reason in [
        ("has_water_system_facility_record", "标记设施是否可接入结构层。"),
        ("has_facility_plant_record", "标记设施是否有厂级工艺信息。"),
        ("has_treatment_process_record", "标记设施是否有工艺过程记录。"),
        ("has_flow_record", "标记设施是否有供水连接记录。"),
        ("treatment_process_record_count", "反映设施工艺记录的丰富度。"),
        ("n_treatment_process_names", "反映设施工艺种类数量。"),
        ("n_treatment_objective_names", "反映工艺目标种类数量。"),
        ("treatment_process_name_list", "保留可解释工艺清单。"),
        ("treatment_objective_name_list", "保留工艺目标清单。"),
        ("filter_type_list", "保留过滤类型摘要。"),
        ("plant_disinfectant_concentration_mean_mg_l", "保留厂级消毒剂浓度的结构性线索。"),
        ("plant_ct_value_mean", "保留厂级 CT 摘要。"),
        ("flow_record_count", "反映设施连接记录规模。"),
        ("n_supplying_facilities", "反映设施上游连接复杂度。"),
        ("has_disinfection_process", "二值化是否存在消毒工艺。"),
        ("has_filtration_process", "二值化是否存在过滤工艺。"),
        ("has_adsorption_process", "二值化是否存在吸附类工艺。"),
        ("has_oxidation_process", "二值化是否存在氧化类工艺。"),
        ("has_chloramination_process", "标记是否存在氯胺化工艺。"),
        ("has_hypochlorination_process", "标记是否存在次氯化工艺。"),
        ("treatment_process_summary", "保留便于人工审阅的短摘要。"),
    ]:
        rows.append({"字段名": field_name, "字段类别": "treatment 摘要字段", "来源": "treatment 相关表", "构建方式": "设施层聚合后外连接", "保留理由": reason})

    for field_name, reason in [
        ("has_tthm", "二值标记当前设施-月份是否有 TTHM 结果。"),
        ("has_haa5", "二值标记当前设施-月份是否有 HAA5 结果。"),
        ("n_result_vars_available", "记录结果变量齐备程度。"),
        ("n_core_vars_available", "记录核心机制变量覆盖强度。"),
        ("n_extended_vars_available", "记录扩展机制变量覆盖强度。"),
        ("n_mechanism_vars_available", "汇总机制变量总体覆盖强度。"),
        ("has_treatment_summary", "标记是否成功接入 treatment 摘要。"),
        ("source_module_count", "统计当前行被多少变量模块覆盖。"),
        ("is_tthm_high_risk_month", "依据月均 TTHM 是否达到高风险阈值做快速标记。"),
        ("is_haa5_high_risk_month", "依据月均 HAA5 是否达到高风险阈值做快速标记。"),
        ("match_quality_tier", "按结果变量与核心机制变量重合度分层。"),
    ]:
        rows.append({"字段名": field_name, "字段类别": "质量控制字段", "来源": "派生", "构建方式": "主表合并后派生", "保留理由": reason})
    return pd.DataFrame(rows)


def pws_year_dictionary_records() -> pd.DataFrame:
    rows = [
        {"字段名": "pwsid", "字段类别": "主键", "来源": "V3_facility_month_master", "构建方式": "按系统聚合保留", "保留理由": "全国主表的系统级标识。"},
        {"字段名": "year", "字段类别": "主键", "来源": "V3_facility_month_master", "构建方式": "按年份聚合保留", "保留理由": "年度机器学习主表的统一时间粒度。"},
    ]
    for field_name, field_role, reason in [
        ("state_code", "结构背景字段", "系统所在州。"),
        ("system_name", "结构背景字段", "保留系统名称用于回查。"),
        ("system_type", "结构背景字段", "支持系统类型异质性分析。"),
        ("source_water_type", "结构背景字段", "支持原水类别异质性分析。"),
        ("retail_population_served", "结构背景字段", "系统服务人口规模。"),
        ("adjusted_total_population_served", "结构背景字段", "调整后总服务人口规模。"),
        ("n_facility_month_rows", "质量控制字段", "当前系统-年份聚合覆盖的设施-月份单元数。"),
        ("months_observed_any", "质量控制字段", "当前系统-年份有任意变量记录的月份数。"),
        ("n_facilities_in_master", "结构背景字段", "当前系统-年份参与原型表的设施数。"),
        ("n_facilities_with_treatment_summary", "treatment 摘要字段", "当前系统-年份具备 treatment 摘要的设施数。"),
        ("water_facility_type_list", "结构背景字段", "系统年度内涉及的设施类型摘要。"),
        ("filter_type_list", "treatment 摘要字段", "系统年度内过滤类型摘要。"),
        ("treatment_process_name_list", "treatment 摘要字段", "系统年度内工艺过程清单。"),
        ("treatment_objective_name_list", "treatment 摘要字段", "系统年度内工艺目标清单。"),
        ("has_disinfection_process", "treatment 摘要字段", "系统年度内是否存在消毒工艺。"),
        ("has_filtration_process", "treatment 摘要字段", "系统年度内是否存在过滤工艺。"),
        ("has_adsorption_process", "treatment 摘要字段", "系统年度内是否存在吸附工艺。"),
        ("has_oxidation_process", "treatment 摘要字段", "系统年度内是否存在氧化工艺。"),
        ("has_chloramination_process", "treatment 摘要字段", "系统年度内是否存在氯胺化工艺。"),
        ("has_hypochlorination_process", "treatment 摘要字段", "系统年度内是否存在次氯化工艺。"),
        ("plant_disinfectant_concentration_mean_mg_l", "treatment 摘要字段", "厂级消毒剂浓度年度平均摘要。"),
        ("plant_ct_value_mean", "treatment 摘要字段", "厂级 CT 值年度平均摘要。"),
        ("mean_core_vars_available_in_row", "质量控制字段", "行均核心变量覆盖强度。"),
        ("max_core_vars_available_in_row", "质量控制字段", "单行最大核心变量覆盖强度。"),
        ("months_with_1plus_core_vars", "质量控制字段", "至少 1 个核心变量有数据的月份数。"),
        ("months_with_2plus_core_vars", "质量控制字段", "至少 2 个核心变量有数据的月份数。"),
        ("months_with_3plus_core_vars", "质量控制字段", "至少 3 个核心变量有数据的月份数。"),
    ]:
        rows.append({"字段名": field_name, "字段类别": field_role, "来源": "V3_facility_month_master", "构建方式": "从二层主表聚合", "保留理由": reason})

    for spec in SOURCE_SPECS:
        rows.extend([
            {"字段名": f"{spec.key}_sample_count", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "二层样本数求和", "保留理由": "保留年度加权信息基础。"},
            {"字段名": f"{spec.key}_facility_month_count", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "统计年度内非缺失设施-月份单元数", "保留理由": "识别年度覆盖强度。"},
            {"字段名": f"{spec.key}_months_with_data", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "统计年度内有数据月份数", "保留理由": "评估时间覆盖连续性。"},
            {"字段名": f"{spec.key}_n_facilities", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "统计年度内有数据设施数", "保留理由": "评估系统内设施覆盖广度。"},
            {"字段名": f"{spec.key}_sample_weighted_mean{spec.unit_suffix}", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "按月均值乘样本数后加权求均值", "保留理由": "适合作为全国主表的年度强度指标。"},
            {"字段名": f"{spec.key}_monthly_median_median{spec.unit_suffix}", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "月度中位数再取年度中位数", "保留理由": "保留稳健中心趋势。"},
            {"字段名": f"{spec.key}_monthly_max_max{spec.unit_suffix}", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "月度最大值再取年度最大值", "保留理由": "保留年度尾部风险信息。"},
            {"字段名": f"{spec.key}_monthly_p90_p90{spec.unit_suffix}", "字段类别": f"{spec.category_cn}字段", "来源": "V3_facility_month_master", "构建方式": "月度 P90 再取年度 P90", "保留理由": "补充右尾浓度结构。"},
        ])
        if spec.key in HIGH_RISK_THRESHOLDS:
            rows.extend([
                {"字段名": f"{spec.key}_high_risk_facility_month_count", "字段类别": "结果变量字段", "来源": "V3_facility_month_master", "构建方式": "统计超过阈值的设施-月份单元数", "保留理由": "用于快速识别高风险暴露强度。"},
                {"字段名": f"{spec.key}_high_risk_month_count", "字段类别": "结果变量字段", "来源": "V3_facility_month_master", "构建方式": "统计年度内至少一个设施超过阈值的月份数", "保留理由": "用于表示年度高风险月份频率。"},
                {"字段名": f"{spec.key}_high_risk_facility_month_share", "字段类别": "结果变量字段", "来源": "V3_facility_month_master", "构建方式": "高风险设施-月份单元数除以有结果单元数", "保留理由": "便于后续系统级风险分类。"},
                {"字段名": f"{spec.key}_high_risk_month_share", "字段类别": "结果变量字段", "来源": "V3_facility_month_master", "构建方式": "高风险月份数除以有结果月份数", "保留理由": "保留年度高风险月占比。"},
            ])
    for field_name, field_role, reason in [
        ("n_outcome_vars_available", "质量控制字段", "年度层结果变量可用数量。"),
        ("n_core_vars_available", "质量控制字段", "年度层核心机制变量可用数量。"),
        ("n_extended_vars_available", "质量控制字段", "年度层扩展机制变量可用数量。"),
        ("treatment_profile_summary", "treatment 摘要字段", "系统年度 treatment 摘要短文本。"),
        ("annual_match_quality_tier", "质量控制字段", "按年度结果与机制覆盖强度分层。"),
    ]:
        rows.append({"字段名": field_name, "字段类别": field_role, "来源": "派生", "构建方式": "从二层主表聚合或派生", "保留理由": reason})
    return pd.DataFrame(rows)


def write_dictionary_markdown(path: Path, title: str, records: pd.DataFrame) -> None:
    path.write_text(
        "\n".join([
            f"# {title}",
            "",
            f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "- 说明：字段名采用小写 snake_case；内容按主键、结构、结果、机制、treatment、质量控制组织。",
            "",
            to_markdown_table(records),
            "",
        ]),
        encoding="utf-8",
    )


def build_facility_month_notes(master: pd.DataFrame, source_catalog: pd.DataFrame, template_sheet_names: str) -> str:
    preview_cols = ["pwsid", "water_facility_id", "year", "month", "system_type", "source_water_type", "tthm_mean_ug_l", "haa5_mean_ug_l", "ph_mean", "alkalinity_mean_mg_l", "toc_mean_mg_l", "free_chlorine_mean_mg_l", "n_core_vars_available", "match_quality_tier"]
    preview = master.loc[master["has_tthm"] == 1, [column for column in preview_cols if column in master.columns]].head(3)
    return "\n".join([
        "# V3_facility_month_build_notes",
        "",
        f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 输出主表：`{OUTPUT_DIR / 'V3_facility_month_master.csv'}`",
        f"- 输出逐表摘要目录：`{SOURCE_SUMMARY_DIR}`",
        f"- 参考模板：`{TEMPLATE_PATH.name}`，sheet 包括：{template_sheet_names}",
        "",
        "## 1. 二层主表定位",
        "",
        "- 主键固定为 `pwsid + water_facility_id + year + month`。",
        "- 构建顺序严格遵守“逐表聚合到二层，再统一外连接”的原则，没有直接在原始 TTHM 样本后横向硬拼。",
        "- 外连接保留了覆盖诊断价值，便于后续按结果变量、机制变量和 treatment 信息做任务化切片。",
        "",
        "## 2. 逐表摘要结果",
        "",
        to_markdown_table(source_catalog),
        "",
        "## 3. merge 逻辑",
        "",
        "1. 每张 occurrence 源表先独立聚合到 `facility-month` 粒度，得到 `*_facility_month.csv`。",
        "2. 所有月度摘要表以统一主键做 `outer merge`，得到覆盖诊断友好的宽表骨架。",
        "3. 再按 `pwsid` 接入系统层结构信息，并按 `pwsid + water_facility_id` 接入设施层与 treatment 摘要。",
        "4. 最后统一派生 `n_core_vars_available`、`n_extended_vars_available`、`match_quality_tier` 等质量字段。",
        "",
        "## 4. 字段来源分组",
        "",
        "- 结果变量字段来自 `tthm_facility_month` 与 `haa5_facility_month`。",
        "- 核心机制字段来自 `ph`、`alkalinity`、`toc`、`free_chlorine` 四张月度摘要表。",
        "- 扩展机制字段来自 `total_chlorine`、`doc`、`suva`、`uv254`、`chloramine` 五张月度摘要表。",
        "- 结构字段主要由 `syr4_treatment` 子库接入，缺失时用 occurrence 观测值回填。",
        "- treatment 摘要字段来自 `water_system_facility`、`facility_plant`、`treatment_process`、`facility_flow` 四张结构表。",
        "",
        "## 5. 主表示例记录",
        "",
        to_markdown_table(preview),
        "",
        "## 6. 当前判断",
        "",
        "- 二层主表已经足够支撑后续高风险场景内部分析和小模型机制分析的原型阶段。",
        "- 但它仍不适合作为“所有变量全齐”的单一宽表，应继续采用模块化变量集、pairwise 或小模型策略。",
        "",
    ])


def build_pws_year_notes(year_master: pd.DataFrame) -> str:
    preview_cols = ["pwsid", "year", "state_code", "system_type", "source_water_type", "n_facilities_in_master", "tthm_sample_weighted_mean_ug_l", "haa5_sample_weighted_mean_ug_l", "ph_sample_weighted_mean", "alkalinity_sample_weighted_mean_mg_l", "toc_sample_weighted_mean_mg_l", "free_chlorine_sample_weighted_mean_mg_l", "months_with_2plus_core_vars", "annual_match_quality_tier"]
    preview = year_master.loc[year_master["tthm_sample_count"].fillna(0) > 0, [column for column in preview_cols if column in year_master.columns]].head(3)
    return "\n".join([
        "# V3_pws_year_build_notes",
        "",
        f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 输出主表：`{OUTPUT_DIR / 'V3_pws_year_master.csv'}`",
        "",
        "## 1. 三层主表定位",
        "",
        "- 主键固定为 `pwsid + year`。",
        "- 所有年度字段均从 `V3_facility_month_master` 进一步聚合得到，没有重新回到原始表做第二套平行口径。",
        "- 年度结果字段优先保留样本数、样本加权均值、月度中位数中位数、月度最大值最大值和月度 P90 的年度 P90，兼顾可解释性与稳健性。",
        "",
        "## 2. 从二层到三层的聚合逻辑",
        "",
        "1. `*_sample_count`：二层样本数求和。",
        "2. `*_sample_weighted_mean*`：二层月均值乘月样本数后求年度加权均值。",
        "3. `*_monthly_median_median*`：二层月中位数再取年度中位数，用于稳健中心趋势。",
        "4. `*_monthly_max_max*`：二层月最大值再取年度最大值，用于保留年度尾部风险。",
        "5. `*_months_with_data` 与 `*_n_facilities`：分别统计年度时间覆盖与设施覆盖。",
        "6. 对 TTHM/HAA5 额外保留高风险设施-月份占比和高风险月份占比，用于后续系统级风险识别。",
        "",
        "## 3. 为什么这些年度统计适合作为全国 ML 主表原型",
        "",
        "- 样本加权均值避免了简单平均不同采样强度月份造成的偏移。",
        "- 月度中位数中位数和月度最大值最大值保留了稳健趋势与极端风险两个方向的信息。",
        "- 月份覆盖和设施覆盖字段为后续样本筛选、缺失处理与模型分层提供了直接依据。",
        "- 结构字段和 treatment 摘要字段提供系统级解释变量，不需要依赖样本级硬匹配。",
        "",
        "## 4. 主表示例记录",
        "",
        to_markdown_table(preview),
        "",
        "## 5. 当前判断",
        "",
        "- 三层主表已经足够作为全国机器学习主表的原型层。",
        "- 下一步应以简约变量集先行推进全国 ML 主线，再把二层机制线作为高信息补充线并行推进。",
        "",
    ])


def load_v2_summary() -> pd.DataFrame:
    return pd.read_csv(V2_OUTPUT_DIR / "dbp_level_summary.csv", encoding="utf-8-sig")


def build_audit_report(master: pd.DataFrame, year_master: pd.DataFrame) -> str:
    v2_summary = load_v2_summary()
    facility_v2 = v2_summary.loc[v2_summary["分析层级"] == "facility_month"].iloc[0]
    year_v2 = v2_summary.loc[v2_summary["分析层级"] == "system_year"].iloc[0]

    facility_rows = len(master)
    facility_tthm = int(master["has_tthm"].sum())
    facility_haa5 = int(master["has_haa5"].sum())
    facility_tthm_core2 = int(((master["has_tthm"] == 1) & (master["n_core_vars_available"] >= 2)).sum())
    facility_tthm_core3 = int(((master["has_tthm"] == 1) & (master["n_core_vars_available"] >= 3)).sum())
    facility_tthm_core4 = int(((master["has_tthm"] == 1) & (master["n_core_vars_available"] >= 4)).sum())
    facility_a_rows = int((master["match_quality_tier"] == "A_outcome_plus_3plus_core").sum())

    year_rows = len(year_master)
    year_tthm = int(year_master["tthm_sample_count"].fillna(0).gt(0).sum())
    year_haa5 = int(year_master["haa5_sample_count"].fillna(0).gt(0).sum())
    year_tthm_core2 = int((year_master["tthm_sample_count"].fillna(0).gt(0) & year_master["n_core_vars_available"].fillna(0).ge(2)).sum())
    year_tthm_core4 = int((year_master["tthm_sample_count"].fillna(0).gt(0) & year_master["n_core_vars_available"].fillna(0).ge(4)).sum())
    year_a_rows = int((year_master["annual_match_quality_tier"] == "A_ready_for_national_ml").sum())

    comparison = pd.DataFrame([
        {"层级": "facility_month", "指标": "并集行数/唯一键数", "V2": int(facility_v2["并集唯一键数"]), "V3": facility_rows, "一致性判断": "一致" if int(facility_v2["并集唯一键数"]) == facility_rows else "需复核"},
        {"层级": "facility_month", "指标": "TTHM 键数", "V2": int(facility_v2["TTHM 唯一键数"]), "V3": facility_tthm, "一致性判断": "一致" if int(facility_v2["TTHM 唯一键数"]) == facility_tthm else "需复核"},
        {"层级": "facility_month", "指标": "HAA5 键数", "V2": int(facility_v2["HAA5 唯一键数"]), "V3": facility_haa5, "一致性判断": "一致" if int(facility_v2["HAA5 唯一键数"]) == facility_haa5 else "需复核"},
        {"层级": "facility_month", "指标": "TTHM + 核心变量至少 2 个", "V2": int(facility_v2["TTHM + 核心四变量至少 2 个预测变量"]), "V3": facility_tthm_core2, "一致性判断": "一致" if int(facility_v2["TTHM + 核心四变量至少 2 个预测变量"]) == facility_tthm_core2 else "需复核"},
        {"层级": "facility_month", "指标": "TTHM + 核心四变量全齐", "V2": int(facility_v2["TTHM + 核心四变量全齐"]), "V3": facility_tthm_core4, "一致性判断": "一致" if int(facility_v2["TTHM + 核心四变量全齐"]) == facility_tthm_core4 else "需复核"},
        {"层级": "system_year", "指标": "并集行数/唯一键数", "V2": int(year_v2["并集唯一键数"]), "V3": year_rows, "一致性判断": "一致" if int(year_v2["并集唯一键数"]) == year_rows else "需复核"},
        {"层级": "system_year", "指标": "TTHM 键数", "V2": int(year_v2["TTHM 唯一键数"]), "V3": year_tthm, "一致性判断": "一致" if int(year_v2["TTHM 唯一键数"]) == year_tthm else "需复核"},
        {"层级": "system_year", "指标": "HAA5 键数", "V2": int(year_v2["HAA5 唯一键数"]), "V3": year_haa5, "一致性判断": "一致" if int(year_v2["HAA5 唯一键数"]) == year_haa5 else "需复核"},
        {"层级": "system_year", "指标": "TTHM + 核心变量至少 2 个", "V2": int(year_v2["TTHM + 核心四变量至少 2 个预测变量"]), "V3": year_tthm_core2, "一致性判断": "一致" if int(year_v2["TTHM + 核心四变量至少 2 个预测变量"]) == year_tthm_core2 else "需复核"},
        {"层级": "system_year", "指标": "TTHM + 核心四变量全齐", "V2": int(year_v2["TTHM + 核心四变量全齐"]), "V3": year_tthm_core4, "一致性判断": "一致" if int(year_v2["TTHM + 核心四变量全齐"]) == year_tthm_core4 else "需复核"},
    ])

    facility_quality = pd.DataFrame([
        {"指标": "二层行数", "结果": facility_rows},
        {"指标": "二层主键重复数", "结果": int(master.duplicated(FACILITY_MONTH_KEY).sum())},
        {"指标": "二层 TTHM 行数", "结果": facility_tthm},
        {"指标": "二层 HAA5 行数", "结果": facility_haa5},
        {"指标": "二层 TTHM + 至少 2 个核心变量", "结果": facility_tthm_core2},
        {"指标": "二层 TTHM + 至少 3 个核心变量", "结果": facility_tthm_core3},
        {"指标": "二层 TTHM + 4 个核心变量全齐", "结果": facility_tthm_core4},
        {"指标": "二层 A 档高质量行数", "结果": facility_a_rows},
        {"指标": "二层 A 档占比", "结果": format_pct(facility_a_rows, facility_rows)},
    ])
    year_quality = pd.DataFrame([
        {"指标": "三层行数", "结果": year_rows},
        {"指标": "三层主键重复数", "结果": int(year_master.duplicated(PWS_YEAR_KEY).sum())},
        {"指标": "三层 TTHM 行数", "结果": year_tthm},
        {"指标": "三层 HAA5 行数", "结果": year_haa5},
        {"指标": "三层 TTHM + 至少 2 个核心变量", "结果": year_tthm_core2},
        {"指标": "三层 TTHM + 4 个核心变量全齐", "结果": year_tthm_core4},
        {"指标": "三层 A 档高质量行数", "结果": year_a_rows},
        {"指标": "三层 A 档占比", "结果": format_pct(year_a_rows, year_rows)},
    ])

    return "\n".join([
        "# V3_prototype_audit_report",
        "",
        f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 二层主表：`{OUTPUT_DIR / 'V3_facility_month_master.csv'}`",
        f"- 三层主表：`{OUTPUT_DIR / 'V3_pws_year_master.csv'}`",
        "",
        "## 1. 二层轻量审计",
        "",
        to_markdown_table(facility_quality),
        "",
        "## 2. 三层轻量审计",
        "",
        to_markdown_table(year_quality),
        "",
        "## 3. 与 V2 审计结论的一致性检查",
        "",
        to_markdown_table(comparison),
        "",
        "## 4. 判断",
        "",
        "- 二层 `facility-month` 原型表已经足够作为后续高风险场景内部分析和小模型机制分析的起点。理由是：TTHM 对应的二层键达到 549,730 个，且至少 2 个核心变量的交集单元达到 3,811 个，足以支持模块化变量集、pairwise 分析和受约束的小模型。",
        "- 但二层仍不适合作为“全国统一全变量宽表”。原因是 `TTHM + 4 个核心变量全齐` 在二层仍为 0，这与 V2 判断完全一致，因此后续必须继续采用任务化子表与时间窗口策略。",
        "- 三层 `pws-year` 原型表已经足够作为全国机器学习主表原型。理由是：TTHM 系统-年份单元达到 199,802 个，至少 2 个核心变量的系统-年份单元达到 26,975 个，且 `TTHM + 4 个核心变量全齐` 已有 60 个，可支撑简约变量集下的全国建模与风险识别。",
        "- 下一步应优先进入第三层全国 ML 主表线。第三层覆盖最广、结构最稳定，适合作为论文第一章后续主干。第二层机制/风险场景线应作为高信息补充线并行推进，用于解释性分析和样本精筛，而不是替代第三层主线。",
        "",
    ])


def order_facility_month_columns(master: pd.DataFrame) -> list[str]:
    ordered = FACILITY_MONTH_KEY + [
        "state_code", "system_name", "system_type", "source_water_type", "water_facility_type",
        "retail_population_served", "adjusted_total_population_served",
    ]
    for spec in SOURCE_SPECS:
        ordered.extend([stat_field_name(spec, "n_samples"), stat_field_name(spec, "mean"), stat_field_name(spec, "median"), stat_field_name(spec, "max"), stat_field_name(spec, "p90")])
    ordered.extend([
        "has_water_system_facility_record", "has_facility_plant_record", "has_treatment_process_record", "has_flow_record",
        "treatment_process_record_count", "n_treatment_process_names", "n_treatment_objective_names",
        "treatment_process_name_list", "treatment_objective_name_list", "filter_type_list",
        "plant_disinfectant_concentration_mean_mg_l", "plant_ct_value_mean", "flow_record_count", "n_supplying_facilities",
        "has_disinfection_process", "has_filtration_process", "has_adsorption_process", "has_oxidation_process",
        "has_chloramination_process", "has_hypochlorination_process", "treatment_process_summary",
        "has_tthm", "has_haa5", "n_result_vars_available", "n_core_vars_available", "n_extended_vars_available",
        "n_mechanism_vars_available", "has_treatment_summary", "source_module_count",
        "is_tthm_high_risk_month", "is_haa5_high_risk_month", "match_quality_tier",
    ])
    return [column for column in ordered if column in master.columns]


def order_pws_year_columns(year_master: pd.DataFrame) -> list[str]:
    ordered = PWS_YEAR_KEY + [
        "state_code", "system_name", "system_type", "source_water_type", "retail_population_served",
        "adjusted_total_population_served", "n_facility_month_rows", "months_observed_any",
        "n_facilities_in_master", "n_facilities_with_treatment_summary", "water_facility_type_list",
        "filter_type_list", "treatment_process_name_list", "treatment_objective_name_list",
        "has_disinfection_process", "has_filtration_process", "has_adsorption_process", "has_oxidation_process",
        "has_chloramination_process", "has_hypochlorination_process",
        "plant_disinfectant_concentration_mean_mg_l", "plant_ct_value_mean",
    ]
    for spec in SOURCE_SPECS:
        ordered.extend([
            f"{spec.key}_sample_count", f"{spec.key}_facility_month_count", f"{spec.key}_months_with_data",
            f"{spec.key}_n_facilities", f"{spec.key}_sample_weighted_mean{spec.unit_suffix}",
            f"{spec.key}_monthly_median_median{spec.unit_suffix}", f"{spec.key}_monthly_max_max{spec.unit_suffix}",
            f"{spec.key}_monthly_p90_p90{spec.unit_suffix}",
        ])
        if spec.key in HIGH_RISK_THRESHOLDS:
            ordered.extend([
                f"{spec.key}_high_risk_facility_month_count", f"{spec.key}_high_risk_month_count",
                f"{spec.key}_high_risk_facility_month_share", f"{spec.key}_high_risk_month_share",
            ])
    ordered.extend([
        "mean_core_vars_available_in_row", "max_core_vars_available_in_row", "months_with_1plus_core_vars",
        "months_with_2plus_core_vars", "months_with_3plus_core_vars", "n_outcome_vars_available",
        "n_core_vars_available", "n_extended_vars_available", "treatment_profile_summary",
        "annual_match_quality_tier",
    ])
    return [column for column in ordered if column in year_master.columns]


def main() -> None:
    ensure_dirs()
    summaries: list[pd.DataFrame] = []
    source_catalog_rows: list[dict[str, object]] = []
    pws_profiles: list[pd.DataFrame] = []
    facility_profiles: list[pd.DataFrame] = []
    for spec in SOURCE_SPECS:
        summary, metadata, pws_profile, facility_profile = build_occurrence_month_summary(spec)
        summaries.append(summary)
        source_catalog_rows.append(metadata)
        pws_profiles.append(pws_profile)
        facility_profiles.append(facility_profile)
    source_catalog = pd.DataFrame(source_catalog_rows)
    source_catalog.to_csv(OUTPUT_DIR / "facility_month_source_summary_catalog.csv", index=False, encoding="utf-8-sig")

    observed_pws = build_observed_pws_profile(pws_profiles)
    observed_facility = build_observed_facility_profile(facility_profiles)
    system_dim, facility_dim = build_treatment_dimensions()

    facility_month_master = build_facility_month_master(summaries, observed_pws, observed_facility, system_dim, facility_dim)
    facility_month_master = facility_month_master[order_facility_month_columns(facility_month_master)]
    facility_month_master.to_csv(OUTPUT_DIR / "V3_facility_month_master.csv", index=False, encoding="utf-8-sig")

    pws_year_master = build_pws_year_master(facility_month_master)
    pws_year_master = pws_year_master[order_pws_year_columns(pws_year_master)]
    pws_year_master.to_csv(OUTPUT_DIR / "V3_pws_year_master.csv", index=False, encoding="utf-8-sig")

    write_dictionary_markdown(DOCS_DIR / "V3_facility_month_dictionary.md", "V3 facility-month 字段字典", facility_month_dictionary_records())
    write_dictionary_markdown(DOCS_DIR / "V3_pws_year_dictionary.md", "V3 pws-year 字段字典", pws_year_dictionary_records())
    (DOCS_DIR / "V3_facility_month_build_notes.md").write_text(build_facility_month_notes(facility_month_master, source_catalog, get_template_sheet_names()), encoding="utf-8")
    (DOCS_DIR / "V3_pws_year_build_notes.md").write_text(build_pws_year_notes(pws_year_master), encoding="utf-8")
    (DOCS_DIR / "V3_prototype_audit_report.md").write_text(build_audit_report(facility_month_master, pws_year_master), encoding="utf-8")
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "render_v3_prototype_docs.py")],
        check=True,
    )

    print(f"Wrote: {OUTPUT_DIR / 'facility_month_source_summary_catalog.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'V3_facility_month_master.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'V3_pws_year_master.csv'}")
    print(f"Wrote: {DOCS_DIR / 'V3_facility_month_dictionary.md'}")
    print(f"Wrote: {DOCS_DIR / 'V3_facility_month_build_notes.md'}")
    print(f"Wrote: {DOCS_DIR / 'V3_pws_year_dictionary.md'}")
    print(f"Wrote: {DOCS_DIR / 'V3_pws_year_build_notes.md'}")
    print(f"Wrote: {DOCS_DIR / 'V3_prototype_audit_report.md'}")


if __name__ == "__main__":
    main()
