# V3_facility_month_build_notes

- 更新时间：2026-03-26 22:31:36
- 输出主表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_facility_month_master.csv`
- 输出逐表摘要目录：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\facility_month_source_tables`
- 主键：`pwsid + water_facility_id + year + month`

## 1. 二层主表定位

- 本表是第二层 facility-month 原型表，用于后续机制分析、高风险场景内部诊断和受约束小模型。
- 构建顺序严格遵守“各源表先聚合到目标层级，再按统一主键外连接”的原则。

## 2. 逐表摘要结果

| summary_table | 变量类别 | 唯一键数 | 非缺失键数 | 聚合函数 | 单位示例 |
| --- | --- | --- | --- | --- | --- |
| tthm_facility_month | 结果变量 | 549730 | 549730 | count, mean, median, max, p90 | UG/L |
| haa5_facility_month | 结果变量 | 481761 | 481761 | count, mean, median, max, p90 | UG/L |
| ph_facility_month | 核心机制变量 | 275174 | 275174 | count, mean, median, max, p90 |  |
| alkalinity_facility_month | 核心机制变量 | 299981 | 299981 | count, mean, median, max, p90 | MG/L |
| toc_facility_month | 核心机制变量 | 363849 | 363849 | count, mean, median, max, p90 | MG/L |
| free_chlorine_facility_month | 核心机制变量 | 215741 | 215741 | count, mean, median, max, p90 | MG/L |
| total_chlorine_facility_month | 扩展机制变量 | 49676 | 49676 | count, mean, median, max, p90 | MG/L |
| doc_facility_month | 扩展机制变量 | 3774 | 3774 | count, mean, median, max, p90 | MG/L | mg/L |
| suva_facility_month | 扩展机制变量 | 3570 | 3570 | count, mean, median, max, p90 | L/MG-M |
| uv254_facility_month | 扩展机制变量 | 3614 | 3614 | count, mean, median, max, p90 | cm-1 |
| chloramine_facility_month | 扩展机制变量 | 1886 | 1886 | count, mean, median, max, p90 | MG/L |

## 3. merge 逻辑

1. 每张 occurrence 源表先独立聚合到 facility-month 粒度。
2. 所有月度摘要表以统一主键做 outer merge。
3. 再按 pwsid 接入系统结构信息，按 pwsid + water_facility_id 接入 treatment 摘要。
4. 最后派生 n_core_vars_available、n_extended_vars_available、match_quality_tier 等质控字段。

## 4. 主表示例记录

| pwsid | water_facility_id | year | month | system_type | source_water_type | tthm_mean_ug_l | haa5_mean_ug_l | ph_mean | alkalinity_mean_mg_l | toc_mean_mg_l | free_chlorine_mean_mg_l | n_core_vars_available | match_quality_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 010106001 | 1186661 | 2012 | 3 | C | SW | 64.475 | 15.4 |  |  |  |  | 0 | D_outcome_only |
| 010106001 | 1186661 | 2012 | 6 | C | SW | 62.9 | 29.4 |  |  |  |  | 0 | D_outcome_only |
| 010106001 | 1186661 | 2012 | 9 | C | SW | 78.9 | 24.575 |  |  |  |  | 0 | D_outcome_only |

## 5. 当前判断

- 二层主表已经足够作为后续高风险场景内部分析和小模型机制分析的起点。
- 但它仍不适合被当作“所有变量全齐的统一宽表”，后续仍需采用模块化变量集、pairwise 或小模型策略。

