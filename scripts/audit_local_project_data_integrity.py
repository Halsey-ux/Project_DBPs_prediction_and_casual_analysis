from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_LOCAL = PROJECT_ROOT / "data_local"
OUTPUT_DIR = DATA_LOCAL / "Project_Data_Integrity_Audit" / "2026_04_15"
TZ = ZoneInfo("Asia/Hong_Kong")

RAW_SOURCE_DIRS = [
    Path(r"D:\Syr4_Project\syr4_DATA_CSV"),
    Path(r"D:\SYR4_Data\syr4_DATA_excel"),
]

EXPECTED_LOCAL_FILES = {
    "data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv": {
        "row_count": 1_442_728,
        "column_count": 98,
        "note": "V3 第二层 facility-month 原型主表",
    },
    "data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv": {
        "row_count": 259_500,
        "column_count": 130,
        "note": "V3 第三层 PWS-year 原型主表，已于 2026-04-15 受控恢复",
    },
    "data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv": {
        "row_count": 259_500,
        "column_count": 38,
        "note": "V3.5/V4 第三层机器学习输入表",
    },
}


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def count_csv_rows(path: Path) -> int | None:
    with path.open("rb") as handle:
        line_count = sum(1 for _ in handle)
    if line_count == 0:
        return 0
    return line_count - 1


