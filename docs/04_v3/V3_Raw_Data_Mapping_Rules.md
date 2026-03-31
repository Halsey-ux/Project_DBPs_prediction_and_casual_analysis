# V3 双主表原始数据映射法则

- 更新时间：2026-03-30 14:25:43（Asia/Hong_Kong）
- 适用主表：
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`
- 文档定位：V3 收尾阶段的数据契约说明。用于固定字段来源、聚合口径、缺失语义、样本分层和禁止误用规则，为后续 V4 派生表与建模任务提供统一边界。

## 1. 本次 V3 收尾更新的目标说明

### 1.1 为什么这一步不等同于建模

- 本次更新的对象是“数据产品契约”，不是“模型性能优化”。
- 核心工作是回答每一列从哪来、按什么键聚合、空白意味着什么、哪些列不能被误当作特征或原始值。
- 因此这一步属于数据治理、方法边界固定和可审计性补充，不属于特征筛选、参数调优或因果估计。

### 1.2 为什么必须在进入 V4 前补这一步

- `V3_facility_month_master` 与 `V3_pws_year_master` 已经足够稳定，但如果没有映射法则文档，后续使用者很容易把二层误当宽表、把三层结果摘要误当原始观测、或把同源目标摘要送回模型。
- V4 要开始生成 `ml_ready` 派生表，必须先固定字段来源、缺失语义和禁止误用规则，否则后续建模会出现目标泄漏、错误缺失处理和跨层误读。
- 这一步完成后，V3 才算从“原型主表”升级为“可审计、可交接、可进入 V4 的稳定数据产品”。

### 1.3 这一步如何服务后续工作

| 后续工作 | 本文档提供的直接支持 |
| --- | --- |
| 描述统计 | 明确二层和三层每个统计量的真实含义，避免把年度上卷量误写成原始样本统计。 |
| 相关性分析 | 明确哪些字段可以做 pairwise / 小模型，哪些字段只是 coverage 或 treatment 摘要。 |
| 机器学习 | 明确禁止误用字段、缺失处理边界和样本分层起点，避免目标泄漏。 |
| 结果解释 | 明确 `*_sample_weighted_mean*`、`*_monthly_max_max*`、`*_high_risk_*` 等字段的解释口径。 |
| 论文写作 | 为“数据来源、聚合规则、缺失限制、样本筛选”章节提供可以直接引用的中文依据。 |

## 2. 二层主表映射总表

### 2.1 二层总原则

- 目标层级固定为 `pwsid + water_facility_id + year + month`。
- occurrence 类源表一律先在原始表内按二层主键聚合，再统一 `outer merge`；不允许在原始 TTHM 样本后直接横向硬拼其他变量。
- 结构背景字段优先取 `syr4_treatment` 维表，缺失时用 occurrence 观测字段回填。
- treatment 相关字段是“设施层摘要后外连接”，不是样本级工艺观测。

### 2.2 二层字段映射总表

| V3 字段名 | 字段类别 | 来源原始文件 | 来源原始字段 | 目标层级 | 聚合方式 | 单位 | 缺失值语义 | 聚合偏差/解释风险 | 后续适用分析 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pwsid`; `water_facility_id`; `year`; `month` | 主键 | 各 occurrence 源表共同键 | `PWSID`; `WATER_FACILITY_ID`; `SAMPLE_COLLECTION_DATE` | facility-month | `SAMPLE_COLLECTION_DATE -> year/month`，`WATER_FACILITY_ID` 标准化后保留 | 不适用 | 主键不存在即该二层单元未进入任一源表并集 | 只是索引，不代表有完整变量覆盖 | join、回写、层级控制 |
| `state_code`; `system_name`; `system_type`; `source_water_type` | 结构背景变量 | `syr4_treatment/SYR4_Water_system_table.csv` + occurrence 回填 | `State Code`; `System Name`; `Source Water Type`; `SYSTEM_TYPE` 等 | facility-month | 先按 `pwsid` 聚合取首个有效值/最大值，再并入二层 | 类别/人数 | treatment 和 occurrence 都无值时留空 | 可能是系统层静态摘要，不代表当月发生变化 | 描述统计、分层、ML 背景特征 |
| `water_facility_type` | 结构背景变量 | `syr4_treatment/SYR4_Water_system_facility_table.csv` + occurrence 回填 | `Water Facility Type`; `WATER_FACILITY_TYPE` | facility-month | 按 `pwsid + water_facility_id` 取首个有效值并入 | 类别 | 设施维表缺失且 occurrence 也无可回填值 | 是设施角色标签，不是当月运行状态 | 设施分层、机制解释 |
| `retail_population_served`; `adjusted_total_population_served` | 结构背景变量 | `SYR4_Water_system_table.csv` + occurrence 回填 | `Retail Population Served`; `Adjusted Total Population Served`; occurrence 同名字段 | facility-month | 按 `pwsid` 取最大值并入 | 人数 | 系统规模信息缺失 | 是系统层规模摘要，不是设施月度人口实测 | 描述统计、规模校正、ML 背景特征 |
| `tthm_n_samples`; `tthm_mean_ug_l`; `tthm_median_ug_l`; `tthm_max_ug_l`; `tthm_p90_ug_l` | 结果变量 | `SYR4_THMs/TOTAL TRIHALOMETHANES (TTHM).csv` | `PWSID`; `WATER_FACILITY_ID`; `SAMPLE_COLLECTION_DATE`; `VALUE`; `UNIT` | facility-month | 对同一二层键下可解析 `VALUE` 求 `count/mean/median/max/p90` | `ug/L` | 该二层键在原始 TTHM 表中没有可用数值，或仅有不可解析/缺失 `VALUE` | 月内不同采样点和不规则采样频次被压缩为月摘要，不等于同步样本 | 高风险月识别、pairwise、二层机制起点 |
| `haa5_n_samples`; `haa5_mean_ug_l`; `haa5_median_ug_l`; `haa5_max_ug_l`; `haa5_p90_ug_l` | 结果变量 | `SYR4_HAAs/HALOACETIC ACIDS (HAA5).csv` | 同上 | facility-month | 同上 | `ug/L` | 同上 | 同上 | HAA5 平行结果线、描述统计 |
| `ph_n_samples`; `ph_mean`; `ph_median`; `ph_max`; `ph_p90` | 核心机制变量 | `SYR4_DBP_Related Parameters/PH.csv` | `PWSID`; `WATER_FACILITY_ID`; `SAMPLE_COLLECTION_DATE`; `VALUE`; `UNIT` | facility-month | 同一二层键下对 `VALUE` 求 `count/mean/median/max/p90` | 原表单位 | 该二层键在 pH 表无可用数值 | 与 TTHM 不是同步样本，只能解释为同月设施环境摘要 | pairwise、机制小模型 |
| `alkalinity_n_samples`; `alkalinity_mean_mg_l`; `alkalinity_median_mg_l`; `alkalinity_max_mg_l`; `alkalinity_p90_mg_l` | 核心机制变量 | `SYR4_DBP_Related Parameters/TOTAL ALKALINITY.csv` | 同上 | facility-month | 同上 | `mg/L` | 该二层键在总碱度表无可用数值 | 同上 | pairwise、机制小模型 |
| `toc_n_samples`; `toc_mean_mg_l`; `toc_median_mg_l`; `toc_max_mg_l`; `toc_p90_mg_l` | 核心机制变量 | `SYR4_DBP_Related Parameters/TOTAL ORGANIC CARBON.csv` | 同上 | facility-month | 同上 | `mg/L` | 该二层键在 TOC 表无可用数值 | 同上 | pairwise、机制小模型 |
| `free_chlorine_n_samples`; `free_chlorine_mean_mg_l`; `free_chlorine_median_mg_l`; `free_chlorine_max_mg_l`; `free_chlorine_p90_mg_l` | 核心机制变量 | `SYR4_Disinfectant Residuals/FREE RESIDUAL CHLORINE (1013).csv` | 同上 | facility-month | 同上 | `mg/L` | 该二层键在游离余氯表无可用数值 | 同上 | pairwise、机制小模型 |
| `total_chlorine_n_samples`; `total_chlorine_mean_mg_l`; `total_chlorine_median_mg_l`; `total_chlorine_max_mg_l`; `total_chlorine_p90_mg_l` | 扩展机制变量 | `SYR4_Disinfectant Residuals/TOTAL CHLORINE (1000).csv` | 同上 | facility-month | 同上 | `mg/L` | 原始表未覆盖或该键无可用数值 | 覆盖率明显低于核心四变量，不宜默认作为全国主线基础变量 | 增强版机制分析、补充特征候选 |
| `doc_n_samples`; `doc_mean_mg_l`; `doc_median_mg_l`; `doc_max_mg_l`; `doc_p90_mg_l` | 扩展机制变量 | `SYR4_DBP_Related Parameters/DOC.csv` | 同上 | facility-month | 同上 | `mg/L` | 多数键不在 DOC 监测覆盖中 | 极稀疏，容易把分析限制到非常小的子样本 | 高信息专题子样本 |
| `suva_n_samples`; `suva_mean_l_mg_m`; `suva_median_l_mg_m`; `suva_max_l_mg_m`; `suva_p90_l_mg_m` | 扩展机制变量 | `SYR4_DBP_Related Parameters/SUVA.csv` | 同上 | facility-month | 同上 | `L/mg-m` | 多数键不在 SUVA 监测覆盖中 | 极稀疏，不适合作为默认宽表变量 | 高信息专题子样本 |
| `uv254_n_samples`; `uv254_mean_cm_inv`; `uv254_median_cm_inv`; `uv254_max_cm_inv`; `uv254_p90_cm_inv` | 扩展机制变量 | `SYR4_DBP_Related Parameters/UV_ABSORBANCE.csv` | 同上 | facility-month | 同上 | `cm-1` | 多数键不在 UV254 监测覆盖中 | 极稀疏，不能默认解释为“低值” | 高信息专题子样本 |
| `chloramine_n_samples`; `chloramine_mean_mg_l`; `chloramine_median_mg_l`; `chloramine_max_mg_l`; `chloramine_p90_mg_l` | 扩展机制变量 | `SYR4_Disinfectant Residuals/CHLORAMINE (1006).csv` | 同上 | facility-month | 同上 | `mg/L` | 多数键不在氯胺监测覆盖中 | 极稀疏，不适合默认纳入第一版全国主线 | 高信息专题子样本 |
| `has_water_system_facility_record`; `has_facility_plant_record`; `has_treatment_process_record`; `has_flow_record` | treatment 摘要字段 | `SYR4_Water_system_facility_table.csv`; `SYR4_Water_system_facility_plant_table.csv`; `SYR4_Treatment_Process_table.csv`; `SYR4_Water_system_flows_table.csv` | 设施或流程表主键字段 | facility-month | 先按设施维度聚合成存在性标记，再按 `pwsid + water_facility_id` 并入 | 0/1 | 留空或 0 表示该设施未成功接入对应 treatment 子表，不等价于“该工艺不存在” | 这是结构表接入状态，不是月度工艺运行记录 | treatment 覆盖诊断、分层 |
| `treatment_process_record_count`; `n_treatment_process_names`; `n_treatment_objective_names` | treatment 摘要字段 | `SYR4_Treatment_Process_table.csv` | `Treatment Process Name`; `Treatment Objective Name` | facility-month | 先按设施统计记录数、工艺种类数、目标种类数，再并入 | 计数 | treatment 流程表无匹配记录 | 表示工艺记录丰富度，不表示处理强度 | treatment 丰富度、专题分析 |
| `treatment_process_name_list`; `treatment_objective_name_list`; `filter_type_list`; `treatment_process_summary` | treatment 摘要字段 | `SYR4_Treatment_Process_table.csv`; `SYR4_Water_system_facility_plant_table.csv` | `Treatment Process Name`; `Treatment Objective Name`; `Filter Type` | facility-month | 先按设施聚合唯一字符串，再并入；`treatment_process_summary` 为列表拼接短摘要 | 文本 | 无匹配 treatment 记录 | 高基数字符串摘要，不能当原始工艺序列或直接原样入模 | 回查、写作、人工解释 |
| `plant_disinfectant_concentration_mean_mg_l`; `plant_ct_value_mean`; `flow_record_count`; `n_supplying_facilities` | treatment 摘要字段 | `SYR4_Water_system_facility_plant_table.csv`; `SYR4_Water_system_flows_table.csv` | `Disinfectant Concentration (mg/L)`; `CT Value`; `Supplying Facility ID` | facility-month | 先按设施对厂级字段求均值，对 flow 字段求记录数/唯一上游设施数，再并入 | `mg/L`; 原表单位；计数 | 设施层无可接入记录 | 厂级均值是静态或半静态摘要，不代表该月实时控制量 | treatment 线索、增强版特征候选 |
| `has_disinfection_process`; `has_filtration_process`; `has_adsorption_process`; `has_oxidation_process`; `has_chloramination_process`; `has_hypochlorination_process` | treatment 摘要字段 | `SYR4_Treatment_Process_table.csv` | `Treatment Objective Name`; `Treatment Process Name` | facility-month | 先按设施对字符串做关键词命中，再并入 | 0/1 | 流程表无记录时留空/0 | 只表示在设施工艺清单中出现过关键词，不保证当月启用 | 低维工艺特征、分层、V4 候选 |
| `has_tthm`; `has_haa5`; `n_result_vars_available`; `n_core_vars_available`; `n_extended_vars_available`; `n_mechanism_vars_available`; `has_treatment_summary`; `source_module_count`; `is_tthm_high_risk_month`; `is_haa5_high_risk_month`; `match_quality_tier` | 质量控制字段 | 主表派生 | 二层结果/机制/treatment 列本身 | facility-month | 合表后按非缺失数量、阈值和规则派生；高风险阈值为 `TTHM >= 80 ug/L`、`HAA5 >= 60 ug/L`；`match_quality_tier` 依据结果变量与核心变量重合度划分 | 计数/0/1/标签 | 上游列缺失会直接传导到这些质控字段 | 是可用度与分层标签，不是环境暴露本身 | 样本验收、分层、V4 准入 |

