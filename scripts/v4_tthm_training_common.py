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
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from io_v4_ml_ready import (
    DEFAULT_BASELINE_FEATURES,
    STRING_COLUMNS,
    build_tthm_anchored_risk_label,
    read_v4_ml_ready_csv,
    validate_v4_ml_ready_schema,
)


INPUT_PATH = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready" / "V4_pws_year_ml_ready.csv"
SPLIT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Splits"
RESULTS_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_Experiments"
MASTER_SPLIT_PATH = SPLIT_DIR / "v4_group_by_pwsid_master_split.csv"
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_results_dir(*path_parts: str) -> Path:
    if not path_parts:
        raise ValueError("At least one path part is required.")
    task_dir = RESULTS_DIR.joinpath(*path_parts)
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


def infer_feature_groups(feature_columns: list[str]) -> tuple[list[str], list[str]]:
    categorical_features = [column for column in feature_columns if column in STRING_COLUMNS]
    numeric_features = [column for column in feature_columns if column not in categorical_features]
    return numeric_features, categorical_features


def build_logistic_regression_pipeline(feature_columns: list[str]) -> Pipeline:
    numeric_features, categorical_features = infer_feature_groups(feature_columns)
    transformers: list[tuple[str, Pipeline, list[str]]] = []

    if numeric_features:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            )
        )

    if categorical_features:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            )
        )

    if not transformers:
        raise ValueError("At least one feature column is required to build the pipeline.")

    preprocessor = ColumnTransformer(
        transformers=transformers
    )
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42,
        solver="lbfgs",
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def build_baseline_pipeline() -> Pipeline:
    return build_logistic_regression_pipeline(DEFAULT_BASELINE_FEATURES)


def prepare_feature_frame(df: pd.DataFrame, feature_columns: list[str] | None = None) -> pd.DataFrame:
    if feature_columns is None:
        feature_columns = DEFAULT_BASELINE_FEATURES

    output = df[feature_columns].copy().astype(object)
    numeric_columns, categorical_columns = infer_feature_groups(feature_columns)
    for column in numeric_columns:
        output[column] = pd.to_numeric(output[column], errors="coerce").astype("float64")
    for column in categorical_columns:
        output[column] = output[column].astype(object)
    output = output.where(pd.notna(output), np.nan)
    return output


