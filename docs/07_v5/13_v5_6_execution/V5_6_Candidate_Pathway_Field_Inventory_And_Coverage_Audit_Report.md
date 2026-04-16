# V5.6 候选通路字段盘点与覆盖审计执行报告

更新时间：2026-04-15 19:56:38（Asia/Hong_Kong）

## 1. 本轮任务定位

本轮 `V5.6` 是数据认识补全和候选通路字段审计，不是正式建模，也不是最终主筛查特征组冻结。本轮只回答当前派生主表中有哪些字段、字段覆盖率如何、字段与 `TTHM/HAA5` 标签能否对齐、候选通路内部覆盖结构如何，以及 complete-case / partial-case 样本基础是否足以支撑后续准入测试。

本轮没有训练树模型、boosting 模型、超参数搜索模型或投票模型；原始 SYR4 数据未被原位修改。

## 2. 输入数据说明

| layer | source_table | rows | columns | tthm_label_available_n | haa5_label_available_n |
| --- | --- | --- | --- | --- | --- |
| pws_year | V3_pws_year_master.csv | 259,500 | 130 | 199,802 | 165,379 |
| facility_month | V3_facility_month_master.csv | 1,442,728 | 98 | 549,730 | 481,761 |
| pws_year_ml_ready | V4_pws_year_ml_ready.csv | 259,500 | 38 | 199,802 | 0 |

`V4_pws_year_ml_ready.csv` 只作为 V4 主线字段对照表使用。该表当前没有 `HAA5` 标签，因此其 HAA5 对齐结果不用于判断 HAA5 可训练性。

## 3. 全字段 inventory 总结

| layer | field_count | high_coverage_fields_n | medium_coverage_fields_n | low_coverage_fields_n | known_candidate_fields_n |
| --- | --- | --- | --- | --- | --- |
| pws_year | 130 | 22 | 40 | 68 | 127 |
| facility_month | 98 | 21 | 25 | 52 | 93 |
| pws_year_ml_ready | 38 | 23 | 6 | 9 | 32 |

高覆盖字段按非缺失率 `>=80%` 统计，中覆盖字段为 `20%-80%`，低覆盖字段为 `<20%`。这些只是数据完整性口径，不代表字段一定可入模。全字段明细见本地 `V5_6_all_field_inventory.csv`。

## 4. 候选通路字段展开

本轮按 V5.5 的候选通路框架继续展开，并额外盘点结果谱系/解释候选通路与合规/纠正行动响应候选通路。字段展开明细见本地 `V5_6_candidate_pathway_field_map.csv`。

第三层 `PWS-year` 通路覆盖摘要：

| layer | pathway_name | fields_existing_n | any_field_non_missing_n | any_field_non_missing_rate | tthm_label_overlap_n | tthm_label_overlap_rate | haa5_label_overlap_n | haa5_label_overlap_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pws_year | 结构背景通路 | 5 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| pws_year | 设施复杂度通路 | 2 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| pws_year | 处理工艺通路 | 9 | 39,475 | 15.21% | 26,704 | 10.29% | 23,693 | 9.13% |
| pws_year | 酸碱与缓冲条件通路 | 16 | 101,685 | 39.18% | 49,217 | 18.97% | 43,124 | 16.62% |
| pws_year | NOM/有机前体物通路 | 32 | 19,704 | 7.59% | 18,754 | 7.23% | 18,441 | 7.11% |
| pws_year | 消毒剂与残余消毒剂通路 | 26 | 9,013 | 3.47% | 4,930 | 1.90% | 3,926 | 1.51% |
| pws_year | 监测覆盖度与证据质量通路 | 13 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| pws_year | 结果谱系/解释候选通路 | 24 | 204,317 | 78.73% | 199,802 | 76.99% | 165,379 | 63.73% |
| pws_year | 合规与纠正行动响应候选通路 | 0 | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

第二层 `facility-month` 通路覆盖摘要：

| layer | pathway_name | fields_existing_n | any_field_non_missing_n | any_field_non_missing_rate | tthm_label_overlap_n | tthm_label_overlap_rate | haa5_label_overlap_n | haa5_label_overlap_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| facility_month | 结构背景通路 | 5 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| facility_month | 设施复杂度通路 | 3 | 1,021,496 | 70.80% | 362,756 | 25.14% | 316,334 | 21.93% |
| facility_month | 处理工艺通路 | 13 | 227,588 | 15.77% | 2,699 | 0.19% | 455 | 0.03% |
| facility_month | 酸碱与缓冲条件通路 | 10 | 495,082 | 34.32% | 10,378 | 0.72% | 7,650 | 0.53% |
| facility_month | NOM/有机前体物通路 | 20 | 363,911 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% |
| facility_month | 消毒剂与残余消毒剂通路 | 17 | 255,624 | 17.72% | 7,182 | 0.50% | 6,432 | 0.45% |
| facility_month | 监测覆盖度与证据质量通路 | 11 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| facility_month | 结果谱系/解释候选通路 | 14 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| facility_month | 合规与纠正行动响应候选通路 | 0 | 0 | 0.00% | 0 | 0.00% | 0 | 0.00% |

## 5. 字段-Y 对齐总结

字段-Y 对齐表中的重叠率采用“字段非缺失且标签可定义的行数 / 该层级总行数”口径。它不是字段预测能力，也不是因果效应。

第三层 `PWS-year` 与 `TTHM` 标签重叠较高的字段：

| layer | field_name | candidate_pathway_guess | non_missing_rate | field_and_tthm_label_n | field_and_tthm_label_rate |
| --- | --- | --- | --- | --- | --- |
| pws_year | adjusted_total_population_served | 结构背景通路 | 100.00% | 199,802 | 76.99% |
| pws_year | annual_match_quality_tier | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | max_core_vars_available_in_row | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | mean_core_vars_available_in_row | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | months_observed_any | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | months_with_1plus_core_vars | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | months_with_2plus_core_vars | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |
| pws_year | months_with_3plus_core_vars | 监测覆盖度与证据质量通路 | 100.00% | 199,802 | 76.99% |

第三层 `PWS-year` 与 `HAA5` 标签重叠较高的字段：

