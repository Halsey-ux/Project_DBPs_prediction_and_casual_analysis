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

from io_v5_facility_month import (
    KEY_COLUMNS,
    LABEL_COLUMN,
    STAGE1_REQUIRED_COLUMNS,
    TARGET_COLUMN,
    read_v5_facility_month_csv,
    validate_v5_facility_month_schema,
)


INPUT_PATH = (
    PROJECT_ROOT
    / "data_local"
    / "V3_Chapter1_Part1_Prototype_Build"
    / "V3_facility_month_master.csv"
)
OUTPUT_DIR = (
    PROJECT_ROOT
    / "data_local"
    / "V5_Chapter1_Part1_Facility_Month_Module"
    / "V5_1"
)
MASTER_SPLIT_PATH = OUTPUT_DIR / "v5_1_group_by_pwsid_master_split.csv"
TASK_SPLIT_PATH = OUTPUT_DIR / "v5_1_tthm_high_risk_month_split_index.csv"
COMPARISON_PATH = OUTPUT_DIR / "v5_1_split_strategy_comparison.csv"
SUMMARY_PATH = OUTPUT_DIR / "V5_1_Facility_Month_Baseline_Split_Summary.md"

TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15
RANDOM_SEED = 42
SPLIT_VERSION = "v001"
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_group_split(values: pd.Series, group_column: str, strategy_name: str) -> pd.DataFrame:
    unique_values = values.dropna().drop_duplicates().reset_index(drop=True)
    rng = np.random.default_rng(RANDOM_SEED)
    shuffled = unique_values.iloc[rng.permutation(len(unique_values))].reset_index(drop=True)
    n_total = len(shuffled)
    n_train = int(round(n_total * TRAIN_SIZE))
    n_validation = int(round(n_total * VALIDATION_SIZE))
    n_test = n_total - n_train - n_validation

    rows: list[dict[str, object]] = []
    for split_name, split_values in (
        ("train", shuffled.iloc[:n_train]),
        ("validation", shuffled.iloc[n_train : n_train + n_validation]),
        ("test", shuffled.iloc[n_train + n_validation : n_train + n_validation + n_test]),
    ):
        for value in split_values.tolist():
            rows.append(
                {
                    group_column: value,
                    "split": split_name,
                    "split_strategy": strategy_name,
                    "random_seed": RANDOM_SEED,
                    "split_version": SPLIT_VERSION,
                }
            )

    output = pd.DataFrame(rows)
    if output[group_column].duplicated().any():
        raise ValueError(f"Split assignment duplicated for {group_column}.")
    return output


