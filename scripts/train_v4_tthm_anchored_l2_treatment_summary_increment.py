from __future__ import annotations

from v4_6_treatment_summary_common import run_level2_reference_experiments


TASK_NAME = "tthm_anchored_risk_prediction"


def main() -> None:
    written_paths, summary_df = run_level2_reference_experiments(TASK_NAME)

    print("Completed anchored level2 treatment summary increment reference experiments")
    for path in written_paths:
        print(f"Wrote: {path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