## 3. 三层主表映射总表

### 3.1 三层总原则

- 目标层级固定为 `pwsid + year`。
- 所有三层年度字段都从 `V3_facility_month_master` 上卷得到，不再回到原始 occurrence 表另做一套口径。
- 因此三层字段必须解释为“系统-年份摘要”，不能解释为单次样本值或单月观测值。

### 3.2 三层字段映射总表

| V3 字段名 | 字段类别 | 来源原始文件 | 来源原始字段 | 中间来源（二层字段） | 目标层级 | 聚合方式 | 单位 | 缺失值语义 | 聚合偏差/解释风险 | 后续适用分析 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pwsid`; `year` | 主键 | 原始 occurrence 各源表 | `PWSID`; `SAMPLE_COLLECTION_DATE` | 二层主键 `pwsid`; `year` | pws-year | 从二层按系统-年份去重保留 | 不适用 | 年度单元未进入二层并集 | 只是索引 | 回写、年度 join |
| `state_code`; `system_name`; `system_type`; `source_water_type`; `retail_population_served`; `adjusted_total_population_served` | 结构背景变量 | `SYR4_Water_system_table.csv` + occurrence 回填 | 同二层 | 二层同名字段 | pws-year | 按 `pwsid + year` 取首个有效值或最大值 | 类别/人数 | 二层已缺失则三层继续缺失 | 仍是系统背景摘要，不是年度动态实测 | ML 背景特征、描述统计 |
| `n_facility_month_rows`; `months_observed_any`; `n_facilities_in_master` | 结构/质控字段 | 各 occurrence + treatment 并集 | 二层键自身 | 二层主键与 `water_facility_id` | pws-year | 统计当年二层行数、唯一月份数、唯一设施数 | 计数 | 年度键仅有结构层而无结果层时仍可能有值 | 反映并集覆盖，不等于某个具体变量的覆盖 | 描述统计、样本验收 |
| `n_facilities_with_treatment_summary` | treatment 摘要字段 | `syr4_treatment` 子库 | treatment 设施记录 | 二层 `has_treatment_summary` + `water_facility_id` | pws-year | 统计当年成功接入 treatment 摘要的设施数 | 计数 | 当年无可接入 treatment 摘要设施 | 反映 treatment 覆盖强度，不代表处理工艺多少 | 增强版特征、质控 |
| `water_facility_type_list`; `filter_type_list`; `treatment_process_name_list`; `treatment_objective_name_list`; `treatment_profile_summary` | 结构/文本摘要字段 | `SYR4_Water_system_facility_table.csv`; `SYR4_Water_system_facility_plant_table.csv`; `SYR4_Treatment_Process_table.csv` | 同二层 | 二层列表型字段 | pws-year | 对年度内所有二层列表去重拼接；`treatment_profile_summary` 为短摘要拼接 | 文本 | 年度内无对应二层文本摘要 | 高基数字符串，不可误当低维特征或原始流程轨迹 | 回查、写作、人工解释 |
| `has_disinfection_process`; `has_filtration_process`; `has_adsorption_process`; `has_oxidation_process`; `has_chloramination_process`; `has_hypochlorination_process` | treatment 摘要字段 | `SYR4_Treatment_Process_table.csv` | `Treatment Objective Name`; `Treatment Process Name` | 二层同名布尔字段 | pws-year | 年度内按 `max` 上卷，只要任一设施-月份命中即记为 1 | 0/1 | 年度内无有效 treatment 命中 | 表示年度内曾出现相关工艺信号，不代表全年持续运行 | 低维工艺特征、ML 背景特征 |
| `plant_disinfectant_concentration_mean_mg_l`; `plant_ct_value_mean` | treatment 摘要字段 | `SYR4_Water_system_facility_plant_table.csv` | `Disinfectant Concentration (mg/L)`; `CT Value` | 二层同名字段 | pws-year | 对年度内设施月度摘要再求均值 | `mg/L`; 原表单位 | 年度内没有任何二层有效值 | 是设施层静态摘要的再平均，不等于年度实际投药或 CT 时序 | 增强版特征、工艺解释 |
| `mean_core_vars_available_in_row`; `max_core_vars_available_in_row`; `months_with_1plus_core_vars`; `months_with_2plus_core_vars`; `months_with_3plus_core_vars`; `n_outcome_vars_available`; `n_core_vars_available`; `n_extended_vars_available`; `annual_match_quality_tier` | 质量控制字段 | 二层派生 | 二层结果/机制覆盖情况 | 二层 `n_core_vars_available` 等 | pws-year | 对年度内二层覆盖字段求均值/最大值/唯一月份数；`annual_match_quality_tier` 依据年度结果与核心变量覆盖规则派生 | 计数/标签 | 年度内没有对应类型有效数据 | 是“年度信息强度”标签，不是水质暴露本身 | 样本分层、V4 准入 |
| `tthm_sample_count`; `tthm_facility_month_count`; `tthm_months_with_data`; `tthm_n_facilities`; `tthm_sample_weighted_mean_ug_l`; `tthm_monthly_median_median_ug_l`; `tthm_monthly_max_max_ug_l`; `tthm_monthly_p90_p90_ug_l`; `tthm_high_risk_facility_month_count`; `tthm_high_risk_month_count`; `tthm_high_risk_facility_month_share`; `tthm_high_risk_month_share` | 结果变量 | `TOTAL TRIHALOMETHANES (TTHM).csv` | 原始 `VALUE`; `UNIT`; 日期与主键字段 | 二层 `tthm_n_samples`; `tthm_mean_ug_l`; `tthm_median_ug_l`; `tthm_max_ug_l`; `tthm_p90_ug_l`; `is_tthm_high_risk_month` | pws-year | `sample_count=sum(n_samples)`；`facility_month_count=size(mean 非缺失行)`；`months_with_data=nunique(month)`；`n_facilities=nunique(water_facility_id)`；`sample_weighted_mean=sum(mean*n_samples)/sum(n_samples)`；`monthly_median_median=年度内月中位数再取中位数`；`monthly_max_max=年度内月最大值再取最大`；`monthly_p90_p90=年度内月 P90 再取 P90`；高风险阈值仍为 `80 ug/L` | `ug/L`/计数/占比 | 年度内没有任何 TTHM 二层有效月度摘要 | 全部都是“年度摘要后的摘要”；同源结果字段不能回送当前目标模型 | 全国主模型目标、描述统计、风险标签构建 |
| `haa5_sample_count`; `haa5_facility_month_count`; `haa5_months_with_data`; `haa5_n_facilities`; `haa5_sample_weighted_mean_ug_l`; `haa5_monthly_median_median_ug_l`; `haa5_monthly_max_max_ug_l`; `haa5_monthly_p90_p90_ug_l`; `haa5_high_risk_facility_month_count`; `haa5_high_risk_month_count`; `haa5_high_risk_facility_month_share`; `haa5_high_risk_month_share` | 结果变量 | `HALOACETIC ACIDS (HAA5).csv` | 同上 | 二层 HAA5 对应字段 | pws-year | 与 TTHM 同口径；高风险阈值为 `60 ug/L` | `ug/L`/计数/占比 | 年度内没有任何 HAA5 二层有效月度摘要 | 同上 | HAA5 平行主线、结果描述 |
| `ph_sample_count`; `ph_facility_month_count`; `ph_months_with_data`; `ph_n_facilities`; `ph_sample_weighted_mean`; `ph_monthly_median_median`; `ph_monthly_max_max`; `ph_monthly_p90_p90` | 核心机制变量 | `PH.csv` | 原始 `VALUE` 等字段 | 二层 pH 对应字段 | pws-year | 与结果变量同样的年度上卷逻辑，但无高风险字段 | 原表单位 | 年度内没有任何 pH 二层有效月度摘要 | 是“年度设施月摘要”的再上卷，不是年度同步 pH 序列 | 全国 ML 核心机制变量 |
| `alkalinity_sample_count`; `alkalinity_facility_month_count`; `alkalinity_months_with_data`; `alkalinity_n_facilities`; `alkalinity_sample_weighted_mean_mg_l`; `alkalinity_monthly_median_median_mg_l`; `alkalinity_monthly_max_max_mg_l`; `alkalinity_monthly_p90_p90_mg_l` | 核心机制变量 | `TOTAL ALKALINITY.csv` | 同上 | 二层总碱度对应字段 | pws-year | 同上 | `mg/L` | 同上 | 同上 | 全国 ML 核心机制变量 |
| `toc_sample_count`; `toc_facility_month_count`; `toc_months_with_data`; `toc_n_facilities`; `toc_sample_weighted_mean_mg_l`; `toc_monthly_median_median_mg_l`; `toc_monthly_max_max_mg_l`; `toc_monthly_p90_p90_mg_l` | 核心机制变量 | `TOTAL ORGANIC CARBON.csv` | 同上 | 二层 TOC 对应字段 | pws-year | 同上 | `mg/L` | 同上 | 同上 | 全国 ML 核心机制变量 |
| `free_chlorine_sample_count`; `free_chlorine_facility_month_count`; `free_chlorine_months_with_data`; `free_chlorine_n_facilities`; `free_chlorine_sample_weighted_mean_mg_l`; `free_chlorine_monthly_median_median_mg_l`; `free_chlorine_monthly_max_max_mg_l`; `free_chlorine_monthly_p90_p90_mg_l` | 核心机制变量 | `FREE RESIDUAL CHLORINE (1013).csv` | 同上 | 二层游离余氯对应字段 | pws-year | 同上 | `mg/L` | 同上 | 同上 | 全国 ML 核心机制变量 |
| `total_chlorine_*` | 扩展机制变量 | `TOTAL CHLORINE (1000).csv` | 同上 | 二层总氯对应字段 | pws-year | 与核心变量同口径年度上卷 | `mg/L` | 年度内没有任何总氯二层有效月度摘要 | 覆盖率低于核心变量，宜作为增强版而非默认主模型输入 | 增强版特征 |
| `doc_*`; `suva_*`; `uv254_*`; `chloramine_*` | 扩展机制变量 | `DOC.csv`; `SUVA.csv`; `UV_ABSORBANCE.csv`; `CHLORAMINE (1006).csv` | 同上 | 二层对应字段 | pws-year | 与核心变量同口径年度上卷 | 各自原表单位 | 年度内没有任何对应二层有效月度摘要 | 极稀疏；更适合高信息子样本，不宜默认纳入全国主模型 | 高信息子样本、专题分析 |

### 3.3 三层年度统计量的固定解释

- `*_sample_weighted_mean*`：不是简单年平均，而是“二层月均值按月样本数加权后的年度均值”。
- `*_monthly_median_median*`：先取每个设施-月份的月中位数，再对年度内这些月中位数取中位数，用于保留稳健中心趋势。
- `*_monthly_max_max*`：先取每个设施-月份的月最大值，再对年度内这些月最大值取最大值，用于保留尾部风险。
- `*_monthly_p90_p90*`：先取每个设施-月份的月 P90，再对年度内这些月 P90 取 P90，用于保留右尾结构。
- `*_high_risk_facility_month_count`：当年达到阈值的设施-月份单元数。
- `*_high_risk_month_count`：当年至少有一个设施达到阈值的月份数。
- `*_high_risk_facility_month_share`：高风险设施-月份单元数 / 有结果的设施-月份单元数。
- `*_high_risk_month_share`：高风险月份数 / 有结果月份数。

## 4. 缺失值语义说明

两张 V3 主表中的空白值都不能简单理解为“普通随机缺失”。它们至少可能对应以下四类情形：

| 情形 | 二层主表中的常见表现 | 三层主表中的常见表现 | 解释要求 |
| --- | --- | --- | --- |
| 1. 原始数据未监测 | 该二层键在对应源表根本没有记录，因此 `*_mean*` 等字段为空 | 上卷后整年该变量都为空 | 代表监测覆盖缺失，不代表变量真实为低值或 0 |
| 2. 原始有记录但没有可用数值 | 原始表可能有该键记录，但 `VALUE` 为空或无法解析成数值，构建脚本已在聚合前过滤掉 | 如果全年都只出现此类无效记录，则年度字段为空 | 在最终主表中通常与“未监测”折叠为同样的空白，需要回溯原始表才能进一步区分 |
| 3. 不在该变量覆盖结构中 | 例如 DOC、SUVA、UV254、chloramine 只在极少子模块或子系统覆盖；treatment 摘要也只在接入相应结构表时存在 | 年度字段延续这种结构性缺失 | 这是模块性缺失，不应当被解释成普通数值缺失 |
| 4. 聚合后没有有效值 | 二层某字段为空时，三层上卷后该变量全年无有效设施-月份可聚合 | `*_sample_weighted_mean*`、`*_monthly_*` 等年度摘要为空 | 这是“上游无有效月度摘要”导致的空白，不应被误写成年度均值为 0 |

### 4.1 对后续机器学习的解释要求

- 这些空白总体上更接近“非随机缺失（MNAR）+ 结构性缺失”的组合，而不是普通随机缺失。
- 在 V4 中，优先做法不是对所有空白统一均值填补，而是：
  - 先按样本分层控制信息强度；
  - 利用 `months_with_*core_vars`、`n_core_vars_available`、`annual_match_quality_tier` 等质控字段显式保留覆盖信息；
  - 对极稀疏扩展变量默认不进入第一版全国主模型；
  - 仅在明确不破坏研究边界时，再对局部变量尝试稳健缺失处理。

## 5. 样本分层规则

### 5.1 第三层 `V3_pws_year_master`

当前正式固定三档样本，并保留一档更严格验收子集：

| 样本层 | 明确筛选条件 | 当前数量 | 这样分层的理由 | 服务 V4 的方式 |
| --- | --- | --- | --- | --- |
| 全国主模型样本 | `tthm_sample_count > 0` | `199,802` | 先保证全国覆盖和目标变量可用，是 baseline 主线 | 作为第一版全国 `TTHM` 年度模型的默认起点 |
| 加强模型样本 | `tthm_sample_count > 0` 且 `n_core_vars_available >= 2` | `26,975` | 至少有两个核心机制变量，能开始测试机制变量增益 | 用于默认特征 + 条件保留字段的增强版模型 |
| 高信息模型样本 | `tthm_sample_count > 0` 且 `n_core_vars_available >= 3` | `6,193` | 信息更集中，更适合解释性和稳健性检查 | 用于高信息解释模型和敏感性分析 |
| 更严格验收子集 | `annual_match_quality_tier = A_ready_for_national_ml` | `4,815` | 不仅要求 `n_core_vars_available >= 3`，还要求 `months_with_2plus_core_vars >= 6`，覆盖更稳定 | 用作高信息模型中的更严格稳健性子集，不作为唯一主模型样本 |

补充说明：

- `n_core_vars_available = 4` 的完整系统-年份仅 `60` 个，不能单独作为主模型训练集。
- 如果切换到 `HAA5` 主线，上述规则应平行替换为 `haa5_sample_count > 0` 及对应目标字段，不改变分层思想。

### 5.2 第二层 `V3_facility_month_master`

二层不是全国统一宽表，而是机制分析和高信息子样本入口，因此固定如下分层：

| 样本层 | 明确筛选条件 | 当前数量 | 这样分层的理由 | 服务 V4 的方式 |
| --- | --- | --- | --- | --- |
| 机制分析起点样本 | `has_tthm = 1` | `549,730` | 先保证有结果变量，适合作为二层 pairwise、场景诊断和局部机制分析入口 | 为后续高风险场景分析和二层小模型提供起点 |
| 更高信息的小模型子样本 | `has_tthm = 1` 且 `n_core_vars_available >= 2` | `3,811` | 至少能在同一设施-月份单元中看到 TTHM 与 2 个核心机制变量 | 用于二层受约束小模型、机制探索、pairwise 强化分析 |
| 更严格的内部诊断子样本 | `has_tthm = 1` 且 `n_core_vars_available >= 3` | `230` | 二层信息最密集，但数量已明显变小，不适合作为默认全国主线 | 仅用于高信息补充分析，不替代第三层主模型 |

补充说明：

- 二层 `TTHM + 4 个核心变量全齐` 仍为 `0`，因此二层不能被误写成“完整全变量宽表”。
- 如果切换到 `HAA5`，也应使用同样的二层规则，只把结果字段改为 `has_haa5 = 1`。

## 6. 禁止误用规则

1. 不能把 `V3_facility_month_master` 误写成全国统一全变量宽表。它是“并集骨架 + 稀疏模块覆盖”，不是“全变量齐备表”。
2. 不能把当前目标同源的结果摘要字段送回模型做特征。例如以 `tthm_sample_weighted_mean_ug_l` 为目标时，`tthm_monthly_median_median_ug_l`、`tthm_monthly_max_max_ug_l`、`tthm_monthly_p90_p90_ug_l`、`tthm_high_risk_*` 一律视为目标泄漏。
3. 不能把 `system_name`、`filter_type_list`、`treatment_process_name_list`、`treatment_objective_name_list`、`treatment_profile_summary` 等字符串摘要字段直接原样入模。它们只适合回查、写作和后续有控制的编码工程。
4. 不能把 `doc_*`、`suva_*`、`uv254_*`、`chloramine_*` 这类极稀疏扩展变量默认并入第一版全国主模型。它们应保留在主表，但只用于高信息子样本或增强版实验。
5. 不能把三层聚合字段误解为原始样本值。`*_sample_weighted_mean*`、`*_monthly_max_max*`、`*_high_risk_*` 都是二层再上卷的年度摘要。
6. 不能把空白值简单当作普通随机缺失。它们往往同时承载“未监测、无有效数值、结构性不覆盖、聚合后无值”四种语义。
7. 不能把 treatment 布尔字段解释为“该月一定运行了该工艺”。它们只表示设施工艺清单中存在对应关键词命中或设施层接入成功。
8. 不能跨层混用口径。第三层负责全国 ML 主线，第二层负责高信息机制与场景线；不能用第二层的稀疏结构替代第三层主线，也不能用第三层年度摘要硬做细粒度机制解释。

## 7. 进入 V4 前的准备结论

- 结论 1：两张 V3 主表相对于原始 SYR4 的字段来源、聚合规则、缺失语义、样本分层和误用边界已经可以被明确固定，因此 V3 的“数据契约补全”条件现已满足。
- 结论 2：进入 V4 时，第三层 `V3_pws_year_master` 应继续作为全国主模型原型；第二层 `V3_facility_month_master` 应作为高信息机制补充线，而不是替代主线。
- 结论 3：V4 的正确起点不是直接把 `V3_pws_year_master` 全字段原样入模，而是基于本文件和 `docs/04_v3/V3_PWS_Year_ML_Field_Selection_Protocol.md` 生成一张独立的 `ml_ready` 派生表。
- 结论 4：可以进入 V4，但前提是严格遵守本文件的缺失解释、样本分层和禁止误用规则。