| layer | field_name | candidate_pathway_guess | non_missing_rate | field_and_haa5_label_n | field_and_haa5_label_rate |
| --- | --- | --- | --- | --- | --- |
| pws_year | adjusted_total_population_served | 结构背景通路 | 100.00% | 165,379 | 63.73% |
| pws_year | annual_match_quality_tier | 监测覆盖度与证据质量通路 | 100.00% | 165,379 | 63.73% |
| pws_year | haa5_facility_month_count | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |
| pws_year | haa5_high_risk_facility_month_count | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |
| pws_year | haa5_high_risk_facility_month_share | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |
| pws_year | haa5_high_risk_month_count | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |
| pws_year | haa5_high_risk_month_share | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |
| pws_year | haa5_monthly_max_max_ug_l | 结果谱系/解释候选通路 | 63.73% | 165,379 | 63.73% |

第二层 `facility-month` 的标签对齐受同月同设施观测重叠约束明显更强，NOM、消毒剂和处理工艺字段虽有机制意义，但与同周期 `TTHM/HAA5` 的直接重叠样本明显有限。

## 6. 通路内部覆盖结构

通路内部覆盖结构显示：结构背景、设施复杂度和证据质量通路的“任意字段覆盖率”较高；水质机制类通路往往由少数强度字段和大量样本数、月份数、设施数类覆盖字段共同组成。后续不能把这些覆盖字段直接解释为化学机制。

| layer | pathway_name | field_count | fields_existing_n | top_coverage_fields | low_coverage_fields | possible_mechanism_fields_n | possible_monitoring_coverage_fields_n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pws_year | 结构背景通路 | 5 | 5 | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.93%) | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.93%) | 0 | 0 |
| pws_year | 设施复杂度通路 | 5 | 2 | n_facilities_in_master(100.00%); water_facility_type_list(87.57%) | n_facilities_in_master(100.00%); water_facility_type_list(87.57%) | 0 | 1 |
| pws_year | 处理工艺通路 | 13 | 9 | has_adsorption_process(15.21%); has_chloramination_process(15.21%); has_disinfection_process(15.21%); has_filtration_process(15.21%); has_hypochlorination_process(15.21%) | has_hypochlorination_process(15.21%); has_oxidation_process(15.21%); treatment_objective_name_list(15.21%); treatment_process_name_list(15.21%); filter_type_list(2.76%) | 0 | 0 |
| pws_year | 酸碱与缓冲条件通路 | 16 | 16 | ph_facility_month_count(28.96%); ph_monthly_max_max(28.96%); ph_monthly_median_median(28.96%); ph_monthly_p90_p90(28.96%); ph_months_with_data(28.96%) | alkalinity_monthly_p90_p90_mg_l(21.22%); alkalinity_months_with_data(21.22%); alkalinity_n_facilities(21.22%); alkalinity_sample_count(21.22%); alkalinity_sample_weighted_mean_mg_l(21.22%) | 8 | 8 |
| pws_year | NOM/有机前体物通路 | 32 | 32 | toc_facility_month_count(7.59%); toc_monthly_max_max_mg_l(7.59%); toc_monthly_median_median_mg_l(7.59%); toc_monthly_p90_p90_mg_l(7.59%); toc_months_with_data(7.59%) | suva_monthly_p90_p90_l_mg_m(0.10%); suva_months_with_data(0.10%); suva_n_facilities(0.10%); suva_sample_count(0.10%); suva_sample_weighted_mean_l_mg_m(0.10%) | 16 | 16 |
| pws_year | 消毒剂与残余消毒剂通路 | 26 | 26 | free_chlorine_facility_month_count(2.85%); free_chlorine_monthly_max_max_mg_l(2.85%); free_chlorine_monthly_median_median_mg_l(2.85%); free_chlorine_monthly_p90_p90_mg_l(2.85%); free_chlorine_months_with_data(2.85%) | chloramine_monthly_p90_p90_mg_l(0.08%); chloramine_months_with_data(0.08%); chloramine_n_facilities(0.08%); chloramine_sample_count(0.08%); chloramine_sample_weighted_mean_mg_l(0.08%) | 14 | 12 |
| pws_year | 监测覆盖度与证据质量通路 | 22 | 13 | annual_match_quality_tier(100.00%); max_core_vars_available_in_row(100.00%); mean_core_vars_available_in_row(100.00%); months_observed_any(100.00%); months_with_1plus_core_vars(100.00%) | n_extended_vars_available(100.00%); n_facilities_with_treatment_summary(100.00%); n_facility_month_rows(100.00%); n_outcome_vars_available(100.00%); treatment_profile_summary(15.21%) | 0 | 4 |
| pws_year | 结果谱系/解释候选通路 | 30 | 24 | tthm_facility_month_count(76.99%); tthm_high_risk_facility_month_count(76.99%); tthm_high_risk_facility_month_share(76.99%); tthm_high_risk_month_count(76.99%); tthm_high_risk_month_share(76.99%) | haa5_monthly_p90_p90_ug_l(63.73%); haa5_months_with_data(63.73%); haa5_n_facilities(63.73%); haa5_sample_count(63.73%); haa5_sample_weighted_mean_ug_l(63.73%) | 0 | 0 |
| pws_year | 合规与纠正行动响应候选通路 | 0 | 0 |  |  | 0 | 0 |
| facility_month | 结构背景通路 | 5 | 5 | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.98%) | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.98%) | 0 | 0 |
| facility_month | 设施复杂度通路 | 5 | 3 | water_facility_type(70.80%); flow_record_count(43.99%); n_supplying_facilities(43.99%) | water_facility_type(70.80%); flow_record_count(43.99%); n_supplying_facilities(43.99%) | 0 | 1 |
| facility_month | 处理工艺通路 | 13 | 13 | treatment_process_summary(15.77%); has_adsorption_process(15.77%); has_chloramination_process(15.77%); has_disinfection_process(15.77%); has_filtration_process(15.77%) | n_treatment_process_names(15.77%); treatment_objective_name_list(15.77%); treatment_process_name_list(15.77%); treatment_process_record_count(15.77%); filter_type_list(3.17%) | 0 | 1 |
| facility_month | 酸碱与缓冲条件通路 | 10 | 10 | alkalinity_max_mg_l(20.79%); alkalinity_mean_mg_l(20.79%); alkalinity_median_mg_l(20.79%); alkalinity_n_samples(20.79%); alkalinity_p90_mg_l(20.79%) | ph_max(19.07%); ph_mean(19.07%); ph_median(19.07%); ph_n_samples(19.07%); ph_p90(19.07%) | 8 | 2 |
| facility_month | NOM/有机前体物通路 | 20 | 20 | toc_max_mg_l(25.22%); toc_mean_mg_l(25.22%); toc_median_mg_l(25.22%); toc_n_samples(25.22%); toc_p90_mg_l(25.22%) | suva_max_l_mg_m(0.25%); suva_mean_l_mg_m(0.25%); suva_median_l_mg_m(0.25%); suva_n_samples(0.25%); suva_p90_l_mg_m(0.25%) | 16 | 4 |
| facility_month | 消毒剂与残余消毒剂通路 | 17 | 17 | free_chlorine_max_mg_l(14.95%); free_chlorine_mean_mg_l(14.95%); free_chlorine_median_mg_l(14.95%); free_chlorine_n_samples(14.95%); free_chlorine_p90_mg_l(14.95%) | chloramine_max_mg_l(0.13%); chloramine_mean_mg_l(0.13%); chloramine_median_mg_l(0.13%); chloramine_n_samples(0.13%); chloramine_p90_mg_l(0.13%) | 14 | 3 |
| facility_month | 监测覆盖度与证据质量通路 | 21 | 11 | has_treatment_summary(100.00%); match_quality_tier(100.00%); n_core_vars_available(100.00%); n_extended_vars_available(100.00%); n_mechanism_vars_available(100.00%) | source_module_count(100.00%); has_water_system_facility_record(47.18%); has_flow_record(43.99%); has_treatment_process_record(15.77%); has_facility_plant_record(10.74%) | 0 | 0 |
| facility_month | 结果谱系/解释候选通路 | 16 | 14 | has_haa5(100.00%); has_tthm(100.00%); is_haa5_high_risk_month(100.00%); is_tthm_high_risk_month(100.00%); tthm_max_ug_l(38.10%) | haa5_max_ug_l(33.39%); haa5_mean_ug_l(33.39%); haa5_median_ug_l(33.39%); haa5_n_samples(33.39%); haa5_p90_ug_l(33.39%) | 0 | 0 |
| facility_month | 合规与纠正行动响应候选通路 | 0 | 0 |  |  | 0 | 0 |
| pws_year_ml_ready | 结构背景通路 | 5 | 5 | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.93%) | adjusted_total_population_served(100.00%); retail_population_served(100.00%); source_water_type(100.00%); state_code(100.00%); system_type(99.93%) | 0 | 0 |
| pws_year_ml_ready | 设施复杂度通路 | 5 | 1 | n_facilities_in_master(100.00%) | n_facilities_in_master(100.00%) | 0 | 1 |
| pws_year_ml_ready | 处理工艺通路 | 13 | 6 | has_adsorption_process(15.21%); has_chloramination_process(15.21%); has_disinfection_process(15.21%); has_filtration_process(15.21%); has_hypochlorination_process(15.21%) | has_chloramination_process(15.21%); has_disinfection_process(15.21%); has_filtration_process(15.21%); has_hypochlorination_process(15.21%); has_oxidation_process(15.21%) | 0 | 0 |
| pws_year_ml_ready | 酸碱与缓冲条件通路 | 4 | 4 | alkalinity_missing_flag(100.00%); ph_missing_flag(100.00%); ph_sample_weighted_mean(28.96%); alkalinity_sample_weighted_mean_mg_l(21.22%) | alkalinity_missing_flag(100.00%); ph_missing_flag(100.00%); ph_sample_weighted_mean(28.96%); alkalinity_sample_weighted_mean_mg_l(21.22%) | 2 | 0 |
| pws_year_ml_ready | NOM/有机前体物通路 | 2 | 2 | toc_missing_flag(100.00%); toc_sample_weighted_mean_mg_l(7.59%) | toc_missing_flag(100.00%); toc_sample_weighted_mean_mg_l(7.59%) | 1 | 0 |
| pws_year_ml_ready | 消毒剂与残余消毒剂通路 | 6 | 4 | free_chlorine_missing_flag(100.00%); total_chlorine_missing_flag(100.00%); free_chlorine_sample_weighted_mean_mg_l(2.85%); total_chlorine_sample_weighted_mean_mg_l(0.47%) | free_chlorine_missing_flag(100.00%); total_chlorine_missing_flag(100.00%); free_chlorine_sample_weighted_mean_mg_l(2.85%); total_chlorine_sample_weighted_mean_mg_l(0.47%) | 2 | 0 |
| pws_year_ml_ready | 监测覆盖度与证据质量通路 | 26 | 11 | alkalinity_missing_flag(100.00%); annual_match_quality_tier(100.00%); free_chlorine_missing_flag(100.00%); months_observed_any(100.00%); months_with_1plus_core_vars(100.00%) | months_with_3plus_core_vars(100.00%); n_core_vars_available(100.00%); ph_missing_flag(100.00%); toc_missing_flag(100.00%); total_chlorine_missing_flag(100.00%) | 0 | 3 |
| pws_year_ml_ready | 结果谱系/解释候选通路 | 8 | 4 | tthm_months_with_data(76.99%); tthm_regulatory_exceed_label(76.99%); tthm_sample_weighted_mean_ug_l(76.99%); tthm_warning_label(76.99%) | tthm_months_with_data(76.99%); tthm_regulatory_exceed_label(76.99%); tthm_sample_weighted_mean_ug_l(76.99%); tthm_warning_label(76.99%) | 0 | 0 |
| pws_year_ml_ready | 合规与纠正行动响应候选通路 | 0 | 0 |  |  | 0 | 0 |

