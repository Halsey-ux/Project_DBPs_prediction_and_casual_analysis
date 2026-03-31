# V3_pws_year_build_notes

- 更新时间：2026-03-26 22:31:36
- 输出主表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_pws_year_master.csv`
- 主键：`pwsid + year`

## 1. 三层主表定位

- 三层主表是全国 ML 主表原型，重点在于覆盖广度、结构稳定性和年度可解释聚合统计。
- 所有年度字段均从 V3_facility_month_master 进一步上卷得到。

## 2. 聚合逻辑

1. `*_sample_count` 是二层样本数求和。
2. `*_sample_weighted_mean*` 是二层月均值按样本数加权后的年度均值。
3. `*_monthly_median_median*` 和 `*_monthly_max_max*` 保留稳健趋势与尾部风险信息。
4. `*_months_with_data`、`*_n_facilities` 和高风险月占比字段为后续任务化筛选提供依据。

## 3. 主表示例记录

| pwsid | year | state_code | system_type | source_water_type | n_facilities_in_master | tthm_sample_weighted_mean_ug_l | haa5_sample_weighted_mean_ug_l | ph_sample_weighted_mean | alkalinity_sample_weighted_mean_mg_l | toc_sample_weighted_mean_mg_l | free_chlorine_sample_weighted_mean_mg_l | months_with_2plus_core_vars | annual_match_quality_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 010106001 | 2012 | CT | C | SW | 1 | 71.56875 | 24.20625 |  |  |  |  | 0.0 | D_outcome_only |
| 010106001 | 2013 | CT | C | SW | 1 | 65.8125 | 20.326666666666664 |  |  |  |  | 0.0 | D_outcome_only |
| 010106001 | 2014 | CT | C | SW | 1 | 45.12 | 9.443235294117647 |  |  |  |  | 0.0 | D_outcome_only |

## 4. 当前判断

- 三层主表已足够作为全国机器学习主表原型。
- 下一步应优先推进第三层全国 ML 主表线，再将第二层机制线作为高信息补充线并行推进。

