from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "tthm_first_round"
MAX_EXCEL_ROWS = 1_048_576
MAX_DATA_ROWS = MAX_EXCEL_ROWS - 1


def split_csv_for_excel(source_csv: Path, output_prefix: str) -> list[Path]:
    part_paths: list[Path] = []
    with source_csv.open("r", encoding="utf-8", newline="") as src:
        reader = csv.reader(src)
        header = next(reader)
        part_index = 1
        row_in_part = 0
        writer = None
        dst_handle = None

        for row in reader:
            if writer is None or row_in_part >= MAX_DATA_ROWS:
                if dst_handle is not None:
                    dst_handle.close()
                part_path = OUTPUT_DIR / f"{output_prefix}_part{part_index}.csv"
                dst_handle = part_path.open("w", encoding="utf-8-sig", newline="")
                writer = csv.writer(dst_handle)
                writer.writerow(header)
                part_paths.append(part_path)
                part_index += 1
                row_in_part = 0

            writer.writerow(row)
            row_in_part += 1

        if dst_handle is not None:
            dst_handle.close()

    return part_paths


def main() -> None:
    corechem_csv = OUTPUT_DIR / "tthm_corechem_dataset.csv"
    split_paths = split_csv_for_excel(corechem_csv, "tthm_corechem_dataset_excel_ready")
    print("split_paths")
    for path in split_paths:
        print(path)


if __name__ == "__main__":
    main()