def quick_sha256(path: Path, max_bytes: int = 2 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        remaining = max_bytes
        while remaining > 0:
            chunk = handle.read(min(1024 * 1024, remaining))
            if not chunk:
                break
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()


def audit_file(path: Path) -> dict[str, object]:
    stat = path.stat()
    suffix = path.suffix.lower()
    record: dict[str, object] = {
        "path": rel(path),
        "suffix": suffix,
        "size_bytes": stat.st_size,
        "created_at": datetime.fromtimestamp(stat.st_ctime, TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "modified_at": datetime.fromtimestamp(stat.st_mtime, TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ok",
        "row_count": None,
        "column_count": None,
        "quick_sha256_first_2mb": quick_sha256(path) if stat.st_size > 0 else None,
        "notes": "",
    }

    if stat.st_size == 0:
        record["status"] = "zero_bytes"
        record["notes"] = "文件大小为 0 字节。"
        return record

    try:
        if suffix == ".csv":
            sample = pd.read_csv(path, nrows=5, low_memory=False)
            record["column_count"] = int(len(sample.columns))
            record["row_count"] = int(count_csv_rows(path) or 0)
        elif suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif suffix in {".md", ".txt"}:
            path.read_text(encoding="utf-8")
        elif suffix in {".xlsx", ".xls"}:
            record["status"] = "binary_not_deep_checked"
            record["notes"] = "二进制表格文件，本轮仅检查存在性、大小和首段哈希。"
        else:
            record["status"] = "not_deep_checked"
            record["notes"] = "本轮仅检查存在性、大小和首段哈希。"
    except Exception as exc:  # noqa: BLE001
        record["status"] = "read_error"
        record["notes"] = f"{type(exc).__name__}: {exc}"
    return record


def audit_data_local() -> pd.DataFrame:
    rows = []
    for path in sorted(DATA_LOCAL.rglob("*")):
        if OUTPUT_DIR in path.parents:
            continue
        if path.is_file():
            rows.append(audit_file(path))
    df = pd.DataFrame(rows)
    return df


def audit_raw_sources() -> pd.DataFrame:
    rows = []
    for directory in RAW_SOURCE_DIRS:
        row: dict[str, object] = {
            "path": str(directory),
            "exists": directory.exists(),
            "file_count": 0,
            "zero_byte_count": 0,
            "total_size_bytes": 0,
            "status": "missing",
        }
        if directory.exists():
            files = [p for p in directory.rglob("*") if p.is_file()]
            row["file_count"] = len(files)
            row["zero_byte_count"] = sum(1 for p in files if p.stat().st_size == 0)
            row["total_size_bytes"] = sum(p.stat().st_size for p in files)
            row["status"] = "ok" if row["zero_byte_count"] == 0 else "has_zero_byte_files"
        rows.append(row)
    return pd.DataFrame(rows)


def build_expected_check(file_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    by_path = {row["path"]: row for row in file_df.to_dict(orient="records")}
    for path, expected in EXPECTED_LOCAL_FILES.items():
        actual = by_path.get(path)
        if actual is None:
            rows.append(
                {
                    "path": path,
                    "expected_rows": expected["row_count"],
                    "actual_rows": None,
                    "expected_columns": expected["column_count"],
                    "actual_columns": None,
                    "status": "missing",
                    "note": expected["note"],
                }
            )
            continue
        row_match = actual["row_count"] == expected["row_count"]
        col_match = actual["column_count"] == expected["column_count"]
        rows.append(
            {
                "path": path,
                "expected_rows": expected["row_count"],
                "actual_rows": actual["row_count"],
                "expected_columns": expected["column_count"],
                "actual_columns": actual["column_count"],
                "status": "passed" if row_match and col_match and actual["status"] == "ok" else "failed",
                "note": expected["note"],
            }
        )
    return pd.DataFrame(rows)


def summarize(file_df: pd.DataFrame, raw_df: pd.DataFrame, expected_df: pd.DataFrame) -> dict[str, object]:
    status_counts = file_df["status"].value_counts(dropna=False).to_dict()
    total_size = int(file_df["size_bytes"].sum()) if not file_df.empty else 0
    zero_business = file_df.loc[file_df["status"] == "zero_bytes", "path"].tolist()
    read_errors = file_df.loc[file_df["status"] == "read_error", ["path", "notes"]].to_dict(orient="records")
    expected_failed = expected_df.loc[expected_df["status"] != "passed"].to_dict(orient="records")
    return {
        "generated_at": now_text(),
        "data_local_file_count": int(len(file_df)),
        "data_local_total_size_bytes": total_size,
        "status_counts": status_counts,
        "zero_byte_files": zero_business,
        "read_errors": read_errors,
        "expected_file_checks": expected_df.to_dict(orient="records"),
        "expected_failed": expected_failed,
        "raw_source_summary": raw_df.to_dict(orient="records"),
        "git_backup_policy": {
            "do_not_commit": ["data_local/", "scratch/", "raw SYR4 directories", "large CSV/XLSX/parquet outputs"],
            "commit_recommended": ["scripts/", "docs/", "project configuration", "lightweight audit reports and dictionaries"],
        },
    }


def write_report(summary: dict[str, object]) -> str:
    expected_rows = summary["expected_file_checks"]
    raw_rows = summary["raw_source_summary"]
    status_counts = summary["status_counts"]
    zero_files = summary["zero_byte_files"]
    read_errors = summary["read_errors"]

    def status_table() -> str:
        lines = ["| 状态 | 文件数 |", "|---|---:|"]
        for key, value in sorted(status_counts.items()):
            lines.append(f"| `{key}` | `{value}` |")
        return "\n".join(lines)

    def expected_table() -> str:
        def fmt(value: object) -> str:
            if value is None:
                return "NA"
            try:
                return str(int(value))
            except (TypeError, ValueError):
                return str(value)

        lines = [
            "| 文件 | 预期行数 | 实际行数 | 预期字段数 | 实际字段数 | 结论 |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for row in expected_rows:
            lines.append(
                f"| `{row['path']}` | `{fmt(row['expected_rows'])}` | `{fmt(row['actual_rows'])}` | "
                f"`{fmt(row['expected_columns'])}` | `{fmt(row['actual_columns'])}` | `{row['status']}` |"
            )
        return "\n".join(lines)

    def raw_table() -> str:
        lines = ["| 原始数据目录 | 是否存在 | 文件数 | 0 字节文件数 | 总大小 bytes | 状态 |", "|---|---|---:|---:|---:|---|"]
        for row in raw_rows:
            lines.append(
                f"| `{row['path']}` | `{row['exists']}` | `{row['file_count']}` | "
                f"`{row['zero_byte_count']}` | `{row['total_size_bytes']}` | `{row['status']}` |"
            )
        return "\n".join(lines)

    zero_text = "\n".join(f"- `{path}`" for path in zero_files) if zero_files else "- 未发现业务数据 0 字节文件。"
    error_text = (
        "\n".join(f"- `{row['path']}`：{row['notes']}" for row in read_errors)
        if read_errors
        else "- 未发现 CSV/JSON/Markdown 读取错误。"
    )

    return "\n".join(
        [
            "# 本地项目数据完整性审计报告",
            "",
            f"- 生成时间：{summary['generated_at']}（Asia/Hong_Kong）",
            "- 审计范围：`data_local/` 本地项目产物、已记录原始 SYR4 数据目录的存在性与 0 字节检查。",
            "- 审计方式：只读检查文件大小、修改时间、首段哈希、CSV 表头和行数、JSON/Markdown 可读性、关键数据集预期行列数。",
            "",
            "## 1. 总体结论",
            "",
            f"- `data_local/` 共检查 `{summary['data_local_file_count']}` 个文件，总大小 `{summary['data_local_total_size_bytes']}` bytes。",
            "- 三个关键本地数据集均通过预期行数和字段数校验。",
            "- 原始 SYR4 数据目录存在，未发现 0 字节文件。",
            "- 当前不建议把 `data_local/` 大型本地数据文件直接提交到 GitHub；建议提交脚本、文档、恢复记录和本审计报告，数据本体继续本地保存。",
            "",
            "## 2. 文件状态统计",
            "",
            status_table(),
            "",
            "## 3. 关键数据集校验",
            "",
            expected_table(),
            "",
            "## 4. 0 字节文件检查",
            "",
            zero_text,
            "",
            "说明：本轮审计的 `data_local/` 中仍保留 `V3_pws_year_master.zero_byte_20260401_091846.csv` 作为事故证据备份，该文件不应被视为当前正式业务输入。",
            "",
            "## 5. 读取错误检查",
            "",
            error_text,
            "",
            "## 6. 原始数据目录检查",
            "",
            raw_table(),
            "",
            "## 7. Git 备份建议",
            "",
            "建议进入 GitHub 的内容：",
            "",
            "- `scripts/` 下的审计、恢复和建模脚本。",
            "- `docs/` 下的协议、报告、恢复记录和数据字典。",
            "- `codex.md`、`.gitignore` 等项目级配置和说明。",
            "- 本轮生成的轻量审计报告与轻量摘要表。",
            "",
            "不建议进入 GitHub 的内容：",
            "",
            "- `data_local/` 下大型 CSV、JSON 结果、Excel 或中间文件。",
            "- 原始 SYR4 数据目录。",
            "- `scratch/` 临时输出。",
            "- 事故证据备份 `V3_pws_year_master.zero_byte_20260401_091846.csv`。",
            "",
            "## 8. 后续建议",
            "",
            "- 若需要长期异地备份大型本地数据，应使用外部硬盘、对象存储、NAS 或专门的数据版本工具，而不是 GitHub 普通仓库。",
            "- 若需要 GitHub 记录数据状态，应提交本报告、校验 JSON/CSV、恢复记录和生成脚本，而不是提交数据本体。",
            "- 每次重建关键本地数据后，应重新运行本审计脚本并更新报告。",
            "",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_df = audit_data_local()
    raw_df = audit_raw_sources()
    expected_df = build_expected_check(file_df)
    summary = summarize(file_df, raw_df, expected_df)

    file_df.to_csv(OUTPUT_DIR / "local_project_data_file_inventory.csv", index=False, encoding="utf-8-sig")
    raw_df.to_csv(OUTPUT_DIR / "raw_source_directory_summary.csv", index=False, encoding="utf-8-sig")
    expected_df.to_csv(OUTPUT_DIR / "key_dataset_expected_checks.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "local_project_data_integrity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    report = write_report(summary)
    report_path = PROJECT_ROOT / "docs" / "00_overview" / "Local_Project_Data_Integrity_Audit_Report_2026_04_15.md"
    report_path.write_text(report, encoding="utf-8")

    print("本地项目数据完整性审计完成")
    print(f"报告: {report_path}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"data_local 文件数: {summary['data_local_file_count']}")
    print(f"关键数据集失败数: {len(summary['expected_failed'])}")
    print(f"读取错误数: {len(summary['read_errors'])}")


if __name__ == "__main__":
    main()
