from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "Project_Data_Integrity_Audit" / "2026_04_15"
REPORT_PATH = DOCS_DIR / "00_overview" / "Legacy_Root_Imports_Cleanup_Audit_Report_2026_04_15.md"
TZ = ZoneInfo("Asia/Hong_Kong")


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_name(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


def find_primary_candidates(legacy_file: Path) -> list[Path]:
    legacy_hash = sha256(legacy_file)
    candidates = []
    for path in DOCS_DIR.rglob("*"):
        if not path.is_file() or "legacy_root_imports" in path.parts:
            continue
        if path.suffix.lower() != legacy_file.suffix.lower():
            continue
        same_hash = sha256(path) == legacy_hash
        name_close = normalize_name(path.stem) == normalize_name(legacy_file.stem)
        if same_hash or name_close:
            candidates.append(path)
    return sorted(candidates)


def classify_legacy_file(legacy_file: Path, candidates: list[Path]) -> dict[str, object]:
    legacy_hash = sha256(legacy_file)
    exact_matches = [path for path in candidates if sha256(path) == legacy_hash]
    same_name = [path for path in candidates if normalize_name(path.stem) == normalize_name(legacy_file.stem)]
    if exact_matches:
        status = "safe_to_remove_candidate"
        reason = "存在正式位置文件与 legacy 文件内容完全一致。"
    elif same_name:
        status = "needs_manual_review"
        reason = "存在名称相近的正式位置文件，但内容不同。"
    else:
        status = "legacy_only_keep_until_reviewed"
        reason = "未找到对应正式位置文件，可能是旧资料或尚未迁移内容。"
    return {
        "legacy_path": rel(legacy_file),
        "size_bytes": legacy_file.stat().st_size,
        "sha256": legacy_hash,
        "candidate_primary_paths": "; ".join(rel(path) for path in candidates),
        "exact_match_paths": "; ".join(rel(path) for path in exact_matches),
        "status": status,
        "reason": reason,
    }


def build_report(df: pd.DataFrame) -> str:
    counts = df["status"].value_counts().to_dict() if not df.empty else {}

    def table_for(status: str) -> str:
        sub = df.loc[df["status"] == status]
        if sub.empty:
            return "- 无。"
        lines = ["| legacy 文件 | 对应正式文件 | 原因 |", "|---|---|---|"]
        for row in sub.to_dict(orient="records"):
            primary = row["exact_match_paths"] or row["candidate_primary_paths"] or "未找到"
            lines.append(f"| `{row['legacy_path']}` | `{primary}` | {row['reason']} |")
        return "\n".join(lines)

    return "\n".join(
        [
            "# legacy_root_imports 清理审计报告",
            "",
            f"- 生成时间：{now_text()}（Asia/Hong_Kong）",
            "- 审计范围：`docs/**/legacy_root_imports/` 下的 Markdown 文件。",
            "- 审计目的：识别早期迁移目录中的重复文件和需要人工确认的旧资料。",
            "- 本报告仅审计，不删除文件。",
            "",
            "## 1. 总体统计",
            "",
            f"- legacy 文件总数：`{len(df)}`",
            f"- 可安全删除候选：`{counts.get('safe_to_remove_candidate', 0)}`",
            f"- 需要人工复核：`{counts.get('needs_manual_review', 0)}`",
            f"- 仅 legacy 存在、暂时保留：`{counts.get('legacy_only_keep_until_reviewed', 0)}`",
            "",
            "## 2. 可安全删除候选",
            "",
            "这些文件在正式位置存在完全相同内容的副本。建议在用户确认后删除 legacy 副本。",
            "",
            table_for("safe_to_remove_candidate"),
            "",
            "## 3. 需要人工复核",
            "",
            "这些文件存在名称相近的正式位置文件，但内容不同。删除前必须确认是否仍保留历史价值。",
            "",
            table_for("needs_manual_review"),
            "",
            "## 4. 仅 legacy 存在，暂时保留",
            "",
            "这些文件没有找到对应正式位置文件。建议暂时保留，除非后续确认已经无历史价值。",
            "",
            table_for("legacy_only_keep_until_reviewed"),
            "",
            "## 5. 建议",
            "",
            "- 当前不建议自动删除全部 `legacy_root_imports`。",
            "- 可优先删除 `safe_to_remove_candidate` 中完全重复的 legacy 副本。",
            "- `needs_manual_review` 和 `legacy_only_keep_until_reviewed` 应先人工确认，再决定是否迁移、合并或删除。",
            "",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    legacy_files = sorted(DOCS_DIR.rglob("legacy_root_imports/*.md"))
    rows = []
    for legacy_file in legacy_files:
        candidates = find_primary_candidates(legacy_file)
        rows.append(classify_legacy_file(legacy_file, candidates))
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "legacy_root_imports_cleanup_audit.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "legacy_root_imports_cleanup_audit.json").write_text(
        json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    REPORT_PATH.write_text(build_report(df), encoding="utf-8")
    print("legacy_root_imports 清理审计完成")
    print(f"报告: {REPORT_PATH}")
    print(f"legacy 文件数: {len(df)}")
    if not df.empty:
        print(df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()