## 7. complete-case / partial-case 可训练性

complete-case 表示通路内所有候选字段在同一行全部非缺失；partial-case 表示至少有 1、2 或 3 个候选字段非缺失。对字段数少于阈值的通路，对应 partial-case 指标标注为不适用。

第三层 `PWS-year` complete/partial-case：

| layer | pathway_name | candidate_field_count | complete_case_n_all_candidate_fields | complete_case_rate_all_candidate_fields | partial_case_n_at_least_1 | partial_case_rate_at_least_1 | partial_case_n_at_least_2 | partial_case_rate_at_least_2 | partial_case_n_at_least_3 | partial_case_rate_at_least_3 | tthm_overlap_complete_case_n | haa5_overlap_complete_case_n | training_feasibility_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pws_year | 结构背景通路 | 5 | 259320 | 0.9993063583815028 | 259500 | 1.0 | 259500 | 1.0 | 259500 | 1.0 | 199,786 | 165,366 | 完整组合样本基础较好，可进入后续模型准入测试。 |
| pws_year | 设施复杂度通路 | 2 | 227243 | 0.8756955684007707 | 259500 | 1.0 | 227243 | 0.8756955684007707 | <NA> | <NA> | 173,799 | 143,083 | 完整组合样本基础较好，可进入后续模型准入测试。 |
| pws_year | 处理工艺通路 | 9 | 7134 | 0.027491329479768786 | 39475 | 0.1521194605009634 | 39457 | 0.15205009633911368 | 39457 | 0.15205009633911368 | 5,876 | 5,536 | 完整组合不足，但 partial-case 或子组合审计仍有基础。 |
| pws_year | 酸碱与缓冲条件通路 | 16 | 28529 | 0.1099383429672447 | 101685 | 0.39184971098265897 | 101685 | 0.39184971098265897 | 101685 | 0.39184971098265897 | 15,472 | 13,604 | 完整组合不足，但 partial-case 或子组合审计仍有基础。 |
| pws_year | NOM/有机前体物通路 | 32 | 221 | 0.0008516377649325626 | 19704 | 0.0759306358381503 | 19704 | 0.0759306358381503 | 19704 | 0.0759306358381503 | 216 | 215 | 完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。 |
| pws_year | 消毒剂与残余消毒剂通路 | 26 | 0 | 0.0 | 9013 | 0.03473217726396917 | 8363 | 0.032227360308285165 | 7636 | 0.02942581888246628 | 0 | 0 | 完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。 |
| pws_year | 监测覆盖度与证据质量通路 | 13 | 39475 | 0.1521194605009634 | 259500 | 1.0 | 259500 | 1.0 | 259500 | 1.0 | 26,704 | 23,693 | 完整组合不足，但 partial-case 或子组合审计仍有基础。 |
| pws_year | 结果谱系/解释候选通路 | 24 | 160864 | 0.6198998073217726 | 204317 | 0.7873487475915222 | 204317 | 0.7873487475915222 | 204317 | 0.7873487475915222 | 160,864 | 160,864 | 仅限盘点和泄露复核，不进入预测输入。 |
| pws_year | 合规与纠正行动响应候选通路 | 0 | 0 | 0.0 | 0 | 0.0 | <NA> | <NA> | <NA> | <NA> | 0 | 0 | 仅限盘点和泄露复核，不进入预测输入。 |

