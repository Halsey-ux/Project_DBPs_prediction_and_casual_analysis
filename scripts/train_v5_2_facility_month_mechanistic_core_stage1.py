from __future__ import annotations

from pathlib import Path

import pandas as pd

from io_v5_facility_month import FINAL_BASELINE_FEATURES, STAGE1_REQUIRED_COLUMNS
from v5_facility_month_training_common import ensure_results_dir, load_base_dataframe, run_binary_experiment


TASK_NAME = "tthm_high_risk_month_prediction"
MECHANISTIC_CORE_STAGE1_FEATURES = FINAL_BASELINE_FEATURES + STAGE1_REQUIRED_COLUMNS


def get_output_dir() -> Path:
    base_output_dir = ensure_results_dir().parent
    output_dir = base_output_dir / "V5_2"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_feature_set_registry() -> pd.DataFrame:
    rows = [
        {
            "feature_set": "baseline_core_minimal_stage1_reference",
            "feature_columns": ",".join(FINAL_BASELINE_FEATURES),
            "required_complete_case_columns": ",".join(STAGE1_REQUIRED_COLUMNS),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l",
            "role": "V5.2 同子样本 baseline 对照；严格沿用 V5.1 冻结版本。",
        },
        {
            "feature_set": "baseline_core_minimal_plus_ph_alkalinity",
            "feature_columns": ",".join(MECHANISTIC_CORE_STAGE1_FEATURES),
            "required_complete_case_columns": ",".join(STAGE1_REQUIRED_COLUMNS),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l",
            "role": "V5.2 正式机制核心 stage1 增强版本；在同子样本上加入 ph_mean 与 alkalinity_mean_mg_l。",
        },
    ]
    return pd.DataFrame(rows)


def build_metric_comparison(result_df: pd.DataFrame) -> pd.DataFrame:
    indexed = result_df.set_index("feature_set")
    reference = indexed.loc["baseline_core_minimal_stage1_reference"]
    enhanced = indexed.loc["baseline_core_minimal_plus_ph_alkalinity"]

    metrics = [
        "pr_auc",
        "roc_auc",
        "balanced_accuracy",
        "specificity",
        "mcc",
        "f1",
        "recall",
        "precision",
    ]
    splits = ["train", "validation", "test"]
    rows: list[dict[str, object]] = []
    for split_name in splits:
        for metric_name in metrics:
            reference_value = float(reference[f"{split_name}_{metric_name}"])
            enhanced_value = float(enhanced[f"{split_name}_{metric_name}"])
            rows.append(
                {
                    "split": split_name,
                    "metric": metric_name,
                    "baseline_core_minimal_stage1_reference": reference_value,
                    "baseline_core_minimal_plus_ph_alkalinity": enhanced_value,
                    "delta": enhanced_value - reference_value,
                }
            )

    return pd.DataFrame(rows)


def build_sample_summary(result_df: pd.DataFrame) -> pd.DataFrame:
    indexed = result_df.set_index("feature_set")
    rows: list[dict[str, object]] = []
    for feature_set in (
        "baseline_core_minimal_stage1_reference",
        "baseline_core_minimal_plus_ph_alkalinity",
    ):
        row = indexed.loc[feature_set]
        for split_name in ("train", "validation", "test"):
            total_rows = int(row[f"{split_name}_rows"])
            positive_rows = int(row[f"positive_count_{split_name}"])
            rows.append(
                {
                    "feature_set": feature_set,
                    "split": split_name,
                    "rows": total_rows,
                    "positive_rows": positive_rows,
                    "positive_rate": (positive_rows / total_rows) if total_rows else None,
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    output_dir = get_output_dir()
    result_path = output_dir / "v5_2_mechanistic_core_stage1_experiment_results.csv"
    feature_set_path = output_dir / "v5_2_mechanistic_core_stage1_feature_sets.csv"
    metric_comparison_path = output_dir / "v5_2_mechanistic_core_stage1_metric_comparison.csv"
    sample_summary_path = output_dir / "v5_2_mechanistic_core_stage1_sample_summary.csv"

    base_df = load_base_dataframe()
    experiments = [
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_minimal_stage1_reference",
            feature_columns=FINAL_BASELINE_FEATURES,
            required_complete_case_columns=STAGE1_REQUIRED_COLUMNS,
            sample_definition=(
                "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l"
            ),
            notes="V5.2 对照参考；严格沿用 V5.1 冻结的同子样本 baseline reference。",
            experiment_id=(
                "tthm_high_risk_month_prediction-"
                "baseline_core_minimal_stage1_reference-"
                "logistic_regression-group_by_pwsid-v001"
            ),
        ),
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_minimal_plus_ph_alkalinity",
            feature_columns=MECHANISTIC_CORE_STAGE1_FEATURES,
            required_complete_case_columns=STAGE1_REQUIRED_COLUMNS,
            sample_definition=(
                "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l"
            ),
            notes="V5.2 正式机制核心 stage1；在与 V5.1 stage1 reference 完全相同的子样本上加入 pH 与 alkalinity 数值字段。",
            experiment_id=(
                "tthm_high_risk_month_prediction-"
                "baseline_core_minimal_plus_ph_alkalinity-"
                "logistic_regression-group_by_pwsid-v001"
            ),
        ),
    ]

    result_df = pd.concat(experiments, ignore_index=True)
    feature_registry_df = build_feature_set_registry()
    metric_comparison_df = build_metric_comparison(result_df)
    sample_summary_df = build_sample_summary(result_df)

    result_df.to_csv(result_path, index=False, encoding="utf-8-sig")
    feature_registry_df.to_csv(feature_set_path, index=False, encoding="utf-8-sig")
    metric_comparison_df.to_csv(metric_comparison_path, index=False, encoding="utf-8-sig")
    sample_summary_df.to_csv(sample_summary_path, index=False, encoding="utf-8-sig")

    print("Completed V5.2 facility-month mechanistic core stage1 experiments")
    print(f"Wrote: {result_path}")
    print(f"Wrote: {feature_set_path}")
    print(f"Wrote: {metric_comparison_path}")
    print(f"Wrote: {sample_summary_path}")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()
