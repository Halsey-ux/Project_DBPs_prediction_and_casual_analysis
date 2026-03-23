from __future__ import annotations

from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "tthm_first_round"
DATE_FORMAT = "%d-%b-%y"

MAIN_PATH = Path(
    r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv"
)

SOURCE_SPECS = {
    "ph": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\PH.csv"
        ),
        "label": "PH",
        "value_output_col": "ph_value",
        "unit_output_col": None,
    },
    "alkalinity": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ALKALINITY.csv"
        ),
        "label": "TOTAL ALKALINITY",
        "value_output_col": "alkalinity_value",
        "unit_output_col": "alkalinity_unit",
    },
    "toc": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ORGANIC CARBON.csv"
        ),
        "label": "TOTAL ORGANIC CARBON",
        "value_output_col": "toc_value",
        "unit_output_col": "toc_unit",
    },
    "free_chlorine": {
        "path": Path(
            r"D:\Syr4_Project\syr4_DATA_CSV\SYR4_Disinfectant Residuals\FREE RESIDUAL CHLORINE (1013).csv"
        ),
        "label": "FREE RESIDUAL CHLORINE (1013)",
        "value_output_col": "free_chlorine_value",
        "unit_output_col": "free_chlorine_unit",
    },
}

STRICT_KEYS = [
    "PWSID",
    "WATER_FACILITY_ID",
    "SAMPLING_POINT_ID",
    "SAMPLE_COLLECTION_DATE",
]
FACILITY_DAY_KEYS = ["PWSID", "WATER_FACILITY_ID", "SAMPLE_COLLECTION_DATE"]
KEY_COLUMNS = STRICT_KEYS

MAIN_BACKGROUND_COLUMNS = [
    "PWSID",
    "STATE_CODE",
    "SYSTEM_NAME",
    "SYSTEM_TYPE",
    "RETAIL_POPULATION_SERVED",
    "ADJUSTED_TOTAL_POPULATION_SERVED",
    "SOURCE_WATER_TYPE",
    "WATER_FACILITY_ID",
    "WATER_FACILITY_TYPE",
    "SAMPLING_POINT_ID",
    "SAMPLING_POINT_TYPE",
    "SAMPLE_TYPE_CODE",
    "SAMPLE_COLLECTION_DATE",
    "DETECT",
    "UNIT",
]
MAIN_EXTRA_COLUMNS = ["VALUE"]


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_string_series(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})


def parse_collection_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format=DATE_FORMAT, errors="coerce")


def build_dtype_map(columns: list[str]) -> dict[str, str]:
    dtype_map = {}
    for column in KEY_COLUMNS + ["STATE_CODE", "SYSTEM_TYPE", "SYSTEM_NAME", "SOURCE_WATER_TYPE", "WATER_FACILITY_TYPE", "SAMPLING_POINT_TYPE", "SAMPLE_TYPE_CODE", "DETECT", "UNIT", "VALUE", "ANALYTE_NAME", "DETECTION_LIMIT_UNIT"]:
        if column in columns:
            dtype_map[column] = "string"
    return dtype_map


def read_table(path: Path, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        usecols=columns,
        dtype=build_dtype_map(columns),
        low_memory=False,
    )
    for column in ["PWSID", "WATER_FACILITY_ID", "SAMPLING_POINT_ID"]:
        if column in df.columns:
            df[column] = clean_string_series(df[column])
    if "SAMPLE_COLLECTION_DATE" in df.columns:
        df["SAMPLE_COLLECTION_DATE"] = parse_collection_date(df["SAMPLE_COLLECTION_DATE"])
    if "UNIT" in df.columns:
        df["UNIT"] = clean_string_series(df["UNIT"])
    if "DETECTION_LIMIT_UNIT" in df.columns:
        df["DETECTION_LIMIT_UNIT"] = clean_string_series(df["DETECTION_LIMIT_UNIT"])
    if "VALUE" in df.columns:
        df["VALUE_NUM"] = pd.to_numeric(df["VALUE"], errors="coerce")
    return df


