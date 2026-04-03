from __future__ import annotations

from pathlib import Path

import pandas as pd

from v4_tthm_training_common import DEFAULT_BASELINE_FEATURES, ensure_results_dir, load_base_dataframe, run_binary_experiment


TASK_NAME = "tthm_regulatory_exceedance_prediction"
MECHANISTIC_STAGE1_FEATURES = DEFAULT_BASELINE_FEATURES + [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
    "ph_missing_flag",
    "alkalinity_missing_flag",
]
MECHANISTIC_STAGE1_COMPLETE_CASE_NO_FLAG_FEATURES = DEFAULT_BASELINE_FEATURES + [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
]
REQUIRED_COMPLETE_CASE_COLUMNS = [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
]


def write_result_csv(task_dir: Path, file_name: str, result_df: pd.DataFrame) -> Path:
    output_path = task_dir / file_name
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def main() -> None:
    base_df = load_base_dataframe()
    task_dir = ensure_results_dir(TASK_NAME)

    experiment_configs = [
        {
            "file_name": "level2_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "level2 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level2_mechanistic_stage1_v4_2_1_logistic_regression_results.csv",
            "feature_columns": MECHANISTIC_STAGE1_FEATURES,
            "feature_set": "mechanistic_stage1_v4_2_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage1_v4_2_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.2.1 level2 mechanistic stage1 with pH, alkalinity, and missing flags",
        },
        {
            "file_name": "level2_complete_case_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_complete_case_reference",
            "required_complete_case_columns": REQUIRED_COMPLETE_CASE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-baseline_default_complete_case_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "level2 complete-case baseline reference on rows with both pH and alkalinity observed",
        },
        {
            "file_name": "level2_mechanistic_stage1_complete_case_v4_2_2_logistic_regression_results.csv",
            "feature_columns": MECHANISTIC_STAGE1_FEATURES,
            "feature_set": "mechanistic_stage1_complete_case_v4_2_2",
            "required_complete_case_columns": REQUIRED_COMPLETE_CASE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage1_complete_case_v4_2_2-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.2.2 complete-case robustness run on rows with both pH and alkalinity observed",
        },
        {
            "file_name": "level2_mechanistic_stage1_complete_case_no_missing_flags_logistic_regression_results.csv",
            "feature_columns": MECHANISTIC_STAGE1_COMPLETE_CASE_NO_FLAG_FEATURES,
            "feature_set": "mechanistic_stage1_complete_case_no_missing_flags",
            "required_complete_case_columns": REQUIRED_COMPLETE_CASE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage1_complete_case_no_missing_flags-logistic_regression-group_by_pwsid-v001",
            "notes": "Complete-case sensitivity run without missing flags on rows with both pH and alkalinity observed",
        },
    ]

    result_frames: list[pd.DataFrame] = []
    written_paths: list[Path] = []
    for config in experiment_configs:
        result_df = run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            level_name="level2",
            feature_columns=config["feature_columns"],
            feature_set=config["feature_set"],
            notes=config["notes"],
            required_complete_case_columns=config["required_complete_case_columns"],
            experiment_id=config["experiment_id"],
        )
        written_paths.append(write_result_csv(task_dir, config["file_name"], result_df))
        result_frames.append(result_df)

    summary_df = pd.concat(result_frames, ignore_index=True)
    summary_path = write_result_csv(
        task_dir,
        "level2_mechanistic_stage1_experiment_summary.csv",
        summary_df,
    )

    print("Completed regulatory level2 mechanistic stage1 experiments")
    for path in written_paths + [summary_path]:
        print(f"Wrote: {path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
