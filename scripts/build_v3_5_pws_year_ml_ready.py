from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from io_v4_ml_ready import (
    ALL_COLUMNS,
    BASELINE_COLUMNS,
    ENHANCED_COLUMNS,
    FLAG_COLUMNS,
    FLOAT_COLUMNS,
    INTEGER_LIKE_COLUMNS,
    KEY_COLUMNS,
    LABEL_COLUMNS,
    LEVEL_COLUMNS,
    MISSING_FLAG_COLUMNS,
    NULLABLE_BINARY_COLUMNS,
    QUALITY_COLUMNS,
    STRING_COLUMNS,
    TREATMENT_FLAG_COLUMNS,
    clean_string_series,
    coerce_float,
    coerce_integer_like,
    coerce_nullable_binary,
    read_v4_ml_ready_csv,
    validate_label_missingness,
    validate_unique_key,
    validate_v4_ml_ready_schema,
)

INPUT_PATH = PROJECT_ROOT / "data_local" / "V3_Chapter1_Part1_Prototype_Build" / "V3_pws_year_master.csv"
OUTPUT_DIR = PROJECT_ROOT / "data_local" / "V4_Chapter1_Part1_ML_Ready"
OUTPUT_PATH = OUTPUT_DIR / "V4_pws_year_ml_ready.csv"
DOCS_DIR = PROJECT_ROOT / "docs"
BUILD_NOTES_PATH = DOCS_DIR / "V3_5_pws_year_ml_ready_build_notes.md"
DICTIONARY_PATH = DOCS_DIR / "V3_5_pws_year_ml_ready_dictionary.md"
TZ = ZoneInfo("Asia/Hong_Kong")

TARGET_COLUMNS = [
    "tthm_sample_weighted_mean_ug_l",
]
SOURCE_COLUMNS = (
    KEY_COLUMNS
    + TARGET_COLUMNS
    + BASELINE_COLUMNS
    + ENHANCED_COLUMNS
    + QUALITY_COLUMNS
)


@dataclass(frozen=True)
class FieldSpec:
    name: str
    category: str
    description: str
    first_model_recommendation: str
    note: str


