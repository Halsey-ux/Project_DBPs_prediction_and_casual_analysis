from __future__ import annotations

from pathlib import Path

import pandas as pd


KEY_COLUMNS = ["pwsid", "year"]
TARGET_COLUMNS = [
    "tthm_sample_weighted_mean_ug_l",
]
LABEL_COLUMNS = [
    "tthm_regulatory_exceed_label",
    "tthm_warning_label",
]
LEVEL_COLUMNS = [
    "level1_flag",
    "level2_flag",
    "level3_flag",
    "ml_level_max",
]
BASELINE_COLUMNS = [
    "state_code",
    "system_type",
    "source_water_type",
    "retail_population_served",
    "adjusted_total_population_served",
    "n_facilities_in_master",
    "has_disinfection_process",
    "has_filtration_process",
    "has_adsorption_process",
    "has_oxidation_process",
    "has_chloramination_process",
    "has_hypochlorination_process",
]
ENHANCED_COLUMNS = [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
    "toc_sample_weighted_mean_mg_l",
    "free_chlorine_sample_weighted_mean_mg_l",
    "total_chlorine_sample_weighted_mean_mg_l",
]
QUALITY_COLUMNS = [
    "months_observed_any",
    "tthm_months_with_data",
    "months_with_1plus_core_vars",
    "months_with_2plus_core_vars",
    "months_with_3plus_core_vars",
    "n_core_vars_available",
    "annual_match_quality_tier",
]
MISSING_FLAG_COLUMNS = [
    "ph_missing_flag",
    "alkalinity_missing_flag",
    "toc_missing_flag",
    "free_chlorine_missing_flag",
    "total_chlorine_missing_flag",
]
INTEGER_LIKE_COLUMNS = [
    "year",
    "retail_population_served",
    "adjusted_total_population_served",
    "n_facilities_in_master",
    "months_observed_any",
    "tthm_months_with_data",
    "months_with_1plus_core_vars",
    "months_with_2plus_core_vars",
    "months_with_3plus_core_vars",
    "n_core_vars_available",
]
STRING_COLUMNS = [
    "pwsid",
    "state_code",
    "system_type",
    "source_water_type",
    "annual_match_quality_tier",
    "ml_level_max",
]
TREATMENT_FLAG_COLUMNS = [
    "has_disinfection_process",
    "has_filtration_process",
    "has_adsorption_process",
    "has_oxidation_process",
    "has_chloramination_process",
    "has_hypochlorination_process",
]
FLOAT_COLUMNS = TARGET_COLUMNS + ENHANCED_COLUMNS
NULLABLE_BINARY_COLUMNS = LABEL_COLUMNS + TREATMENT_FLAG_COLUMNS
FLAG_COLUMNS = [
    "level1_flag",
    "level2_flag",
    "level3_flag",
] + MISSING_FLAG_COLUMNS
ALL_COLUMNS = (
    KEY_COLUMNS
    + TARGET_COLUMNS
    + LABEL_COLUMNS
    + LEVEL_COLUMNS
    + BASELINE_COLUMNS
    + ENHANCED_COLUMNS
    + QUALITY_COLUMNS
    + MISSING_FLAG_COLUMNS
)
CSV_READ_DTYPE_MAP = {
    "pwsid": "string",
    "state_code": "string",
    "system_type": "string",
    "source_water_type": "string",
    "annual_match_quality_tier": "string",
    "ml_level_max": "string",
}


def clean_string_series(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})


def coerce_integer_like(series: pd.Series, column_name: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    non_null = numeric.dropna()
    if not non_null.empty and not non_null.mod(1).eq(0).all():
        raise ValueError(f"字段 {column_name} 存在非整数值，无法按整数型写入。")
    return numeric.astype("Int64")


def coerce_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def coerce_nullable_binary(series: pd.Series, column_name: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    non_null = numeric.dropna()
    if not non_null.empty and not non_null.isin([0, 1]).all():
        bad_values = sorted(non_null.loc[~non_null.isin([0, 1])].unique().tolist())
        raise ValueError(f"字段 {column_name} 出现非 0/1 值：{bad_values[:10]}")
    return numeric.astype("Int8")


def validate_nullable_binary_series(series: pd.Series, column_name: str) -> None:
    non_null = series.dropna()
    if not non_null.isin([0, 1]).all():
        bad_values = sorted(non_null.loc[~non_null.isin([0, 1])].unique().tolist())
        raise ValueError(f"字段 {column_name} 在回读校验中出现非 0/1 值：{bad_values[:10]}")


def validate_unique_key(df: pd.DataFrame) -> None:
    duplicated = df.duplicated(subset=KEY_COLUMNS, keep=False)
    if duplicated.any():
        raise ValueError(f"输出主键不唯一，重复行数：{int(duplicated.sum())}")


def validate_label_missingness(df: pd.DataFrame) -> None:
    target_missing = df["tthm_sample_weighted_mean_ug_l"].isna()
    for column in LABEL_COLUMNS:
        if df.loc[target_missing, column].notna().any():
            raise ValueError(f"字段 {column} 在目标缺失样本中出现非空值。")


def coerce_v4_ml_ready_types(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    for column in STRING_COLUMNS:
        if column in output.columns:
            output[column] = clean_string_series(output[column])

    for column in INTEGER_LIKE_COLUMNS:
        if column in output.columns:
            output[column] = coerce_integer_like(output[column], column)

    for column in FLOAT_COLUMNS:
        if column in output.columns:
            output[column] = coerce_float(output[column])

    for column in NULLABLE_BINARY_COLUMNS:
        if column in output.columns:
            output[column] = coerce_nullable_binary(output[column], column)

    for column in FLAG_COLUMNS:
        if column in output.columns:
            output[column] = coerce_nullable_binary(output[column], column)

    return output


def read_v4_ml_ready_csv(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path, encoding="utf-8-sig", dtype=CSV_READ_DTYPE_MAP)
    missing_columns = [column for column in ALL_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"V4 ml_ready 缺少必需字段：{missing_columns}")
    df = df[ALL_COLUMNS].copy()
    return coerce_v4_ml_ready_types(df)


def validate_v4_ml_ready_schema(df: pd.DataFrame) -> None:
    if list(df.columns) != ALL_COLUMNS:
        raise ValueError("V4 ml_ready 字段顺序或字段集合不符合 schema。")

    for column in INTEGER_LIKE_COLUMNS:
        if str(df[column].dtype) != "Int64":
            raise ValueError(f"字段 {column} dtype 不是 Int64，而是 {df[column].dtype}")

    for column in NULLABLE_BINARY_COLUMNS + FLAG_COLUMNS:
        if str(df[column].dtype) != "Int8":
            raise ValueError(f"字段 {column} dtype 不是 Int8，而是 {df[column].dtype}")
        validate_nullable_binary_series(df[column], column)

    for column in FLOAT_COLUMNS:
        if str(df[column].dtype) not in {"float64", "Float64"}:
            raise ValueError(f"字段 {column} dtype 不是浮点型，而是 {df[column].dtype}")

    for column in STRING_COLUMNS:
        if str(df[column].dtype) != "string":
            raise ValueError(f"字段 {column} dtype 不是 string，而是 {df[column].dtype}")

    validate_unique_key(df)
    validate_label_missingness(df)