def audit_table(name: str, path: Path, reference_columns: list[str]) -> dict[str, object]:
    audit_columns = [
        "ANALYTE_NAME",
        "PWSID",
        "WATER_FACILITY_ID",
        "SAMPLING_POINT_ID",
        "SAMPLE_COLLECTION_DATE",
        "UNIT",
        "DETECTION_LIMIT_UNIT",
        "VALUE",
    ]
    df = read_table(path, audit_columns)
    columns_in_file = list(pd.read_csv(path, nrows=0).columns)
    top_units = clean_string_series(df["UNIT"]).dropna().value_counts().head(5).to_dict()
    top_detection_units = (
        clean_string_series(df["DETECTION_LIMIT_UNIT"])
        .dropna()
        .value_counts()
        .head(5)
        .to_dict()
    )
    analyte_names = clean_string_series(df["ANALYTE_NAME"]).dropna().value_counts().head(5).to_dict()
    return {
        "table_name": name,
        "path": str(path),
        "row_count": int(len(df)),
        "column_count": int(len(columns_in_file)),
        "same_columns_as_tthm": columns_in_file == reference_columns,
        "missing_pwsid": int(df["PWSID"].isna().sum()),
        "missing_water_facility_id": int(df["WATER_FACILITY_ID"].isna().sum()),
        "missing_sampling_point_id": int(df["SAMPLING_POINT_ID"].isna().sum()),
        "missing_sample_collection_date": int(df["SAMPLE_COLLECTION_DATE"].isna().sum()),
        "date_parse_failures": int(df["SAMPLE_COLLECTION_DATE"].isna().sum()),
        "strict_key_unique_rows": int(df[STRICT_KEYS].drop_duplicates().shape[0]),
        "facility_day_unique_rows": int(df[FACILITY_DAY_KEYS].drop_duplicates().shape[0]),
        "strict_key_duplicate_rows": int(df.duplicated(STRICT_KEYS).sum()),
        "facility_day_duplicate_rows": int(df.duplicated(FACILITY_DAY_KEYS).sum()),
        "non_numeric_value_rows": int(df["VALUE_NUM"].isna().sum()),
        "analyte_names_top5": "; ".join(
            f"{key}:{value}" for key, value in analyte_names.items()
        )
        or "NA",
        "unit_top5": "; ".join(f"{key}:{value}" for key, value in top_units.items())
        or "NA",
        "detection_limit_unit_top5": "; ".join(
            f"{key}:{value}" for key, value in top_detection_units.items()
        )
        or "NA",
    }


def aggregate_source(
    source_df: pd.DataFrame,
    group_keys: list[str],
    value_output_col: str,
    unit_output_col: str | None,
) -> pd.DataFrame:
    aggregation = {
        value_output_col: ("VALUE_NUM", "median"),
        "source_group_rows": ("VALUE_NUM", "size"),
    }
    if unit_output_col is not None:
        aggregation[unit_output_col] = ("UNIT", "first")
    return source_df.groupby(group_keys, dropna=False).agg(**aggregation).reset_index()


