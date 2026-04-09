from __future__ import annotations

import pandas as pd

from io_v5_facility_month import (
    BASELINE_CORE_MINIMAL_FEATURES,
    BASELINE_CORE_PLUS_WATER_FACILITY_TYPE_FEATURES,
    BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES,
    FINAL_BASELINE_FEATURES,
    STAGE1_REQUIRED_COLUMNS,
)
from v5_facility_month_training_common import ensure_results_dir, load_base_dataframe, run_binary_experiment


TASK_NAME = "tthm_high_risk_month_prediction"


def build_feature_set_registry() -> pd.DataFrame:
    rows = [
        {
            "feature_set": "baseline_core_minimal",
            "feature_columns": ",".join(BASELINE_CORE_MINIMAL_FEATURES),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set",
            "role": "用于判断 has_treatment_summary 是否值得进入正式 baseline 之前的最小稳定结构底座",
        },
        {
            "feature_set": "baseline_core_with_has_treatment_summary",
            "feature_columns": ",".join(BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set",
            "role": "条件性 baseline 对照；用于判断 has_treatment_summary 是否值得进入正式 baseline",
        },
        {
            "feature_set": "baseline_core_plus_water_facility_type",
            "feature_columns": ",".join(BASELINE_CORE_PLUS_WATER_FACILITY_TYPE_FEATURES),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set",
            "role": "条件性 baseline 对照；用于判断 water_facility_type 是否值得进入正式 baseline",
        },
        {
            "feature_set": "baseline_core_minimal_stage1_reference",
            "feature_columns": ",".join(FINAL_BASELINE_FEATURES),
            "sample_definition": "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l",
            "role": "为 V5.2 baseline + pH + alkalinity 提供同子样本 baseline reference",
        },
    ]
    return pd.DataFrame(rows)


def main() -> None:
    output_dir = ensure_results_dir()
    result_path = output_dir / "v5_1_baseline_experiment_results.csv"
    feature_set_path = output_dir / "v5_1_baseline_feature_sets.csv"

    base_df = load_base_dataframe()
    experiments = [
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_minimal",
            feature_columns=BASELINE_CORE_MINIMAL_FEATURES,
            sample_definition="target_non_missing_and_complete_case_on_feature_set",
            notes="最小稳定结构 baseline；不含 has_treatment_summary 与 water_facility_type。",
        ),
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_with_has_treatment_summary",
            feature_columns=BASELINE_CORE_WITH_HAS_TREATMENT_SUMMARY_FEATURES,
            sample_definition="target_non_missing_and_complete_case_on_feature_set",
            notes="条件性 baseline 对照；用于判断 has_treatment_summary 是否值得进入正式 baseline。",
        ),
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_plus_water_facility_type",
            feature_columns=BASELINE_CORE_PLUS_WATER_FACILITY_TYPE_FEATURES,
            sample_definition="target_non_missing_and_complete_case_on_feature_set",
            notes="条件性 baseline 对照；用于判断 water_facility_type 是否值得进入正式 baseline。",
        ),
        run_binary_experiment(
            base_df,
            task_name=TASK_NAME,
            feature_set="baseline_core_minimal_stage1_reference",
            feature_columns=FINAL_BASELINE_FEATURES,
            required_complete_case_columns=STAGE1_REQUIRED_COLUMNS,
            sample_definition=(
                "target_non_missing_and_complete_case_on_feature_set_and_ph_mean_and_alkalinity_mean_mg_l"
            ),
            notes="V5.2 对照参考；只使用最终正式 baseline 特征，但样本限制在 pH + alkalinity 可用子集。",
        ),
    ]

    result_df = pd.concat(experiments, ignore_index=True)
    feature_registry_df = build_feature_set_registry()

    result_df.to_csv(result_path, index=False, encoding="utf-8-sig")
    feature_registry_df.to_csv(feature_set_path, index=False, encoding="utf-8-sig")

    print("Completed V5.1 facility-month baseline experiments")
    print(f"Wrote: {result_path}")
    print(f"Wrote: {feature_set_path}")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()
