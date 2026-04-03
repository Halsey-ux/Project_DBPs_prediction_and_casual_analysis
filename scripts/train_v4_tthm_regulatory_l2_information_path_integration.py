from __future__ import annotations

from v4_7_information_path_integration_common import run_level2_information_path_experiments


TASK_NAME = "tthm_regulatory_exceedance_prediction"


def main() -> None:
    written_paths, summary_df = run_level2_information_path_experiments(TASK_NAME)

    print("Completed regulatory level2 information path integration experiments")
    for path in written_paths:
        print(f"Wrote: {path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
