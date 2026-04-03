from __future__ import annotations

import pandas as pd

from v4_5_structural_conditional_common import (
    STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
    run_experiment_configs,
)
from v4_6_treatment_summary_common import (
    STRUCTURAL_AND_TREATMENT_COMBINED_V4_6_1_FEATURES,
    TREATMENT_SUMMARY_INCREMENT_V4_6_1_FEATURES,
)
from v4_tthm_training_common import DEFAULT_BASELINE_FEATURES


WATER_QUALITY_INCREMENT_V4_7_1_FEATURES = [
    "ph_sample_weighted_mean",
    "alkalinity_sample_weighted_mean_mg_l",
    "toc_sample_weighted_mean_mg_l",
    "ph_missing_flag",
    "alkalinity_missing_flag",
    "toc_missing_flag",
]


def merge_feature_groups(*feature_groups: list[str]) -> list[str]:
    merged: list[str] = []
    for feature_group in feature_groups:
        for feature_name in feature_group:
            if feature_name not in merged:
                merged.append(feature_name)
    return merged


WATER_QUALITY_REFERENCE_V4_7_1_FEATURES = merge_feature_groups(
    DEFAULT_BASELINE_FEATURES,
    WATER_QUALITY_INCREMENT_V4_7_1_FEATURES,
)

SYSTEM_BACKGROUND_REFERENCE_V4_7_1_FEATURES = STRUCTURAL_AND_TREATMENT_COMBINED_V4_6_1_FEATURES

FULL_INTEGRATION_V4_7_1_FEATURES = merge_feature_groups(
    SYSTEM_BACKGROUND_REFERENCE_V4_7_1_FEATURES,
    WATER_QUALITY_INCREMENT_V4_7_1_FEATURES,
)

STRUCTURAL_AND_WATER_QUALITY_V4_7_1_FEATURES = merge_feature_groups(
    STRUCTURAL_CONDITIONAL_INCREMENT_V4_5_1_FEATURES,
    WATER_QUALITY_INCREMENT_V4_7_1_FEATURES,
)

TREATMENT_AND_WATER_QUALITY_V4_7_1_FEATURES = merge_feature_groups(
    TREATMENT_SUMMARY_INCREMENT_V4_6_1_FEATURES,
    WATER_QUALITY_INCREMENT_V4_7_1_FEATURES,
)


def build_level2_information_path_configs(task_name: str) -> list[dict[str, object]]:
    return [
        {
            "file_name": "level2_baseline_reference_logistic_regression_results.csv",
            "feature_columns": DEFAULT_BASELINE_FEATURES,
            "feature_set": "baseline_default_reference",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-baseline_default_reference-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 baseline reference with class_weight=balanced",
        },
        {
            "file_name": "level2_water_quality_reference_v4_7_1_logistic_regression_results.csv",
            "feature_columns": WATER_QUALITY_REFERENCE_V4_7_1_FEATURES,
            "feature_set": "water_quality_reference_v4_7_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-water_quality_reference_v4_7_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 water-quality reference with baseline, pH, alkalinity, TOC, and missing flags",
        },
        {
            "file_name": "level2_system_background_reference_v4_7_1_logistic_regression_results.csv",
            "feature_columns": SYSTEM_BACKGROUND_REFERENCE_V4_7_1_FEATURES,
            "feature_set": "system_background_reference_v4_7_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-system_background_reference_v4_7_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 system-background reference with baseline, structural conditional, and treatment summary features",
        },
        {
            "file_name": "level2_structural_and_water_quality_v4_7_1_logistic_regression_results.csv",
            "feature_columns": STRUCTURAL_AND_WATER_QUALITY_V4_7_1_FEATURES,
            "feature_set": "structural_and_water_quality_v4_7_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-structural_and_water_quality_v4_7_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 ablation with structural conditional and water-quality features but without treatment summary",
        },
        {
            "file_name": "level2_treatment_and_water_quality_v4_7_1_logistic_regression_results.csv",
            "feature_columns": TREATMENT_AND_WATER_QUALITY_V4_7_1_FEATURES,
            "feature_set": "treatment_and_water_quality_v4_7_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-treatment_and_water_quality_v4_7_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 ablation with treatment summary and water-quality features but without structural conditional features",
        },
        {
            "file_name": "level2_full_integration_v4_7_1_logistic_regression_results.csv",
            "feature_columns": FULL_INTEGRATION_V4_7_1_FEATURES,
            "feature_set": "full_integration_v4_7_1",
            "required_complete_case_columns": [],
            "experiment_id": f"{task_name}-level2-full_integration_v4_7_1-logistic_regression-group_by_pwsid-v001",
            "notes": "V4.7 level2 full integration run with system-background and water-quality information paths combined",
        },
    ]


def run_level2_information_path_experiments(task_name: str) -> tuple[list[object], pd.DataFrame]:
    return run_experiment_configs(
        task_name=task_name,
        level_name="level2",
        version_name="V4_7",
        summary_file_name="level2_information_path_integration_experiment_summary.csv",
        experiment_configs=build_level2_information_path_configs(task_name),
    )