第二层 `facility-month` complete/partial-case：

| layer | pathway_name | candidate_field_count | complete_case_n_all_candidate_fields | complete_case_rate_all_candidate_fields | partial_case_n_at_least_1 | partial_case_rate_at_least_1 | partial_case_n_at_least_2 | partial_case_rate_at_least_2 | partial_case_n_at_least_3 | partial_case_rate_at_least_3 | tthm_overlap_complete_case_n | haa5_overlap_complete_case_n | training_feasibility_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| facility_month | 结构背景通路 | 5 | 1442436 | 0.9997976056470796 | 1442728 | 1.0 | 1442728 | 1.0 | 1442728 | 1.0 | 549,646 | 481,740 | 完整组合样本基础较好，可进入后续模型准入测试。 |
| facility_month | 设施复杂度通路 | 3 | 634695 | 0.43992699940667956 | 1021496 | 0.7080308970228623 | 634695 | 0.43992699940667956 | 634695 | 0.43992699940667956 | 292,360 | 260,656 | 完整组合样本基础较好，可进入后续模型准入测试。 |
| facility_month | 处理工艺通路 | 13 | 45758 | 0.03171630411276415 | 227588 | 0.15774837668638855 | 227588 | 0.15774837668638855 | 227567 | 0.1577338209281306 | 951 | 147 | 完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。 |
| facility_month | 酸碱与缓冲条件通路 | 10 | 80073 | 0.05550110623762761 | 495082 | 0.34315685285098785 | 495082 | 0.34315685285098785 | 495082 | 0.34315685285098785 | 2,638 | 2,291 | 完整组合不足，但 partial-case 或子组合审计仍有基础。 |
| facility_month | NOM/有机前体物通路 | 20 | 2877 | 0.0019941388813414585 | 363911 | 0.2522381211149988 | 363911 | 0.2522381211149988 | 363911 | 0.2522381211149988 | 5 | 3 | 完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。 |
| facility_month | 消毒剂与残余消毒剂通路 | 17 | 0 | 0.0 | 255624 | 0.17718100709211992 | 252755 | 0.17519241326154342 | 244785 | 0.16966815643697217 | 0 | 0 | 完整组合或标签重叠基础不足，更适合专题审计或先验语义复核。 |
| facility_month | 监测覆盖度与证据质量通路 | 11 | 126979 | 0.08801312513516062 | 1442728 | 1.0 | 1442728 | 1.0 | 1442728 | 1.0 | 1,149 | 257 | 完整组合不足，但 partial-case 或子组合审计仍有基础。 |
| facility_month | 结果谱系/解释候选通路 | 14 | 466774 | 0.32353569071924854 | 1442728 | 1.0 | 1442728 | 1.0 | 1442728 | 1.0 | 466,774 | 466,774 | 仅限盘点和泄露复核，不进入预测输入。 |
| facility_month | 合规与纠正行动响应候选通路 | 0 | 0 | 0.0 | 0 | 0.0 | <NA> | <NA> | <NA> | <NA> | 0 | 0 | 仅限盘点和泄露复核，不进入预测输入。 |

当前没有正式 train / validation / test split 审计。本轮输出的是未切分总体审计；split 口径下的正负样本基础应在下一轮模型准入测试或特征冻结前补做。

## 7.1 通路字段明细与 n>=1/2/3 标签对齐结果

本节补充展开每个候选通路内部的具体字段、每个字段与 `TTHM/HAA5` 标签同时可用的条数和覆盖率，以及整条通路在同一行内至少有 `1`、`2`、`3` 个字段非缺失时能够与 `TTHM/HAA5` 标签对齐的样本条数。

读法说明：字段表中的覆盖率分母为该层级总行数；`TTHM/HAA5 对齐条数` 表示该字段非缺失且对应标签同一行可定义。通路 `n>=k` 表中的总体可用条数表示该通路内至少 `k` 个字段同一行非缺失；`TTHM/HAA5 对齐条数` 表示同时满足 `n>=k` 且目标标签可定义。`pws_year_ml_ready` 是第三层 TTHM 建模派生表，当前没有 HAA5 标签，本节不作为 HAA5 对齐明细展开。

### 第三层 PWS-year

#### 结构背景通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| system_type | 259,320 | 99.93% | 199,786 | 76.99% | 165,366 | 63.72% | possible_context_or_structure |
| source_water_type | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_context_or_structure |
| retail_population_served | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_context_or_structure |
| adjusted_total_population_served | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_context_or_structure |
| state_code | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_context_or_structure |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=2 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=3 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |

