from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from pandas.testing import assert_frame_equal


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_v3_chapter1_part1_prototypes import (  # noqa: E402
    PWS_YEAR_KEY,
    build_pws_year_master,
    order_pws_year_columns,
)
from build_v3_5_pws_year_ml_ready import (  # noqa: E402
    SOURCE_COLUMNS,
    build_dataset,
    compute_summary,
)
from io_v4_ml_ready import read_v4_ml_ready_csv  # noqa: E402


TZ = ZoneInfo("Asia/Hong_Kong")
V3_DIR = PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build"
FACILITY_MONTH_PATH = V3_DIR / "V3_facility_month_master.csv"
PWS_YEAR_PATH = V3_DIR / "V3_pws_year_master.csv"
RECOVERY_TMP_PATH = V3_DIR / "V3_pws_year_master.recovered_tmp.csv"
VALIDATION_PATH = V3_DIR / "V3_pws_year_master_recovery_validation.json"
V4_ML_READY_PATH = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready" / "V4_pws_year_ml_ready.csv"

EXPECTED_V3 = {
    "row_count": 259_500,
    "column_count": 130,
    "duplicate_key_count": 0,
    "tthm_system_year_count": 199_802,
    "haa5_system_year_count": 165_379,
    "tthm_core2_count": 26_975,
    "tthm_core4_count": 60,
}

EXPECTED_V4 = {
    "row_count": 259_500,
    "column_count": 38,
    "level1_count": 199_802,
    "level2_count": 26_975,
    "level3_count": 6_193,
    "regulatory_positive": 5_618,
    "warning_positive": 19_853,
}


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def backup_current_zero_byte_file() -> str | None:
    if not PWS_YEAR_PATH.exists() or PWS_YEAR_PATH.stat().st_size != 0:
        return None
    timestamp = PWS_YEAR_PATH.stat().st_mtime
    suffix = datetime.fromtimestamp(timestamp, TZ).strftime("%Y%m%d_%H%M%S")
    backup_path = V3_DIR / f"V3_pws_year_master.zero_byte_{suffix}.csv"
    if not backup_path.exists():
        shutil.copy2(PWS_YEAR_PATH, backup_path)
    return str(backup_path)


def compute_v3_validation(year_master: pd.DataFrame) -> dict[str, int]:
    return {
        "row_count": int(len(year_master)),
        "column_count": int(len(year_master.columns)),
        "duplicate_key_count": int(year_master.duplicated(PWS_YEAR_KEY).sum()),
        "tthm_system_year_count": int(year_master["tthm_sample_count"].fillna(0).gt(0).sum()),
        "haa5_system_year_count": int(year_master["haa5_sample_count"].fillna(0).gt(0).sum()),
        "tthm_core2_count": int(
            (
                year_master["tthm_sample_count"].fillna(0).gt(0)
                & year_master["n_core_vars_available"].fillna(0).ge(2)
            ).sum()
        ),
        "tthm_core4_count": int(
            (
                year_master["tthm_sample_count"].fillna(0).gt(0)
                & year_master["n_core_vars_available"].fillna(0).ge(4)
            ).sum()
        ),
    }


def assert_expected(actual: dict[str, int], expected: dict[str, int], label: str) -> None:
    mismatches = {
        key: {"actual": actual.get(key), "expected": expected_value}
        for key, expected_value in expected.items()
        if actual.get(key) != expected_value
    }
    if mismatches:
        raise ValueError(f"{label} 校验失败：{mismatches}")


def build_recovered_pws_year() -> pd.DataFrame:
    if not FACILITY_MONTH_PATH.exists() or FACILITY_MONTH_PATH.stat().st_size == 0:
        raise FileNotFoundError(f"无法读取二层主表：{FACILITY_MONTH_PATH}")
    facility_month = pd.read_csv(FACILITY_MONTH_PATH, encoding="utf-8-sig", low_memory=False)
    year_master = build_pws_year_master(facility_month)
    year_master = year_master[order_pws_year_columns(year_master)]
    return year_master


def compare_with_existing_v4_ml_ready(year_master: pd.DataFrame) -> dict[str, object]:
    source_df = year_master[SOURCE_COLUMNS].copy()
    regenerated_ml_ready = build_dataset(source_df)
    regenerated_summary = compute_summary(regenerated_ml_ready)
    assert_expected(regenerated_summary, EXPECTED_V4, "V4 ml-ready 摘要")

    existing_ml_ready = read_v4_ml_ready_csv(V4_ML_READY_PATH)
    existing_summary = compute_summary(existing_ml_ready)
    assert_expected(existing_summary, EXPECTED_V4, "现有 V4 ml-ready 摘要")

    regenerated_ml_ready = regenerated_ml_ready.sort_values(["pwsid", "year"]).reset_index(drop=True)
    existing_ml_ready = existing_ml_ready.sort_values(["pwsid", "year"]).reset_index(drop=True)
    assert_frame_equal(
        regenerated_ml_ready,
        existing_ml_ready,
        check_dtype=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )

    return {
        "regenerated_summary": regenerated_summary,
        "existing_summary": existing_summary,
        "frame_equal": True,
    }


def main() -> None:
    backup_path = backup_current_zero_byte_file()
    year_master = build_recovered_pws_year()
    v3_validation = compute_v3_validation(year_master)
    assert_expected(v3_validation, EXPECTED_V3, "V3 pws-year 摘要")

    v4_comparison = compare_with_existing_v4_ml_ready(year_master)

    year_master.to_csv(RECOVERY_TMP_PATH, index=False, encoding="utf-8-sig")
    reloaded = pd.read_csv(RECOVERY_TMP_PATH, nrows=5, encoding="utf-8-sig", low_memory=False)
    if len(reloaded.columns) != EXPECTED_V3["column_count"]:
        raise ValueError("临时恢复文件字段数不符合预期")
    RECOVERY_TMP_PATH.replace(PWS_YEAR_PATH)

    validation_report = {
        "recovery_time": now_text(),
        "recovery_method": "rebuild_from_existing_V3_facility_month_master_using_original_V3_aggregation_logic",
        "source_facility_month_path": str(FACILITY_MONTH_PATH),
        "recovered_pws_year_path": str(PWS_YEAR_PATH),
        "zero_byte_backup_path": backup_path,
        "v3_validation": v3_validation,
        "v3_expected": EXPECTED_V3,
        "v4_ml_ready_comparison": v4_comparison,
        "status": "passed",
    }
    VALIDATION_PATH.write_text(json.dumps(validation_report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("V3_pws_year_master 恢复完成")
    print(f"输出文件: {PWS_YEAR_PATH}")
    print(f"0 字节备份: {backup_path}")
    print(f"校验报告: {VALIDATION_PATH}")
    print(f"V3 校验: {v3_validation}")
    print(f"V4 ml-ready 对齐: {v4_comparison['frame_equal']}")


if __name__ == "__main__":
    main()
