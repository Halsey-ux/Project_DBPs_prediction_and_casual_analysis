# V4：V3_pws_year_master 第三层机器学习字段筛选规范

## 1. 文档目的

本规范用于回答一个具体问题：当 `V3_pws_year_master.csv` 进入后续机器学习阶段时，哪些字段应保留为训练特征，哪些字段只应保留在主表中用于回查、描述统计或解释分析，哪些字段应明确排除，避免目标泄漏、信息重复、覆盖率过低或编码复杂度过高。

本规范不修改原始第三层主表，也不覆盖 `V3_pws_year_master.csv`。其作用是为后续派生机器学习就绪表提供统一字段口径。

适用主表：

- `D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_pws_year_master.csv`

相关说明文档：

- `docs/04_v3\V3_PWS_Year_Dictionary.md`
- `docs/04_v3\V3_PWS_Year_Build_Notes.md`
- `docs/04_v3\V3_Prototype_Audit_Report.md`

---

## 2. 基本原则

第三层主表的定位是“全国机器学习主表原型”，但原表同时承载了数据产品、描述统计、解释分析和后续 ML 四种用途，因此后续建模不应直接把全部 130 个字段原样喂给模型，而应按以下原则筛选：

1. 结果变量与由结果变量派生的摘要字段必须分离，避免目标泄漏。
2. 标识字段保留用于索引、回查和结果回写，但不直接入模。
3. 高基数字符串摘要字段先保留在主表中，不作为第一版模型的直接输入。
4. 覆盖极低的扩展机制字段先不作为第一版全国主模型默认特征。
5. 质量控制字段应保留，因为它们能够刻画监测覆盖差异和匹配强度。
6. 原表永远保留完整版本；机器学习阶段只从原表派生 `ml_ready` 子集。

---

## 3. 字段处理分类

本规范将字段分为 4 类：

1. `A_建议保留并入模`
2. `B_条件保留`
3. `C_保留在主表但第一版不入模`
4. `D_禁止作为特征入模`

---

## 4. A 类：建议保留并入模

这一类字段适合作为第一版全国 ML 主模型的默认特征。

### 4.1 结构背景字段

| 字段名 | 建议 | 原因 |
| --- | --- | --- |
| `state_code` | 保留 | 可刻画州际监管、地理和制度差异。 |
| `system_type` | 保留 | 是全国尺度下很重要的系统异质性变量。 |
| `source_water_type` | 保留 | 是 DBP 风险的重要背景变量。 |
| `retail_population_served` | 保留 | 反映系统规模。 |
| `adjusted_total_population_served` | 保留 | 提供调整后人口规模。 |
| `n_facilities_in_master` | 保留 | 反映系统年度设施覆盖范围。 |

### 4.2 treatment 低维摘要字段

| 字段名 | 建议 | 原因 |
| --- | --- | --- |
| `has_disinfection_process` | 保留 | 是低维、稳定、可解释的工艺信号。 |
| `has_filtration_process` | 保留 | 可反映工艺屏障差异。 |
| `has_adsorption_process` | 保留 | 提供有机物去除能力线索。 |
| `has_oxidation_process` | 保留 | 反映强化氧化语境。 |
| `has_chloramination_process` | 保留 | 对 THM/HAA 形成路径有解释价值。 |
| `has_hypochlorination_process` | 保留 | 对消毒工艺差异有解释价值。 |

### 4.3 核心机制变量年度强度字段

| 字段名 | 建议 | 原因 |
| --- | --- | --- |
| `ph_sample_weighted_mean` | 保留 | 第三层核心机制变量。 |
| `alkalinity_sample_weighted_mean_mg_l` | 保留 | 第三层核心机制变量。 |
| `toc_sample_weighted_mean_mg_l` | 保留 | 第三层核心机制变量。 |
| `free_chlorine_sample_weighted_mean_mg_l` | 保留 | 第三层核心机制变量。 |

### 4.4 质量控制字段