def merge_with_priority(
    base_df: pd.DataFrame,
    strict_agg: pd.DataFrame,
    facility_agg: pd.DataFrame,
    value_output_col: str,
    unit_output_col: str | None,
    match_prefix: str,
) -> tuple[pd.DataFrame, dict[str, int]]:
    strict_fields = [value_output_col, "source_group_rows"]
    if unit_output_col is not None:
        strict_fields.append(unit_output_col)

    strict_match = base_df[STRICT_KEYS].merge(
        strict_agg[STRICT_KEYS + strict_fields],
        on=STRICT_KEYS,
        how="left",
    )

    result = pd.DataFrame(index=base_df.index)
    result[value_output_col] = strict_match[value_output_col]
    if unit_output_col is not None:
        result[unit_output_col] = strict_match[unit_output_col]
    result[f"{match_prefix}_source_rows"] = strict_match["source_group_rows"]
    result[f"{match_prefix}_match_level"] = np.where(
        strict_match[value_output_col].notna(), "strict", pd.NA
    )

    strict_mask = result[value_output_col].notna()
    unmatched_index = base_df.index[~strict_mask]

    if len(unmatched_index) > 0:
        facility_fields = [value_output_col, "source_group_rows"]
        if unit_output_col is not None:
            facility_fields.append(unit_output_col)

        facility_match = base_df.loc[unmatched_index, FACILITY_DAY_KEYS].merge(
            facility_agg[FACILITY_DAY_KEYS + facility_fields],
            on=FACILITY_DAY_KEYS,
            how="left",
        )
        facility_mask = facility_match[value_output_col].notna().to_numpy()

        result.loc[unmatched_index, value_output_col] = facility_match[value_output_col].to_numpy()
        if unit_output_col is not None:
            result.loc[unmatched_index, unit_output_col] = facility_match[unit_output_col].to_numpy()
        result.loc[unmatched_index, f"{match_prefix}_source_rows"] = facility_match[
            "source_group_rows"
        ].to_numpy()
        result.loc[unmatched_index, f"{match_prefix}_match_level"] = np.where(
            facility_mask, "facility_day", pd.NA
        )

    merge_stats = {
        "strict_matches": int((result[f"{match_prefix}_match_level"] == "strict").sum()),
        "facility_day_matches": int(
            (result[f"{match_prefix}_match_level"] == "facility_day").sum()
        ),
    }
    merge_stats["total_matches"] = (
        merge_stats["strict_matches"] + merge_stats["facility_day_matches"]
    )
    return result, merge_stats


def compose_match_source(df: pd.DataFrame) -> pd.Series:
    output = pd.Series("", index=df.index, dtype="string")
    for source_name in SOURCE_SPECS:
        match_col = f"{source_name}_match_level"
        descriptor = np.where(
            df[match_col].notna(),
            f"{source_name}=" + df[match_col].astype("string"),
            "",
        )
        output = np.where(
            descriptor != "",
            np.where(output == "", descriptor, output + "|" + descriptor),
            output,
        )
    output = pd.Series(output, index=df.index, dtype="string")
    return output.mask(output == "", "none")


def to_markdown_table(df: pd.DataFrame) -> str:
    frame = df.copy()
    frame = frame.fillna("")
    headers = [str(column) for column in frame.columns]
    rows = [[str(value) for value in row] for row in frame.to_numpy().tolist()]
    separator = ["---"] * len(headers)
    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for row in rows:
        table_lines.append("| " + " | ".join(row) + " |")
    return "\n".join(table_lines)


def format_pct(numerator: int | float, denominator: int | float) -> str:
    if denominator == 0:
        return "0.00%"
    return f"{(numerator / denominator) * 100:.2f}%"


