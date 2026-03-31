from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from io_v4_ml_ready import DEFAULT_BASELINE_FEATURES, build_tthm_anchored_risk_label, read_v4_ml_ready_csv, validate_v4_ml_ready_schema


INPUT_PATH = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready" / "V4_pws_year_ml_ready.csv"
SPLIT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Splits"
RESULTS_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Experiments"
MASTER_SPLIT_PATH = SPLIT_DIR / "v4_group_by_pwsid_master_split.csv"
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_results_dir(task_name: str) -> Path:
    task_dir = RESULTS_DIR / task_name
    task_dir.mkdir(parents=True, exist_ok=True)
    return task_dir


def load_base_dataframe() -> pd.DataFrame:
    df = read_v4_ml_ready_csv(INPUT_PATH)
    validate_v4_ml_ready_schema(df)
    split_df = pd.read_csv(MASTER_SPLIT_PATH, encoding="utf-8-sig", dtype={"pwsid": "string", "split": "string"})
    merged = df.merge(split_df[["pwsid", "split"]], on="pwsid", how="left", validate="many_to_one")
    if merged["split"].isna().any():
        raise ValueError("Split assignment is missing for some rows.")
    return merged


def build_regulatory_dataset(df: pd.DataFrame) -> pd.DataFrame:
    subset = df.loc[(df["level1_flag"] == 1) & df["tthm_regulatory_exceed_label"].notna()].copy()
    subset["target_value"] = subset["tthm_regulatory_exceed_label"].astype(int)
    return subset


def build_anchored_dataset(df: pd.DataFrame) -> pd.DataFrame:
    anchored = build_tthm_anchored_risk_label(df["tthm_sample_weighted_mean_ug_l"])
    subset = df.loc[(df["level1_flag"] == 1) & anchored.notna()].copy()
    subset["target_value"] = anchored.loc[subset.index].astype(int)
    return subset


def build_baseline_pipeline() -> Pipeline:
    numeric_features = ["retail_population_served", "n_facilities_in_master"]
    categorical_features = ["system_type", "source_water_type"]
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42,
        solver="lbfgs",
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def prepare_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    output = df[DEFAULT_BASELINE_FEATURES].copy().astype(object)
    numeric_columns = ["retail_population_served", "n_facilities_in_master"]
    categorical_columns = ["system_type", "source_water_type"]
    for column in numeric_columns:
        output[column] = pd.to_numeric(output[column], errors="coerce").astype("float64")
    for column in categorical_columns:
        output[column] = output[column].astype(object)
    output = output.where(pd.notna(output), np.nan)
    return output


def evaluate_binary_classification(model: Pipeline, df: pd.DataFrame) -> dict[str, float]:
    probabilities = model.predict_proba(prepare_feature_frame(df))[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    y_true = df["target_value"].astype(int)
    return {
        "pr_auc": float(average_precision_score(y_true, probabilities)),
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
    }


def build_result_row(task_name: str, target_column: str, train_df: pd.DataFrame, validation_df: pd.DataFrame, test_df: pd.DataFrame, validation_metrics: dict[str, float], test_metrics: dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "experiment_id": f"{task_name}-level1-baseline_default-logistic_regression-group_by_pwsid-v001",
                "task_name": task_name,
                "level_name": "level1",
                "feature_set": "baseline_default",
                "split_strategy": "group_by_pwsid",
                "model_name": "logistic_regression",
                "target_column": target_column,
                "train_rows": int(len(train_df)),
                "validation_rows": int(len(validation_df)),
                "test_rows": int(len(test_df)),
                "positive_count_train": int(train_df["target_value"].sum()),
                "positive_count_validation": int(validation_df["target_value"].sum()),
                "positive_count_test": int(test_df["target_value"].sum()),
                "validation_pr_auc": validation_metrics["pr_auc"],
                "validation_roc_auc": validation_metrics["roc_auc"],
                "validation_f1": validation_metrics["f1"],
                "validation_recall": validation_metrics["recall"],
                "validation_precision": validation_metrics["precision"],
                "test_pr_auc": test_metrics["pr_auc"],
                "test_roc_auc": test_metrics["roc_auc"],
                "test_f1": test_metrics["f1"],
                "test_recall": test_metrics["recall"],
                "test_precision": test_metrics["precision"],
                "run_time": now_text(),
                "notes": "baseline_default with class_weight=balanced",
            }
        ]
    )


def split_three_way(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_df = df.loc[df["split"] == "train"].copy()
    validation_df = df.loc[df["split"] == "validation"].copy()
    test_df = df.loc[df["split"] == "test"].copy()
    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError("Train/validation/test split is incomplete.")
    return train_df, validation_df, test_df