#### 设施复杂度通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n_facilities_in_master | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_monitoring_coverage |
| water_facility_type_list | 227,243 | 87.57% | 173,799 | 66.97% | 143,083 | 55.14% | possible_context_or_structure |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=2 | 227,243 | 87.57% | 173,799 | 66.97% | 143,083 | 55.14% |
| n>=3 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 |

#### 处理工艺通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| has_disinfection_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| has_filtration_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| has_adsorption_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| has_oxidation_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| has_chloramination_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| has_hypochlorination_process | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| filter_type_list | 7,152 | 2.76% | 5,878 | 2.27% | 5,537 | 2.13% | possible_context_or_structure |
| treatment_process_name_list | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |
| treatment_objective_name_list | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% | possible_context_or_structure |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 39,475 | 15.21% | 26,704 | 10.29% | 23,693 | 9.13% |
| n>=2 | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% |
| n>=3 | 39,457 | 15.21% | 26,702 | 10.29% | 23,692 | 9.13% |

#### 酸碱与缓冲条件通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ph_sample_count | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_monitoring_coverage |
| ph_facility_month_count | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_monitoring_coverage |
| ph_months_with_data | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_monitoring_coverage |
| ph_n_facilities | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_monitoring_coverage |
| ph_sample_weighted_mean | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_mechanism_intensity |
| ph_monthly_median_median | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_mechanism_intensity |
| ph_monthly_max_max | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_mechanism_intensity |
| ph_monthly_p90_p90 | 75,155 | 28.96% | 30,968 | 11.93% | 26,365 | 10.16% | possible_mechanism_intensity |
| alkalinity_sample_count | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_monitoring_coverage |
| alkalinity_facility_month_count | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_monitoring_coverage |
| alkalinity_months_with_data | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_monitoring_coverage |
| alkalinity_n_facilities | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_monitoring_coverage |
| alkalinity_sample_weighted_mean_mg_l | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_mechanism_intensity |
| alkalinity_monthly_median_median_mg_l | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_mechanism_intensity |
| alkalinity_monthly_max_max_mg_l | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_mechanism_intensity |
| alkalinity_monthly_p90_p90_mg_l | 55,059 | 21.22% | 33,721 | 12.99% | 30,363 | 11.70% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 101,685 | 39.18% | 49,217 | 18.97% | 43,124 | 16.62% |
| n>=2 | 101,685 | 39.18% | 49,217 | 18.97% | 43,124 | 16.62% |
| n>=3 | 101,685 | 39.18% | 49,217 | 18.97% | 43,124 | 16.62% |

#### NOM/有机前体物通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| toc_sample_count | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_monitoring_coverage |
| toc_facility_month_count | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_monitoring_coverage |
| toc_months_with_data | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_monitoring_coverage |
| toc_n_facilities | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_monitoring_coverage |
| toc_sample_weighted_mean_mg_l | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_mechanism_intensity |
| toc_monthly_median_median_mg_l | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_mechanism_intensity |
| toc_monthly_max_max_mg_l | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_mechanism_intensity |
| toc_monthly_p90_p90_mg_l | 19,699 | 7.59% | 18,750 | 7.23% | 18,437 | 7.10% | possible_mechanism_intensity |
| doc_sample_count | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_monitoring_coverage |
| doc_facility_month_count | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_monitoring_coverage |
| doc_months_with_data | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_monitoring_coverage |
| doc_n_facilities | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_monitoring_coverage |
| doc_sample_weighted_mean_mg_l | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_mechanism_intensity |
| doc_monthly_median_median_mg_l | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_mechanism_intensity |
| doc_monthly_max_max_mg_l | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_mechanism_intensity |
| doc_monthly_p90_p90_mg_l | 291 | 0.11% | 260 | 0.10% | 258 | 0.10% | possible_mechanism_intensity |
| suva_sample_count | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_monitoring_coverage |
| suva_facility_month_count | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_monitoring_coverage |
| suva_months_with_data | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_monitoring_coverage |
| suva_n_facilities | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_monitoring_coverage |
| suva_sample_weighted_mean_l_mg_m | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_mechanism_intensity |
| suva_monthly_median_median_l_mg_m | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_mechanism_intensity |
| suva_monthly_max_max_l_mg_m | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_mechanism_intensity |
| suva_monthly_p90_p90_l_mg_m | 267 | 0.10% | 262 | 0.10% | 261 | 0.10% | possible_mechanism_intensity |
| uv254_sample_count | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_monitoring_coverage |
| uv254_facility_month_count | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_monitoring_coverage |
| uv254_months_with_data | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_monitoring_coverage |
| uv254_n_facilities | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_monitoring_coverage |
| uv254_sample_weighted_mean_cm_inv | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_mechanism_intensity |
| uv254_monthly_median_median_cm_inv | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_mechanism_intensity |
| uv254_monthly_max_max_cm_inv | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_mechanism_intensity |
| uv254_monthly_p90_p90_cm_inv | 268 | 0.10% | 238 | 0.09% | 237 | 0.09% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 19,704 | 7.59% | 18,754 | 7.23% | 18,441 | 7.11% |
| n>=2 | 19,704 | 7.59% | 18,754 | 7.23% | 18,441 | 7.11% |
| n>=3 | 19,704 | 7.59% | 18,754 | 7.23% | 18,441 | 7.11% |

#### 消毒剂与残余消毒剂通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| plant_disinfectant_concentration_mean_mg_l | 1,369 | 0.53% | 1,191 | 0.46% | 984 | 0.38% | possible_mechanism_intensity |
| plant_ct_value_mean | 735 | 0.28% | 702 | 0.27% | 647 | 0.25% | possible_mechanism_intensity |
| free_chlorine_sample_count | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_monitoring_coverage |
| free_chlorine_facility_month_count | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_monitoring_coverage |
| free_chlorine_months_with_data | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_monitoring_coverage |
| free_chlorine_n_facilities | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_monitoring_coverage |
| free_chlorine_sample_weighted_mean_mg_l | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_mechanism_intensity |
| free_chlorine_monthly_median_median_mg_l | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_mechanism_intensity |
| free_chlorine_monthly_max_max_mg_l | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_mechanism_intensity |
| free_chlorine_monthly_p90_p90_mg_l | 7,392 | 2.85% | 3,547 | 1.37% | 2,759 | 1.06% | possible_mechanism_intensity |
| total_chlorine_sample_count | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_monitoring_coverage |
| total_chlorine_facility_month_count | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_monitoring_coverage |
| total_chlorine_months_with_data | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_monitoring_coverage |
| total_chlorine_n_facilities | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_monitoring_coverage |
| total_chlorine_sample_weighted_mean_mg_l | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_mechanism_intensity |
| total_chlorine_monthly_median_median_mg_l | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_mechanism_intensity |
| total_chlorine_monthly_max_max_mg_l | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_mechanism_intensity |
| total_chlorine_monthly_p90_p90_mg_l | 1,231 | 0.47% | 783 | 0.30% | 661 | 0.25% | possible_mechanism_intensity |
| chloramine_sample_count | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_monitoring_coverage |
| chloramine_facility_month_count | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_monitoring_coverage |
| chloramine_months_with_data | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_monitoring_coverage |
| chloramine_n_facilities | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_monitoring_coverage |
| chloramine_sample_weighted_mean_mg_l | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_mechanism_intensity |
| chloramine_monthly_median_median_mg_l | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_mechanism_intensity |
| chloramine_monthly_max_max_mg_l | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_mechanism_intensity |
| chloramine_monthly_p90_p90_mg_l | 209 | 0.08% | 158 | 0.06% | 142 | 0.05% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 9,013 | 3.47% | 4,930 | 1.90% | 3,926 | 1.51% |
| n>=2 | 8,363 | 3.22% | 4,425 | 1.71% | 3,573 | 1.38% |
| n>=3 | 7,636 | 2.94% | 3,731 | 1.44% | 2,934 | 1.13% |

