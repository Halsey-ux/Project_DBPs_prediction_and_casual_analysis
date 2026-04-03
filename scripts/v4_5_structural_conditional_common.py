from __future__ import annotations

from pathlib import Path

import pandas as pd

from v4_tthm_training_common import (
    DEFAULT_BASELINE_FEATURES,
    ensure_results_dir,
    load_base_dataframe,
    run_binary_experiment,
)


STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES = DEFAULT_BASELINE_FEATURES + [
    "months_observed_any",
    "tthm_months_with_data",
    "months_with_1plus_core_vars",
    "months_with_2plus_core_vars",
    "months_with_3plus_core_vars",
    "n_core_vars_available",
    "annual_match_quality_tier",
]

STRUCTURAL_CONDITIONAL_WITHOUT_ANNUAL_MATCH_QUALITY_TIER_FEATURES = DEFAULT_BASELINE_FEATURES + [
    "months_observed_any",
    "tthm_months_with_data",
    "months_with_1plus_core_vars",
    "months_with_2plus_core_vars",
    "months_with_3plus_core_vars",
    "n_core_vars_available",
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


def build_level1_main_configs(task_name: str) -> list[dict[str, object]]:
    return [
        {
            "file_name": "level1_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 level1 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level1_structural_conditional_increment_v4_5_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
            "feature_set": "structural_conditional_increment_v4_5_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-structural_conditional_increment_v4_5_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 main run on full level1 with baseline features, coverage counts, and annual_match_quality_tier",
        },
        {
            "file_name": "level1_baseline_without_n_facilities_sensitivity_logistic_regression_results.csv",
            "feature_columns": BASELINE_WITHOUT_N_FACILITIES_FEATURES,
            "feature_set": "baseline_without_n_facilities_sensitivity",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-baseline_without_n_facilities_sensitivity-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 light sensitivity check that removes n_facilities_in_master from the level1 baseline feature set",
        },
        {
            "file_name": "level1_structural_conditional_without_annual_match_quality_tier_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_WITHOUT_ANNUAL_MATCH_QUALITY_TIER_FEATURES,
            "feature_set": "structural_conditional_without_annual_match_quality_tier",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-structural_conditional_without_annual_match_quality_tier-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 ablation run on full level1 with coverage counts but without annual_match_quality_tier",
        },
    ]


def build_level2_reference_configs(task_name: str) -> list[dict[str, object]]:
    return [
        {
            "file_name": "level2_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 level2 baseline reference with class_weight=balanced for comparison against level1",
        },
        {
            "file_name": "level2_structural_conditional_increment_v4_5_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
            "feature_set": "structural_conditional_increment_v4_5_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-structural_conditional_increment_v4_5_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 recommended level2 reference run with the same structural conditional feature set used on level1",
        },
        {
            "file_name": "level2_structural_conditional_without_annual_match_quality_tier_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_WITHOUT_ANNUAL_MATCH_QUALITY_TIER_FEATURES,
            "feature_set": "structural_conditional_without_annual_match_quality_tier",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-structural_conditional_without_annual_match_quality_tier-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.5 level2 ablation run with coverage counts but without annual_match_quality_tier",
        },
    ]


def run_experiment_configs(
    *,
    task_name: str,
    level_name: str,
    version_name: str,
    summary_file_name: str,
    experiment_configs: list[dict[str, object]],
) -> tuple[list[Path], pd.DataFrame]:
    base_df = load_base_dataframe()
    task_dir = ensure_results_dir(version_name, task_name)

    result_frames: list[pd.DataFrame] = []
    written_paths: list[Path] = []
    for config in experiment_configs:
        result_df = run_binary_experiment(
            base_df,
            task_name=task_name,
            level_name=level_name,
            feature_columns=config["feature_columns"],
            feature_set=config["feature_set"],
            notes=config["notes"],
            required_complete_case_columns=config["required_complete_case_columns"],
            experiment_id=config["experiment_id"],
        )
        written_paths.append(write_result_csv(task_dir, config["file_name"], result_df))
        result_frames.append(result_df)

    summary_df = pd.concat(result_frames, ignore_index=True)
    summary_path = write_result_csv(task_dir, summary_file_name, summary_df)
    written_paths.append(summary_path)
    return written_paths, summary_df
