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
TOC_INCREMENT_FEATURES = MECHANISTIC_STAGE1_FEATURES + [
    "toc_sample_weighted_mean_mg_l",
    "toc_missing_flag",
]
COMPLETE_CASE_REFERENCE_COLUMNS = [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
    "toc_sample_weighted_mean_mg_l",
]
TOC_INCREMENT_COMPLETE_CASE_NO_FLAG_FEATURES = DEFAULT_BASELINE_FEATURES + [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
    "toc_sample_weighted_mean_mg_l",
]
BASELINE_WITHOUT_N_FACILITIES_FEATURES = [
    "system_type",
    "source_water_type",
    "retail_population_served",
]


def write_result_csv(task_dir: Path, file_name: str, result_df: pd.DataFrame) -> Path:
    output_path = task_dir / file_name
    result_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def main() -> None:
    base_df = load_base_dataframe()
    task_dir = ensure_results_dir("V4_3", TASK_NAME)

    experiment_configs = [
        {
            "file_name": "level2_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.3 level2 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level2_mechanistic_stage1_reference_v4_2_1_logistic_regression_results.csv",
            "feature_columns": MECHANISTIC_STAGE1_FEATURES,
            "feature_set": "mechanistic_stage1_reference_v4_2_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage1_reference_v4_2_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.3 reference run that reuses the V4.2.1 level2 mechanistic stage1 feature set",
        },
        {
            "file_name": "level2_toc_increment_v4_3_1_logistic_regression_results.csv",
            "feature_columns": TOC_INCREMENT_FEATURES,
            "feature_set": "mechanistic_stage2_toc_increment_v4_3_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage2_toc_increment_v4_3_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.3 main run on full level2 with TOC, toc_missing_flag, and median imputation",
        },
        {
            "file_name": "level2_complete_case_mechanistic_stage1_reference_logistic_regression_results.csv",
            "feature_columns": MECHANISTIC_STAGE1_FEATURES,
            "feature_set": "mechanistic_stage1_complete_case_reference",
            "required_complete_case_columns": COMPLETE_CASE_REFERENCE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage1_complete_case_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "Complete-case reference on rows where pH, alkalinity, and TOC are all observed, without adding TOC to the model",
        },
        {
            "file_name": "level2_complete_case_toc_increment_logistic_regression_results.csv",
            "feature_columns": TOC_INCREMENT_FEATURES,
            "feature_set": "mechanistic_stage2_toc_increment_complete_case",
            "required_complete_case_columns": COMPLETE_CASE_REFERENCE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage2_toc_increment_complete_case-logistic_regression-group_by_pwsid-v001",
            "notes": "Complete-case TOC increment run on rows where pH, alkalinity, and TOC are all observed",
        },
        {
            "file_name": "level2_complete_case_toc_increment_no_missing_flags_logistic_regression_results.csv",
            "feature_columns": TOC_INCREMENT_COMPLETE_CASE_NO_FLAG_FEATURES,
            "feature_set": "mechanistic_stage2_toc_increment_complete_case_no_missing_flags",
            "required_complete_case_columns": COMPLETE_CASE_REFERENCE_COLUMNS,
            "experiment_id": f"{TASK_NAME}-level2-mechanistic_stage2_toc_increment_complete_case_no_missing_flags-logistic_regression-group_by_pwsid-v001",
            "notes": "Complete-case sensitivity run without pH, alkalinity, or TOC missing flags",
        },
        {
            "file_name": "level2_baseline_without_n_facilities_sensitivity_logistic_regression_results.csv",
            "feature_columns": BASELINE_WITHOUT_N_FACILITIES_FEATURES,
            "feature_set": "baseline_without_n_facilities_sensitivity",
            "required_complete_case_columns": [],
            "experiment_id": f"{TASK_NAME}-level2-baseline_without_n_facilities_sensitivity-logistic_regression-group_by_pwsid-v001",
            "notes": "Light sensitivity check that removes n_facilities_in_master from the baseline feature set",
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
        "level2_toc_increment_experiment_summary.csv",
        summary_df,
    )

    print("Completed regulatory level2 TOC increment experiments")
    for path in written_paths + [summary_path]:
        print(f"Wrote: {path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
