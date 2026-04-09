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

from io_v5_facility_month import (
    CATEGORICAL_FEATURE_COLUMNS,
    FINAL_BASELINE_FEATURES,
    LABEL_COLUMN,
    TARGET_COLUMN,
    infer_feature_groups,
    read_v5_facility_month_csv,
    validate_v5_facility_month_schema,
)


INPUT_PATH = (
    PROJECT_ROOT
    / "data_local"
    / "V3_Chapter1_Part1_Prototype_Build"
    / "V3_facility_month_master.csv"
)
RESULTS_DIR = (
    PROJECT_ROOT
    / "data_local"
    / "V5_Chapter1_Part1_Facility_Month_Module"
    / "V5_1"
)
MASTER_SPLIT_PATH = RESULTS_DIR / "v5_1_group_by_pwsid_master_split.csv"
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_results_dir() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR


def load_base_dataframe() -> pd.DataFrame:
    df = read_v5_facility_month_csv(INPUT_PATH)
    validate_v5_facility_month_schema(df)
    split_df = pd.read_csv(
        MASTER_SPLIT_PATH,
        encoding="utf-8-sig",
        dtype={"pwsid": "string", "split": "string"},
    )
    merged = df.merge(split_df[["pwsid", "split"]], on="pwsid", how="left", validate="many_to_one")
    if merged["split"].isna().any():
        raise ValueError("Split assignment is missing for some rows.")
    return merged


def build_binary_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    subset = df.loc[df[TARGET_COLUMN].notna()].copy()
    subset["target_value"] = subset[LABEL_COLUMN].astype(int)
    return subset, LABEL_COLUMN


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

    preprocessor = ColumnTransformer(transformers=transformers)
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=4000,
        random_state=42,
        solver="lbfgs",
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def prepare_feature_frame(df: pd.DataFrame, feature_columns: list[str] | None = None) -> pd.DataFrame:
    if feature_columns is None:
        feature_columns = FINAL_BASELINE_FEATURES

    output = df[feature_columns].copy()
    for column in feature_columns:
        if column in CATEGORICAL_FEATURE_COLUMNS:
            output[column] = output[column].astype("string").astype(object)
        else:
            output[column] = pd.to_numeric(output[column], errors="coerce").astype("float64")
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


def summarize_target_class_counts(df: pd.DataFrame) -> dict[int, int]:
    counts = df["target_value"].astype(int).value_counts().sort_index()
    return {int(label): int(count) for label, count in counts.items()}


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


def build_result_row(
    *,
    task_name: str,
    target_column: str,
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    train_metrics: dict[str, float],
    validation_metrics: dict[str, float],
    test_metrics: dict[str, float],
    feature_set: str,
    feature_columns: list[str],
    required_complete_case_columns: list[str],
    sample_definition: str,
    notes: str,
    experiment_id: str | None = None,
    split_strategy: str = "group_by_pwsid",
    model_name: str = "logistic_regression",
) -> pd.DataFrame:
    if experiment_id is None:
        experiment_id = f"{task_name}-{feature_set}-{model_name}-{split_strategy}-v001"

    row: dict[str, object] = {
        "experiment_id": experiment_id,
        "task_name": task_name,
        "target_column": target_column,
        "feature_set": feature_set,
        "split_strategy": split_strategy,
        "model_name": model_name,
        "sample_definition": sample_definition,
        "train_rows": int(len(train_df)),
        "validation_rows": int(len(validation_df)),
        "test_rows": int(len(test_df)),
        "positive_count_train": int(train_df["target_value"].sum()),
        "positive_count_validation": int(validation_df["target_value"].sum()),
        "positive_count_test": int(test_df["target_value"].sum()),
        "feature_columns": ",".join(feature_columns),
        "required_complete_case_columns": ",".join(required_complete_case_columns),
        "run_time": now_text(),
        "notes": notes,
    }

    for prefix, metrics in (
        ("train", train_metrics),
        ("validation", validation_metrics),
        ("test", test_metrics),
    ):
        row[f"{prefix}_pr_auc"] = metrics["pr_auc"]
        row[f"{prefix}_roc_auc"] = metrics["roc_auc"]
        row[f"{prefix}_balanced_accuracy"] = metrics["balanced_accuracy"]
        row[f"{prefix}_specificity"] = metrics["specificity"]
        row[f"{prefix}_mcc"] = metrics["mcc"]
        row[f"{prefix}_f1"] = metrics["f1"]
        row[f"{prefix}_recall"] = metrics["recall"]
        row[f"{prefix}_precision"] = metrics["precision"]
        row[f"{prefix}_tp"] = metrics["tp"]
        row[f"{prefix}_tn"] = metrics["tn"]
        row[f"{prefix}_fp"] = metrics["fp"]
        row[f"{prefix}_fn"] = metrics["fn"]

    return pd.DataFrame([row])


def split_three_way(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_df = df.loc[df["split"] == "train"].copy()
    validation_df = df.loc[df["split"] == "validation"].copy()
    test_df = df.loc[df["split"] == "test"].copy()
    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError("Train/validation/test split is incomplete.")
    return train_df, validation_df, test_df


def filter_complete_case(
    df: pd.DataFrame,
    feature_columns: list[str],
    required_complete_case_columns: list[str] | None = None,
) -> pd.DataFrame:
    if required_complete_case_columns is None:
        required_complete_case_columns = []
    columns = list(dict.fromkeys([*feature_columns, *required_complete_case_columns]))
    return df.loc[df[columns].notna().all(axis=1)].copy()


def run_binary_experiment(
    base_df: pd.DataFrame,
    *,
    task_name: str,
    feature_set: str,
    feature_columns: list[str],
    sample_definition: str,
    notes: str,
    required_complete_case_columns: list[str] | None = None,
    experiment_id: str | None = None,
) -> pd.DataFrame:
    if required_complete_case_columns is None:
        required_complete_case_columns = []

    dataset, target_column = build_binary_dataset(base_df)
    dataset = filter_complete_case(dataset, feature_columns, required_complete_case_columns)
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
            train_metrics=unavailable_metrics,
            validation_metrics=unavailable_metrics,
            test_metrics=unavailable_metrics,
            feature_set=feature_set,
            feature_columns=feature_columns,
            required_complete_case_columns=required_complete_case_columns,
            sample_definition=sample_definition,
            notes=infeasible_notes,
            experiment_id=experiment_id,
        )

    model = build_logistic_regression_pipeline(feature_columns)
    model.fit(prepare_feature_frame(train_df, feature_columns), train_df["target_value"].astype(int))

    train_metrics = evaluate_binary_classification(model, train_df, feature_columns)
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
        train_metrics=train_metrics,
        validation_metrics=validation_metrics,
        test_metrics=test_metrics,
        feature_set=feature_set,
        feature_columns=feature_columns,
        required_complete_case_columns=required_complete_case_columns,
        sample_definition=sample_definition,
        notes=output_notes,
        experiment_id=experiment_id,
    )
