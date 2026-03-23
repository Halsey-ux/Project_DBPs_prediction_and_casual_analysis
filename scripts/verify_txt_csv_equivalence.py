from __future__ import annotations

import argparse
import csv
from pathlib import Path


def detect_delimiter(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        sample = f.readline()
    return "\t" if "\t" in sample else ","


def iter_rows(path: Path, delimiter: str, encoding: str):
    with path.open("r", encoding=encoding, errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            yield row


def iter_txt_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".txt":
            yield path


def compare_one(txt_path: Path, csv_path: Path) -> tuple[bool, str]:
    txt_delimiter = detect_delimiter(txt_path)
    txt_iter = iter_rows(txt_path, txt_delimiter, "utf-8-sig")
    csv_iter = iter_rows(csv_path, ",", "utf-8")
    row_num = 0

    while True:
        try:
            txt_row = next(txt_iter)
            txt_has = True
        except StopIteration:
            txt_has = False
            txt_row = None

        try:
            csv_row = next(csv_iter)
            csv_has = True
        except StopIteration:
            csv_has = False
            csv_row = None

        if not txt_has and not csv_has:
            return True, "OK"

        row_num += 1
        if txt_has != csv_has:
            return False, f"ROWCOUNT_MISMATCH at row {row_num}"
        if txt_row != csv_row:
            return False, f"CONTENT_MISMATCH at row {row_num}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify mirrored CSV files match source TXT files after parsing.")
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--csv-root", required=True)
    args = parser.parse_args()

    input_root = Path(args.input_root)
    csv_root = Path(args.csv_root)
    files = list(iter_txt_files(input_root))

    print(f"FOUND_FILES\t{len(files)}")

    issues = []
    ok = 0
    for index, txt_path in enumerate(files, start=1):
        rel = txt_path.relative_to(input_root)
        csv_path = (csv_root / rel).with_suffix(".csv")
        if not csv_path.exists():
            issues.append(f"MISSING_CSV\t{rel}")
            continue

        success, message = compare_one(txt_path, csv_path)
        if success:
            ok += 1
        else:
            issues.append(f"{message}\t{rel}")

        if index % 10 == 0:
            print(f"PROGRESS\t{index}/{len(files)}\tlast={rel}")

    print(f"OK_FILES\t{ok}")
    print(f"ISSUES\t{len(issues)}")
    for issue in issues[:500]:
        print(issue)
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