| 字段名 | 建议 | 原因 |
| --- | --- | --- |
| `months_observed_any` | 保留 | 反映年度实际观测覆盖。 |
| `tthm_months_with_data` / `haa5_months_with_data` | 条件保留，见任务定义 | 如果该变量不是当前目标，可作为辅助质量特征。 |
| `months_with_1plus_core_vars` | 保留 | 反映机制变量年度可用度。 |
| `months_with_2plus_core_vars` | 保留 | 反映中等信息强度。 |
| `months_with_3plus_core_vars` | 保留 | 反映高信息强度。 |
| `n_core_vars_available` | 保留 | 直接用于样本质量分层。 |
| `annual_match_quality_tier` | 保留 | 直接用于样本质量分层或分模型。 |

---

## 5. B 类：条件保留

这一类字段可以进入第二版或增强版模型，但不建议一上来全部纳入。

### 5.1 结果变量对侧字段

当目标是 `TTHM` 时，可条件保留：

- `haa5_sample_weighted_mean_ug_l`
- `haa5_months_with_data`
- `haa5_n_facilities`

当目标是 `HAA5` 时，可条件保留：

- `tthm_sample_weighted_mean_ug_l`
- `tthm_months_with_data`
- `tthm_n_facilities`

说明：

- 如果研究目标是“平行结果变量共现预测”，这些字段可以作为辅助输入。
- 如果研究目标强调避免结果间信息耦合过强，则第一版建议先不用。

### 5.2 扩展但仍相对可用的机制变量

| 字段名 | 建议 | 原因 |
| --- | --- | --- |
| `total_chlorine_sample_weighted_mean_mg_l` | 条件保留 | 比 DOC/SUVA/UV254 更常见，可用于增强版模型。 |
| `plant_disinfectant_concentration_mean_mg_l` | 条件保留 | 有工艺线索，但覆盖不如基础结构字段稳定。 |
| `plant_ct_value_mean` | 条件保留 | 有工艺意义，但覆盖和含义需谨慎解释。 |
| `n_facilities_with_treatment_summary` | 条件保留 | 可作为 treatment 覆盖强度指标。 |

### 5.3 核心机制变量的替代统计量

以下字段不适合第一版主模型默认全部加入，但可在增强版模型中测试：

- `ph_monthly_median_median`
- `alkalinity_monthly_median_median_mg_l`
- `toc_monthly_median_median_mg_l`
- `free_chlorine_monthly_median_median_mg_l`

说明：

- 这些字段与 `*_sample_weighted_mean*` 含义相近但不完全相同。
- 若与均值字段同时进入模型，可能引入较强共线性。
- 更合理的做法是“一次只选一类年度摘要口径”。

---

## 6. C 类：保留在主表但第一版不入模

这类字段有数据产品价值，但不建议作为第一版全国 ML 主模型的直接特征。

### 6.1 高基数字符串摘要字段

- `system_name`
- `water_facility_type_list`
- `filter_type_list`
- `treatment_process_name_list`
- `treatment_objective_name_list`
- `treatment_profile_summary`

原因：

- 文本和列表字段编码复杂；
- 很容易导致高维稀疏编码问题；
- 第一版模型不需要先把复杂工艺字符串展开。

### 6.2 结果变量覆盖强度字段

- `tthm_sample_count`
- `tthm_facility_month_count`
- `tthm_n_facilities`
- `haa5_sample_count`
- `haa5_facility_month_count`
- `haa5_n_facilities`

原因：

- 这些字段更适合做描述统计、加权、误差解释和样本验收；
- 是否进入模型取决于你是否希望模型利用“监测密度”本身。

第一版建议：

- 保留在主表
- 不作为默认训练特征
- 需要时单独做敏感性分析

### 6.3 极度稀疏的扩展机制变量

- `doc_*`
- `suva_*`
- `uv254_*`
- `chloramine_*`

原因：

- 覆盖率明显偏低；
- 在全国主模型中直接引入，容易让模型复杂度上升但收益有限；
- 更适合作为高信息子样本补充变量。

---

## 7. D 类：禁止作为特征入模

这类字段如果进入模型，容易造成目标泄漏或方法错误。

### 7.1 主键和索引字段