def evaluate_binary_classification(
    model: Pipeline,
    df: pd.DataFrame,
    feature_columns: list[str] | None = None,
) -> dict[str, float]:
    probabilities = model.predict_proba(prepare_feature_frame(df, feature_columns))[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    y_true = df["target_value"].astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, predictions, labels=[0, 1]).ravel()
    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    pr_auc = np.nan
    roc_auc = np.nan
    if y_true.nunique() >= 2:
        pr_auc = float(average_precision_score(y_true, probabilities))
        roc_auc = float(roc_auc_score(y_true, probabilities))
    return {
        "pr_auc": pr_auc,
        "roc_auc": roc_auc,
        "balanced_accuracy": float(balanced_accuracy_score(y_true, predictions)),
        "specificity": specificity,
        "mcc": float(matthews_corrcoef(y_true, predictions)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
    }


def build_unavailable_metrics() -> dict[str, float]:
    return {
        "pr_auc": np.nan,
        "roc_auc": np.nan,
        "balanced_accuracy": np.nan,
        "specificity": np.nan,
        "mcc": np.nan,
        "f1": np.nan,
        "recall": np.nan,
        "precision": np.nan,
        "tp": np.nan,
        "tn": np.nan,
        "fp": np.nan,
        "fn": np.nan,
    }


def summarize_target_class_counts(df: pd.DataFrame) -> dict[int, int]:
    counts = df["target_value"].astype(int).value_counts().sort_index()
    return {int(label): int(count) for label, count in counts.items()}


def build_result_row(
    task_name: str,
    target_column: str,
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    validation_metrics: dict[str, float],
    test_metrics: dict[str, float],
    *,
    experiment_id: str | None = None,
    level_name: str = "level1",
    feature_set: str = "baseline_default",
    split_strategy: str = "group_by_pwsid",
    model_name: str = "logistic_regression",
    feature_columns: list[str] | None = None,
    required_complete_case_columns: list[str] | None = None,
    notes: str = "baseline_default with class_weight=balanced",
) -> pd.DataFrame:
    if feature_columns is None:
        feature_columns = DEFAULT_BASELINE_FEATURES
    if required_complete_case_columns is None:
        required_complete_case_columns = []
    if experiment_id is None:
        experiment_id = f"{task_name}-{level_name}-{feature_set}-{model_name}-{split_strategy}-v001"

    return pd.DataFrame(
        [
            {
                "experiment_id": experiment_id,
                "task_name": task_name,
                "level_name": level_name,
                "feature_set": feature_set,
                "split_strategy": split_strategy,
                "model_name": model_name,
                "target_column": target_column,
                "train_rows": int(len(train_df)),
                "validation_rows": int(len(validation_df)),
                "test_rows": int(len(test_df)),
                "positive_count_train": int(train_df["target_value"].sum()),
                "positive_count_validation": int(validation_df["target_value"].sum()),
                "positive_count_test": int(test_df["target_value"].sum()),
                "validation_pr_auc": validation_metrics["pr_auc"],
                "validation_roc_auc": validation_metrics["roc_auc"],
                "validation_balanced_accuracy": validation_metrics["balanced_accuracy"],
                "validation_specificity": validation_metrics["specificity"],
                "validation_mcc": validation_metrics["mcc"],
                "validation_f1": validation_metrics["f1"],
                "validation_recall": validation_metrics["recall"],
                "validation_precision": validation_metrics["precision"],
                "validation_tp": validation_metrics["tp"],
                "validation_tn": validation_metrics["tn"],
                "validation_fp": validation_metrics["fp"],
                "validation_fn": validation_metrics["fn"],
                "test_pr_auc": test_metrics["pr_auc"],
                "test_roc_auc": test_metrics["roc_auc"],
                "test_balanced_accuracy": test_metrics["balanced_accuracy"],
                "test_specificity": test_metrics["specificity"],
                "test_mcc": test_metrics["mcc"],
                "test_f1": test_metrics["f1"],
                "test_recall": test_metrics["recall"],
                "test_precision": test_metrics["precision"],
                "test_tp": test_metrics["tp"],
                "test_tn": test_metrics["tn"],
                "test_fp": test_metrics["fp"],
                "test_fn": test_metrics["fn"],
                "feature_columns": ",".join(feature_columns),
                "required_complete_case_columns": ",".join(required_complete_case_columns),
                "run_time": now_text(),
                "notes": notes,
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


def build_binary_dataset(df: pd.DataFrame, task_name: str, level_name: str) -> tuple[pd.DataFrame, str]:
    level_column = f"{level_name}_flag"
    if level_column not in df.columns:
        raise ValueError(f"Unsupported level_name: {level_name}")

    if task_name == "tthm_regulatory_exceedance_prediction":
        subset = df.loc[(df[level_column] == 1) & df["tthm_regulatory_exceed_label"].notna()].copy()
        subset["target_value"] = subset["tthm_regulatory_exceed_label"].astype(int)
        return subset, "tthm_regulatory_exceed_label"

    if task_name == "tthm_anchored_risk_prediction":
        anchored = build_tthm_anchored_risk_label(df["tthm_sample_weighted_mean_ug_l"])
        subset = df.loc[(df[level_column] == 1) & anchored.notna()].copy()
        subset["target_value"] = anchored.loc[subset.index].astype(int)
        return subset, "tthm_anchored_risk_label"

    raise ValueError(f"Unsupported task_name: {task_name}")


def filter_complete_case(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    if not required_columns:
        return df.copy()
    return df.loc[df[required_columns].notna().all(axis=1)].copy()


def run_binary_experiment(
    base_df: pd.DataFrame,
    *,
    task_name: str,
    level_name: str,
    feature_columns: list[str],
    feature_set: str,
    notes: str,
    required_complete_case_columns: list[str] | None = None,
    experiment_id: str | None = None,
) -> pd.DataFrame:
    if required_complete_case_columns is None:
        required_complete_case_columns = []

    dataset, target_column = build_binary_dataset(base_df, task_name=task_name, level_name=level_name)
    dataset = filter_complete_case(dataset, required_complete_case_columns)
    train_df, validation_df, test_df = split_three_way(dataset)

    train_class_counts = summarize_target_class_counts(train_df)
    validation_class_counts = summarize_target_class_counts(validation_df)
    test_class_counts = summarize_target_class_counts(test_df)
    single_class_splits = [
        split_name
        for split_name, split_df in (
            ("train", train_df),
            ("validation", validation_df),
            ("test", test_df),
        )
        if split_df["target_value"].astype(int).nunique() < 2
    ]

    if "train" in single_class_splits:
        unavailable_metrics = build_unavailable_metrics()
        infeasible_notes = (
            f"{notes} | not_run_due_to_single_class_train_split "
            f"(train={train_class_counts}; validation={validation_class_counts}; test={test_class_counts})"
        )
        return build_result_row(
            task_name=task_name,
            target_column=target_column,
            train_df=train_df,
            validation_df=validation_df,
            test_df=test_df,
            validation_metrics=unavailable_metrics,
            test_metrics=unavailable_metrics,
            experiment_id=experiment_id,
            level_name=level_name,
            feature_set=feature_set,
            feature_columns=feature_columns,
            required_complete_case_columns=required_complete_case_columns,
            notes=infeasible_notes,
        )

    model = build_logistic_regression_pipeline(feature_columns)
    model.fit(prepare_feature_frame(train_df, feature_columns), train_df["target_value"].astype(int))

    validation_metrics = evaluate_binary_classification(model, validation_df, feature_columns)
    test_metrics = evaluate_binary_classification(model, test_df, feature_columns)
    output_notes = notes
    if single_class_splits:
        output_notes = (
            f"{notes} | single_class_eval_split_detected "
            f"(train={train_class_counts}; validation={validation_class_counts}; test={test_class_counts})"
        )

    return build_result_row(
        task_name=task_name,
        target_column=target_column,
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        validation_metrics=validation_metrics,
        test_metrics=test_metrics,
        experiment_id=experiment_id,
        level_name=level_name,
        feature_set=feature_set,
        feature_columns=feature_columns,
        required_complete_case_columns=required_complete_case_columns,
        notes=output_notes,
    )
