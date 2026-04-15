# V3 pws-year 字段字典

- 更新时间：2026-03-26 22:31:36
- 说明：所有年度字段均从 V3_facility_month_master 进一步上卷得到。

| 字段名 | 字段类别 | 来源 | 构建方式 | 保留理由 |
| --- | :-: | --- | --- | --- |
| pwsid | 主键 | V3_facility_month_master | 从二层主表上卷 | 全国系统级主键。 |
| year | 主键 | V3_facility_month_master | 从二层主表上卷 | 年度主键。 |
| state_code | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 便于州际差异分析。 |
| system_name | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 便于回查。 |
| system_type | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 反映系统类型差异。 |
| source_water_type | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 反映水源类型差异。 |
| retail_population_served | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 保留人口规模。 |
| adjusted_total_population_served | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 保留调整后人口规模。 |
| n_facility_month_rows | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 反映当年覆盖的设施-月份单元数。 |
| months_observed_any | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 反映当年有任意数据的月份数。 |
| n_facilities_in_master | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 反映当年参与聚合的设施数。 |
| n_facilities_with_treatment_summary | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 反映可接入 treatment 摘要的设施数。 |
| water_facility_type_list | 结构背景字段 | V3_facility_month_master | 从二层主表聚合 | 摘要设施类型。 |
| filter_type_list | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 摘要过滤类型。 |
| treatment_process_name_list | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 摘要工艺名称。 |
| treatment_objective_name_list | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 摘要工艺目标。 |
| has_disinfection_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在消毒工艺。 |
| has_filtration_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在过滤工艺。 |
| has_adsorption_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在吸附工艺。 |
| has_oxidation_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在氧化工艺。 |
| has_chloramination_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在氯胺化工艺。 |
| has_hypochlorination_process | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 是否存在次氯化工艺。 |
| plant_disinfectant_concentration_mean_mg_l | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 保留消毒剂浓度结构线索。 |
| plant_ct_value_mean | treatment 摘要字段 | V3_facility_month_master | 从二层主表聚合 | 保留 CT 结构线索。 |
| mean_core_vars_available_in_row | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 反映平均核心变量覆盖强度。 |
| max_core_vars_available_in_row | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 反映最高核心变量覆盖强度。 |
| months_with_1plus_core_vars | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 至少 1 个核心变量有数据的月份数。 |
| months_with_2plus_core_vars | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 至少 2 个核心变量有数据的月份数。 |
| months_with_3plus_core_vars | 质量控制字段 | V3_facility_month_master | 从二层主表聚合 | 至少 3 个核心变量有数据的月份数。 |
| tthm_sample_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| tthm_facility_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| tthm_months_with_data | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| tthm_n_facilities | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| tthm_sample_weighted_mean_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| tthm_monthly_median_median_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| tthm_monthly_max_max_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| tthm_monthly_p90_p90_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| tthm_high_risk_facility_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险单元数量。 |
| tthm_high_risk_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险月份频率。 |
| tthm_high_risk_facility_month_share | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险强度。 |
| tthm_high_risk_month_share | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度高风险月占比。 |
| haa5_sample_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| haa5_facility_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| haa5_months_with_data | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| haa5_n_facilities | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| haa5_sample_weighted_mean_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| haa5_monthly_median_median_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| haa5_monthly_max_max_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| haa5_monthly_p90_p90_ug_l | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| haa5_high_risk_facility_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险单元数量。 |
| haa5_high_risk_month_count | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险月份频率。 |
| haa5_high_risk_facility_month_share | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映高风险强度。 |
| haa5_high_risk_month_share | 结果变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度高风险月占比。 |
| ph_sample_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| ph_facility_month_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| ph_months_with_data | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| ph_n_facilities | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| ph_sample_weighted_mean | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| ph_monthly_median_median | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| ph_monthly_max_max | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| ph_monthly_p90_p90 | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| alkalinity_sample_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| alkalinity_facility_month_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| alkalinity_months_with_data | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| alkalinity_n_facilities | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| alkalinity_sample_weighted_mean_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| alkalinity_monthly_median_median_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| alkalinity_monthly_max_max_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| alkalinity_monthly_p90_p90_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| toc_sample_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| toc_facility_month_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| toc_months_with_data | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| toc_n_facilities | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| toc_sample_weighted_mean_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| toc_monthly_median_median_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| toc_monthly_max_max_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| toc_monthly_p90_p90_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| free_chlorine_sample_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| free_chlorine_facility_month_count | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| free_chlorine_months_with_data | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| free_chlorine_n_facilities | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| free_chlorine_sample_weighted_mean_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| free_chlorine_monthly_median_median_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| free_chlorine_monthly_max_max_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| free_chlorine_monthly_p90_p90_mg_l | 核心机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| total_chlorine_sample_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| total_chlorine_facility_month_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| total_chlorine_months_with_data | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| total_chlorine_n_facilities | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| total_chlorine_sample_weighted_mean_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| total_chlorine_monthly_median_median_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| total_chlorine_monthly_max_max_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| total_chlorine_monthly_p90_p90_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| doc_sample_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| doc_facility_month_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| doc_months_with_data | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| doc_n_facilities | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| doc_sample_weighted_mean_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| doc_monthly_median_median_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| doc_monthly_max_max_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| doc_monthly_p90_p90_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| suva_sample_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| suva_facility_month_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| suva_months_with_data | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| suva_n_facilities | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| suva_sample_weighted_mean_l_mg_m | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| suva_monthly_median_median_l_mg_m | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| suva_monthly_max_max_l_mg_m | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| suva_monthly_p90_p90_l_mg_m | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| uv254_sample_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| uv254_facility_month_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| uv254_months_with_data | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| uv254_n_facilities | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| uv254_sample_weighted_mean_cm_inv | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| uv254_monthly_median_median_cm_inv | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| uv254_monthly_max_max_cm_inv | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| uv254_monthly_p90_p90_cm_inv | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| chloramine_sample_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度加权基础。 |
| chloramine_facility_month_count | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映年度单元覆盖强度。 |
| chloramine_months_with_data | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映时间覆盖连续性。 |
| chloramine_n_facilities | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 反映设施覆盖广度。 |
| chloramine_sample_weighted_mean_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 适合作为全国主表的年度强度指标。 |
| chloramine_monthly_median_median_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留稳健中心趋势。 |
| chloramine_monthly_max_max_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留年度尾部风险信息。 |
| chloramine_monthly_p90_p90_mg_l | 扩展机制变量字段 | V3_facility_month_master | 从二层主表聚合 | 保留右尾浓度结构。 |
| n_outcome_vars_available | 质量控制字段 | 派生 | 从二层主表聚合或派生 | 统计年度结果变量可用数量。 |
| n_core_vars_available | 质量控制字段 | 派生 | 从二层主表聚合或派生 | 统计年度核心变量可用数量。 |
| n_extended_vars_available | 质量控制字段 | 派生 | 从二层主表聚合或派生 | 统计年度扩展变量可用数量。 |
| treatment_profile_summary | treatment 摘要字段 | 派生 | 从二层主表聚合或派生 | 保留系统年度短摘要。 |
| annual_match_quality_tier | 质量控制字段 | 派生 | 从二层主表聚合或派生 | 按年度结果与核心变量覆盖度分层。 |

