from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from io_v4_ml_ready import build_tthm_anchored_risk_label, read_v4_ml_ready_csv, validate_v4_ml_ready_schema


INPUT_PATH = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready" / "V4_pws_year_ml_ready.csv"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Splits"
MASTER_SPLIT_PATH = OUTPUT_DIR / "v4_group_by_pwsid_master_split.csv"
REGULATORY_SPLIT_PATH = OUTPUT_DIR / "v4_tthm_regulatory_exceedance_level1_split_index.csv"
ANCHORED_SPLIT_PATH = OUTPUT_DIR / "v4_tthm_anchored_risk_level1_split_index.csv"
SUMMARY_PATH = OUTPUT_DIR / "v4_tthm_split_summary.md"

TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15
RANDOM_SEED = 42
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_master_group_split(df: pd.DataFrame) -> pd.DataFrame:
    unique_pwsid = pd.Series(df["pwsid"].dropna().unique(), name="pwsid")
    shuffled = unique_pwsid.iloc[np.random.default_rng(RANDOM_SEED).permutation(len(unique_pwsid))].reset_index(drop=True)
    n_total = len(shuffled)
    n_train = int(round(n_total * TRAIN_SIZE))
    n_validation = int(round(n_total * VALIDATION_SIZE))
    n_test = n_total - n_train - n_validation
    train_pwsid = shuffled.iloc[:n_train]
    validation_pwsid = shuffled.iloc[n_train : n_train + n_validation]
    test_pwsid = shuffled.iloc[n_train + n_validation : n_train + n_validation + n_test]

    rows = []
    for split_name, values in [
        ("train", train_pwsid),
        ("validation", validation_pwsid),
        ("test", test_pwsid),
    ]:
        for pwsid in values.tolist():
            rows.append(
                {
                    "pwsid": pwsid,
                    "split": split_name,
                    "split_strategy": "group_by_pwsid",
                    "random_seed": RANDOM_SEED,
                    "split_version": "v001",
                }
            )
    output = pd.DataFrame(rows).sort_values(["split", "pwsid"]).reset_index(drop=True)
    if output["pwsid"].duplicated().any():
        raise ValueError("Master split contains duplicated pwsid values.")
    return output


def attach_master_split(df: pd.DataFrame, split_df: pd.DataFrame) -> pd.DataFrame:
    merged = df.merge(split_df[["pwsid", "split"]], on="pwsid", how="left", validate="many_to_one")
    if merged["split"].isna().any():
        raise ValueError("Some rows did not receive a split assignment.")
    return merged


def build_task_split_index(df: pd.DataFrame, task_name: str) -> pd.DataFrame:
    if task_name == "tthm_regulatory_exceedance_prediction":
        subset = df.loc[(df["level1_flag"] == 1) & df["tthm_regulatory_exceed_label"].notna()].copy()
        subset["target_column"] = "tthm_regulatory_exceed_label"
        subset["target_value"] = subset["tthm_regulatory_exceed_label"].astype("Int8")
    elif task_name == "tthm_anchored_risk_prediction":
        anchored = build_tthm_anchored_risk_label(df["tthm_sample_weighted_mean_ug_l"])
        subset = df.loc[(df["level1_flag"] == 1) & anchored.notna()].copy()
        subset["target_column"] = "tthm_anchored_risk_label"
        subset["target_value"] = anchored.loc[subset.index].astype("Int8")
    else:
        raise ValueError(f"Unsupported task: {task_name}")

    subset["task_name"] = task_name
    subset["level_name"] = "level1"
    return subset[
        ["task_name", "level_name", "pwsid", "year", "split", "target_column", "target_value"]
    ].sort_values(["split", "pwsid", "year"]).reset_index(drop=True)


def build_summary_markdown(master_split: pd.DataFrame, regulatory_index: pd.DataFrame, anchored_index: pd.DataFrame) -> str:
    master_counts = master_split["split"].value_counts().to_dict()
    regulatory_counts = regulatory_index["split"].value_counts().to_dict()
    anchored_counts = anchored_index["split"].value_counts().to_dict()
    return "\n".join(
        [
            "# V4 TTHM split summary",
            "",
            f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
            f"- 输入文件：`{INPUT_PATH}`",
            f"- 切分策略：`group_by_pwsid`",
            f"- 随机种子：`{RANDOM_SEED}`",
            "",
            "## 1. 主切分概况",
            "",
            f"- train PWS 数：`{master_counts.get('train', 0)}`",
            f"- validation PWS 数：`{master_counts.get('validation', 0)}`",
            f"- test PWS 数：`{master_counts.get('test', 0)}`",
            "",
            "## 2. 任务样本量",
            "",
            f"- `tthm_regulatory_exceedance_prediction` 行数：train `{regulatory_counts.get('train', 0)}` / validation `{regulatory_counts.get('validation', 0)}` / test `{regulatory_counts.get('test', 0)}`",
            f"- `tthm_anchored_risk_prediction` 行数：train `{anchored_counts.get('train', 0)}` / validation `{anchored_counts.get('validation', 0)}` / test `{anchored_counts.get('test', 0)}`",
            "",
        ]
    )


def main() -> None:
    ensure_output_dir()
    df = read_v4_ml_ready_csv(INPUT_PATH)
    validate_v4_ml_ready_schema(df)
    master_split = build_master_group_split(df)
    merged = attach_master_split(df, master_split)
    regulatory_index = build_task_split_index(merged, "tthm_regulatory_exceedance_prediction")
    anchored_index = build_task_split_index(merged, "tthm_anchored_risk_prediction")

    master_split.to_csv(MASTER_SPLIT_PATH, index=False, encoding="utf-8-sig")
    regulatory_index.to_csv(REGULATORY_SPLIT_PATH, index=False, encoding="utf-8-sig")
    anchored_index.to_csv(ANCHORED_SPLIT_PATH, index=False, encoding="utf-8-sig")
    SUMMARY_PATH.write_text(
        build_summary_markdown(master_split, regulatory_index, anchored_index),
        encoding="utf-8",
    )

    print("Built V4 TTHM split files")
    print(f"Wrote: {MASTER_SPLIT_PATH}")
    print(f"Wrote: {REGULATORY_SPLIT_PATH}")
    print(f"Wrote: {ANCHORED_SPLIT_PATH}")
    print(f"Wrote: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