- `pwsid`
- `year`

说明：

- 可以保留在 `ml_ready` 表中作为索引字段；
- 不应直接作为数值或类别特征喂给模型。

### 7.2 当前目标的同源结果摘要字段

如果当前目标是 `tthm_sample_weighted_mean_ug_l` 或 `TTHM` 高风险标签，则以下字段禁止入模：

- `tthm_monthly_median_median_ug_l`
- `tthm_monthly_max_max_ug_l`
- `tthm_monthly_p90_p90_ug_l`
- `tthm_high_risk_facility_month_count`
- `tthm_high_risk_month_count`
- `tthm_high_risk_facility_month_share`
- `tthm_high_risk_month_share`

如果当前目标是 `haa5_sample_weighted_mean_ug_l` 或 `HAA5` 高风险标签，则以下字段禁止入模：

- `haa5_monthly_median_median_ug_l`
- `haa5_monthly_max_max_ug_l`
- `haa5_monthly_p90_p90_ug_l`
- `haa5_high_risk_facility_month_count`
- `haa5_high_risk_month_count`
- `haa5_high_risk_facility_month_share`
- `haa5_high_risk_month_share`

原因：

- 这些字段与目标变量来自同一结果模块、同一年度聚合过程；
- 它们会把目标本身的信息重新送回模型，形成目标泄漏；
- 即使模型表现变好，也没有实际科学意义。

---

## 8. 第一版全国 ML 推荐字段集

以下字段集适合作为第一版 `TTHM` 年度全国模型的起始输入。

### 8.1 索引字段

- `pwsid`
- `year`

### 8.2 目标字段

二选一：

- 回归：`tthm_sample_weighted_mean_ug_l`
- 分类：另行派生 `tthm_high_risk_year_label`

### 8.3 推荐默认特征

- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `n_facilities_in_master`
- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`
- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `free_chlorine_sample_weighted_mean_mg_l`
- `months_observed_any`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`
- `annual_match_quality_tier`

### 8.4 第二版增强特征候选

- `total_chlorine_sample_weighted_mean_mg_l`
- `plant_disinfectant_concentration_mean_mg_l`
- `plant_ct_value_mean`
- `n_facilities_with_treatment_summary`

---

## 9. 样本分层建议

基于当前第三层主表，后续 ML 不建议只做一个单一训练集，而建议至少准备三档样本：

### 9.1 主模型

- 样本条件：`TTHM` 非缺失
- 目标：全国广覆盖 baseline
- 特征：使用第 8 节推荐默认特征

### 9.2 加强模型

- 样本条件：`TTHM` 非缺失且 `n_core_vars_available >= 2`
- 目标：在较高信息样本中测试机制变量增益
- 特征：默认特征 + 条件保留字段

### 9.3 高信息模型

- 样本条件：`TTHM` 非缺失且 `n_core_vars_available >= 3`
- 目标：更强解释性和稳健性检查
- 特征：默认特征 + 增强特征

说明：

- `n_core_vars_available = 4` 的完整样本过少，不应单独作为主模型训练集。

---

## 10. 后续执行建议

基于本规范，建议下一步直接生成一份独立的第三层机器学习就绪表，例如：

- `data_local/V4_ML_Ready/V4_pws_year_ml_ready_tthm.csv`

该表应：

1. 保留索引字段；
2. 保留目标字段；
3. 保留本规范中 `A_建议保留并入模` 的字段；
4. 可选加入 `B_条件保留` 字段；
5. 排除 `D_禁止作为特征入模` 字段；
6. 明确保留一份字段清单和构建脚本。

---

## 11. 最短结论

`V3_pws_year_master.csv` 不应被直接当作训练表原样喂给模型。正确做法是：

- 保留完整主表作为数据产品；
- 另建一张机器学习就绪表；
- 第一版模型优先使用结构背景字段、低维 treatment 字段、核心机制年度均值字段和质量控制字段；
- 当前目标同源的结果摘要字段必须排除，避免目标泄漏；
- 极度稀疏的扩展变量先不作为全国主模型默认特征。

