from __future__ import annotations

from v4_5_structural_conditional_common import build_level2_reference_configs, run_experiment_configs


TASK_NAME = "tthm_regulatory_exceedance_prediction"
LEVEL_NAME = "level2"
SUMMARY_FILE_NAME = "level2_structural_conditional_reference_summary.csv"


def main() -> None:
    written_paths, summary_df = run_experiment_configs(
        task_name=TASK_NAME,
        level_name=LEVEL_NAME,
        version_name="V4_5",
        summary_file_name=SUMMARY_FILE_NAME,
        experiment_configs=build_level2_reference_configs(TASK_NAME),
    )

    print("Completed regulatory level2 structural conditional reference experiments")
    for path in written_paths:
        print(f"Wrote: {path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