FIELD_SPECS = [
    FieldSpec("pwsid", "主键/回查", "公共供水系统唯一编号。", "不适用", "保留用于索引、回查和结果回写，禁止直接作为模型特征。"),
    FieldSpec("year", "主键/回查", "系统年度主键。", "不适用", "保留用于分年回查与时间切分，禁止直接作为模型特征。"),
    FieldSpec("tthm_sample_weighted_mean_ug_l", "目标", "第三层 TTHM 年度样本加权均值，单位为 ug/L。", "不适用", "本轮固定为唯一连续型主结果变量。"),
    FieldSpec("tthm_regulatory_exceed_label", "标签", "当 TTHM 年度样本加权均值大于等于 80 ug/L 时记为 1，否则记为 0。", "不适用", "80 ug/L 为法规阈值；目标缺失时标签留空。"),
    FieldSpec("tthm_warning_label", "标签", "当 TTHM 年度样本加权均值大于等于 60 ug/L 时记为 1，否则记为 0。", "不适用", "60 ug/L 仅作为预警阈值，不能写成法规阈值；目标缺失时标签留空。"),
    FieldSpec("level1_flag", "level 分层", "标记是否满足 level1：TTHM 目标非缺失。", "不适用", "全国主模型 baseline 样本定义。"),
    FieldSpec("level2_flag", "level 分层", "标记是否满足 level2：在 level1 基础上 n_core_vars_available >= 2。", "不适用", "增强模型样本定义。"),
    FieldSpec("level3_flag", "level 分层", "标记是否满足 level3：在 level1 基础上 n_core_vars_available >= 3。", "不适用", "高信息验证模型样本定义；level3 包含于 level2。"),
    FieldSpec("ml_level_max", "level 分层", "记录每条记录当前可达到的最高 level。", "不适用", "便于后续直接筛选 level1 / level2 / level3 / not_ml_ready。"),
    FieldSpec("state_code", "baseline 候选特征", "州代码。", "条件", "保留为 baseline 候选特征，但不能在文档中写成“必须入模”。"),
    FieldSpec("system_type", "baseline 候选特征", "供水系统类型。", "是", "适合作为第一版主模型的低维结构背景变量。"),
    FieldSpec("source_water_type", "baseline 候选特征", "原水类型。", "是", "适合作为第一版主模型的结构背景变量。"),
    FieldSpec("retail_population_served", "baseline 候选特征", "零售服务人口。", "是", "反映系统规模。"),
    FieldSpec("adjusted_total_population_served", "baseline 候选特征", "调整后总服务人口。", "是", "提供规模的补充口径。"),
    FieldSpec("n_facilities_in_master", "baseline 候选特征", "该系统当年进入第三层主表聚合的设施数。", "是", "反映系统年度设施覆盖范围。"),
    FieldSpec("has_disinfection_process", "baseline 候选特征", "年度 treatment 摘要中是否存在消毒工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("has_filtration_process", "baseline 候选特征", "年度 treatment 摘要中是否存在过滤工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("has_adsorption_process", "baseline 候选特征", "年度 treatment 摘要中是否存在吸附工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("has_oxidation_process", "baseline 候选特征", "年度 treatment 摘要中是否存在氧化工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("has_chloramination_process", "baseline 候选特征", "年度 treatment 摘要中是否存在氯胺化工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("has_hypochlorination_process", "baseline 候选特征", "年度 treatment 摘要中是否存在次氯化工艺。", "是", "保留原始缺失；有值时统一用 0/1 表示。"),
    FieldSpec("ph_sample_weighted_mean", "增强候选特征", "年度 pH 样本加权均值。", "是", "核心机制变量。"),
    FieldSpec("alkalinity_sample_weighted_mean_mg_l", "增强候选特征", "年度总碱度样本加权均值，单位为 mg/L。", "是", "核心机制变量。"),
    FieldSpec("toc_sample_weighted_mean_mg_l", "增强候选特征", "年度 TOC 样本加权均值，单位为 mg/L。", "是", "核心机制变量。"),
    FieldSpec("free_chlorine_sample_weighted_mean_mg_l", "增强候选特征", "年度游离余氯样本加权均值，单位为 mg/L。", "是", "核心机制变量。"),
    FieldSpec("total_chlorine_sample_weighted_mean_mg_l", "增强候选特征", "年度总氯样本加权均值，单位为 mg/L。", "条件", "保留为增强模型候选特征，不默认进入第一版全国主模型。"),
    FieldSpec("months_observed_any", "质控/覆盖", "该系统当年有任意数据的月份数。", "是", "反映年度监测覆盖。"),
    FieldSpec("tthm_months_with_data", "质控/覆盖", "该系统当年有 TTHM 数据的月份数。", "条件", "更适合作为样本质控和敏感性分析字段。"),
    FieldSpec("months_with_1plus_core_vars", "质控/覆盖", "至少 1 个核心机制变量有数据的月份数。", "是", "反映低门槛机制覆盖。"),
    FieldSpec("months_with_2plus_core_vars", "质控/覆盖", "至少 2 个核心机制变量有数据的月份数。", "是", "反映中等信息强度。"),
    FieldSpec("months_with_3plus_core_vars", "质控/覆盖", "至少 3 个核心机制变量有数据的月份数。", "是", "反映高信息强度。"),
    FieldSpec("n_core_vars_available", "质控/覆盖", "年度层可用核心机制变量数量。", "是", "同时用于样本分层和覆盖控制。"),
    FieldSpec("annual_match_quality_tier", "质控/覆盖", "V3 第三层既有的年度匹配质量分层。", "否", "保留用于样本筛选、对照和敏感性分析，默认不进入第一版主模型。"),
    FieldSpec("ph_missing_flag", "缺失标记", "当年度 pH 均值缺失时记为 1，否则记为 0。", "是", "保留原始缺失，同时显式暴露缺失模式。"),
    FieldSpec("alkalinity_missing_flag", "缺失标记", "当年度总碱度均值缺失时记为 1，否则记为 0。", "是", "保留原始缺失，同时显式暴露缺失模式。"),
    FieldSpec("toc_missing_flag", "缺失标记", "当年度 TOC 均值缺失时记为 1，否则记为 0。", "是", "保留原始缺失，同时显式暴露缺失模式。"),
    FieldSpec("free_chlorine_missing_flag", "缺失标记", "当年度游离余氯均值缺失时记为 1，否则记为 0。", "是", "保留原始缺失，同时显式暴露缺失模式。"),
    FieldSpec("total_chlorine_missing_flag", "缺失标记", "当年度总氯均值缺失时记为 1，否则记为 0。", "条件", "仅在增强模型引入总氯时一并使用。"),
]


def now_text() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ensure_directories() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_source() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"未找到输入文件：{INPUT_PATH}")
    df = pd.read_csv(
        INPUT_PATH,
        usecols=SOURCE_COLUMNS,
        dtype={
            "pwsid": "string",
            "state_code": "string",
            "system_type": "string",
            "source_water_type": "string",
            "annual_match_quality_tier": "string",
        },
        encoding="utf-8-sig",
    )
    missing_columns = [column for column in SOURCE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"输入文件缺少必需字段：{missing_columns}")
    return df


def build_labels(target: pd.Series, threshold: float) -> pd.Series:
    label = pd.Series(pd.NA, index=target.index, dtype="Int8")
    observed = target.notna()
    label.loc[observed] = target.loc[observed].ge(threshold).astype("Int8")
    return label


def build_ml_level_max(level1: pd.Series, level2: pd.Series, level3: pd.Series) -> pd.Series:
    output = pd.Series("not_ml_ready", index=level1.index, dtype="string")
    output.loc[level1 == 1] = "level1"
    output.loc[level2 == 1] = "level2"
    output.loc[level3 == 1] = "level3"
    return output


def build_dataset(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    for column in STRING_COLUMNS:
        if column in output.columns:
            output[column] = clean_string_series(output[column])

    for column in INTEGER_LIKE_COLUMNS:
        output[column] = coerce_integer_like(output[column], column)

    for column in TARGET_COLUMNS + ENHANCED_COLUMNS:
        output[column] = coerce_float(output[column])

    for column in TREATMENT_FLAG_COLUMNS:
        output[column] = coerce_nullable_binary(output[column], column)

    target = output["tthm_sample_weighted_mean_ug_l"]
    output["tthm_regulatory_exceed_label"] = build_labels(target, 80.0)
    output["tthm_warning_label"] = build_labels(target, 60.0)

    level1 = target.notna().astype("Int8")
    level2 = (target.notna() & output["n_core_vars_available"].fillna(0).ge(2)).astype("Int8")
    level3 = (target.notna() & output["n_core_vars_available"].fillna(0).ge(3)).astype("Int8")
    output["level1_flag"] = level1
    output["level2_flag"] = level2
    output["level3_flag"] = level3
    output["ml_level_max"] = build_ml_level_max(level1, level2, level3)

    output["ph_missing_flag"] = output["ph_sample_weighted_mean"].isna().astype("Int8")
    output["alkalinity_missing_flag"] = output["alkalinity_sample_weighted_mean_mg_l"].isna().astype("Int8")
    output["toc_missing_flag"] = output["toc_sample_weighted_mean_mg_l"].isna().astype("Int8")
    output["free_chlorine_missing_flag"] = output["free_chlorine_sample_weighted_mean_mg_l"].isna().astype("Int8")
    output["total_chlorine_missing_flag"] = output["total_chlorine_sample_weighted_mean_mg_l"].isna().astype("Int8")

    output = output[ALL_COLUMNS].sort_values(KEY_COLUMNS).reset_index(drop=True)

    validate_unique_key(output)
    validate_label_missingness(output)
    return output


def compute_summary(df: pd.DataFrame) -> dict[str, int]:
    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "level1_count": int(df["level1_flag"].sum()),
        "level2_count": int(df["level2_flag"].sum()),
        "level3_count": int(df["level3_flag"].sum()),
        "regulatory_positive": int(df["tthm_regulatory_exceed_label"].fillna(0).sum()),
        "regulatory_negative": int(((df["tthm_regulatory_exceed_label"] == 0) & df["tthm_regulatory_exceed_label"].notna()).sum()),
        "warning_positive": int(df["tthm_warning_label"].fillna(0).sum()),
        "warning_negative": int(((df["tthm_warning_label"] == 0) & df["tthm_warning_label"].notna()).sum()),
        "target_missing": int(df["tthm_sample_weighted_mean_ug_l"].isna().sum()),
    }


def build_notes_markdown(summary: dict[str, int]) -> str:
    baseline_features = "、".join(BASELINE_COLUMNS)
    enhanced_features = "、".join(ENHANCED_COLUMNS)
    return "\n".join(
        [
            "# V3.5 pws-year ML-ready 构建说明",
            "",
            f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
            f"- 输入文件：`{INPUT_PATH}`",
            f"- 输出文件：`{OUTPUT_PATH}`",
            "",
            "## 1. 本轮目标",
            "",
            "- 仅基于第三层 `V3_pws_year_master.csv` 派生一张可直接进入 V4 机器学习阶段的数据输入层。",
            "- 本轮只服务于 `TTHM` 主线，不把第二层 `facility-month` 字段横向拼入，也不启动正式模型训练。",
            "",
            "## 2. 输出数据集概况",
            "",
            f"- 行数：`{summary['row_count']}`",
            f"- 字段数：`{summary['column_count']}`",
            f"- `level1` 样本数：`{summary['level1_count']}`",
            f"- `level2` 样本数：`{summary['level2_count']}`",
            f"- `level3` 样本数：`{summary['level3_count']}`",
            f"- `tthm_regulatory_exceed_label=1`：`{summary['regulatory_positive']}`",
            f"- `tthm_regulatory_exceed_label=0`：`{summary['regulatory_negative']}`",
            f"- `tthm_warning_label=1`：`{summary['warning_positive']}`",
            f"- `tthm_warning_label=0`：`{summary['warning_negative']}`",
            f"- `TTHM` 目标缺失行数：`{summary['target_missing']}`",
            "",
            "## 3. 主结果变量定义",
            "",
            "- 唯一连续型主结果变量固定为 `tthm_sample_weighted_mean_ug_l`。",
            "- 它表示在 `pwsid + year` 粒度下的 TTHM 年度样本加权均值，单位为 `ug/L`。",
            "- 本轮不把其他 `tthm_*` 摘要字段并列写成主标签体系。",
            "",
            "## 4. 标签定义",
            "",
            "- `tthm_regulatory_exceed_label`：当 `tthm_sample_weighted_mean_ug_l >= 80` 时记为 `1`，否则记为 `0`。",
            "- `tthm_warning_label`：当 `tthm_sample_weighted_mean_ug_l >= 60` 时记为 `1`，否则记为 `0`。",
            "- `80 ug/L` 是法规阈值；`60 ug/L` 只是预警阈值，不能写成法规阈值。",
            "- 当目标变量缺失时，这两个标签均保持为空值，不把缺失样本误写为负类。",
            "",
            "## 5. level1 / level2 / level3 规则",
            "",
            "- `level1`：`tthm_sample_weighted_mean_ug_l` 非缺失。",
            "- `level2`：满足 `level1` 且 `n_core_vars_available >= 2`。",
            "- `level3`：满足 `level1` 且 `n_core_vars_available >= 3`。",
            "- 始终满足“`level3` 包含于 `level2`，`level2` 包含于 `level1`”。",
            "- `TTHM + 4 个核心变量全齐` 的 `60` 条记录仍只作为补充检查，不单独定义为新的正式 level。",
            "",
            "## 6. 保留字段口径",
            "",
            f"- baseline 候选特征：{baseline_features}。",
            f"- 增强候选特征：{enhanced_features}。",
            "- 质控/覆盖字段保留在表内，用于样本筛选、模型对照和敏感性分析。",
            "- `annual_match_quality_tier` 保留，但默认不进入第一版主模型特征。",
            "- `state_code` 仅保留为 baseline 候选特征，后续是否纳入由模型对照实验决定。",
            "",
            "## 7. 缺失标记生成规则",
            "",
            "- 对 `ph`、`alkalinity`、`toc`、`free_chlorine` 和 `total_chlorine` 年度均值各生成一列缺失标记。",
            "- 缺失标记为 `1` 表示该变量缺失，为 `0` 表示非缺失。",
            "- 原始数值列保持原始缺失状态，不做覆盖式插补。",
            "",
            "## 8. 基础清洗规则",
            "",
            "- 校验输出主键 `pwsid + year` 唯一。",
            "- 统一字符串字段、整数型字段、连续型字段和 0/1 布尔字段口径。",
            "- treatment 二值字段仅在原表有值时保留为 `0/1`，没有 treatment 摘要时仍保留为空。",
            "- 目标缺失样本不生成分类标签，同时 `level1_flag`、`level2_flag`、`level3_flag` 统一为 `0`。",
            "- 输出后按显式 schema 再次回读，确认关键字段不会在回读阶段漂移为错误 dtype。",
            "",
            "## 9. 本轮明确不做的事情",
            "",
            "- 不切分训练集 / 验证集 / 测试集。",
            "- 不做标准化、one-hot 编码、最终训练矩阵生成。",
            "- 不做复杂插补、多重插补或面向模型性能优化的缺失修补。",
            "- 不做异常值裁剪或正式模型训练。",
            "- 不把 `system_name`、`pwsid`、`year` 或与目标同源的 `tthm_*` 摘要字段写入第一版 `TTHM` 模型特征。",
            "",
        ]
    )


def build_dictionary_markdown() -> str:
    header = [
        "# V3.5 pws-year ML-ready 字段字典",
        "",
        f"- 更新时间：{now_text()}（Asia/Hong_Kong）",
        f"- 对应数据集：`{OUTPUT_PATH}`",
        "",
        "| 字段名 | 字段类别 | 中文说明 | 是否建议进入第一版主模型 | 备注与禁用说明 |",
        "| --- | --- | --- | --- | --- |",
    ]
    rows = [
        f"| `{spec.name}` | {spec.category} | {spec.description} | {spec.first_model_recommendation} | {spec.note} |"
        for spec in FIELD_SPECS
    ]
    rows.extend(
        [
            "",
            "## 附加说明",
            "",
            "- 第一版 `TTHM` 主模型明确禁止把与目标同源的 `tthm_monthly_median_median_ug_l`、`tthm_monthly_max_max_ug_l`、`tthm_monthly_p90_p90_ug_l`、`tthm_high_risk_*` 系列字段作为输入特征。",
            "- `system_name`、各类字符串列表摘要字段和结果同源摘要字段不进入本轮 `ml_ready` 输出表。",
            "- `annual_match_quality_tier` 虽然保留在表内，但文档口径固定为“默认不进入第一版主模型”。",
            "- `state_code` 固定为候选特征，不写成“必须入模”。",
            "",
        ]
    )
    return "\n".join(header + rows)


def write_outputs(df: pd.DataFrame) -> dict[str, int]:
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    reloaded = read_v4_ml_ready_csv(OUTPUT_PATH)
    validate_v4_ml_ready_schema(reloaded)

    summary = compute_summary(df)
    BUILD_NOTES_PATH.write_text(build_notes_markdown(summary), encoding="utf-8")
    DICTIONARY_PATH.write_text(build_dictionary_markdown(), encoding="utf-8")
    return summary


def main() -> None:
    ensure_directories()
    source_df = read_source()
    ml_ready_df = build_dataset(source_df)
    summary = write_outputs(ml_ready_df)
    print("V3.5 ml_ready 构建完成")
    print(f"输出文件: {OUTPUT_PATH}")
    print(f"行数: {summary['row_count']}")
    print(f"字段数: {summary['column_count']}")
    print(f"level1 / level2 / level3: {summary['level1_count']} / {summary['level2_count']} / {summary['level3_count']}")
    print(
        "regulatory 正负样本: "
        f"{summary['regulatory_positive']} / {summary['regulatory_negative']}"
    )
    print(
        "warning 正负样本: "
        f"{summary['warning_positive']} / {summary['warning_negative']}"
    )


if __name__ == "__main__":
    main()
