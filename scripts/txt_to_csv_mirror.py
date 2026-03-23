from __future__ import annotations

import argparse
import csv
from pathlib import Path


def detect_delimiter(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        sample = f.readline()
    return "\t" if "\t" in sample else ","


def iter_txt_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".txt":
            yield path


def convert_one(src: Path, dst: Path) -> dict:
    delimiter = detect_delimiter(src)
    dst.parent.mkdir(parents=True, exist_ok=True)

    rows = 0
    with src.open("r", encoding="utf-8-sig", errors="replace", newline="") as fin, dst.open(
        "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin, delimiter=delimiter)
        writer = csv.writer(fout, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        for row in reader:
            writer.writerow(row)
            rows += 1

    return {"rows_including_header": rows, "source_delimiter": "tab" if delimiter == "\t" else "comma"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Mirror TXT files as CSV while preserving directory structure.")
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    input_root = Path(args.input_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    files = list(iter_txt_files(input_root))
    print(f"FOUND_FILES\t{len(files)}")

    for index, src in enumerate(files, start=1):
        rel = src.relative_to(input_root)
        dst = (output_root / rel).with_suffix(".csv")
        stats = convert_one(src, dst)
        print(
            f"DONE\t{index}/{len(files)}\t{rel}\trows_including_header={stats['rows_including_header']}"
            f"\tsource_delimiter={stats['source_delimiter']}"
        )

    print("ALL_DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
