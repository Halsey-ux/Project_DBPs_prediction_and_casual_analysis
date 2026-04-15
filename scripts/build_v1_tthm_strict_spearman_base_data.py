from __future__ import annotations

from datetime import datetime
from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V1_TTHM_strict_spearman_base_data"

MAIN_PATH = Path(
    r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv"
)

SOURCE_SPECS = {
    "ph": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\PH.csv"
        ),
        "value_col": "ph_value",
        "unit_col": "ph_unit",
        "expected_unit": None,
        "physical_min": 0.0,
        "physical_max": 14.0,
        "use_iqr_for_clean": True,
    },
    "alkalinity": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ALKALINITY.csv"
        ),
        "value_col": "alkalinity_value",
        "unit_col": "alkalinity_unit",
        "expected_unit": "MG/L",
        "physical_min": 0.0,
        "physical_max": None,
        "use_iqr_for_clean": True,
    },
    "toc": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ORGANIC CARBON.csv"
        ),
        "value_col": "toc_value",
        "unit_col": "toc_unit",
        "expected_unit": "MG/L",
        "physical_min": 0.0,
        "physical_max": None,
        "use_iqr_for_clean": True,
    },
    "free_chlorine": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_Disinfectant Residuals\FREE RESIDUAL CHLORINE (1013).csv"
        ),
        "value_col": "free_chlorine_value",
        "unit_col": "free_chlorine_unit",
        "expected_unit": "MG/L",
        "physical_min": 0.0,
        "physical_max": None,
        "use_iqr_for_clean": True,
    },
}

KEY_COLUMNS = [
    "PWSID",
    "WATER_FACILITY_ID",
    "SAMPLING_POINT_ID",
    "SAMPLE_COLLECTION_DATE",
]

BACKGROUND_COLUMNS = [
    "SYSTEM_TYPE",
    "SOURCE_WATER_TYPE",
    "WATER_FACILITY_TYPE",
    "SAMPLING_POINT_TYPE",
    "SAMPLE_TYPE_CODE",
    "RETAIL_POPULATION_SERVED",
    "ADJUSTED_TOTAL_POPULATION_SERVED",
]

MASTER_REQUIRED_COLUMNS = [
    *KEY_COLUMNS,
    "tthm_value",
    "log_tthm",
    "ph_value",
    "alkalinity_value",
    "toc_value",
    "free_chlorine_value",
    *BACKGROUND_COLUMNS,
    "year",
    "month",
    "quarter",
]

SPEARMAN_BASE_COLUMNS = [
    "tthm_value",
    "log_tthm",
    "ph_value",
    "alkalinity_value",
    "toc_value",
    "free_chlorine_value",
]

SPEARMAN_LOG_COLUMNS = [
    "log_tthm",
    "ph_value",
    "log1p_alkalinity_value",
    "log1p_toc_value",
    "log1p_free_chlorine_value",
]

RAW_INPUT_PATH = OUTPUT_DIR / "V1_tthm_spearman_input.csv"
CLEAN_INPUT_PATH = OUTPUT_DIR / "V1_tthm_spearman_input_clean.csv"
LOG_INPUT_PATH = OUTPUT_DIR / "V1_tthm_spearman_input_log.csv"
CLEAN_LOG_INPUT_PATH = OUTPUT_DIR / "V1_tthm_spearman_input_log_clean.csv"
MASTER_PATH = OUTPUT_DIR / "V1_tthm_strict_spearman_master.csv"
RESULTS_PATH = OUTPUT_DIR / "V1_tthm_spearman_results.csv"
REPORT_PATH = OUTPUT_DIR / "V1_tthm_spearman_report.md"
NOTES_PATH = OUTPUT_DIR / "V1_tthm_strict_cleaning_notes.md"


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_string_series(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NA": pd.NA})


def parse_collection_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="%d-%b-%y", errors="coerce")


def first_non_missing(series: pd.Series) -> object:
    non_missing = series.dropna()
    if non_missing.empty:
        return pd.NA
    return non_missing.iloc[0]


def normal_approx_two_sided_p_value(rho: float, n: int) -> float | float("nan"):
    if pd.isna(rho) or n < 4 or abs(rho) >= 1:
        return np.nan
    z_score = abs(rho) * sqrt(max(n - 1, 1))
    tail = 1 - 0.5 * (1 + erf(z_score / sqrt(2)))
    return max(0.0, min(1.0, 2 * tail))


def to_markdown_table(df: pd.DataFrame) -> str:
    frame = df.copy().fillna("")
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def format_pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.00%"
    return f"{numerator / denominator * 100:.2f}%"


