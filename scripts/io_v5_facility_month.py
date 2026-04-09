from __future__ import annotations

from pathlib import Path

import pandas as pd


KEY_COLUMNS = ["pwsid", "water_facility_id", "year", "month"]
TARGET_COLUMN = "tthm_mean_ug_l"
LABEL_COLUMN = "is_tthm_high_risk_month"

BASELINE_CORE_MINIMAL_FEATURES = [
    "month",
    "state_code",
    "system_type",
    "source_water_type",
    "retail_population_served",
    "adjusted_total_population_served",
]

BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES = [
    *BASELINE_CORE_MINIMAL_FEATURES,
    "has_treatment_summary",
]

BASELINE_CORE_PLUS_WATER_FACILITY_TYPE_FEATURES = [
    *BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES,
    "water_facility_type",
]

FINAL_BASELINE_FEATURES = BASELINE_CORE_MINIMAL_FEATURES.copy()
STAGE1_REQUIRED_COLUMNS = ["ph_mean", "alkalinity_mean_mg_l"]

DETAILED_TREATMENT_FLAG_COLUMNS = [
    "has_disinfection_process",
    "has_filtration_process",
    "has_adsorption_process",
    "has_oxidation_process",
    "has_chloramination_process",
    "has_hypochlorination_process",
]

STRING_COLUMNS = [
    "pwsid",
    "water_facility_id",
    "state_code",
    "system_type",
    "source_water_type",
    "water_facility_type",
]

INTEGER_LIKE_COLUMNS = [
    "year",
    "month",
    "retail_population_served",
    "adjusted_total_population_served",
]

FLOAT_COLUMNS = [
    TARGET_COLUMN,
    *STAGE1_REQUIRED_COLUMNS,
]

NULLABLE_BINARY_COLUMNS = [
    LABEL_COLUMN,
    "has_treatment_summary",
    *DETAILED_TREATMENT_FLAG_COLUMNS,
]

CATEGORICAL_FEATURE_COLUMNS = {
    "month",
    "state_code",
    "system_type",
    "source_water_type",
    "has_treatment_summary",
    "water_facility_type",
}

ALL_COLUMNS = [
    *KEY_COLUMNS,
    TARGET_COLUMN,
    LABEL_COLUMN,
    *BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES[1:],
    "water_facility_type",
    *DETAILED_TREATMENT_FLAG_COLUMNS,
    *STAGE1_REQUIRED_COLUMNS,
]

CSV_READ_DTYPE_MAP = {
    "pwsid": "string",
    "water_facility_id": "string",
    "state_code": "string",
    "system_type": "string",
    "source_water_type": "string",
    "water_facility_type": "string",
}


def clean_string_series(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})


def coerce_integer_like(series: pd.Series, column_name: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    non_null = numeric.dropna()
    if not non_null.empty and not non_null.mod(1).eq(0).all():
        raise ValueError(f"Column {column_name} contains non-integer values.")
    return numeric.astype("Int64")


def coerce_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def coerce_nullable_binary(series: pd.Series, column_name: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    non_null = numeric.dropna()
    if not non_null.empty and not non_null.isin([0, 1]).all():
        bad_values = sorted(non_null.loc[~non_null.isin([0, 1])].unique().tolist())
        raise ValueError(f"Column {column_name} contains values outside 0/1: {bad_values[:10]}")
    return numeric.astype("Int8")


def validate_nullable_binary_series(series: pd.Series, column_name: str) -> None:
    non_null = series.dropna()
    if not non_null.isin([0, 1]).all():
        bad_values = sorted(non_null.loc[~non_null.isin([0, 1])].unique().tolist())
        raise ValueError(f"Column {column_name} failed 0/1 validation: {bad_values[:10]}")


def validate_unique_key(df: pd.DataFrame) -> None:
    duplicated = df.duplicated(subset=KEY_COLUMNS, keep=False)
    if duplicated.any():
        raise ValueError(f"Primary key is not unique. Duplicated rows: {int(duplicated.sum())}")


def validate_tthm_high_risk_label(df: pd.DataFrame) -> None:
    target_available = df[TARGET_COLUMN].notna()
    expected = (df.loc[target_available, TARGET_COLUMN] >= 80.0).astype("Int8")
    observed = df.loc[target_available, LABEL_COLUMN]
    if observed.isna().any():
        raise ValueError(f"Column {LABEL_COLUMN} contains null values when {TARGET_COLUMN} is present.")
    mismatched = expected.ne(observed)
    if mismatched.any():
        raise ValueError(f"Column {LABEL_COLUMN} does not match the >=80 ug/L threshold.")


def coerce_v5_facility_month_types(df: pd.DataFrame) -> pd.DataFrame:
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

    return output


def read_v5_facility_month_csv(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    df = pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
        dtype=CSV_READ_DTYPE_MAP,
        usecols=ALL_COLUMNS,
        low_memory=False,
    )
    missing_columns = [column for column in ALL_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"V5 facility-month table is missing required columns: {missing_columns}")
    return coerce_v5_facility_month_types(df[ALL_COLUMNS].copy())


def validate_v5_facility_month_schema(df: pd.DataFrame) -> None:
    if list(df.columns) != ALL_COLUMNS:
        raise ValueError("V5 facility-month columns do not match the expected schema.")

    for column in STRING_COLUMNS:
        if str(df[column].dtype) != "string":
            raise ValueError(f"Column {column} must be string, got {df[column].dtype}")

    for column in INTEGER_LIKE_COLUMNS:
        if str(df[column].dtype) != "Int64":
            raise ValueError(f"Column {column} must be Int64, got {df[column].dtype}")

    for column in FLOAT_COLUMNS:
        if str(df[column].dtype) not in {"float64", "Float64"}:
            raise ValueError(f"Column {column} must be float-like, got {df[column].dtype}")

    for column in NULLABLE_BINARY_COLUMNS:
        if str(df[column].dtype) != "Int8":
            raise ValueError(f"Column {column} must be Int8, got {df[column].dtype}")
        validate_nullable_binary_series(df[column], column)

    validate_unique_key(df)
    validate_tthm_high_risk_label(df)


def infer_feature_groups(feature_columns: list[str]) -> tuple[list[str], list[str]]:
    categorical_features = [column for column in feature_columns if column in CATEGORICAL_FEATURE_COLUMNS]
    numeric_features = [column for column in feature_columns if column not in CATEGORICAL_FEATURE_COLUMNS]
    return numeric_features, categorical_features
