from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V2_Chapter1_Part1_DBP_Data_Foundation"

RAW_ROOT = Path(r"D:\Syr4_Project\syr4_DATA_CSV")

STRICT_LEVEL = "strict_sample"
FACILITY_MONTH_LEVEL = "facility_month"
SYSTEM_YEAR_LEVEL = "system_year"
LEVEL_ORDER = [STRICT_LEVEL, FACILITY_MONTH_LEVEL, SYSTEM_YEAR_LEVEL]

CORE4_PREDICTORS = ["ph", "alkalinity", "toc", "free_chlorine"]
CORE5_PREDICTORS = [*CORE4_PREDICTORS, "total_chlorine"]
SUPPLEMENTAL_PREDICTORS = ["doc", "suva", "uv254"]


@dataclass(frozen=True)
class SourceSpec:
    key: str
    label: str
    category: str
    path: Path
    natural_level: str
    notes: str = ""


SOURCE_SPECS = [
    SourceSpec(
        key="tthm",
        label="TTHM",
        category="结果变量",
        path=RAW_ROOT / "SYR4_THMs" / "TOTAL TRIHALOMETHANES (TTHM).csv",
        natural_level="样本级 occurrence",
        notes="THM 总量结果变量。",
    ),
    SourceSpec(
        key="haa5",
        label="HAA5",
        category="结果变量",
        path=RAW_ROOT / "SYR4_HAAs" / "HALOACETIC ACIDS (HAA5).csv",
        natural_level="样本级 occurrence",
        notes="HAA 总量结果变量。",
    ),
    SourceSpec(
        key="ph",
        label="pH",
        category="反应条件",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "PH.csv",
        natural_level="样本级 occurrence",
        notes="酸碱条件。",
    ),
    SourceSpec(
        key="alkalinity",
        label="总碱度",
        category="前体/反应条件",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "TOTAL ALKALINITY.csv",
        natural_level="样本级 occurrence",
        notes="缓冲能力与反应环境代理变量。",
    ),
    SourceSpec(
        key="toc",
        label="TOC",
        category="前体变量",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "TOTAL ORGANIC CARBON.csv",
        natural_level="样本级 occurrence",
        notes="DBP 前体总量代理变量。",
    ),
    SourceSpec(
        key="doc",
        label="DOC",
        category="前体变量",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "DOC.csv",
        natural_level="样本级 occurrence",
        notes="溶解性有机碳，前体更贴近反应相。",
    ),
    SourceSpec(
        key="suva",
        label="SUVA",
        category="前体变量",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "SUVA.csv",
        natural_level="样本级 occurrence",
        notes="芳香性与腐殖化特征代理变量。",
    ),
    SourceSpec(
        key="uv254",
        label="UV254",
        category="前体变量",
        path=RAW_ROOT / "SYR4_DBP_Related Parameters" / "UV_ABSORBANCE.csv",
        natural_level="样本级 occurrence",
        notes="紫外吸光度，反映芳香性有机物负荷。",
    ),
    SourceSpec(
        key="free_chlorine",
        label="游离余氯",
        category="消毒过程变量",
        path=RAW_ROOT
        / "SYR4_Disinfectant Residuals"
        / "FREE RESIDUAL CHLORINE (1013).csv",
        natural_level="样本级 occurrence",
        notes="更贴近有效氧化剂暴露。",
    ),
    SourceSpec(
        key="total_chlorine",
        label="总氯",
        category="消毒过程变量",
        path=RAW_ROOT / "SYR4_Disinfectant Residuals" / "TOTAL CHLORINE (1000).csv",
        natural_level="样本级 occurrence",
        notes="游离氯与化合氯总和。",
    ),
    SourceSpec(
        key="chloramine",
        label="氯胺",
        category="消毒过程变量",
        path=RAW_ROOT / "SYR4_Disinfectant Residuals" / "CHLORAMINE (1006).csv",
        natural_level="样本级 occurrence",
        notes="用于辨识以氯胺为主的消毒语境。",
    ),
]