#### 监测覆盖度与证据质量通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n_outcome_vars_available | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| n_core_vars_available | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| n_extended_vars_available | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| annual_match_quality_tier | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| months_observed_any | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| months_with_1plus_core_vars | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_monitoring_coverage |
| months_with_2plus_core_vars | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_monitoring_coverage |
| months_with_3plus_core_vars | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_monitoring_coverage |
| mean_core_vars_available_in_row | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| max_core_vars_available_in_row | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| n_facility_month_rows | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_evidence_quality |
| n_facilities_with_treatment_summary | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% | possible_monitoring_coverage |
| treatment_profile_summary | 39,475 | 15.21% | 26,704 | 10.29% | 23,693 | 9.13% | needs_review |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=2 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=3 | 259,500 | 100.00% | 199,802 | 76.99% | 165,379 | 63.73% |

#### 结果谱系/解释候选通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tthm_sample_count | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_facility_month_count | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_months_with_data | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_n_facilities | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_sample_weighted_mean_ug_l | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_monthly_median_median_ug_l | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_monthly_max_max_ug_l | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_monthly_p90_p90_ug_l | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_high_risk_facility_month_count | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_high_risk_month_count | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_high_risk_facility_month_share | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| tthm_high_risk_month_share | 199,802 | 76.99% | 199,802 | 76.99% | 160,864 | 61.99% | possible_outcome_or_label |
| haa5_sample_count | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_facility_month_count | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_months_with_data | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_n_facilities | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_sample_weighted_mean_ug_l | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_monthly_median_median_ug_l | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_monthly_max_max_ug_l | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_monthly_p90_p90_ug_l | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_high_risk_facility_month_count | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_high_risk_month_count | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_high_risk_facility_month_share | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |
| haa5_high_risk_month_share | 165,379 | 63.73% | 160,864 | 61.99% | 165,379 | 63.73% | possible_outcome_or_label |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 204,317 | 78.73% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=2 | 204,317 | 78.73% | 199,802 | 76.99% | 165,379 | 63.73% |
| n>=3 | 204,317 | 78.73% | 199,802 | 76.99% | 165,379 | 63.73% |

### 第二层 facility-month

#### 结构背景通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| system_type | 1,442,436 | 99.98% | 549,646 | 38.10% | 481,740 | 33.39% | possible_context_or_structure |
| source_water_type | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_context_or_structure |
| retail_population_served | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_context_or_structure |
| adjusted_total_population_served | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_context_or_structure |
| state_code | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_context_or_structure |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=2 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=3 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |

#### 设施复杂度通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| water_facility_type | 1,021,496 | 70.80% | 362,756 | 25.14% | 316,334 | 21.93% | possible_context_or_structure |
| n_supplying_facilities | 634,695 | 43.99% | 292,360 | 20.26% | 260,656 | 18.07% | possible_context_or_structure |
| flow_record_count | 634,695 | 43.99% | 292,360 | 20.26% | 260,656 | 18.07% | possible_monitoring_coverage |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 1,021,496 | 70.80% | 362,756 | 25.14% | 316,334 | 21.93% |
| n>=2 | 634,695 | 43.99% | 292,360 | 20.26% | 260,656 | 18.07% |
| n>=3 | 634,695 | 43.99% | 292,360 | 20.26% | 260,656 | 18.07% |

#### 处理工艺通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| has_disinfection_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| has_filtration_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| has_adsorption_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| has_oxidation_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| has_chloramination_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| has_hypochlorination_process | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| treatment_process_record_count | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_monitoring_coverage |
| n_treatment_process_names | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| n_treatment_objective_names | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| filter_type_list | 45,779 | 3.17% | 951 | 0.07% | 147 | 0.01% | possible_context_or_structure |
| treatment_process_name_list | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| treatment_objective_name_list | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |
| treatment_process_summary | 227,588 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | possible_context_or_structure |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 227,588 | 15.77% | 2,699 | 0.19% | 455 | 0.03% |
| n>=2 | 227,588 | 15.77% | 2,699 | 0.19% | 455 | 0.03% |
| n>=3 | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% |

#### 酸碱与缓冲条件通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ph_n_samples | 275,174 | 19.07% | 9,796 | 0.68% | 7,203 | 0.50% | possible_monitoring_coverage |
| ph_mean | 275,174 | 19.07% | 9,796 | 0.68% | 7,203 | 0.50% | possible_mechanism_intensity |
| ph_median | 275,174 | 19.07% | 9,796 | 0.68% | 7,203 | 0.50% | possible_mechanism_intensity |
| ph_max | 275,174 | 19.07% | 9,796 | 0.68% | 7,203 | 0.50% | possible_mechanism_intensity |
| ph_p90 | 275,174 | 19.07% | 9,796 | 0.68% | 7,203 | 0.50% | possible_mechanism_intensity |
| alkalinity_n_samples | 299,981 | 20.79% | 3,220 | 0.22% | 2,738 | 0.19% | possible_monitoring_coverage |
| alkalinity_mean_mg_l | 299,981 | 20.79% | 3,220 | 0.22% | 2,738 | 0.19% | possible_mechanism_intensity |
| alkalinity_median_mg_l | 299,981 | 20.79% | 3,220 | 0.22% | 2,738 | 0.19% | possible_mechanism_intensity |
| alkalinity_max_mg_l | 299,981 | 20.79% | 3,220 | 0.22% | 2,738 | 0.19% | possible_mechanism_intensity |
| alkalinity_p90_mg_l | 299,981 | 20.79% | 3,220 | 0.22% | 2,738 | 0.19% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 495,082 | 34.32% | 10,378 | 0.72% | 7,650 | 0.53% |
| n>=2 | 495,082 | 34.32% | 10,378 | 0.72% | 7,650 | 0.53% |
| n>=3 | 495,082 | 34.32% | 10,378 | 0.72% | 7,650 | 0.53% |

