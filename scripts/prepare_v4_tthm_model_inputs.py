from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from io_v4_ml_ready import (
    DEFAULT_BASELINE_FEATURES,
    ENHANCED_CONDITIONAL_FEATURES,
    ENHANCED_DEFAULT_FEATURES,
    STRUCTURAL_CONDITIONAL_FEATURES,
    TREATMENT_CONDITIONAL_FEATURES,
    build_tthm_anchored_risk_label,
    read_v4_ml_ready_csv,
    validate_v4_ml_ready_schema,
)


INPUT_PATH = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready" / "V4_pws_year_ml_ready.csv"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Model_Prep"
TASK_OVERVIEW_PATH = OUTPUT_DIR / "v4_tthm_task_overview.csv"
MISSINGNESS_PATH = OUTPUT_DIR / "v4_tthm_feature_missingness.csv"
PREP_SUMMARY_PATH = OUTPUT_DIR / "v4_tthm_model_prep_summary.md"
TZ = ZoneInfo("Asia/Hong_Kong")

TASK_SPECS = [
    {
        "task_name": "tthm_regulatory_exceedance_prediction",
        "task_type": "classification",
        "target_column": "tthm_regulatory_exceed_label",
        "subset_rule": "level1_only",
        "primary_metrics": "PR-AUC; ROC-AUC; F1; Recall; Precision",
    },
    {
        "task_name": "tthm_anchored_risk_prediction",
        "task_type": "classification",
        "target_column": "tthm_anchored_risk_label",
        "subset_rule": "anchored_level1_only",
        "primary_metrics": "PR-AUC; ROC-AUC; F1; Recall; Precision",
    },
    {
        "task_name": "tthm_regression",
        "task_type": "regression",
        "target_column": "tthm_sample_weighted_mean_ug_l",
        "subset_rule": "level1_only",
        "primary_metrics": "MAE; RMSE; R2",
    },
]


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def attach_anchored_label(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["tthm_anchored_risk_label"] = build_tthm_anchored_risk_label(
        output["tthm_sample_weighted_mean_ug_l"]
    )
    return output


def task_subset(df: pd.DataFrame, task_name: str, target_column: str) -> pd.DataFrame:
    if task_name == "tthm_anchored_risk_prediction":
        return df.loc[(df["level1_flag"] == 1) & df[target_column].notna()].copy()
    return df.loc[(df["level1_flag"] == 1) & df[target_column].notna()].copy()


def build_task_overview(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for spec in TASK_SPECS:
        subset = task_subset(df, spec["task_name"], spec["target_column"])
        row: dict[str, object] = {
            "task_name": spec["task_name"],
            "task_type": spec["task_type"],
            "target_column": spec["target_column"],
            "subset_rule": spec["subset_rule"],
            "n_rows": int(len(subset)),
            "primary_metrics": spec["primary_metrics"],
        }
        if spec["task_type"] == "classification":
            positive_count = int((subset[spec["target_column"]] == 1).sum())
            negative_count = int((subset[spec["target_column"]] == 0).sum())
            positive_rate = round(positive_count / len(subset), 6) if len(subset) else None
            row["positive_count"] = positive_count
            row["negative_count"] = negative_count
            row["positive_rate"] = positive_rate
        else:
            row["positive_count"] = None
            row["negative_count"] = None
            row["positive_rate"] = None
            row["target_mean"] = round(float(subset[spec["target_column"]].mean()), 6) if len(subset) else None
            row["target_std"] = round(float(subset[spec["target_column"]].std()), 6) if len(subset) > 1 else None
        rows.append(row)
    return pd.DataFrame(rows)


def build_missingness(df: pd.DataFrame) -> pd.DataFrame:
    feature_groups = {
        "baseline_default": DEFAULT_BASELINE_FEATURES,
        "structural_conditional": STRUCTURAL_CONDITIONAL_FEATURES,
        "treatment_conditional": TREATMENT_CONDITIONAL_FEATURES,
        "enhanced_default": ENHANCED_DEFAULT_FEATURES,
        "enhanced_conditional": ENHANCED_CONDITIONAL_FEATURES,
    }
    rows: list[dict[str, object]] = []
    for group_name, features in feature_groups.items():
        for feature in features:
            rows.append(
                {
                    "feature_group": group_name,
                    "feature_name": feature,
                    "missing_count": int(df[feature].isna().sum()),
                    "missing_rate": round(float(df[feature].isna().mean()), 6),
                }
            )
    return pd.DataFrame(rows)


def build_summary_markdown(df: pd.DataFrame, task_overview: pd.DataFrame, missingness: pd.DataFrame) -> str:
    reg_row = task_overview.loc[
        task_overview["task_name"] == "tthm_regulatory_exceedance_prediction"
    ].iloc[0]
    anchored_row = task_overview.loc[
        task_overview["task_name"] == "tthm_anchored_risk_prediction"
    ].iloc[0]
    high_missing = missingness.sort_values("missing_rate", ascending=False).head(6)
    high_missing_lines = [
        f"- `{row.feature_name}`：缺失率 `{row.missing_rate:.2%}`"
        for row in high_missing.itertuples(index=False)
    ]
    return "\n".join(
        [
            "# V4 TTHM model prep summary",
            "",
            f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
            f"- 输入文件：`{INPUT_PATH}`",
            f"- 输出目录：`{OUTPUT_DIR}`",
            "",
            "## 1. 当前数据入口",
            "",
            "- 已通过 `scripts/io_v4_ml_ready.py` 统一读取并完成 schema 校验。",
            "- 本轮不训练模型，只固定任务、特征和样本准备口径。",
            "",
            "## 2. 当前样本概况",
            "",
            f"- `level1`：`{int(df['level1_flag'].sum())}`",
            f"- `level2`：`{int(df['level2_flag'].sum())}`",
            f"- `level3`：`{int(df['level3_flag'].sum())}`",
            "",
            "## 3. 当前正式任务",
            "",
            f"- `tthm_regulatory_exceedance_prediction`：正类 `{int(reg_row['positive_count'])}`，负类 `{int(reg_row['negative_count'])}`，正类比例 `{float(reg_row['positive_rate']):.2%}`",
            f"- `tthm_anchored_risk_prediction`：正类 `{int(anchored_row['positive_count'])}`，负类 `{int(anchored_row['negative_count'])}`，正类比例 `{float(anchored_row['positive_rate']):.2%}`",
            "",
            "## 4. 推荐实验顺序",
            "",
            "- 第一轮：`level1 + baseline_default`",
            "- 第二轮：`level1 + baseline_default + structural_conditional`",
            "- 第三轮：`level1 + baseline_default + treatment_conditional`",
            "- 第四轮：`level2 + baseline_default + enhanced_default`",
            "",
            "## 5. 当前最需要警惕的高缺失特征",
            "",
            *high_missing_lines,
            "",
        ]
    )


def main() -> None:
    ensure_output_dir()
    df = read_v4_ml_ready_csv(INPUT_PATH)
    validate_v4_ml_ready_schema(df)
    df = attach_anchored_label(df)
    task_overview = build_task_overview(df)
    missingness = build_missingness(df)
    task_overview.to_csv(TASK_OVERVIEW_PATH, index=False, encoding="utf-8-sig")
    missingness.to_csv(MISSINGNESS_PATH, index=False, encoding="utf-8-sig")
    PREP_SUMMARY_PATH.write_text(
        build_summary_markdown(df, task_overview, missingness),
        encoding="utf-8",
    )
    print("V4 TTHM model prep completed")
    print(f"Wrote: {TASK_OVERVIEW_PATH}")
    print(f"Wrote: {MISSINGNESS_PATH}")
    print(f"Wrote: {PREP_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
