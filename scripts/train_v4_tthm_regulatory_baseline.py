from __future__ import annotations

from pathlib import Path

from v4_tthm_training_common import (
    build_baseline_pipeline,
    build_regulatory_dataset,
    build_result_row,
    ensure_results_dir,
    evaluate_binary_classification,
    load_base_dataframe,
    prepare_feature_frame,
    split_three_way,
)


def main() -> None:
    task_name = "tthm_regulatory_exceedance_prediction"
    target_column = "tthm_regulatory_exceed_label"
    task_dir = ensure_results_dir(task_name)
    result_path = task_dir / "baseline_default_logistic_regression_results.csv"

    base_df = load_base_dataframe()
    dataset = build_regulatory_dataset(base_df)
    train_df, validation_df, test_df = split_three_way(dataset)

    model = build_baseline_pipeline()
    model.fit(prepare_feature_frame(train_df), train_df["target_value"])

    validation_metrics = evaluate_binary_classification(model, validation_df)
    test_metrics = evaluate_binary_classification(model, test_df)
    result_df = build_result_row(
        task_name=task_name,
        target_column=target_column,
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        validation_metrics=validation_metrics,
        test_metrics=test_metrics,
    )
    result_df.to_csv(result_path, index=False, encoding="utf-8-sig")

    print("Completed regulatory baseline training")
    print(f"Wrote: {result_path}")
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()