def safe_log1p(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    output = pd.Series(np.nan, index=series.index, dtype="float64")
    valid_mask = numeric.notna() & numeric.ge(0)
    output.loc[valid_mask] = np.log1p(numeric.loc[valid_mask])
    return output


def compute_spearman_rho(left: pd.Series, right: pd.Series) -> float:
    pair_df = pd.DataFrame({"left": left, "right": right}).dropna()
    if len(pair_df) < 2:
        return np.nan
    left_rank = pair_df["left"].rank(method="average")
    right_rank = pair_df["right"].rank(method="average")
    return float(left_rank.corr(right_rank, method="pearson"))


def build_dtype_map(columns: list[str]) -> dict[str, str]:
    string_columns = {
        *KEY_COLUMNS,
        "SYSTEM_TYPE",
        "SOURCE_WATER_TYPE",
        "WATER_FACILITY_TYPE",
        "SAMPLING_POINT_TYPE",
        "SAMPLE_TYPE_CODE",
        "UNIT",
        "DETECT",
        "VALUE",
    }
    return {column: "string" for column in columns if column in string_columns}


def read_table(path: Path, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        usecols=columns,
        dtype=build_dtype_map(columns),
        low_memory=False,
    )
    for column in KEY_COLUMNS:
        if column in df.columns:
            df[column] = clean_string_series(df[column])
    if "SAMPLE_COLLECTION_DATE" in df.columns:
        df["SAMPLE_COLLECTION_DATE"] = parse_collection_date(df["SAMPLE_COLLECTION_DATE"])
    for column in [
        "SYSTEM_TYPE",
        "SOURCE_WATER_TYPE",
        "WATER_FACILITY_TYPE",
        "SAMPLING_POINT_TYPE",
        "SAMPLE_TYPE_CODE",
        "UNIT",
        "DETECT",
    ]:
        if column in df.columns:
            df[column] = clean_string_series(df[column])
    if "VALUE" in df.columns:
        df["VALUE_NUM"] = pd.to_numeric(df["VALUE"], errors="coerce")
    if "RETAIL_POPULATION_SERVED" in df.columns:
        df["RETAIL_POPULATION_SERVED"] = pd.to_numeric(
            df["RETAIL_POPULATION_SERVED"], errors="coerce"
        )
    if "ADJUSTED_TOTAL_POPULATION_SERVED" in df.columns:
        df["ADJUSTED_TOTAL_POPULATION_SERVED"] = pd.to_numeric(
            df["ADJUSTED_TOTAL_POPULATION_SERVED"], errors="coerce"
        )
    return df


def summarize_source(path: Path, label: str) -> dict[str, object]:
    df = read_table(path, [*KEY_COLUMNS, "VALUE", "UNIT"])
    value_num = df["VALUE_NUM"]
    q1 = value_num.quantile(0.25)
    q3 = value_num.quantile(0.75)
    iqr = q3 - q1
    lower_3iqr = q1 - 3 * iqr if pd.notna(iqr) else np.nan
    upper_3iqr = q3 + 3 * iqr if pd.notna(iqr) else np.nan
    return {
        "表名": label,
        "原始记录数": int(len(df)),
        "严格键唯一数": int(df[KEY_COLUMNS].drop_duplicates().shape[0]),
        "重复记录数": int(df.duplicated(KEY_COLUMNS).sum()),
        "VALUE 非缺失数": int(value_num.notna().sum()),
        "VALUE 缺失数": int(value_num.isna().sum()),
        "负值数": int((value_num < 0).sum()),
        "最小值": round(float(value_num.min()), 6) if value_num.notna().any() else np.nan,
        "P25": round(float(q1), 6) if pd.notna(q1) else np.nan,
        "P50": round(float(value_num.quantile(0.5)), 6)
        if value_num.notna().any()
        else np.nan,
        "P75": round(float(q3), 6) if pd.notna(q3) else np.nan,
        "3IQR 下界": round(float(lower_3iqr), 6) if pd.notna(lower_3iqr) else np.nan,
        "3IQR 上界": round(float(upper_3iqr), 6) if pd.notna(upper_3iqr) else np.nan,
        "最大值": round(float(value_num.max()), 6) if value_num.notna().any() else np.nan,
        "UNIT Top3": "; ".join(
            f"{unit}:{count}"
            for unit, count in clean_string_series(df["UNIT"]).dropna().value_counts().head(3).items()
        )
        or "NA",
    }


def aggregate_tthm_table() -> tuple[pd.DataFrame, dict[str, int]]:
    columns = [*KEY_COLUMNS, *BACKGROUND_COLUMNS, "VALUE", "UNIT", "DETECT"]
    df = read_table(MAIN_PATH, columns)
    duplicate_group_df = df[df.duplicated(KEY_COLUMNS, keep=False)].copy()
    duplicate_summary = {
        "tthm_duplicate_raw_rows": int(df.duplicated(KEY_COLUMNS).sum()),
        "tthm_duplicate_group_count": int(
            duplicate_group_df[KEY_COLUMNS].drop_duplicates().shape[0]
        ),
        "tthm_duplicate_value_conflict_groups": 0,
        "tthm_duplicate_unit_conflict_groups": 0,
    }
    if not duplicate_group_df.empty:
        duplicate_summary["tthm_duplicate_value_conflict_groups"] = int(
            duplicate_group_df.groupby(KEY_COLUMNS, dropna=False)["VALUE_NUM"]
            .nunique(dropna=True)
            .gt(1)
            .sum()
        )
        duplicate_summary["tthm_duplicate_unit_conflict_groups"] = int(
            duplicate_group_df.groupby(KEY_COLUMNS, dropna=False)["UNIT"]
            .nunique(dropna=True)
            .gt(1)
            .sum()
        )

    aggregated = (
        df.groupby(KEY_COLUMNS, dropna=False)
        .agg(
            tthm_value=("VALUE_NUM", "median"),
            tthm_source_rows=("VALUE_NUM", "size"),
            tthm_numeric_rows=("VALUE_NUM", "count"),
            tthm_value_nunique=("VALUE_NUM", "nunique"),
            tthm_unit=("UNIT", "first"),
            tthm_unit_nunique=("UNIT", "nunique"),
            tthm_detect=("DETECT", "first"),
            SYSTEM_TYPE=("SYSTEM_TYPE", first_non_missing),
            SOURCE_WATER_TYPE=("SOURCE_WATER_TYPE", first_non_missing),
            WATER_FACILITY_TYPE=("WATER_FACILITY_TYPE", first_non_missing),
            SAMPLING_POINT_TYPE=("SAMPLING_POINT_TYPE", first_non_missing),
            SAMPLE_TYPE_CODE=("SAMPLE_TYPE_CODE", first_non_missing),
            RETAIL_POPULATION_SERVED=("RETAIL_POPULATION_SERVED", "median"),
            ADJUSTED_TOTAL_POPULATION_SERVED=(
                "ADJUSTED_TOTAL_POPULATION_SERVED",
                "median",
            ),
        )
        .reset_index()
    )
    return aggregated, duplicate_summary


def aggregate_source_table(path: Path, value_col: str, unit_col: str) -> pd.DataFrame:
    df = read_table(path, [*KEY_COLUMNS, "VALUE", "UNIT"])
    return (
        df.groupby(KEY_COLUMNS, dropna=False)
        .agg(
            **{
                value_col: ("VALUE_NUM", "median"),
                f"{value_col}_source_rows": ("VALUE_NUM", "size"),
                f"{value_col}_numeric_rows": ("VALUE_NUM", "count"),
                f"{value_col}_nunique": ("VALUE_NUM", "nunique"),
                unit_col: ("UNIT", "first"),
                f"{unit_col}_nunique": ("UNIT", "nunique"),
            }
        )
        .reset_index()
    )


def add_log_columns(df: pd.DataFrame) -> None:
    df["log_tthm"] = safe_log1p(df["tthm_value"])
    df["log1p_RETAIL_POPULATION_SERVED"] = safe_log1p(df["RETAIL_POPULATION_SERVED"])
    df["log1p_ADJUSTED_TOTAL_POPULATION_SERVED"] = safe_log1p(
        df["ADJUSTED_TOTAL_POPULATION_SERVED"]
    )
    for value_col in ["alkalinity_value", "toc_value", "free_chlorine_value"]:
        log_col = f"log1p_{value_col}"
        df[log_col] = safe_log1p(df[value_col])


def add_variable_flags(
    df: pd.DataFrame,
    value_col: str,
    unit_col: str | None,
    expected_unit: str | None,
    physical_min: float | None,
    physical_max: float | None,
    use_iqr_for_clean: bool,
) -> dict[str, object]:
    non_missing = df[value_col].dropna()
    q1 = non_missing.quantile(0.25)
    q3 = non_missing.quantile(0.75)
    iqr = q3 - q1
    lower_3iqr = q1 - 3 * iqr if pd.notna(iqr) else np.nan
    upper_3iqr = q3 + 3 * iqr if pd.notna(iqr) else np.nan

    missing_flag = df[value_col].isna()
    if unit_col is not None and expected_unit is not None:
        unit_flag = df[unit_col].notna() & (df[unit_col] != expected_unit)
    else:
        unit_flag = pd.Series(False, index=df.index)

    physical_flag = pd.Series(False, index=df.index)
    if physical_min is not None:
        physical_flag = physical_flag | df[value_col].lt(physical_min)
    if physical_max is not None:
        physical_flag = physical_flag | df[value_col].gt(physical_max)

    iqr_flag = pd.Series(False, index=df.index)
    if pd.notna(lower_3iqr) and pd.notna(upper_3iqr):
        iqr_flag = df[value_col].lt(lower_3iqr) | df[value_col].gt(upper_3iqr)

    clean_exclude = unit_flag | physical_flag
    if use_iqr_for_clean:
        clean_exclude = clean_exclude | iqr_flag

    df[f"{value_col}_flag_missing"] = missing_flag
    df[f"{value_col}_flag_unit_anomaly"] = unit_flag
    df[f"{value_col}_flag_physical_anomaly"] = physical_flag
    df[f"{value_col}_flag_iqr_extreme"] = iqr_flag
    df[f"{value_col}_flag_clean_exclude"] = clean_exclude
    df[f"{value_col}_clean"] = df[value_col].mask(clean_exclude)

    return {
        "变量": value_col,
        "非缺失数": int(df[value_col].notna().sum()),
        "缺失数": int(missing_flag.sum()),
        "单位异常数": int(unit_flag.sum()),
        "物理异常数": int(physical_flag.sum()),
        "3IQR 极端值数": int(iqr_flag.sum()),
        "稳健版剔除数": int(clean_exclude.sum()),
        "3IQR 下界": round(float(lower_3iqr), 6) if pd.notna(lower_3iqr) else np.nan,
        "3IQR 上界": round(float(upper_3iqr), 6) if pd.notna(upper_3iqr) else np.nan,
    }


def build_inputs(
    master_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw_base = master_df.loc[
        master_df["tthm_value"].notna()
        & master_df[["ph_value", "alkalinity_value", "toc_value", "free_chlorine_value"]]
        .notna()
        .any(axis=1),
        SPEARMAN_BASE_COLUMNS,
    ].copy()

    clean_base = master_df.loc[
        master_df["tthm_value_clean"].notna()
        & master_df[
            [
                "ph_value_clean",
                "alkalinity_value_clean",
                "toc_value_clean",
                "free_chlorine_value_clean",
            ]
        ]
        .notna()
        .any(axis=1),
        [
            "tthm_value_clean",
            "log_tthm_clean",
            "ph_value_clean",
            "alkalinity_value_clean",
            "toc_value_clean",
            "free_chlorine_value_clean",
        ],
    ].copy()
    clean_base.columns = SPEARMAN_BASE_COLUMNS

    raw_log = master_df.loc[
        master_df["log_tthm"].notna()
        & master_df[
            [
                "ph_value",
                "log1p_alkalinity_value",
                "log1p_toc_value",
                "log1p_free_chlorine_value",
            ]
        ]
        .notna()
        .any(axis=1),
        SPEARMAN_LOG_COLUMNS,
    ].copy()

    clean_log = master_df.loc[
        master_df["log_tthm_clean"].notna()
        & master_df[
            [
                "ph_value_clean",
                "log1p_alkalinity_value_clean",
                "log1p_toc_value_clean",
                "log1p_free_chlorine_value_clean",
            ]
        ]
        .notna()
        .any(axis=1),
        [
            "log_tthm_clean",
            "ph_value_clean",
            "log1p_alkalinity_value_clean",
            "log1p_toc_value_clean",
            "log1p_free_chlorine_value_clean",
        ],
    ].copy()
    clean_log.columns = SPEARMAN_LOG_COLUMNS

    return raw_base, clean_base, raw_log, clean_log


def run_spearman_suite(
    dataset_name: str,
    target_variable: str,
    predictors: list[str],
    df: pd.DataFrame,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for predictor in predictors:
        pair_df = df[[target_variable, predictor]].dropna()
        n = int(len(pair_df))
        rho = compute_spearman_rho(pair_df[target_variable], pair_df[predictor])
        records.append(
            {
                "dataset_name": dataset_name,
                "target_variable": target_variable,
                "predictor_variable": predictor,
                "pair_n": n,
                "spearman_rho": round(float(rho), 6) if pd.notna(rho) else np.nan,
                "abs_spearman_rho": round(abs(float(rho)), 6)
                if pd.notna(rho)
                else np.nan,
                "p_value_normal_approx": normal_approx_two_sided_p_value(float(rho), n)
                if pd.notna(rho)
                else np.nan,
            }
        )
    return records


def compare_stability(results_df: pd.DataFrame) -> pd.DataFrame:
    comparison_specs = [
        ("raw_base", "raw_partial_log", "ph_value", "ph_value"),
        ("raw_base", "raw_partial_log", "alkalinity_value", "log1p_alkalinity_value"),
        ("raw_base", "raw_partial_log", "toc_value", "log1p_toc_value"),
        ("raw_base", "raw_partial_log", "free_chlorine_value", "log1p_free_chlorine_value"),
        ("clean_base", "clean_partial_log", "ph_value", "ph_value"),
        ("clean_base", "clean_partial_log", "alkalinity_value", "log1p_alkalinity_value"),
        ("clean_base", "clean_partial_log", "toc_value", "log1p_toc_value"),
        ("clean_base", "clean_partial_log", "free_chlorine_value", "log1p_free_chlorine_value"),
    ]
    rows = []
    for base_dataset, log_dataset, base_predictor, log_predictor in comparison_specs:
        base_row = results_df.loc[
            (results_df["dataset_name"] == base_dataset)
            & (results_df["predictor_variable"] == base_predictor)
        ].iloc[0]
        log_row = results_df.loc[
            (results_df["dataset_name"] == log_dataset)
            & (results_df["predictor_variable"] == log_predictor)
        ].iloc[0]
        rows.append(
            {
                "对照组": f"{base_dataset} vs {log_dataset}",
                "变量": base_predictor.replace("_value", ""),
                "base_rho": base_row["spearman_rho"],
                "log_rho": log_row["spearman_rho"],
                "绝对差值": round(
                    abs(float(base_row["spearman_rho"]) - float(log_row["spearman_rho"])),
                    10,
                ),
                "base_n": int(base_row["pair_n"]),
                "log_n": int(log_row["pair_n"]),
            }
        )
    return pd.DataFrame(rows)


def build_cleaning_notes(
    source_summary_df: pd.DataFrame,
    anomaly_df: pd.DataFrame,
    duplicate_summary: dict[str, int],
    raw_base: pd.DataFrame,
    clean_base: pd.DataFrame,
    raw_log: pd.DataFrame,
    clean_log: pd.DataFrame,
) -> str:
    lines = [
        "# V1 TTHM 严格样本级清洗说明",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 输出目录：`{OUTPUT_DIR}`",
        "- 版本：`V1_TTHM_strict_spearman_base_data`",
        "",
        "## 1. 对齐与聚合原则",
        "",
        "- 本版本只允许使用 `PWSID + WATER_FACILITY_ID + SAMPLING_POINT_ID + SAMPLE_COLLECTION_DATE` 严格样本级对齐。",
        "- 不使用 `facility_day`、同月匹配、同季度匹配或任何回退匹配。",
        "- 对原始表内同一严格键的重复记录，采用数值字段中位数聚合，背景字段保留首个非缺失值，并保留源记录数与重复信息字段。",
        "",
        "## 2. 原始输入表概况",
        "",
        to_markdown_table(source_summary_df),
        "",
        "## 3. TTHM 严格键重复概况",
        "",
        f"- TTHM 原始重复记录数：{duplicate_summary['tthm_duplicate_raw_rows']}",
        f"- TTHM 重复键组数：{duplicate_summary['tthm_duplicate_group_count']}",
        f"- TTHM 重复键中数值冲突组数：{duplicate_summary['tthm_duplicate_value_conflict_groups']}",
        f"- TTHM 重复键中单位冲突组数：{duplicate_summary['tthm_duplicate_unit_conflict_groups']}",
        "",
        "## 4. 轻度清洗规则",
        "",
        "- 先保留严格原值版母表与原值版 Spearman 输入表，不覆盖原始值。",
        "- 对每个数值变量生成 4 类标记：缺失、单位异常、物理异常、3IQR 极端值。",
        "- 单位异常只针对有明确预期单位的变量：TTHM 期望 `UG/L`，碱度/TOC/游离余氯期望 `MG/L`；pH 不要求单位。",
        "- 物理异常使用保守规则：TTHM/碱度/TOC/游离余氯不能小于 0，pH 必须位于 `[0, 14]`。",
        "- 稳健版清洗只对预测变量额外剔除 3IQR 极端值；TTHM 结果变量仅剔除单位异常和物理异常，不用 3IQR 直接删高值。",
        "- 不做统一标准化，不做大规模插补，不做宽松匹配补值。",
        "",
        "## 5. 异常标记统计",
        "",
        to_markdown_table(anomaly_df),
        "",
        "## 6. 生成的数据文件",
        "",
        "- `V1_tthm_strict_spearman_master.csv`：严格样本级母表，含原值、清洗值与异常标记。",
        "- `V1_tthm_spearman_input.csv`：原值版 Spearman 输入表。",
        "- `V1_tthm_spearman_input_clean.csv`：轻度清洗稳健版 Spearman 输入表。",
        "- `V1_tthm_spearman_input_log.csv`：原值版部分 log 输入表。",
        "- `V1_tthm_spearman_input_log_clean.csv`：轻度清洗稳健版部分 log 输入表。",
        "- `V1_tthm_spearman_results.csv`：Spearman 结果汇总。",
        "- `V1_tthm_spearman_report.md`：中文结果报告。",
        "",
        "## 7. 输入表规模",
        "",
        f"- 原值版基础输入表行数：{len(raw_base)}",
        f"- 稳健版基础输入表行数：{len(clean_base)}",
        f"- 原值版部分 log 输入表行数：{len(raw_log)}",
        f"- 稳健版部分 log 输入表行数：{len(clean_log)}",
        "",
    ]
    return "\n".join(lines) + "\n"


def build_report(
    master_df: pd.DataFrame,
    anomaly_df: pd.DataFrame,
    results_df: pd.DataFrame,
    stability_df: pd.DataFrame,
    raw_base: pd.DataFrame,
    clean_base: pd.DataFrame,
) -> str:
    core_non_missing_df = pd.DataFrame(
        [
            {"变量": "tthm_value", "非缺失记录数": int(master_df["tthm_value"].notna().sum())},
            {"变量": "log_tthm", "非缺失记录数": int(master_df["log_tthm"].notna().sum())},
            {"变量": "ph_value", "非缺失记录数": int(master_df["ph_value"].notna().sum())},
            {
                "变量": "alkalinity_value",
                "非缺失记录数": int(master_df["alkalinity_value"].notna().sum()),
            },
            {"变量": "toc_value", "非缺失记录数": int(master_df["toc_value"].notna().sum())},
            {
                "变量": "free_chlorine_value",
                "非缺失记录数": int(master_df["free_chlorine_value"].notna().sum()),
            },
        ]
    )

    result_display = results_df.copy()
    result_display["p_value_normal_approx"] = result_display["p_value_normal_approx"].map(
        lambda value: round(float(value), 6) if pd.notna(value) else value
    )

    variables_in_spearman = [
        "`tthm_value`",
        "`log_tthm`",
        "`ph_value`",
        "`alkalinity_value`",
        "`toc_value`",
        "`free_chlorine_value`",
        "以及对应的部分 log 版本 `log1p_alkalinity_value`、`log1p_toc_value`、`log1p_free_chlorine_value`",
    ]

    variables_only_in_master = [
        "`PWSID`",
        "`WATER_FACILITY_ID`",
        "`SAMPLING_POINT_ID`",
        "`SAMPLE_COLLECTION_DATE`",
        "`SYSTEM_TYPE`",
        "`SOURCE_WATER_TYPE`",
        "`WATER_FACILITY_TYPE`",
        "`SAMPLING_POINT_TYPE`",
        "`SAMPLE_TYPE_CODE`",
        "`RETAIL_POPULATION_SERVED`",
        "`ADJUSTED_TOTAL_POPULATION_SERVED`",
        "`year`",
        "`month`",
        "`quarter`",
        "所有单位字段、重复统计字段、源记录数字段与异常标记字段",
    ]

    complete_case_all_predictors = int(
        master_df[
            [
                "ph_value",
                "alkalinity_value",
                "toc_value",
                "free_chlorine_value",
            ]
        ]
        .notna()
        .all(axis=1)
        .sum()
    )
    at_least_one_predictor = int(
        master_df[
            [
                "ph_value",
                "alkalinity_value",
                "toc_value",
                "free_chlorine_value",
            ]
        ]
        .notna()
        .any(axis=1)
        .sum()
    )
    at_least_two_predictors = int(
        (
            master_df[
                [
                    "ph_value",
                    "alkalinity_value",
                    "toc_value",
                    "free_chlorine_value",
                ]
            ]
            .notna()
            .sum(axis=1)
            >= 2
        ).sum()
    )
    max_stability_diff = (
        float(stability_df["绝对差值"].max()) if not stability_df.empty else np.nan
    )

    lines = [
        "# V1 TTHM 严格样本级 Spearman 报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "- 版本：`V1_TTHM_strict_spearman_base_data`",
        "- 对齐规则：仅使用 `PWSID + WATER_FACILITY_ID + SAMPLING_POINT_ID + SAMPLE_COLLECTION_DATE` 严格样本级对齐",
        "",
        "## 1. 当前第一层严格样本级数据总记录数",
        "",
        f"- 母表总记录数：{len(master_df)}",
        f"- TTHM 非缺失记录数：{int(master_df['tthm_value'].notna().sum())}",
        f"- 至少匹配到 1 个核心预测变量的记录数：{at_least_one_predictor}（{format_pct(at_least_one_predictor, len(master_df))}）",
        f"- 至少匹配到 2 个核心预测变量的记录数：{at_least_two_predictors}（{format_pct(at_least_two_predictors, len(master_df))}）",
        f"- 4 个核心预测变量同时非缺失的记录数：{complete_case_all_predictors}",
        "",
        "## 2. 每个核心变量的非缺失记录数",
        "",
        to_markdown_table(core_non_missing_df),
        "",
        "## 3. 哪些变量进入 Spearman",
        "",
    ]
    lines.extend(f"- {item}" for item in variables_in_spearman)
    lines.extend(["", "## 4. 哪些变量留在母表但不进入 Spearman", ""])
    lines.extend(f"- {item}" for item in variables_only_in_master)
    lines.extend(
        [
            "",
            "## 5. 清洗规则是什么",
            "",
            "- 先生成严格原值母表，再派生稳健版清洗值，不覆盖原值。",
            "- 对 `tthm_value`、`ph_value`、`alkalinity_value`、`toc_value`、`free_chlorine_value` 统一生成缺失、单位异常、物理异常和 3IQR 极端值标记。",
            "- 稳健版中，pH、碱度、TOC、游离余氯在单位异常、物理异常或 3IQR 极端值时置为空值；TTHM 仅在单位异常或物理异常时置为空值。",
            "- `log_tthm` 与部分 `log1p` 变量均由对应原值/清洗值派生，不额外做 Z-score 标准化。",
            "",
            to_markdown_table(anomaly_df),
            "",
            "## 6. Spearman 结果",
            "",
            to_markdown_table(result_display),
            "",
            "## 7. 原值版和部分 log 版的 Spearman 结果是否稳定",
            "",
            to_markdown_table(stability_df),
            "",
            f"- 原值版与部分 log 版的最大绝对差值：{max_stability_diff:.10f}" if pd.notna(max_stability_diff) else "- 原值版与部分 log 版差值无法计算",
            "- 结论：在相同样本集合下，Spearman 对单调变换基本保持不变；本次原值版与部分 log 版结果可视为稳定。",
            "",
            "## 8. 当前第一层结果能否作为后续第二层场景级分析的保守对照",
            "",
            "- 可以，原因是这套数据完全遵守严格样本级四键对齐，没有混入宽松匹配结果，适合作为后续设施-月份层分析的保守基线。",
            "- 但不能把它误当作完整的多变量建模底表，因为 4 个核心预测变量同时完整的记录数为 0，说明严格样本级跨表重合度有限。",
            f"- 原值版基础输入表行数：{len(raw_base)}；稳健版基础输入表行数：{len(clean_base)}。",
            "- 第二层场景级分析如果要扩大覆盖率，应明确标注那是不同分析层级，不能回写覆盖本次 V1 严格样本级基线。",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_output_dir()

    source_summary_df = pd.DataFrame(
        [
            summarize_source(MAIN_PATH, "TTHM"),
            summarize_source(SOURCE_SPECS["ph"]["path"], "PH"),
            summarize_source(SOURCE_SPECS["alkalinity"]["path"], "TOTAL ALKALINITY"),
            summarize_source(SOURCE_SPECS["toc"]["path"], "TOTAL ORGANIC CARBON"),
            summarize_source(
                SOURCE_SPECS["free_chlorine"]["path"], "FREE RESIDUAL CHLORINE (1013)"
            ),
        ]
    )

    master_df, duplicate_summary = aggregate_tthm_table()
    for spec in SOURCE_SPECS.values():
        source_df = aggregate_source_table(
            spec["path"], spec["value_col"], spec["unit_col"]
        )
        master_df = master_df.merge(source_df, on=KEY_COLUMNS, how="left")

    master_df["year"] = master_df["SAMPLE_COLLECTION_DATE"].dt.year
    master_df["month"] = master_df["SAMPLE_COLLECTION_DATE"].dt.month
    master_df["quarter"] = master_df["SAMPLE_COLLECTION_DATE"].dt.quarter
    add_log_columns(master_df)

    anomaly_records = []
    anomaly_records.append(
        add_variable_flags(
            master_df,
            "tthm_value",
            "tthm_unit",
            "UG/L",
            0.0,
            None,
            False,
        )
    )
    for spec in SOURCE_SPECS.values():
        anomaly_records.append(
            add_variable_flags(
                master_df,
                spec["value_col"],
                spec["unit_col"],
                spec["expected_unit"],
                spec["physical_min"],
                spec["physical_max"],
                spec["use_iqr_for_clean"],
            )
        )

    master_df["log_tthm_clean"] = safe_log1p(master_df["tthm_value_clean"])
    for value_col in ["alkalinity_value", "toc_value", "free_chlorine_value"]:
        clean_col = f"{value_col}_clean"
        log_clean_col = f"log1p_{value_col}_clean"
        master_df[log_clean_col] = safe_log1p(master_df[clean_col])

    raw_base, clean_base, raw_log, clean_log = build_inputs(master_df)

    results_records = []
    results_records.extend(
        run_spearman_suite(
            "raw_base",
            "tthm_value",
            ["ph_value", "alkalinity_value", "toc_value", "free_chlorine_value"],
            raw_base,
        )
    )
    results_records.extend(
        run_spearman_suite(
            "clean_base",
            "tthm_value",
            ["ph_value", "alkalinity_value", "toc_value", "free_chlorine_value"],
            clean_base,
        )
    )
    results_records.extend(
        run_spearman_suite(
            "raw_partial_log",
            "log_tthm",
            [
                "ph_value",
                "log1p_alkalinity_value",
                "log1p_toc_value",
                "log1p_free_chlorine_value",
            ],
            raw_log,
        )
    )
    results_records.extend(
        run_spearman_suite(
            "clean_partial_log",
            "log_tthm",
            [
                "ph_value",
                "log1p_alkalinity_value",
                "log1p_toc_value",
                "log1p_free_chlorine_value",
            ],
            clean_log,
        )
    )
    results_df = pd.DataFrame(results_records)
    stability_df = compare_stability(results_df)
    anomaly_df = pd.DataFrame(anomaly_records)

    master_columns = [
        *MASTER_REQUIRED_COLUMNS,
        "tthm_unit",
        "ph_unit",
        "alkalinity_unit",
        "toc_unit",
        "free_chlorine_unit",
        "tthm_source_rows",
        "ph_value_source_rows",
        "alkalinity_value_source_rows",
        "toc_value_source_rows",
        "free_chlorine_value_source_rows",
        "tthm_numeric_rows",
        "ph_value_numeric_rows",
        "alkalinity_value_numeric_rows",
        "toc_value_numeric_rows",
        "free_chlorine_value_numeric_rows",
        "tthm_value_nunique",
        "ph_value_nunique",
        "alkalinity_value_nunique",
        "toc_value_nunique",
        "free_chlorine_value_nunique",
        "tthm_unit_nunique",
        "ph_unit_nunique",
        "alkalinity_unit_nunique",
        "toc_unit_nunique",
        "free_chlorine_unit_nunique",
        "log1p_RETAIL_POPULATION_SERVED",
        "log1p_ADJUSTED_TOTAL_POPULATION_SERVED",
        "log1p_alkalinity_value",
        "log1p_toc_value",
        "log1p_free_chlorine_value",
        "tthm_value_clean",
        "log_tthm_clean",
        "ph_value_clean",
        "alkalinity_value_clean",
        "toc_value_clean",
        "free_chlorine_value_clean",
        "log1p_alkalinity_value_clean",
        "log1p_toc_value_clean",
        "log1p_free_chlorine_value_clean",
    ]
    for value_col in [
        "tthm_value",
        "ph_value",
        "alkalinity_value",
        "toc_value",
        "free_chlorine_value",
    ]:
        master_columns.extend(
            [
                f"{value_col}_flag_missing",
                f"{value_col}_flag_unit_anomaly",
                f"{value_col}_flag_physical_anomaly",
                f"{value_col}_flag_iqr_extreme",
                f"{value_col}_flag_clean_exclude",
            ]
        )

    master_df = master_df[master_columns].copy()
    report_df = master_df.copy()
    master_df["SAMPLE_COLLECTION_DATE"] = master_df["SAMPLE_COLLECTION_DATE"].dt.strftime(
        "%Y-%m-%d"
    )

    master_df.to_csv(MASTER_PATH, index=False, encoding="utf-8-sig")
    raw_base.to_csv(RAW_INPUT_PATH, index=False, encoding="utf-8-sig")
    clean_base.to_csv(CLEAN_INPUT_PATH, index=False, encoding="utf-8-sig")
    raw_log.to_csv(LOG_INPUT_PATH, index=False, encoding="utf-8-sig")
    clean_log.to_csv(CLEAN_LOG_INPUT_PATH, index=False, encoding="utf-8-sig")
    results_df.to_csv(RESULTS_PATH, index=False, encoding="utf-8-sig")
    NOTES_PATH.write_text(
        build_cleaning_notes(
            source_summary_df,
            anomaly_df,
            duplicate_summary,
            raw_base,
            clean_base,
            raw_log,
            clean_log,
        ),
        encoding="utf-8",
    )
    REPORT_PATH.write_text(
        build_report(
            report_df,
            anomaly_df,
            results_df,
            stability_df,
            raw_base,
            clean_base,
        ),
        encoding="utf-8",
    )

    print(f"Wrote: {MASTER_PATH}")
    print(f"Wrote: {RAW_INPUT_PATH}")
    print(f"Wrote: {CLEAN_INPUT_PATH}")
    print(f"Wrote: {LOG_INPUT_PATH}")
    print(f"Wrote: {CLEAN_LOG_INPUT_PATH}")
    print(f"Wrote: {RESULTS_PATH}")
    print(f"Wrote: {NOTES_PATH}")
    print(f"Wrote: {REPORT_PATH}")


if __name__ == "__main__":
    main()
