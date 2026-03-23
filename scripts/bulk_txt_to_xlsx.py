from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


EXCEL_MAX_ROWS = 1_048_576
MAX_DATA_ROWS_PER_SHEET = EXCEL_MAX_ROWS - 1
INVALID_SHEET_CHARS = set("[]:*?/\\")
INVALID_XML_RE = re.compile(
    "["  # XML 1.0 disallowed chars except TAB/LF/CR
    "\x00-\x08"
    "\x0B-\x0C"
    "\x0E-\x1F"
    "\uD800-\uDFFF"
    "\uFFFE-\uFFFF"
    "]"
)


def iter_txt_files(root: Path, exclude_root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() != ".txt":
            continue
        if exclude_root in path.parents:
            continue
        yield path


def detect_delimiter(first_line: str) -> str:
    return "\t" if "\t" in first_line else ","


def col_letter(index: int) -> str:
    letters = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def safe_sheet_name(stem: str, sheet_index: int) -> str:
    base = "".join("_" if ch in INVALID_SHEET_CHARS else ch for ch in stem).strip()
    base = base or "Sheet"
    suffix = f"_{sheet_index}"
    max_base_len = 31 - len(suffix)
    if max_base_len < 1:
        return f"S{suffix}"[:31]
    return f"{base[:max_base_len]}{suffix}"


def build_cell_xml(row_index: int, col_index: int, value: str) -> str:
    if value is None:
        value = ""
    value = INVALID_XML_RE.sub("", str(value))
    if value == "":
        return ""
    ref = f"{col_letter(col_index)}{row_index}"
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'


def write_sheet_header(sheet_handle) -> None:
    sheet_handle.write(
        b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        b'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        b"<sheetData>"
    )


def write_sheet_footer(sheet_handle) -> None:
    sheet_handle.write(b"</sheetData></worksheet>")


def write_row(sheet_handle, row_index: int, row_values: list[str]) -> None:
    cells = []
    for col_index, value in enumerate(row_values, start=1):
        cell_xml = build_cell_xml(row_index, col_index, value)
        if cell_xml:
            cells.append(cell_xml)
    row_xml = f'<row r="{row_index}">{"".join(cells)}</row>'
    sheet_handle.write(row_xml.encode("utf-8"))


def open_new_sheet(zip_file: ZipFile, stem: str, sheet_index: int):
    sheet_path = f"xl/worksheets/sheet{sheet_index}.xml"
    handle = zip_file.open(sheet_path, "w")
    write_sheet_header(handle)
    return handle


def convert_one_file(src: Path, dst: Path) -> dict:
    dst.parent.mkdir(parents=True, exist_ok=True)

    with src.open("r", encoding="utf-8-sig", errors="replace", newline="") as infile:
        first_line = infile.readline().rstrip("\r\n")
        if not first_line:
            raise ValueError(f"Empty file: {src}")
        delimiter = detect_delimiter(first_line)
        infile.seek(0)
        reader = csv.reader(infile, delimiter=delimiter)
        header = [item.strip('"') for item in next(reader)]

        total_rows = 0
        sheet_index = 1
        current_sheet_rows = 0
        sheet_row_counts: list[int] = []

        with ZipFile(dst, "w", compression=ZIP_DEFLATED, compresslevel=6) as zf:
            sheet_handle = open_new_sheet(zf, src.stem, sheet_index)
            write_row(sheet_handle, 1, header)

            for row in reader:
                row = [item.strip('"') for item in row]
                total_rows += 1

                if current_sheet_rows == MAX_DATA_ROWS_PER_SHEET:
                    write_sheet_footer(sheet_handle)
                    sheet_handle.close()
                    sheet_row_counts.append(current_sheet_rows)
                    sheet_index += 1
                    current_sheet_rows = 0
                    sheet_handle = open_new_sheet(zf, src.stem, sheet_index)
                    write_row(sheet_handle, 1, header)

                current_sheet_rows += 1
                write_row(sheet_handle, current_sheet_rows + 1, row)

            write_sheet_footer(sheet_handle)
            sheet_handle.close()
            sheet_row_counts.append(current_sheet_rows)

            write_workbook_files(zf, src.stem, sheet_index)

    return {
        "rows": total_rows,
        "cols": len(header),
        "delimiter": "tab" if delimiter == "\t" else "comma",
        "sheets": sheet_index,
        "sheet_row_counts": sheet_row_counts,
    }


def write_workbook_files(zip_file: ZipFile, stem: str, sheet_count: int) -> None:
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
    ]
    for i in range(1, sheet_count + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    workbook_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for i in range(1, sheet_count + 1):
        workbook_rels.append(
            f'<Relationship Id="rId{i}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i}.xml"/>'
        )
    workbook_rels.append("</Relationships>")

    workbook = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>',
    ]
    for i in range(1, sheet_count + 1):
        workbook.append(
            f'<sheet name="{escape(safe_sheet_name(stem, i))}" sheetId="{i}" r:id="rId{i}"/>'
        )
    workbook.append("</sheets></workbook>")

    zip_file.writestr("[Content_Types].xml", "".join(content_types))
    zip_file.writestr("_rels/.rels", root_rels)
    zip_file.writestr("xl/_rels/workbook.xml.rels", "".join(workbook_rels))
    zip_file.writestr("xl/workbook.xml", "".join(workbook))


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert tab/comma-delimited TXT files to XLSX.")
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    input_root = Path(args.input_root)
    output_root = Path(args.output_root)

    if not input_root.exists():
        print(f"Input root does not exist: {input_root}", file=sys.stderr)
        return 1

    output_root.mkdir(parents=True, exist_ok=True)
    files = list(iter_txt_files(input_root, output_root))
    print(f"FOUND_FILES\t{len(files)}")

    for index, src in enumerate(files, start=1):
        rel = src.relative_to(input_root)
        dst = (output_root / rel).with_suffix(".xlsx")
        stats = convert_one_file(src, dst)
        sheet_stats = ",".join(str(v) for v in stats["sheet_row_counts"])
        print(
            f"DONE\t{index}/{len(files)}\t{rel}\trows={stats['rows']}\tcols={stats['cols']}"
            f"\tdelim={stats['delimiter']}\tsheets={stats['sheets']}\tsheet_rows={sheet_stats}"
        )

    print("ALL_DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
