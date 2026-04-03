from __future__ import annotations

import pandas as pd

from io_v4_ml_ready import TREATMENT_CONDITIONAL_FEATURES
from v4_5_structural_conditional_common import (
    STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
    run_experiment_configs,
)
from v4_tthm_training_common import DEFAULT_BASELINE_FEATURES


TREATMENT_SUMMARY_INCREMENT_V4_6_1_FEATURES = DEFAULT_BASELINE_FEATURES + TREATMENT_CONDITIONAL_FEATURES
STRUCTURAL_AND_TREATMENT_COMBINED_V4_6_1_FEATURES = (
    STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES + TREATMENT_CONDITIONAL_FEATURES
)


def build_level1_main_configs(task_name: str) -> list[dict[str, object]]:
    return [
        {
            "file_name": "level1_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level1 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level1_structural_conditional_reference_v4_5_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
            "feature_set": "structural_conditional_reference_v4_5_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-structural_conditional_reference_v4_5_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level1 structural conditional reference reused from V4.5 for treatment-summary comparison",
        },
        {
            "file_name": "level1_treatment_summary_increment_v4_6_1_logistic_regression_results.csv",
            "feature_columns": TREATMENT_SUMMARY_INCREMENT_V4_6_1_FEATURES,
            "feature_set": "treatment_summary_increment_v4_6_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-treatment_summary_increment_v4_6_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level1 treatment summary increment on top of the baseline feature set",
        },
        {
            "file_name": "level1_structural_and_treatment_combined_v4_6_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_AND_TREATMENT_COMBINED_V4_6_1_FEATURES,
            "feature_set": "structural_and_treatment_combined_v4_6_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level1-structural_and_treatment_combined_v4_6_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level1 combined run with structural conditional and treatment summary features",
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
            "notes": "V4.6 level2 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level2_structural_conditional_reference_v4_5_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
            "feature_set": "structural_conditional_reference_v4_5_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-structural_conditional_reference_v4_5_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level2 structural conditional reference reused from V4.5 for treatment-summary comparison",
        },
        {
            "file_name": "level2_treatment_summary_increment_v4_6_1_logistic_regression_results.csv",
            "feature_columns": TREATMENT_SUMMARY_INCREMENT_V4_6_1_FEATURES,
            "feature_set": "treatment_summary_increment_v4_6_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-treatment_summary_increment_v4_6_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level2 treatment summary increment on top of the baseline feature set",
        },
        {
            "file_name": "level2_structural_and_treatment_combined_v4_6_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_AND_TREATMENT_COMBINED_V4_6_1_FEATURES,
            "feature_set": "structural_and_treatment_combined_v4_6_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-structural_and_treatment_combined_v4_6_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.6 level2 combined run with structural conditional and treatment summary features",
        },
    ]


def run_level1_main_experiments(task_name: str) -> tuple[list[object], pd.DataFrame]:
    return run_experiment_configs(
        task_name=task_name,
        level_name="level1",
        version_name="V4_6",
        summary_file_name="level1_treatment_summary_increment_experiment_summary.csv",
        experiment_configs=build_level1_main_configs(task_name),
    )


def run_level2_reference_experiments(task_name: str) -> tuple[list[object], pd.DataFrame]:
    return run_experiment_configs(
        task_name=task_name,
        level_name="level2",
        version_name="V4_6",
        summary_file_name="level2_treatment_summary_increment_experiment_summary.csv",
        experiment_configs=build_level2_reference_configs(task_name),
    )