#### NOM/有机前体物通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| toc_n_samples | 363,849 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% | possible_monitoring_coverage |
| toc_mean_mg_l | 363,849 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% | possible_mechanism_intensity |
| toc_median_mg_l | 363,849 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% | possible_mechanism_intensity |
| toc_max_mg_l | 363,849 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% | possible_mechanism_intensity |
| toc_p90_mg_l | 363,849 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% | possible_mechanism_intensity |
| doc_n_samples | 3,774 | 0.26% | 9 | 0.00% | 3 | 0.00% | possible_monitoring_coverage |
| doc_mean_mg_l | 3,774 | 0.26% | 9 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| doc_median_mg_l | 3,774 | 0.26% | 9 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| doc_max_mg_l | 3,774 | 0.26% | 9 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| doc_p90_mg_l | 3,774 | 0.26% | 9 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| suva_n_samples | 3,570 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_monitoring_coverage |
| suva_mean_l_mg_m | 3,570 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| suva_median_l_mg_m | 3,570 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| suva_max_l_mg_m | 3,570 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| suva_p90_l_mg_m | 3,570 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| uv254_n_samples | 3,614 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_monitoring_coverage |
| uv254_mean_cm_inv | 3,614 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| uv254_median_cm_inv | 3,614 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| uv254_max_cm_inv | 3,614 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |
| uv254_p90_cm_inv | 3,614 | 0.25% | 5 | 0.00% | 3 | 0.00% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 363,911 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% |
| n>=2 | 363,911 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% |
| n>=3 | 363,911 | 25.22% | 2,824 | 0.20% | 1,662 | 0.12% |

#### 消毒剂与残余消毒剂通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| plant_disinfectant_concentration_mean_mg_l | 10,743 | 0.74% | 163 | 0.01% | 20 | 0.00% | possible_mechanism_intensity |
| plant_ct_value_mean | 8,066 | 0.56% | 121 | 0.01% | 3 | 0.00% | possible_mechanism_intensity |
| free_chlorine_n_samples | 215,741 | 14.95% | 5,446 | 0.38% | 4,769 | 0.33% | possible_monitoring_coverage |
| free_chlorine_mean_mg_l | 215,741 | 14.95% | 5,446 | 0.38% | 4,769 | 0.33% | possible_mechanism_intensity |
| free_chlorine_median_mg_l | 215,741 | 14.95% | 5,446 | 0.38% | 4,769 | 0.33% | possible_mechanism_intensity |
| free_chlorine_max_mg_l | 215,741 | 14.95% | 5,446 | 0.38% | 4,769 | 0.33% | possible_mechanism_intensity |
| free_chlorine_p90_mg_l | 215,741 | 14.95% | 5,446 | 0.38% | 4,769 | 0.33% | possible_mechanism_intensity |
| total_chlorine_n_samples | 49,676 | 3.44% | 2,385 | 0.17% | 2,398 | 0.17% | possible_monitoring_coverage |
| total_chlorine_mean_mg_l | 49,676 | 3.44% | 2,385 | 0.17% | 2,398 | 0.17% | possible_mechanism_intensity |
| total_chlorine_median_mg_l | 49,676 | 3.44% | 2,385 | 0.17% | 2,398 | 0.17% | possible_mechanism_intensity |
| total_chlorine_max_mg_l | 49,676 | 3.44% | 2,385 | 0.17% | 2,398 | 0.17% | possible_mechanism_intensity |
| total_chlorine_p90_mg_l | 49,676 | 3.44% | 2,385 | 0.17% | 2,398 | 0.17% | possible_mechanism_intensity |
| chloramine_n_samples | 1,886 | 0.13% | 111 | 0.01% | 101 | 0.01% | possible_monitoring_coverage |
| chloramine_mean_mg_l | 1,886 | 0.13% | 111 | 0.01% | 101 | 0.01% | possible_mechanism_intensity |
| chloramine_median_mg_l | 1,886 | 0.13% | 111 | 0.01% | 101 | 0.01% | possible_mechanism_intensity |
| chloramine_max_mg_l | 1,886 | 0.13% | 111 | 0.01% | 101 | 0.01% | possible_mechanism_intensity |
| chloramine_p90_mg_l | 1,886 | 0.13% | 111 | 0.01% | 101 | 0.01% | possible_mechanism_intensity |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 255,624 | 17.72% | 7,182 | 0.50% | 6,432 | 0.45% |
| n>=2 | 252,755 | 17.52% | 7,140 | 0.49% | 6,415 | 0.44% |
| n>=3 | 244,785 | 16.97% | 7,019 | 0.49% | 6,412 | 0.44% |

#### 监测覆盖度与证据质量通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n_result_vars_available | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| n_core_vars_available | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| n_extended_vars_available | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| n_mechanism_vars_available | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| source_module_count | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| match_quality_tier | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_evidence_quality |
| has_water_system_facility_record | 680,668 | 47.18% | 298,105 | 20.66% | 263,206 | 18.24% | needs_review |
| has_facility_plant_record | 154,963 | 10.74% | 6,687 | 0.46% | 2,739 | 0.19% | needs_review |
| has_flow_record | 634,695 | 43.99% | 292,360 | 20.26% | 260,656 | 18.07% | needs_review |
| has_treatment_process_record | 227,567 | 15.77% | 2,699 | 0.19% | 455 | 0.03% | needs_review |
| has_treatment_summary | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | needs_review |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=2 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=3 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |

#### 结果谱系/解释候选通路

字段层面对齐：