def attach_split(df: pd.DataFrame, split_df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    merged = df.merge(split_df[[group_column, "split"]], on=group_column, how="left", validate="many_to_one")
    if merged["split"].isna().any():
        raise ValueError(f"Some rows did not receive a split assignment for {group_column}.")
    return merged


def build_task_split_index(df: pd.DataFrame) -> pd.DataFrame:
    subset = df.loc[df[TARGET_COLUMN].notna()].copy()
    subset["task_name"] = "tthm_high_risk_month_prediction"
    subset["target_column"] = LABEL_COLUMN
    subset["target_value"] = subset[LABEL_COLUMN].astype("Int8")
    return subset[
        [
            "task_name",
            *KEY_COLUMNS,
            "split",
            "target_column",
            "target_value",
        ]
    ].sort_values(["split", "pwsid", "water_facility_id", "year", "month"]).reset_index(drop=True)


def build_strategy_comparison(df: pd.DataFrame) -> pd.DataFrame:
    target_df = df.loc[df[TARGET_COLUMN].notna()].copy()
    stage1_df = target_df.loc[target_df[STAGE1_REQUIRED_COLUMNS].notna().all(axis=1)].copy()
    target_df["facility_key"] = (
        target_df["pwsid"].fillna(pd.NA).astype("string")
        + "__"
        + target_df["water_facility_id"].fillna(pd.NA).astype("string")
    )
    stage1_df["facility_key"] = (
        stage1_df["pwsid"].fillna(pd.NA).astype("string")
        + "__"
        + stage1_df["water_facility_id"].fillna(pd.NA).astype("string")
    )

    comparison_rows: list[dict[str, object]] = []
    strategy_specs = [
        ("group_by_pwsid", target_df, "pwsid"),
        ("group_by_pwsid_plus_water_facility_id", target_df, "facility_key"),
    ]

    for strategy_name, source_df, group_column in strategy_specs:
        split_df = build_group_split(source_df[group_column], group_column=group_column, strategy_name=strategy_name)
        merged_target = attach_split(target_df, split_df, group_column=group_column)
        merged_stage1 = attach_split(stage1_df, split_df, group_column=group_column)

        for dataset_name, dataset_df in (
            ("official_target_pool", merged_target),
            ("v5_2_stage1_reference_pool", merged_stage1),
        ):
            for split_name in ("train", "validation", "test"):
                subset = dataset_df.loc[dataset_df["split"] == split_name]
                comparison_rows.append(
                    {
                        "strategy_name": strategy_name,
                        "group_column": group_column,
                        "dataset_name": dataset_name,
                        "split": split_name,
                        "n_groups": int(split_df.loc[split_df["split"] == split_name, group_column].nunique()),
                        "rows": int(len(subset)),
                        "positive_rows": int(subset[LABEL_COLUMN].sum()),
                        "positive_rate": float(subset[LABEL_COLUMN].mean()) if len(subset) else np.nan,
                    }
                )

    return pd.DataFrame(comparison_rows)


def build_summary_markdown(comparison_df: pd.DataFrame) -> str:
    official = comparison_df.loc[
        (comparison_df["strategy_name"] == "group_by_pwsid")
        & (comparison_df["dataset_name"] == "official_target_pool")
    ].copy()
    stage1 = comparison_df.loc[
        (comparison_df["strategy_name"] == "group_by_pwsid")
        & (comparison_df["dataset_name"] == "v5_2_stage1_reference_pool")
    ].copy()

    def line_block(title: str, subset: pd.DataFrame) -> list[str]:
        rows = [f"## {title}", ""]
        for split_name in ("train", "validation", "test"):
            row = subset.loc[subset["split"] == split_name].iloc[0]
            rows.append(
                "- "
                f"{split_name}: rows `{int(row['rows'])}` / positives `{int(row['positive_rows'])}` / "
                f"positive_rate `{row['positive_rate']:.4f}` / groups `{int(row['n_groups'])}`"
            )
        rows.append("")
        return rows

    return "\n".join(
        [
            "# V5.1 Facility-Month baseline split summary",
            "",
            f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
            f"- 输入文件：`{INPUT_PATH}`",
            "- 正式切分策略：`group_by_pwsid`",
            "- 随机种子：`42`",
            "- 切分版本：`v001`",
            "",
            "## 正式判断",
            "",
            "- `group_by_pwsid` 被固定为正式主切分，因为它同时阻断同一系统跨设施、跨月份泄漏。",
            "- `group_by_pwsid + water_facility_id` 虽然可以阻断设施级泄漏，但仍允许同一系统的不同设施进入不同集合，不够严格。",
            "",
            *line_block("正式目标样本池", official),
            *line_block("V5.2 对照子样本池（baseline + pH + alkalinity 同子样本参考）", stage1),
        ]
    )


def main() -> None:
    ensure_output_dir()
    df = read_v5_facility_month_csv(INPUT_PATH)
    validate_v5_facility_month_schema(df)

    target_df = df.loc[df[TARGET_COLUMN].notna()].copy()
    master_split = build_group_split(df["pwsid"], group_column="pwsid", strategy_name="group_by_pwsid")
    merged = attach_split(df, master_split, group_column="pwsid")
    task_split = build_task_split_index(merged)
    comparison_df = build_strategy_comparison(df)

    master_split.to_csv(MASTER_SPLIT_PATH, index=False, encoding="utf-8-sig")
    task_split.to_csv(TASK_SPLIT_PATH, index=False, encoding="utf-8-sig")
    comparison_df.to_csv(COMPARISON_PATH, index=False, encoding="utf-8-sig")
    SUMMARY_PATH.write_text(build_summary_markdown(comparison_df), encoding="utf-8")

    print("Built V5.1 facility-month split files")
    print(f"Wrote: {MASTER_SPLIT_PATH}")
    print(f"Wrote: {TASK_SPLIT_PATH}")
    print(f"Wrote: {COMPARISON_PATH}")
    print(f"Wrote: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
