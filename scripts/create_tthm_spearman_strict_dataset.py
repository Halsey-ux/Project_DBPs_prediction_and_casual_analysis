from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data_local" / "tthm_first_round"
SOURCE_PATH = DATA_DIR / "tthm_corechem_dataset.csv"
OUTPUT_PATH = DATA_DIR / "tthm_spearman_strict_dataset.csv"

KEY_COLUMNS = [
    "PWSID",
    "WATER_FACILITY_ID",
    "SAMPLING_POINT_ID",
    "SAMPLE_COLLECTION_DATE",
]

STRICT_VALUE_SPECS = {
    "ph_value": "ph_match_level",
    "alkalinity_value": "alkalinity_match_level",
    "toc_value": "toc_match_level",
    "free_chlorine_value": "free_chlorine_match_level",
}

KEEP_COLUMNS = [
    "PWSID",
    "WATER_FACILITY_ID",
    "SAMPLING_POINT_ID",
    "SAMPLE_COLLECTION_DATE",
    "year",
    "month",
    "quarter",
    "tthm_value",
    "log_tthm",
    "ph_value",
    "alkalinity_value",
    "toc_value",
    "free_chlorine_value",
    "strict_predictor_count",
    "strict_variable_set",
]


def main() -> None:
    df = pd.read_csv(SOURCE_PATH, low_memory=False)

    missing_keys = [column for column in KEY_COLUMNS if column not in df.columns]
    if missing_keys:
        raise ValueError(f"Missing first-layer key columns: {missing_keys}")

    for value_column, match_column in STRICT_VALUE_SPECS.items():
        if value_column not in df.columns or match_column not in df.columns:
            raise ValueError(f"Missing required columns: {value_column}, {match_column}")
        df.loc[df[match_column] != "strict", value_column] = pd.NA

    strict_presence = df[list(STRICT_VALUE_SPECS.keys())].notna()
    df["strict_predictor_count"] = strict_presence.sum(axis=1)
    df["strict_variable_set"] = strict_presence.apply(
        lambda row: "|".join(row.index[row].tolist()) if row.any() else pd.NA,
        axis=1,
    )

    spearman_df = df.loc[
        df["tthm_value"].notna() & (df["strict_predictor_count"] >= 1), KEEP_COLUMNS
    ].copy()

    spearman_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Wrote: {OUTPUT_PATH}")
    print(f"Rows: {len(spearman_df)}")
    print(
        "Strict predictor count distribution:",
        spearman_df["strict_predictor_count"].value_counts().sort_index().to_dict(),
    )


if __name__ == "__main__":
    main()