| 字段名 | 字段非缺失条数 | 字段覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 | 初步字段属性 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| has_tthm | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_outcome_or_label |
| has_haa5 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_outcome_or_label |
| is_tthm_high_risk_month | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_outcome_or_label |
| is_haa5_high_risk_month | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% | possible_outcome_or_label |
| tthm_n_samples | 549,730 | 38.10% | 549,730 | 38.10% | 466,774 | 32.35% | possible_outcome_or_label |
| tthm_mean_ug_l | 549,730 | 38.10% | 549,730 | 38.10% | 466,774 | 32.35% | possible_outcome_or_label |
| tthm_median_ug_l | 549,730 | 38.10% | 549,730 | 38.10% | 466,774 | 32.35% | possible_outcome_or_label |
| tthm_max_ug_l | 549,730 | 38.10% | 549,730 | 38.10% | 466,774 | 32.35% | possible_outcome_or_label |
| tthm_p90_ug_l | 549,730 | 38.10% | 549,730 | 38.10% | 466,774 | 32.35% | possible_outcome_or_label |
| haa5_n_samples | 481,761 | 33.39% | 466,774 | 32.35% | 481,761 | 33.39% | possible_outcome_or_label |
| haa5_mean_ug_l | 481,761 | 33.39% | 466,774 | 32.35% | 481,761 | 33.39% | possible_outcome_or_label |
| haa5_median_ug_l | 481,761 | 33.39% | 466,774 | 32.35% | 481,761 | 33.39% | possible_outcome_or_label |
| haa5_max_ug_l | 481,761 | 33.39% | 466,774 | 32.35% | 481,761 | 33.39% | possible_outcome_or_label |
| haa5_p90_ug_l | 481,761 | 33.39% | 466,774 | 32.35% | 481,761 | 33.39% | possible_outcome_or_label |

通路层面 n>=1/2/3 对齐：

| 字段数阈值 | 总体可用条数 | 总体覆盖率 | TTHM 对齐条数 | TTHM 对齐率 | HAA5 对齐条数 | HAA5 对齐率 |
| --- | --- | --- | --- | --- | --- | --- |
| n>=1 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=2 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |
| n>=3 | 1,442,728 | 100.00% | 549,730 | 38.10% | 481,761 | 33.39% |

## 8. 当前能确定的结论

- `PWS-year` 结构背景通路和设施复杂度通路具备较好的数据覆盖基础，可进入后续主筛查准入测试，但仍需先验因果-语义复核。
- `PWS-year` 酸碱与缓冲条件通路有中等覆盖和一定标签重叠基础，更适合可选机制证据模块或高信息子样本测试。
- `NOM/有机前体物通路` 与 `消毒剂与残余消毒剂通路` 机制意义较强，但完整组合覆盖和标签重叠不足，不宜直接承担全国主筛查主力输入。
- 监测覆盖度与证据质量字段覆盖稳定，但它们主要服务证据等级和可信度判断，不应解释为导致 DBP 的化学机制因素。
- 结果谱系、同周期目标代理、合规/违规、纠正行动和监管响应类字段只能用于字段存在性、解释或泄露风险审计，不能作为前置预测输入。

## 9. 当前不能确定的结论

- 本轮不判断任何字段的最终模型准入。
- 本轮不判断任何候选通路的最终因果效应。
- 本轮不判断任何字段或通路是否带来稳定模型增量性能。
- 本轮不冻结最终主筛查输入组。

## 10. 术语解释与读法说明

- 非缺失率：表示某个字段在某张表中有有效记录的比例。例如 `PWS-year` 结构背景字段几乎全覆盖，说明这些字段数据较完整；但非缺失率高只代表可用基础好，不代表一定适合作为模型输入。
- 字段-Y 重叠率：表示某个字段非缺失且目标标签 `TTHM` 或 `HAA5` 同时可用的样本比例。例如消毒剂字段具有机制意义，但在第三层与 `TTHM/HAA5` 标签的重叠样本较少，因此不能直接承担广覆盖主筛查主力输入。
- 通路覆盖率：本报告中的通路覆盖率主要指“任意字段覆盖率”，即通路内至少一个字段非缺失的样本比例；它不同于完整组合覆盖率。
- complete-case：表示某个候选特征组合中的所有候选字段在同一行全部非缺失。如果 complete-case 样本很少，整条通路不适合直接作为完整特征组训练。
- partial-case：表示某条通路中只有部分字段可用。partial-case 可以支持单字段、子组合、缺失指示、分层建模或专题审计，但不能等同于完整通路可训练。
- 候选通路：当前按解释机制、监管语义和字段名称临时组织出来的字段集合，不是最终因果通路，也不是最终模型特征组。
- 字段准入：指某个字段是否允许进入后续模型或解释模块。它需要综合覆盖率、字段-Y 对齐、时间顺序、泄露风险、解释语义、稳定性和增量价值，而不是只看一个指标。
- 泄露风险：指字段可能直接或间接包含目标结果、同周期结果、监管响应或后验信息，使模型训练时“偷看答案”。例如 `tthm_*`、`haa5_*`、合规/违规和纠正行动字段都必须先做泄露复核。

结合本轮输出，三个典型读法是：第一，结构背景和设施复杂度通路覆盖率高，但仍要判断它们是风险画像变量、工程背景变量还是机制变量；第二，NOM 通路更接近机制解释，但覆盖率和字段-Y 重叠不足，不应直接承担全国主筛查主力输入；第三，监测覆盖度、样本数、设施数和 match quality 类字段可能对风险识别有帮助，但更可能属于证据质量或监测强度变量。

## 11. 后续先验因果-语义分析待复核清单

- 所有 `tthm_*`、`haa5_*`、`has_tthm`、`has_haa5` 和高风险标签字段。
- 所有样本数、月份数、设施数、记录数、`source_module_count`、`match_quality_tier`、`annual_match_quality_tier` 和缺失标记字段。
- 所有合规、违规、纠正行动和监管响应类字段；当前主表中未发现明显字段，也应在后续原始模块审计中保留该类检查。
- 所有消毒剂与残余消毒剂字段，尤其是 `free_chlorine_*`、`total_chlorine_*`、`chloramine_*`、`plant_disinfectant_concentration_mean_mg_l` 和 `plant_ct_value_mean`。
- NOM 通路中的 `toc/doc/uv254/suva` 强度字段与样本数、月份数、设施数覆盖字段的拆分。
- 酸碱通路中的 `ph/alkalinity` 强度字段与样本数、月份数、设施数覆盖字段的拆分。

## 12. 下一步建议

下一步应先进入先验因果-语义分析，围绕泄露风险、时间顺序、应用可得性、机制强度字段与监测覆盖字段的拆分进行复核。完成该复核后，再进入主筛查特征组冻结和 split 口径下的模型准入测试。

## 13. 结论提醒

本轮的“可用”“覆盖较好”“对齐较好”只代表数据审计意义上的可用基础，不等于已经证明该字段有预测价值、因果作用或稳定模型增量。