def build_report(
    audit_df: pd.DataFrame,
    match_summary_df: pd.DataFrame,
    missingness_df: pd.DataFrame,
    units_df: pd.DataFrame,
    combination_df: pd.DataFrame,
    corechem_df: pd.DataFrame,
    baseline_df: pd.DataFrame,
) -> str:
    total_rows = len(corechem_df)
    numeric_tthm_rows = int(corechem_df["tthm_value"].notna().sum())
    any_corechem_rows = int((corechem_df["matched_corechem_count"] > 0).sum())
    two_plus_rows = int((corechem_df["matched_corechem_count"] >= 2).sum())
    facility_day_rows = int((corechem_df["match_level"] == "facility_day").sum())
    strict_only_rows = int((corechem_df["match_level"] == "strict").sum())

    pair_counts = []
    for predictor in [
        "ph_value",
        "alkalinity_value",
        "toc_value",
        "free_chlorine_value",
    ]:
        pair_counts.append(
            {
                "variable": predictor,
                "pairwise_non_missing_with_tthm": int(
                    (corechem_df["tthm_value"].notna() & corechem_df[predictor].notna()).sum()
                ),
            }
        )
    pair_df = pd.DataFrame(pair_counts)

    analysis_judgement = [
        "Spearman: 可以进入下一步，但应以 pairwise complete 的探索性相关分析为主。",
        "Baseline ML: 只能做受限版本。`tthm_baseline_clean.csv` 采用 `tthm_value` 非缺失且至少 2 个核心化学变量非缺失的子集，适合做第一轮 baseline 和缺失机制评估。",
    ]
    if int((corechem_df["matched_corechem_count"] == 4).sum()) == 0:
        analysis_judgement.append(
            "4 个核心化学变量同时完整的记录数为 0，因此当前数据集不支持“四变量完整案例”模型。"
        )

    data_issues = [
        "5 张表字段结构一致，4 个关键键字段全部存在，日期格式均可按 `%d-%b-%y` 解析。",
        "各表存在同键重复记录，正式合并前必须先按键聚合；本脚本使用组内 `median` 作为首轮稳健汇总值。",
        "TTHM 与 4 个核心化学变量的跨表重合度偏低，严格匹配和同设施同日匹配合计覆盖率仍较低。",
        "PH 表的 `UNIT` 基本为空，因此本轮仅输出 `ph_value`，不强行构造 `ph_unit`。",
        "TOTAL ORGANIC CARBON 文件内 `ANALYTE_NAME` 主要显示为 `CARBON, TOTAL`，论文使用前建议再做一次语义核验。",
        "原始表中存在非数值 `VALUE` 记录；本轮未改写源数据，只在派生分析表中将无法解析的数值保留为缺失。",
    ]

    lines = [
        "# TTHM First-Round Core Chemistry Merge Report",
        "",
        f"- Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Output directory: `{OUTPUT_DIR}`",
        f"- Main table: `{MAIN_PATH}`",
        "",
        "## 1. Scope",
        "",
        "This round is intentionally limited to `TTHM + PH + TOTAL ALKALINITY + TOTAL ORGANIC CARBON + FREE RESIDUAL CHLORINE`.",
        "It is designed for first-round Spearman screening, feature screening, and constrained baseline machine learning.",
        "",
        "## 2. Alignment rules",
        "",
        "Priority 1: strict key match on `PWSID + WATER_FACILITY_ID + SAMPLING_POINT_ID + SAMPLE_COLLECTION_DATE`.",
        "Priority 2: facility-day match on `PWSID + WATER_FACILITY_ID + SAMPLE_COLLECTION_DATE`.",
        "No month-level or quarter-level relaxation is used in this round.",
        "",
        "## 3. Field compatibility audit",
        "",
        to_markdown_table(audit_df),
        "",
        "## 4. Merge summary",
        "",
        to_markdown_table(match_summary_df),
        "",
        "## 5. Missingness of analysis columns",
        "",
        to_markdown_table(missingness_df),
        "",
        "## 6. Unit situation",
        "",
        to_markdown_table(units_df),
        "",
        "## 7. Predictor overlap with numeric TTHM",
        "",
        to_markdown_table(pair_df),
        "",
        "## 8. Predictor combination counts",
        "",
        to_markdown_table(combination_df),
        "",
        "## 9. Dataset readiness",
        "",
        f"- Total TTHM rows in merged dataset: {total_rows}",
        f"- Numeric `tthm_value` rows: {numeric_tthm_rows} ({format_pct(numeric_tthm_rows, total_rows)})",
        f"- Rows with at least 1 matched core chemistry variable: {any_corechem_rows} ({format_pct(any_corechem_rows, total_rows)})",
        f"- Rows with at least 2 matched core chemistry variables: {two_plus_rows} ({format_pct(two_plus_rows, total_rows)})",
        f"- Rows using only strict matches: {strict_only_rows} ({format_pct(strict_only_rows, total_rows)})",
        f"- Rows involving facility-day fallback: {facility_day_rows} ({format_pct(facility_day_rows, total_rows)})",
        f"- `tthm_baseline_clean.csv` rows: {len(baseline_df)}",
        "",
        "## 10. Important data issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in data_issues)
    lines.extend(
        [
            "",
            "## 11. Judgement for next analysis step",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in analysis_judgement)
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_output_dir()

    reference_columns = list(pd.read_csv(MAIN_PATH, nrows=0).columns)
    audit_records = [audit_table("tthm", MAIN_PATH, reference_columns)]
    for source_name, spec in SOURCE_SPECS.items():
        audit_records.append(audit_table(source_name, spec["path"], reference_columns))
    audit_df = pd.DataFrame(audit_records)

    main_df = read_table(MAIN_PATH, MAIN_BACKGROUND_COLUMNS + MAIN_EXTRA_COLUMNS).copy()
    main_df = main_df.rename(columns={"VALUE": "tthm_value_raw"})
    main_df["tthm_value"] = pd.to_numeric(main_df["tthm_value_raw"], errors="coerce")
    main_df["year"] = main_df["SAMPLE_COLLECTION_DATE"].dt.year
    main_df["month"] = main_df["SAMPLE_COLLECTION_DATE"].dt.month
    main_df["quarter"] = main_df["SAMPLE_COLLECTION_DATE"].dt.quarter
    main_df["log_tthm"] = np.where(
        main_df["tthm_value"].notna(), np.log1p(main_df["tthm_value"]), np.nan
    )

    corechem_df = main_df[MAIN_BACKGROUND_COLUMNS].copy()
    corechem_df["tthm_value"] = main_df["tthm_value"]
    corechem_df["year"] = main_df["year"]
    corechem_df["month"] = main_df["month"]
    corechem_df["quarter"] = main_df["quarter"]
    corechem_df["log_tthm"] = main_df["log_tthm"]

    match_summary_records = []
    units_records = []

    for source_name, spec in SOURCE_SPECS.items():
        source_df = read_table(
            spec["path"],
            ["PWSID", "WATER_FACILITY_ID", "SAMPLING_POINT_ID", "SAMPLE_COLLECTION_DATE", "UNIT", "VALUE"],
        )
        strict_agg = aggregate_source(
            source_df,
            STRICT_KEYS,
            spec["value_output_col"],
            spec["unit_output_col"],
        )
        facility_agg = aggregate_source(
            source_df,
            FACILITY_DAY_KEYS,
            spec["value_output_col"],
            spec["unit_output_col"],
        )
        merged_columns, merge_stats = merge_with_priority(
            corechem_df,
            strict_agg,
            facility_agg,
            spec["value_output_col"],
            spec["unit_output_col"],
            source_name,
        )
        for column in merged_columns.columns:
            corechem_df[column] = merged_columns[column]

        source_total_rows = len(source_df)
        units_top = clean_string_series(source_df["UNIT"]).dropna().value_counts().head(5).to_dict()
        units_records.append(
            {
                "source": source_name,
                "raw_unit_top5": "; ".join(f"{key}:{value}" for key, value in units_top.items())
                or "NA",
                "merged_unit_non_missing": int(corechem_df.get(spec["unit_output_col"], pd.Series(dtype="object")).notna().sum())
                if spec["unit_output_col"]
                else 0,
            }
        )
        match_summary_records.append(
            {
                "source": source_name,
                "source_total_rows": int(source_total_rows),
                "strict_matched_tthm_rows": merge_stats["strict_matches"],
                "facility_day_matched_tthm_rows": merge_stats["facility_day_matches"],
                "total_matched_tthm_rows": merge_stats["total_matches"],
                "match_ratio_vs_tthm_rows": format_pct(merge_stats["total_matches"], len(corechem_df)),
                "match_rule_used": "strict + facility_day fallback",
            }
        )

    match_cols = [f"{source_name}_match_level" for source_name in SOURCE_SPECS]
    corechem_df["matched_corechem_count"] = corechem_df[match_cols].notna().sum(axis=1)
    corechem_df["match_level"] = np.select(
        [
            corechem_df["matched_corechem_count"] == 0,
            corechem_df[match_cols].eq("facility_day").any(axis=1),
        ],
        ["unmatched", "facility_day"],
        default="strict",
    )
    corechem_df["match_source"] = compose_match_source(corechem_df)
    corechem_df["SAMPLE_COLLECTION_DATE"] = corechem_df["SAMPLE_COLLECTION_DATE"].dt.strftime(
        "%Y-%m-%d"
    )

    ordered_columns = [
        "PWSID",
        "STATE_CODE",
        "SYSTEM_NAME",
        "SYSTEM_TYPE",
        "RETAIL_POPULATION_SERVED",
        "ADJUSTED_TOTAL_POPULATION_SERVED",
        "SOURCE_WATER_TYPE",
        "WATER_FACILITY_ID",
        "WATER_FACILITY_TYPE",
        "SAMPLING_POINT_ID",
        "SAMPLING_POINT_TYPE",
        "SAMPLE_TYPE_CODE",
        "SAMPLE_COLLECTION_DATE",
        "DETECT",
        "UNIT",
        "tthm_value",
        "year",
        "month",
        "quarter",
        "log_tthm",
        "ph_value",
        "alkalinity_value",
        "alkalinity_unit",
        "toc_value",
        "toc_unit",
        "free_chlorine_value",
        "free_chlorine_unit",
        "match_level",
        "match_source",
        "matched_corechem_count",
        "ph_match_level",
        "alkalinity_match_level",
        "toc_match_level",
        "free_chlorine_match_level",
        "ph_source_rows",
        "alkalinity_source_rows",
        "toc_source_rows",
        "free_chlorine_source_rows",
    ]
    corechem_df = corechem_df[ordered_columns]

    baseline_df = corechem_df.loc[
        corechem_df["tthm_value"].notna() & (corechem_df["matched_corechem_count"] >= 2)
    ].copy()

    missingness_columns = [
        "tthm_value",
        "ph_value",
        "alkalinity_value",
        "alkalinity_unit",
        "toc_value",
        "toc_unit",
        "free_chlorine_value",
        "free_chlorine_unit",
        "match_level",
    ]
    missingness_df = pd.DataFrame(
        [
            {
                "column": column,
                "missing_count": int(corechem_df[column].isna().sum()),
                "missing_rate": format_pct(int(corechem_df[column].isna().sum()), len(corechem_df)),
            }
            for column in missingness_columns
        ]
    )

    combination_df = (
        corechem_df.loc[corechem_df["tthm_value"].notna(), [
            "ph_value",
            "alkalinity_value",
            "toc_value",
            "free_chlorine_value",
        ]]
        .notna()
        .astype(int)
        .astype(str)
        .agg("".join, axis=1)
        .value_counts()
        .rename_axis("pattern_ph_alk_toc_fcl")
        .reset_index(name="row_count")
    )

    match_summary_df = pd.DataFrame(match_summary_records)
    units_df = pd.DataFrame(units_records)

    corechem_path = OUTPUT_DIR / "tthm_corechem_dataset.csv"
    baseline_path = OUTPUT_DIR / "tthm_baseline_clean.csv"
    report_path = OUTPUT_DIR / "tthm_corechem_merge_report.md"
    audit_path = OUTPUT_DIR / "tthm_field_audit.csv"
    missingness_path = OUTPUT_DIR / "tthm_missingness_summary.csv"
    match_summary_path = OUTPUT_DIR / "tthm_match_summary.csv"
    combinations_path = OUTPUT_DIR / "tthm_predictor_combinations.csv"

    corechem_df.to_csv(corechem_path, index=False)
    baseline_df.to_csv(baseline_path, index=False)
    audit_df.to_csv(audit_path, index=False)
    missingness_df.to_csv(missingness_path, index=False)
    match_summary_df.to_csv(match_summary_path, index=False)
    combination_df.to_csv(combinations_path, index=False)
    report_path.write_text(
        build_report(
            audit_df,
            match_summary_df,
            missingness_df,
            units_df,
            combination_df.head(10),
            corechem_df,
            baseline_df,
        ),
        encoding="utf-8",
    )

    print(f"Wrote: {corechem_path}")
    print(f"Wrote: {baseline_path}")
    print(f"Wrote: {report_path}")
    print(f"Wrote: {audit_path}")
    print(f"Wrote: {missingness_path}")
    print(f"Wrote: {match_summary_path}")
    print(f"Wrote: {combinations_path}")


if __name__ == "__main__":
    main()
