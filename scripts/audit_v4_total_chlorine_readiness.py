from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from v4_tthm_training_common import build_binary_dataset, ensure_results_dir, load_base_dataframe


RESULT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Experiments" / "V4_4b" / "total_chlorine_readiness_audit"
FACILITY_MONTH_PATH = (
    PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build" / "V3_facility_month_master.csv"
)

TOTAL_CHLORINE_COLUMN = "total_chlorine_sample_weighted_mean_mg_l"
FREE_CHLORINE_COLUMN = "free_chlorine_sample_weighted_mean_mg_l"
PH_COLUMN = "ph_sample_weighted_mean"
ALKALINITY_COLUMN = "alkalinity_sample_weighted_mean_mg_l"
TOC_COLUMN = "toc_sample_weighted_mean_mg_l"

TASKS = [
    "tthm_regulatory_exceedance_prediction",
    "tthm_anchored_risk_prediction",
]
LEVELS = ["level1", "level2", "level3"]
COMPLETE_CASE_COLUMNS = [PH_COLUMN, ALKALINITY_COLUMN, TOC_COLUMN, TOTAL_CHLORINE_COLUMN]


def write_csv(df: pd.DataFrame, file_name: str) -> Path:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULT_DIR / file_name
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def build_level_coverage_summary(base_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for level in LEVELS:
        level_df = base_df.loc[base_df[f"{level}_flag"] == 1].copy()
        total_rows = len(level_df)
        total_non_missing = int(level_df[TOTAL_CHLORINE_COLUMN].notna().sum())
        free_non_missing = int(level_df[FREE_CHLORINE_COLUMN].notna().sum())
        complete_case_rows = int(level_df[COMPLETE_CASE_COLUMNS].notna().all(axis=1).sum())
        rows.append(
            {
                "dataset_scope": "pws_year",
                "level_name": level,
                "rows": total_rows,
                "total_chlorine_non_missing_rows": total_non_missing,
                "total_chlorine_non_missing_rate": float(total_non_missing / total_rows) if total_rows else 0.0,
                "free_chlorine_non_missing_rows": free_non_missing,
                "free_chlorine_non_missing_rate": float(free_non_missing / total_rows) if total_rows else 0.0,
                "total_vs_free_non_missing_ratio": (
                    float(total_non_missing / free_non_missing) if free_non_missing else pd.NA
                ),
                "ph_alkalinity_toc_total_chlorine_complete_case_rows": complete_case_rows,
                "ph_alkalinity_toc_total_chlorine_complete_case_rate": (
                    float(complete_case_rows / total_rows) if total_rows else 0.0
                ),
            }
        )
    return pd.DataFrame(rows)


def summarize_split_class_counts(df: pd.DataFrame) -> str:
    chunks: list[str] = []
    for split in ["train", "validation", "test"]:
        part = df.loc[df["split"] == split, "target_value"].astype(int)
        counts = part.value_counts().sort_index().to_dict()
        chunks.append(f"{split}={counts}")
    return "; ".join(chunks)


def build_task_level_readiness_summary(base_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for task_name in TASKS:
        for level in ["level2", "level3"]:
            dataset, target_column = build_binary_dataset(base_df, task_name=task_name, level_name=level)
            total_rows = len(dataset)
            total_non_missing = int(dataset[TOTAL_CHLORINE_COLUMN].notna().sum())
            free_non_missing = int(dataset[FREE_CHLORINE_COLUMN].notna().sum())

            complete_case_df = dataset.loc[dataset[COMPLETE_CASE_COLUMNS].notna().all(axis=1)].copy()
            split_class_counts = summarize_split_class_counts(complete_case_df) if not complete_case_df.empty else ""

            train_part = complete_case_df.loc[complete_case_df["split"] == "train", "target_value"]
            validation_part = complete_case_df.loc[complete_case_df["split"] == "validation", "target_value"]
            test_part = complete_case_df.loc[complete_case_df["split"] == "test", "target_value"]

            rows.append(
                {
                    "task_name": task_name,
                    "level_name": level,
                    "target_column": target_column,
                    "rows": total_rows,
                    "positive_count": int(dataset["target_value"].sum()),
                    "total_chlorine_non_missing_rows": total_non_missing,
                    "total_chlorine_non_missing_rate": float(total_non_missing / total_rows) if total_rows else 0.0,
                    "free_chlorine_non_missing_rows": free_non_missing,
                    "free_chlorine_non_missing_rate": float(free_non_missing / total_rows) if total_rows else 0.0,
                    "ph_alkalinity_toc_total_chlorine_complete_case_rows": int(len(complete_case_df)),
                    "ph_alkalinity_toc_total_chlorine_complete_case_rate": (
                        float(len(complete_case_df) / total_rows) if total_rows else 0.0
                    ),
                    "complete_case_train_rows": int(len(train_part)),
                    "complete_case_validation_rows": int(len(validation_part)),
                    "complete_case_test_rows": int(len(test_part)),
                    "complete_case_train_positive_count": int(train_part.sum()) if len(train_part) else 0,
                    "complete_case_validation_positive_count": int(validation_part.sum()) if len(validation_part) else 0,
                    "complete_case_test_positive_count": int(test_part.sum()) if len(test_part) else 0,
                    "complete_case_train_n_classes": int(train_part.nunique()) if len(train_part) else 0,
                    "complete_case_validation_n_classes": int(validation_part.nunique()) if len(validation_part) else 0,
                    "complete_case_test_n_classes": int(test_part.nunique()) if len(test_part) else 0,
                    "is_logistic_train_feasible_on_complete_case": bool(train_part.nunique() >= 2),
                    "split_class_counts_complete_case": split_class_counts,
                }
            )
    return pd.DataFrame(rows)


def build_missingness_signal_summary(base_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for task_name in TASKS:
        dataset, _ = build_binary_dataset(base_df, task_name=task_name, level_name="level2")
        total_observed = dataset.loc[dataset[TOTAL_CHLORINE_COLUMN].notna()].copy()
        total_missing = dataset.loc[dataset[TOTAL_CHLORINE_COLUMN].isna()].copy()
        rows.append(
            {
                "task_name": task_name,
                "level_name": "level2",
                "total_chlorine_observed_rows": int(len(total_observed)),
                "total_chlorine_missing_rows": int(len(total_missing)),
                "positive_rate_when_total_chlorine_observed": (
                    float(total_observed["target_value"].mean()) if not total_observed.empty else pd.NA
                ),
                "positive_rate_when_total_chlorine_missing": (
                    float(total_missing["target_value"].mean()) if not total_missing.empty else pd.NA
                ),
                "observed_positive_count": int(total_observed["target_value"].sum()) if not total_observed.empty else 0,
                "missing_positive_count": int(total_missing["target_value"].sum()) if not total_missing.empty else 0,
            }
        )
    return pd.DataFrame(rows)


def build_observed_value_summary(base_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for task_name in TASKS:
        dataset, _ = build_binary_dataset(base_df, task_name=task_name, level_name="level2")
        observed = dataset.loc[dataset[TOTAL_CHLORINE_COLUMN].notna()].copy()
        grouped = observed.groupby("target_value")[TOTAL_CHLORINE_COLUMN]
        for target_value, series in grouped:
            rows.append(
                {
                    "task_name": task_name,
                    "level_name": "level2",
                    "target_value": int(target_value),
                    "rows": int(series.shape[0]),
                    "mean_total_chlorine_mg_l": float(series.mean()),
                    "median_total_chlorine_mg_l": float(series.median()),
                    "min_total_chlorine_mg_l": float(series.min()),
                    "max_total_chlorine_mg_l": float(series.max()),
                }
            )
    return pd.DataFrame(rows)


def build_facility_month_summary() -> pd.DataFrame:
    usecols = [
        "pwsid",
        "water_facility_id",
        "year",
        "month",
        "tthm_mean_ug_l",
        "ph_mean",
        "alkalinity_mean_mg_l",
        "toc_mean_mg_l",
        "free_chlorine_mean_mg_l",
        "total_chlorine_mean_mg_l",
        "n_core_vars_available",
        "match_quality_tier",
    ]
    df = pd.read_csv(FACILITY_MONTH_PATH, encoding="utf-8-sig", usecols=usecols)
    rows_total = len(df)
    rows_with_tthm = int(df["tthm_mean_ug_l"].notna().sum())
    rows_with_total_chlorine = int(df["total_chlorine_mean_mg_l"].notna().sum())
    rows_with_tthm_and_total = int(df[["tthm_mean_ug_l", "total_chlorine_mean_mg_l"]].notna().all(axis=1).sum())
    rows_with_four_core_and_total = int(
        df[["tthm_mean_ug_l", "ph_mean", "alkalinity_mean_mg_l", "toc_mean_mg_l", "total_chlorine_mean_mg_l"]]
        .notna()
        .all(axis=1)
        .sum()
    )
    rows_with_four_core_and_free = int(
        df[["tthm_mean_ug_l", "ph_mean", "alkalinity_mean_mg_l", "toc_mean_mg_l", "free_chlorine_mean_mg_l"]]
        .notna()
        .all(axis=1)
        .sum()
    )
    return pd.DataFrame(
        [
            {
                "dataset_scope": "facility_month",
                "rows": rows_total,
                "rows_with_tthm": rows_with_tthm,
                "rows_with_total_chlorine": rows_with_total_chlorine,
                "rows_with_tthm_and_total_chlorine": rows_with_tthm_and_total,
                "rows_with_tthm_ph_alkalinity_toc_total_chlorine": rows_with_four_core_and_total,
                "rows_with_tthm_ph_alkalinity_toc_free_chlorine": rows_with_four_core_and_free,
                "total_chlorine_non_missing_rate": float(rows_with_total_chlorine / rows_total) if rows_total else 0.0,
                "tthm_and_total_chlorine_overlap_rate": float(rows_with_tthm_and_total / rows_total) if rows_total else 0.0,
                "tthm_four_core_total_chlorine_rate": float(rows_with_four_core_and_total / rows_total) if rows_total else 0.0,
                "tthm_four_core_free_chlorine_rate": float(rows_with_four_core_and_free / rows_total) if rows_total else 0.0,
            }
        ]
    )


def build_recommendation_table(
    level_coverage_df: pd.DataFrame,
    task_level_df: pd.DataFrame,
    facility_month_df: pd.DataFrame,
) -> pd.DataFrame:
    level2_total_non_missing = int(
        level_coverage_df.loc[level_coverage_df["level_name"] == "level2", "total_chlorine_non_missing_rows"].iloc[0]
    )
    level2_total_rate = float(
        level_coverage_df.loc[level_coverage_df["level_name"] == "level2", "total_chlorine_non_missing_rate"].iloc[0]
    )
    feasible_rows = int(task_level_df["is_logistic_train_feasible_on_complete_case"].sum())
    facility_overlap = int(facility_month_df["rows_with_tthm_and_total_chlorine"].iloc[0])
    recommendation = "do_not_start_v4_5_yet"
    rationale = (
        "total_chlorine 在 PWS-year level2 的覆盖率极低，且在 level2/level3 complete-case 下没有任何一个任务层级具备可合法训练 "
        "LogisticRegression 的 train split；更适合作为先补充审计、再决定是否推进的变量。"
    )
    return pd.DataFrame(
        [
            {
                "stage_name": "V4.4b",
                "audit_name": "total_chlorine_readiness_audit",
                "level2_total_chlorine_non_missing_rows": level2_total_non_missing,
                "level2_total_chlorine_non_missing_rate": level2_total_rate,
                "n_task_level_complete_case_train_feasible_rows": feasible_rows,
                "facility_month_tthm_total_chlorine_overlap_rows": facility_overlap,
                "recommendation": recommendation,
                "rationale": rationale,
            }
        ]
    )


def main() -> None:
    ensure_results_dir("V4_4b", "total_chlorine_readiness_audit")
    base_df = load_base_dataframe()

    level_coverage_df = build_level_coverage_summary(base_df)
    task_level_df = build_task_level_readiness_summary(base_df)
    missingness_df = build_missingness_signal_summary(base_df)
    observed_value_df = build_observed_value_summary(base_df)
    facility_month_df = build_facility_month_summary()
    recommendation_df = build_recommendation_table(level_coverage_df, task_level_df, facility_month_df)

    output_paths = [
        write_csv(level_coverage_df, "pws_year_level_total_chlorine_coverage_summary.csv"),
        write_csv(task_level_df, "task_level_total_chlorine_complete_case_readiness.csv"),
        write_csv(missingness_df, "level2_total_chlorine_missingness_signal_summary.csv"),
        write_csv(observed_value_df, "level2_total_chlorine_observed_value_summary.csv"),
        write_csv(facility_month_df, "facility_month_total_chlorine_overlap_summary.csv"),
        write_csv(recommendation_df, "v4_4b_total_chlorine_readiness_recommendation.csv"),
    ]

    print("Completed V4.4b total_chlorine readiness audit")
    for path in output_paths:
        print(f"Wrote: {path}")
    print(level_coverage_df.to_string(index=False))
    print(task_level_df.to_string(index=False))
    print(facility_month_df.to_string(index=False))
    print(recommendation_df.to_string(index=False))


if __name__ == "__main__":
    main()
