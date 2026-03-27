# V3 facility-month 字段字典

- 更新时间：2026-03-26 22:31:36
- 说明：字段名使用小写 snake_case；主要按主键、结构、结果、机制、treatment 和质控分组。

| 字段名 | 字段类别 | 来源 | 构建方式 | 保留理由 |
| --- | --- | --- | --- | --- |
| pwsid | 主键 | 统一主键 | 标准化保留 | 系统级 join 主键。 |
| water_facility_id | 主键 | 统一主键 | 标准化保留 | 保留设施异质性。 |
| year | 主键 | 统一主键 | 标准化保留 | 固定年度粒度。 |
| month | 主键 | 统一主键 | 标准化保留 | 固定月度粒度。 |
| state_code | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 便于州际差异分析。 |
| system_name | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 便于回查和写作。 |
| system_type | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 反映系统类型差异。 |
| source_water_type | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 反映水源类型差异。 |
| water_facility_type | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 区分 TP/DS 等设施角色。 |
| retail_population_served | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 保留人口规模信息。 |
| adjusted_total_population_served | 结构背景字段 | treatment + occurrence fallback | 维表 join 或回填 | 保留调整后人口规模信息。 |
| tthm_n_samples | 结果变量字段 | tthm_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| tthm_mean_ug_l | 结果变量字段 | tthm_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| tthm_median_ug_l | 结果变量字段 | tthm_facility_month | 月度聚合 | 降低异常值影响。 |
| tthm_max_ug_l | 结果变量字段 | tthm_facility_month | 月度聚合 | 保留尾部风险信息。 |
| tthm_p90_ug_l | 结果变量字段 | tthm_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| haa5_n_samples | 结果变量字段 | haa5_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| haa5_mean_ug_l | 结果变量字段 | haa5_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| haa5_median_ug_l | 结果变量字段 | haa5_facility_month | 月度聚合 | 降低异常值影响。 |
| haa5_max_ug_l | 结果变量字段 | haa5_facility_month | 月度聚合 | 保留尾部风险信息。 |
| haa5_p90_ug_l | 结果变量字段 | haa5_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| ph_n_samples | 核心机制变量字段 | ph_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| ph_mean | 核心机制变量字段 | ph_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| ph_median | 核心机制变量字段 | ph_facility_month | 月度聚合 | 降低异常值影响。 |
| ph_max | 核心机制变量字段 | ph_facility_month | 月度聚合 | 保留尾部风险信息。 |
| ph_p90 | 核心机制变量字段 | ph_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| alkalinity_n_samples | 核心机制变量字段 | alkalinity_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| alkalinity_mean_mg_l | 核心机制变量字段 | alkalinity_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| alkalinity_median_mg_l | 核心机制变量字段 | alkalinity_facility_month | 月度聚合 | 降低异常值影响。 |
| alkalinity_max_mg_l | 核心机制变量字段 | alkalinity_facility_month | 月度聚合 | 保留尾部风险信息。 |
| alkalinity_p90_mg_l | 核心机制变量字段 | alkalinity_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| toc_n_samples | 核心机制变量字段 | toc_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| toc_mean_mg_l | 核心机制变量字段 | toc_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| toc_median_mg_l | 核心机制变量字段 | toc_facility_month | 月度聚合 | 降低异常值影响。 |
| toc_max_mg_l | 核心机制变量字段 | toc_facility_month | 月度聚合 | 保留尾部风险信息。 |
| toc_p90_mg_l | 核心机制变量字段 | toc_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| free_chlorine_n_samples | 核心机制变量字段 | free_chlorine_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| free_chlorine_mean_mg_l | 核心机制变量字段 | free_chlorine_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| free_chlorine_median_mg_l | 核心机制变量字段 | free_chlorine_facility_month | 月度聚合 | 降低异常值影响。 |
| free_chlorine_max_mg_l | 核心机制变量字段 | free_chlorine_facility_month | 月度聚合 | 保留尾部风险信息。 |
| free_chlorine_p90_mg_l | 核心机制变量字段 | free_chlorine_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| total_chlorine_n_samples | 扩展机制变量字段 | total_chlorine_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| total_chlorine_mean_mg_l | 扩展机制变量字段 | total_chlorine_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| total_chlorine_median_mg_l | 扩展机制变量字段 | total_chlorine_facility_month | 月度聚合 | 降低异常值影响。 |
| total_chlorine_max_mg_l | 扩展机制变量字段 | total_chlorine_facility_month | 月度聚合 | 保留尾部风险信息。 |
| total_chlorine_p90_mg_l | 扩展机制变量字段 | total_chlorine_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| doc_n_samples | 扩展机制变量字段 | doc_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| doc_mean_mg_l | 扩展机制变量字段 | doc_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| doc_median_mg_l | 扩展机制变量字段 | doc_facility_month | 月度聚合 | 降低异常值影响。 |
| doc_max_mg_l | 扩展机制变量字段 | doc_facility_month | 月度聚合 | 保留尾部风险信息。 |
| doc_p90_mg_l | 扩展机制变量字段 | doc_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| suva_n_samples | 扩展机制变量字段 | suva_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| suva_mean_l_mg_m | 扩展机制变量字段 | suva_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| suva_median_l_mg_m | 扩展机制变量字段 | suva_facility_month | 月度聚合 | 降低异常值影响。 |
| suva_max_l_mg_m | 扩展机制变量字段 | suva_facility_month | 月度聚合 | 保留尾部风险信息。 |
| suva_p90_l_mg_m | 扩展机制变量字段 | suva_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| uv254_n_samples | 扩展机制变量字段 | uv254_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| uv254_mean_cm_inv | 扩展机制变量字段 | uv254_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| uv254_median_cm_inv | 扩展机制变量字段 | uv254_facility_month | 月度聚合 | 降低异常值影响。 |
| uv254_max_cm_inv | 扩展机制变量字段 | uv254_facility_month | 月度聚合 | 保留尾部风险信息。 |
| uv254_p90_cm_inv | 扩展机制变量字段 | uv254_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| chloramine_n_samples | 扩展机制变量字段 | chloramine_facility_month | 月度聚合 | 保留样本量，用于后续加权与质控。 |
| chloramine_mean_mg_l | 扩展机制变量字段 | chloramine_facility_month | 月度聚合 | 二层主分析的主要强度指标。 |
| chloramine_median_mg_l | 扩展机制变量字段 | chloramine_facility_month | 月度聚合 | 降低异常值影响。 |
| chloramine_max_mg_l | 扩展机制变量字段 | chloramine_facility_month | 月度聚合 | 保留尾部风险信息。 |
| chloramine_p90_mg_l | 扩展机制变量字段 | chloramine_facility_month | 月度聚合 | 保留右尾浓度结构。 |
| has_water_system_facility_record | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 标记是否可接入结构层。 |
| has_facility_plant_record | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 标记是否有厂级工艺信息。 |
| has_treatment_process_record | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 标记是否有工艺过程信息。 |
| has_flow_record | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 标记是否有 flow 信息。 |
| treatment_process_record_count | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 反映工艺记录丰富度。 |
| n_treatment_process_names | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 反映工艺种类数量。 |
| n_treatment_objective_names | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 反映工艺目标种类数量。 |
| treatment_process_name_list | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留工艺名称清单。 |
| treatment_objective_name_list | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留工艺目标清单。 |
| filter_type_list | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留过滤类型摘要。 |
| plant_disinfectant_concentration_mean_mg_l | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留消毒剂浓度结构线索。 |
| plant_ct_value_mean | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留 CT 结构摘要。 |
| flow_record_count | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 反映设施连接规模。 |
| n_supplying_facilities | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 反映设施上游复杂度。 |
| has_disinfection_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在消毒工艺。 |
| has_filtration_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在过滤工艺。 |
| has_adsorption_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在吸附工艺。 |
| has_oxidation_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在氧化工艺。 |
| has_chloramination_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在氯胺化工艺。 |
| has_hypochlorination_process | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 是否存在次氯化工艺。 |
| treatment_process_summary | treatment 摘要字段 | treatment 相关表 | 设施层聚合后外连接 | 保留短摘要。 |
| has_tthm | 质量控制字段 | 派生 | 主表合并后派生 | 标记当前行是否有 TTHM 结果。 |
| has_haa5 | 质量控制字段 | 派生 | 主表合并后派生 | 标记当前行是否有 HAA5 结果。 |
| n_result_vars_available | 质量控制字段 | 派生 | 主表合并后派生 | 统计结果变量可用数量。 |
| n_core_vars_available | 质量控制字段 | 派生 | 主表合并后派生 | 统计核心变量可用数量。 |
| n_extended_vars_available | 质量控制字段 | 派生 | 主表合并后派生 | 统计扩展变量可用数量。 |
| n_mechanism_vars_available | 质量控制字段 | 派生 | 主表合并后派生 | 汇总机制变量覆盖强度。 |
| has_treatment_summary | 质量控制字段 | 派生 | 主表合并后派生 | 标记 treatment 摘要是否可用。 |
| source_module_count | 质量控制字段 | 派生 | 主表合并后派生 | 统计当前行被多少模块覆盖。 |
| is_tthm_high_risk_month | 质量控制字段 | 派生 | 主表合并后派生 | 快速标记 TTHM 高风险月。 |
| is_haa5_high_risk_month | 质量控制字段 | 派生 | 主表合并后派生 | 快速标记 HAA5 高风险月。 |
| match_quality_tier | 质量控制字段 | 派生 | 主表合并后派生 | 按结果与核心变量重合度分层。 |