PAIRED_TOC_ALK_PATH = (
    RAW_ROOT / "SYR4_DBP_Related Parameters" / "Paired TOC-Alkalinity.csv"
)
TREATMENT_DIR = RAW_ROOT / "syr4_treatment"

TREATMENT_TABLE_PATHS = {
    "water_system": TREATMENT_DIR / "SYR4_Water_system_table.csv",
    "water_system_facility": TREATMENT_DIR / "SYR4_Water_system_facility_table.csv",
    "facility_plant": TREATMENT_DIR / "SYR4_Water_system_facility_plant_table.csv",
    "treatment_process": TREATMENT_DIR / "SYR4_Treatment_Process_table.csv",
    "facility_flow": TREATMENT_DIR / "SYR4_Water_system_flows_table.csv",
}


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_string(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NA": pd.NA})


def normalize_facility_id_value(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    if text.endswith(".00"):
        text = text[:-3]
    elif text.endswith(".0"):
        text = text[:-2]
    return text


def normalize_facility_id_series(series: pd.Series) -> pd.Series:
    return series.map(normalize_facility_id_value, na_action="ignore").astype("string")


def parse_sample_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="%d-%b-%y", errors="coerce")


def hash_key_frame(frame: pd.DataFrame) -> np.ndarray:
    normalized = frame.copy()
    for column in normalized.columns:
        normalized[column] = normalized[column].astype("string")
    return pd.util.hash_pandas_object(normalized, index=False).to_numpy(dtype="uint64")


def top_units(counter: Counter[str], n: int = 5) -> str:
    if not counter:
        return "NA"
    return "; ".join(f"{unit}:{count}" for unit, count in counter.most_common(n))


def set_to_array(values: set[int]) -> np.ndarray:
    if not values:
        return np.array([], dtype="uint64")
    return np.array(sorted(values), dtype="uint64")


def intersect_count(arrays: Iterable[np.ndarray]) -> int:
    filtered = [array for array in arrays if array.size > 0]
    if not filtered:
        return 0
    current = filtered[0]
    for array in filtered[1:]:
        current = np.intersect1d(current, array, assume_unique=True)
        if current.size == 0:
            return 0
    return int(current.size)


def format_pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.00%"
    return f"{numerator / denominator * 100:.2f}%"


def to_markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy().fillna("")
    headers = [str(column) for column in display.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in display.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def build_presence_frame(
    source_hashes: dict[str, dict[str, np.ndarray]],
    level: str,
) -> pd.DataFrame:
    arrays = [source_hashes[spec.key][level] for spec in SOURCE_SPECS]
    arrays = [array for array in arrays if array.size > 0]
    if not arrays:
        columns = ["key_hash", *[spec.key for spec in SOURCE_SPECS]]
        return pd.DataFrame(columns=columns)

    all_keys = np.unique(np.concatenate(arrays))
    presence = pd.DataFrame({"key_hash": all_keys})
    key_index = pd.Index(presence["key_hash"])
    for spec in SOURCE_SPECS:
        values = source_hashes[spec.key][level]
        presence[spec.key] = key_index.isin(values)
    return presence


def scan_occurrence_source(spec: SourceSpec) -> dict[str, object]:
    usecols = [
        "PWSID",
        "WATER_FACILITY_ID",
        "SAMPLING_POINT_ID",
        "SAMPLE_COLLECTION_DATE",
        "VALUE",
        "UNIT",
    ]
    row_count = 0
    numeric_row_count = 0
    unit_counter: Counter[str] = Counter()
    pws_ids: set[str] = set()
    facility_ids: set[str] = set()
    level_key_sets = {level: set() for level in LEVEL_ORDER}

    for chunk in pd.read_csv(
        spec.path,
        usecols=usecols,
        dtype={
            "PWSID": "string",
            "WATER_FACILITY_ID": "string",
            "SAMPLING_POINT_ID": "string",
            "SAMPLE_COLLECTION_DATE": "string",
            "VALUE": "string",
            "UNIT": "string",
        },
        low_memory=False,
        chunksize=250000,
    ):
        row_count += len(chunk)
        chunk["PWSID"] = clean_string(chunk["PWSID"])
        chunk["WATER_FACILITY_ID"] = normalize_facility_id_series(
            clean_string(chunk["WATER_FACILITY_ID"])
        )
        chunk["SAMPLING_POINT_ID"] = clean_string(chunk["SAMPLING_POINT_ID"])
        chunk["SAMPLE_COLLECTION_DATE"] = parse_sample_date(
            clean_string(chunk["SAMPLE_COLLECTION_DATE"])
        )
        chunk["VALUE_NUM"] = pd.to_numeric(chunk["VALUE"], errors="coerce")
        chunk["UNIT"] = clean_string(chunk["UNIT"])

        numeric = chunk.loc[chunk["VALUE_NUM"].notna()].copy()
        if numeric.empty:
            continue

        numeric_row_count += len(numeric)
        numeric["year"] = numeric["SAMPLE_COLLECTION_DATE"].dt.year.astype("Int64")
        numeric["month"] = numeric["SAMPLE_COLLECTION_DATE"].dt.month.astype("Int64")

        unit_counter.update(
            unit for unit in numeric["UNIT"].dropna().astype(str).tolist() if unit
        )
        pws_ids.update(
            value for value in numeric["PWSID"].dropna().astype(str).tolist() if value
        )
        facility_ids.update(
            value
            for value in numeric["WATER_FACILITY_ID"].dropna().astype(str).tolist()
            if value
        )

        level_columns = {
            STRICT_LEVEL: [
                "PWSID",
                "WATER_FACILITY_ID",
                "SAMPLING_POINT_ID",
                "SAMPLE_COLLECTION_DATE",
            ],
            FACILITY_MONTH_LEVEL: ["PWSID", "WATER_FACILITY_ID", "year", "month"],
            SYSTEM_YEAR_LEVEL: ["PWSID", "year"],
        }
        for level, columns in level_columns.items():
            key_frame = numeric[columns].dropna().drop_duplicates()
            if key_frame.empty:
                continue
            if "SAMPLE_COLLECTION_DATE" in key_frame.columns:
                key_frame = key_frame.assign(
                    SAMPLE_COLLECTION_DATE=key_frame["SAMPLE_COLLECTION_DATE"].dt.strftime(
                        "%Y-%m-%d"
                    )
                )
            hashes = np.unique(hash_key_frame(key_frame))
            level_key_sets[level].update(int(value) for value in hashes.tolist())

    return {
        "key": spec.key,
        "label": spec.label,
        "category": spec.category,
        "path": str(spec.path),
        "natural_level": spec.natural_level,
        "notes": spec.notes,
        "row_count": int(row_count),
        "numeric_row_count": int(numeric_row_count),
        "unit_top5": top_units(unit_counter),
        "unique_pws_count": int(len(pws_ids)),
        "unique_facility_count": int(len(facility_ids)),
        "facility_ids": sorted(facility_ids),
        "level_hashes": {
            level: set_to_array(level_key_sets[level]) for level in LEVEL_ORDER
        },
    }


def scan_paired_toc_alk() -> dict[str, object]:
    df = pd.read_csv(
        PAIRED_TOC_ALK_PATH,
        dtype={
            "PWSID": "string",
            "Water.Facility.ID": "string",
            "Year": "string",
            "Month": "string",
        },
        low_memory=False,
    )
    df["PWSID"] = clean_string(df["PWSID"])
    df["Water.Facility.ID"] = normalize_facility_id_series(
        clean_string(df["Water.Facility.ID"])
    )
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Month"] = pd.to_numeric(df["Month"], errors="coerce").astype("Int64")
    key_frame = df[["PWSID", "Water.Facility.ID", "Year", "Month"]].dropna().drop_duplicates()
    return {
        "row_count": int(len(df)),
        "unique_facility_month_keys": int(len(key_frame)),
        "unique_pws_count": int(df["PWSID"].dropna().nunique()),
        "unique_facility_count": int(df["Water.Facility.ID"].dropna().nunique()),
        "hashes": np.unique(
            hash_key_frame(
                key_frame.rename(
                    columns={
                        "Water.Facility.ID": "WATER_FACILITY_ID",
                        "Year": "year",
                        "Month": "month",
                    }
                )
            )
        ),
    }


def read_treatment_header(path: Path) -> list[str]:
    return pd.read_csv(path, nrows=0).columns.tolist()


def scan_treatment_tables(
    occurrence_results: dict[str, dict[str, object]]
) -> dict[str, object]:
    water_system_header = read_treatment_header(TREATMENT_TABLE_PATHS["water_system"])
    facility_header = read_treatment_header(TREATMENT_TABLE_PATHS["water_system_facility"])
    plant_header = read_treatment_header(TREATMENT_TABLE_PATHS["facility_plant"])
    process_header = read_treatment_header(TREATMENT_TABLE_PATHS["treatment_process"])
    flow_header = read_treatment_header(TREATMENT_TABLE_PATHS["facility_flow"])

    facility_df = pd.read_csv(
        TREATMENT_TABLE_PATHS["water_system_facility"],
        usecols=["Water System ID", "Water Facility ID", "Water Facility Type"],
        low_memory=False,
    )
    plant_df = pd.read_csv(
        TREATMENT_TABLE_PATHS["facility_plant"],
        usecols=["Treatment Plant ID", "Water Facility ID"],
        low_memory=False,
    )
    process_df = pd.read_csv(
        TREATMENT_TABLE_PATHS["treatment_process"],
        usecols=["Treatment Process ID", "Water Facility ID"],
        low_memory=False,
    )

    facility_ids = {
        value
        for value in normalize_facility_id_series(facility_df["Water Facility ID"])
        .dropna()
        .astype(str)
        .tolist()
        if value
    }
    plant_facility_ids = {
        value
        for value in normalize_facility_id_series(plant_df["Water Facility ID"])
        .dropna()
        .astype(str)
        .tolist()
        if value
    }
    process_facility_ids = {
        value
        for value in normalize_facility_id_series(process_df["Water Facility ID"])
        .dropna()
        .astype(str)
        .tolist()
        if value
    }

    tthm_facilities = set(occurrence_results["tthm"]["facility_ids"])
    haa5_facilities = set(occurrence_results["haa5"]["facility_ids"])

    return {
        "headers": {
            "water_system": water_system_header,
            "water_system_facility": facility_header,
            "facility_plant": plant_header,
            "treatment_process": process_header,
            "facility_flow": flow_header,
        },
        "row_counts": {
            "water_system_facility": int(len(facility_df)),
            "facility_plant": int(len(plant_df)),
            "treatment_process": int(len(process_df)),
        },
        "unique_facility_counts": {
            "water_system_facility": int(len(facility_ids)),
            "facility_plant": int(len(plant_facility_ids)),
            "treatment_process": int(len(process_facility_ids)),
        },
        "tthm_overlap": {
            "in_water_system_facility": int(len(tthm_facilities & facility_ids)),
            "in_facility_plant": int(len(tthm_facilities & plant_facility_ids)),
            "in_treatment_process": int(len(tthm_facilities & process_facility_ids)),
            "tthm_unique_facilities": int(len(tthm_facilities)),
        },
        "haa5_overlap": {
            "in_water_system_facility": int(len(haa5_facilities & facility_ids)),
            "in_facility_plant": int(len(haa5_facilities & plant_facility_ids)),
            "in_treatment_process": int(len(haa5_facilities & process_facility_ids)),
            "haa5_unique_facilities": int(len(haa5_facilities)),
        },
    }


def build_source_inventory(results: dict[str, dict[str, object]]) -> pd.DataFrame:
    rows = []
    for spec in SOURCE_SPECS:
        item = results[spec.key]
        rows.append(
            {
                "变量键": spec.key,
                "变量名": spec.label,
                "变量类别": spec.category,
                "文件路径": item["path"],
                "原始记录数": item["row_count"],
                "数值非缺失原始行数": item["numeric_row_count"],
                "严格样本级唯一键数": len(item["level_hashes"][STRICT_LEVEL]),
                "设施-月份级唯一键数": len(item["level_hashes"][FACILITY_MONTH_LEVEL]),
                "系统-年份级唯一键数": len(item["level_hashes"][SYSTEM_YEAR_LEVEL]),
                "唯一 PWS 数": item["unique_pws_count"],
                "唯一设施数": item["unique_facility_count"],
                "单位 Top5": item["unit_top5"],
                "自然粒度": item["natural_level"],
                "备注": item["notes"],
            }
        )
    return pd.DataFrame(rows)


def build_level_variable_coverage(
    source_hashes: dict[str, dict[str, np.ndarray]]
) -> pd.DataFrame:
    rows = []
    for level in LEVEL_ORDER:
        presence = build_presence_frame(source_hashes, level)
        union_count = int(len(presence))
        tthm_count = int(presence["tthm"].sum()) if "tthm" in presence else 0
        haa5_count = int(presence["haa5"].sum()) if "haa5" in presence else 0

        for spec in SOURCE_SPECS:
            key_count = int(presence[spec.key].sum()) if spec.key in presence else 0
            intersect_tthm = (
                int((presence[spec.key] & presence["tthm"]).sum())
                if {"tthm", spec.key}.issubset(presence.columns)
                else 0
            )
            intersect_haa5 = (
                int((presence[spec.key] & presence["haa5"]).sum())
                if {"haa5", spec.key}.issubset(presence.columns)
                else 0
            )
            rows.append(
                {
                    "分析层级": level,
                    "变量键": spec.key,
                    "变量名": spec.label,
                    "变量类别": spec.category,
                    "唯一键数": key_count,
                    "占全变量并集覆盖率": format_pct(key_count, union_count),
                    "与 TTHM 交集键数": intersect_tthm,
                    "占 TTHM 键覆盖率": format_pct(intersect_tthm, tthm_count),
                    "与 HAA5 交集键数": intersect_haa5,
                    "占 HAA5 键覆盖率": format_pct(intersect_haa5, haa5_count),
                }
            )
    return pd.DataFrame(rows)


def build_level_summary(source_hashes: dict[str, dict[str, np.ndarray]]) -> pd.DataFrame:
    rows = []
    for level in LEVEL_ORDER:
        presence = build_presence_frame(source_hashes, level)
        union_key_count = int(len(presence))
        tthm_count = int(presence["tthm"].sum())
        haa5_count = int(presence["haa5"].sum())
        tthm_haa5_overlap = int((presence["tthm"] & presence["haa5"]).sum())

        predictor_any_core4 = presence[CORE4_PREDICTORS].any(axis=1)
        predictor_any_core5 = presence[CORE5_PREDICTORS].any(axis=1)
        predictor_two_core4 = presence[CORE4_PREDICTORS].sum(axis=1) >= 2
        predictor_two_core5 = presence[CORE5_PREDICTORS].sum(axis=1) >= 2

        rows.append(
            {
                "分析层级": level,
                "并集唯一键数": union_key_count,
                "TTHM 唯一键数": tthm_count,
                "HAA5 唯一键数": haa5_count,
                "TTHM-HAA5 交集键数": tthm_haa5_overlap,
                "TTHM 中 HAA5 覆盖率": format_pct(tthm_haa5_overlap, tthm_count),
                "HAA5 中 TTHM 覆盖率": format_pct(tthm_haa5_overlap, haa5_count),
                "TTHM + 核心四变量至少 1 个预测变量": int(
                    (presence["tthm"] & predictor_any_core4).sum()
                ),
                "TTHM + 核心四变量至少 2 个预测变量": int(
                    (presence["tthm"] & predictor_two_core4).sum()
                ),
                "TTHM + 核心四变量全齐": int(
                    presence[["tthm", *CORE4_PREDICTORS]].all(axis=1).sum()
                ),
                "TTHM + 扩展五变量至少 1 个预测变量": int(
                    (presence["tthm"] & predictor_any_core5).sum()
                ),
                "TTHM + 扩展五变量至少 2 个预测变量": int(
                    (presence["tthm"] & predictor_two_core5).sum()
                ),
                "TTHM + 扩展五变量全齐": int(
                    presence[["tthm", *CORE5_PREDICTORS]].all(axis=1).sum()
                ),
                "HAA5 + 核心四变量至少 1 个预测变量": int(
                    (presence["haa5"] & predictor_any_core4).sum()
                ),
                "HAA5 + 核心四变量至少 2 个预测变量": int(
                    (presence["haa5"] & predictor_two_core4).sum()
                ),
                "HAA5 + 核心四变量全齐": int(
                    presence[["haa5", *CORE4_PREDICTORS]].all(axis=1).sum()
                ),
                "HAA5 + 扩展五变量全齐": int(
                    presence[["haa5", *CORE5_PREDICTORS]].all(axis=1).sum()
                ),
                "TTHM + DOC/SUVA/UV254 全齐": int(
                    presence[["tthm", *SUPPLEMENTAL_PREDICTORS]].all(axis=1).sum()
                ),
                "HAA5 + DOC/SUVA/UV254 全齐": int(
                    presence[["haa5", *SUPPLEMENTAL_PREDICTORS]].all(axis=1).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def build_relationship_summary(
    source_hashes: dict[str, dict[str, np.ndarray]],
    paired_summary: dict[str, object],
    treatment_summary: dict[str, object],
) -> pd.DataFrame:
    tthm_facility_month = source_hashes["tthm"][FACILITY_MONTH_LEVEL]
    haa5_facility_month = source_hashes["haa5"][FACILITY_MONTH_LEVEL]
    paired_hashes = paired_summary["hashes"]

    rows = [
        {
            "关系对象": "Paired TOC-Alkalinity",
            "自然粒度": "PWSID + WATER_FACILITY_ID + year + month",
            "唯一键数": paired_summary["unique_facility_month_keys"],
            "与 TTHM 设施-月份交集键数": int(
                np.intersect1d(paired_hashes, tthm_facility_month, assume_unique=True).size
            ),
            "与 HAA5 设施-月份交集键数": int(
                np.intersect1d(paired_hashes, haa5_facility_month, assume_unique=True).size
            ),
            "说明": "说明该表应在设施-月份级接入，而不是样本级硬拼。",
        },
        {
            "关系对象": "treatment water_system_facility",
            "自然粒度": "facility 映射表",
            "唯一键数": treatment_summary["unique_facility_counts"][
                "water_system_facility"
            ],
            "与 TTHM 设施交集键数": treatment_summary["tthm_overlap"][
                "in_water_system_facility"
            ],
            "与 HAA5 设施交集键数": treatment_summary["haa5_overlap"][
                "in_water_system_facility"
            ],
            "说明": "用于把监测结果挂回 system-facility 结构层。",
        },
        {
            "关系对象": "treatment facility_plant",
            "自然粒度": "facility plant 属性表",
            "唯一键数": treatment_summary["unique_facility_counts"]["facility_plant"],
            "与 TTHM 设施交集键数": treatment_summary["tthm_overlap"]["in_facility_plant"],
            "与 HAA5 设施交集键数": treatment_summary["haa5_overlap"]["in_facility_plant"],
            "说明": "更适合作为设施层解释变量，不适合样本级 join。",
        },
        {
            "关系对象": "treatment process",
            "自然粒度": "facility-process 一对多表",
            "唯一键数": treatment_summary["unique_facility_counts"]["treatment_process"],
            "与 TTHM 设施交集键数": treatment_summary["tthm_overlap"][
                "in_treatment_process"
            ],
            "与 HAA5 设施交集键数": treatment_summary["haa5_overlap"][
                "in_treatment_process"
            ],
            "说明": "适合作为设施级工艺背景，需要先聚合结果层再接入。",
        },
    ]
    return pd.DataFrame(rows)


def build_audit_report(
    source_inventory: pd.DataFrame,
    level_summary: pd.DataFrame,
    level_variable_coverage: pd.DataFrame,
    relationship_summary: pd.DataFrame,
    paired_summary: dict[str, object],
    treatment_summary: dict[str, object],
) -> str:
    strict_summary = level_summary.loc[
        level_summary["分析层级"] == STRICT_LEVEL
    ].iloc[0]
    facility_summary = level_summary.loc[
        level_summary["分析层级"] == FACILITY_MONTH_LEVEL
    ].iloc[0]
    system_summary = level_summary.loc[
        level_summary["分析层级"] == SYSTEM_YEAR_LEVEL
    ].iloc[0]

    lines = [
        "# 第一章第一部分 DBP 数据基础审计报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 输出目录：`{OUTPUT_DIR}`",
        "- 目的：为第一章第一部分提供变量覆盖、跨表可拼接性、分层数据路线与 V1 重新定位依据。",
        "",
        "## 1. 本次审计纳入的 DBP 相关文件",
        "",
        to_markdown_table(
            source_inventory[
                [
                    "变量名",
                    "变量类别",
                    "原始记录数",
                    "数值非缺失原始行数",
                    "严格样本级唯一键数",
                    "设施-月份级唯一键数",
                    "系统-年份级唯一键数",
                    "单位 Top5",
                ]
            ]
        ),
        "",
        "## 2. 三层级总体可用性摘要",
        "",
        to_markdown_table(level_summary),
        "",
        "## 3. 与 TTHM/HAA5 的变量交集覆盖",
        "",
        "### 3.1 严格样本级",
        "",
        to_markdown_table(
            level_variable_coverage.loc[
                level_variable_coverage["分析层级"] == STRICT_LEVEL
            ]
        ),
        "",
        "### 3.2 设施-月份级",
        "",
        to_markdown_table(
            level_variable_coverage.loc[
                level_variable_coverage["分析层级"] == FACILITY_MONTH_LEVEL
            ]
        ),
        "",
        "### 3.3 系统-年份级",
        "",
        to_markdown_table(
            level_variable_coverage.loc[
                level_variable_coverage["分析层级"] == SYSTEM_YEAR_LEVEL
            ]
        ),
        "",
        "## 4. 特殊表关系与结构层接入证据",
        "",
        to_markdown_table(relationship_summary),
        "",
        f"- Paired TOC-Alkalinity 原始行数：{paired_summary['row_count']}，唯一设施-月份键数：{paired_summary['unique_facility_month_keys']}。",
        f"- treatment `water_system_facility` 唯一设施数：{treatment_summary['unique_facility_counts']['water_system_facility']}。",
        f"- treatment `facility_plant` 唯一设施数：{treatment_summary['unique_facility_counts']['facility_plant']}。",
        f"- treatment `treatment_process` 唯一设施数：{treatment_summary['unique_facility_counts']['treatment_process']}。",
        "",
        "## 5. 审计结论",
        "",
        (
            f"- 严格样本级下，TTHM 共有 {strict_summary['TTHM 唯一键数']} 个非缺失唯一键，"
            f"但 `TTHM + 核心四变量全齐` 仅有 {strict_summary['TTHM + 核心四变量全齐']} 个，"
            "说明样本级四键严格对齐更适合作为可拼接性审计和保守基线，而不是后续主建模底表。"
        ),
        (
            f"- 设施-月份级把 TTHM 非缺失键提升到 {facility_summary['TTHM 唯一键数']} 个，"
            f"`TTHM + 核心四变量至少 2 个预测变量` 提升到 {facility_summary['TTHM + 核心四变量至少 2 个预测变量']} 个，"
            f"但 `TTHM + 核心四变量全齐` 仍为 {facility_summary['TTHM + 核心四变量全齐']} 个，"
            "说明设施-月份级更适合作为机制分析主层级的起点，但需要采用分模块变量集、时间窗口约束或 pairwise/小模型策略，而不是直接假定存在完整多变量底表。"
        ),
        (
            f"- 系统-年份级进一步把 TTHM 非缺失键压缩为 {system_summary['TTHM 唯一键数']} 个系统-年份单元，"
            f"`TTHM + 核心四变量全齐` 达到 {system_summary['TTHM + 核心四变量全齐']} 个，"
            "覆盖最广，但时间与设施内异质性被显著平均化，更适合作为全国机器学习主表；即便如此，也仍应采用简约变量集和聚合统计，而不宜直接假设细粒度机理变量完备。"
        ),
        (
            f"- Paired TOC-Alkalinity 仅与 {int(relationship_summary.loc[relationship_summary['关系对象'] == 'Paired TOC-Alkalinity', '与 TTHM 设施-月份交集键数'].iloc[0])} "
            "个 TTHM 设施-月份键重合，说明它应被视为专题化 reduced dataset，而不是通用主表。"
        ),
        "- treatment 表与样本结果表属于不同数据库层：前者是结构与工艺解释层，后者是 occurrence 结果层，因此不能直接按单条样本机械一对一连接。",
        "- HAA5 应与 TTHM 平行纳入同一三层级框架，而不是等 TTHM 全部完成后再另起一套方法口径。",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_output_dir()

    source_results: dict[str, dict[str, object]] = {}
    source_hashes: dict[str, dict[str, np.ndarray]] = {}
    for spec in SOURCE_SPECS:
        result = scan_occurrence_source(spec)
        source_results[spec.key] = result
        source_hashes[spec.key] = result["level_hashes"]

    paired_summary = scan_paired_toc_alk()
    treatment_summary = scan_treatment_tables(source_results)

    source_inventory = build_source_inventory(source_results)
    level_summary = build_level_summary(source_hashes)
    level_variable_coverage = build_level_variable_coverage(source_hashes)
    relationship_summary = build_relationship_summary(
        source_hashes, paired_summary, treatment_summary
    )

    source_inventory.to_csv(
        OUTPUT_DIR / "dbp_source_inventory.csv", index=False, encoding="utf-8-sig"
    )
    level_summary.to_csv(
        OUTPUT_DIR / "dbp_level_summary.csv", index=False, encoding="utf-8-sig"
    )
    level_variable_coverage.to_csv(
        OUTPUT_DIR / "dbp_level_variable_coverage.csv",
        index=False,
        encoding="utf-8-sig",
    )
    relationship_summary.to_csv(
        OUTPUT_DIR / "dbp_relationship_summary.csv", index=False, encoding="utf-8-sig"
    )
    (OUTPUT_DIR / "V2_DBP_data_foundation_audit_report.md").write_text(
        build_audit_report(
            source_inventory,
            level_summary,
            level_variable_coverage,
            relationship_summary,
            paired_summary,
            treatment_summary,
        ),
        encoding="utf-8",
    )

    print(f"Wrote: {OUTPUT_DIR / 'dbp_source_inventory.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'dbp_level_summary.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'dbp_level_variable_coverage.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'dbp_relationship_summary.csv'}")
    print(f"Wrote: {OUTPUT_DIR / 'V2_DBP_data_foundation_audit_report.md'}")


if __name__ == "__main__":
    main()
