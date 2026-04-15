# V5.5 候选信息通路 Readiness Audit 执行报告

更新时间：2026-04-15 10:42（Asia/Hong_Kong）

## 1. 本轮任务定位

`V5.5` 的任务不是训练新模型，也不是继续扩展单个变量增量实验，而是把 `V5.4` 已固定的候选信息通路审计与框架组装协议落地为第一轮可执行审计。

本轮目标是基于当前已经构建的 V3 主表，盘点候选通路在 `PWS-year` 第三层和 `facility-month` 第二层中的字段存在性、字段覆盖率、通路级覆盖率、与 `TTHM/HAA5` 审计标签的重叠覆盖率、应用可获得性、目标泄露风险和框架角色。

本轮输出用于后续 `V5.6 Main Screening Admission Test Design And Feature Set Freeze`，不代表已经进入正式建模。

## 2. 输入数据与层级

本轮审计使用两张当前正式 V3 主表：

- 第三层 `PWS-year`：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`
- 第二层 `facility-month`：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`

本次复跑确认：

| 层级 | 输入表 | 行数 | 输入状态 |
|---|---:|---:|---|
| `PWS-year` | `V3_pws_year_master.csv` | `259,500` | 已使用正式恢复后的第三层主表 |
| `facility-month` | `V3_facility_month_master.csv` | `1,442,728` | 已使用第二层正式原型主表 |

第三层如需审计 `TTHM/HAA5` 标签重叠，本轮优先使用主表内已有结果摘要字段判定标签是否可定义；该标签仅用于覆盖率与重叠率审计，不作为新增预测输入。

## 3. 新增脚本与输出

新增脚本：

- `scripts/audit_v5_5_candidate_pathway_readiness.py`

本地输出目录：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/`

本轮输出文件：

- `V5_5_candidate_field_coverage.csv`
- `V5_5_candidate_pathway_readiness_summary.csv`
- `V5_5_candidate_pathway_readiness_summary.json`
- `V5_5_future_raw_module_boundary_notes.csv`

这些输出属于本地审计结果。CSV/JSON 可用于报告引用和后续准入测试设计；大型本地数据仍不进入 GitHub。

## 4. 候选通路字段清单

本轮优先审计已经进入 V3 主表或可由 V3 主表字段直接识别的候选信息通路。

| 通路 | 候选字段规则 | 主要审计层级 |
|---|---|---|
| 结构背景通路 | `system_type`、`source_water_type`、`retail_population_served`、`adjusted_total_population_served`、`state_code` | `PWS-year` 与 `facility-month` |
| 处理工艺通路 | `has_disinfection_process`、`has_filtration_process`、`has_adsorption_process`、`has_oxidation_process`、`has_chloramination_process`、`has_hypochlorination_process`、`treatment_process_record_count`、`n_treatment_process_names`、`n_treatment_objective_names`、`filter_type_list` | `PWS-year` 与 `facility-month` |
| 设施复杂度通路 | `water_facility_type`、`n_facilities_in_master`、`n_supplying_facilities`、`flow_record_count`、`water_facility_type_list` | `PWS-year` 与 `facility-month` |
| NOM/有机前体物通路 | `toc_*`、`doc_*`、`uv254_*`、`suva_*` | `PWS-year` 与 `facility-month` |
| 酸碱与缓冲条件通路 | `ph_*`、`alkalinity_*` | `PWS-year` 与 `facility-month` |
| 消毒剂与残余消毒剂通路 | `free_chlorine_*`、`total_chlorine_*`、`chloramine_*`、`plant_disinfectant_concentration_mean_mg_l`、`plant_ct_value_mean` | `PWS-year` 与 `facility-month` |
| 监测覆盖度与证据质量通路 | `n_result_vars_available`、`n_outcome_vars_available`、`n_core_vars_available`、`n_extended_vars_available`、`n_mechanism_vars_available`、`source_module_count`、`match_quality_tier`、`annual_match_quality_tier`、`months_with_1plus_core_vars`、`months_with_2plus_core_vars`、`months_with_3plus_core_vars` | `PWS-year` 与 `facility-month` |

字段级完整审计结果见本地 `V5_5_candidate_field_coverage.csv`。

## 5. 字段级覆盖率结果摘要

字段级审计确认了一个关键事实：结构背景字段和证据质量字段在两个层级中覆盖最稳定；处理工艺、设施复杂度和水质机制字段的字段存在性与覆盖率在两个层级之间明显不同。

第三层 `PWS-year` 中：

- 结构背景字段基本全覆盖，`source_water_type`、`retail_population_served`、`adjusted_total_population_served`、`state_code` 覆盖率为 `100.00%`，`system_type` 为 `99.93%`。
- 处理工艺字段中，`has_*_process` 字段覆盖率约 `15.21%`，`filter_type_list` 覆盖率约 `2.76%`；`treatment_process_record_count`、`n_treatment_process_names`、`n_treatment_objective_names` 未出现在当前第三层主表中。
- 设施复杂度字段中，`n_facilities_in_master` 覆盖率为 `100.00%`，`water_facility_type_list` 覆盖率约 `87.57%`；单设施类型与 flow 相关字段主要存在于第二层。
- 酸碱与缓冲字段在第三层形成中等覆盖，通路级覆盖率为 `39.18%`。
- NOM/有机前体物字段在第三层覆盖有限，通路级覆盖率为 `7.59%`。
- 消毒剂与残余消毒剂字段在第三层覆盖偏低，通路级覆盖率为 `3.47%`。

第二层 `facility-month` 中：

- 结构背景字段仍为全覆盖。
- 设施复杂度字段通路级覆盖率为 `70.80%`，明显高于处理工艺和部分水质通路。
- 酸碱与缓冲条件通路覆盖率为 `34.32%`，适合作为局部机制证据候选。
- NOM/有机前体物通路覆盖率为 `25.22%`，但与同周期 `TTHM/HAA5` 标签的重叠较低，不能直接写成广覆盖主模型输入。
- 消毒剂与残余消毒剂通路覆盖率为 `17.72%`，但存在时序和运行状态接近性风险，仍需专题审计。

## 6. 通路级覆盖率与标签重叠结果

通路级审计结果如下。这里的 `TTHM/HAA5 标签重叠率` 指通路任一字段非缺失且目标标签可定义的行占该层级总行数的比例，不等同于字段自身覆盖率。

| 层级 | 通路 | 字段数 | 通路覆盖率 | TTHM 标签重叠率 | HAA5 标签重叠率 | 推荐角色 | 下一步 |
|---|---|---:|---:|---:|---:|---|---|
| `PWS-year` | 结构背景通路 | `5` | `100.00%` | `76.99%` | `63.73%` | `main_screening_candidate` | `enter_model_admission_test` |
| `PWS-year` | 处理工艺通路 | `7` | `15.21%` | `10.29%` | `9.13%` | `main_screening_candidate` | `audit_more_before_modeling` |
| `PWS-year` | 设施复杂度通路 | `2` | `100.00%` | `76.99%` | `63.73%` | `main_screening_candidate` | `enter_model_admission_test` |
| `PWS-year` | NOM/有机前体物通路 | `32` | `7.59%` | `7.23%` | `7.11%` | `optional_mechanistic_evidence_candidate` | `audit_more_before_modeling` |
| `PWS-year` | 酸碱与缓冲条件通路 | `16` | `39.18%` | `18.97%` | `16.62%` | `optional_mechanistic_evidence_candidate` | `enter_model_admission_test` |
| `PWS-year` | 消毒剂与残余消毒剂通路 | `26` | `3.47%` | `1.90%` | `1.51%` | `exploratory_future_module` | `defer_to_future_raw_module_audit` |
| `PWS-year` | 监测覆盖度与证据质量通路 | `7` | `100.00%` | `76.99%` | `63.73%` | `evidence_quality_module_candidate` | `use_for_evidence_quality_only` |
| `facility-month` | 结构背景通路 | `5` | `100.00%` | `38.10%` | `33.39%` | `main_screening_candidate` | `enter_model_admission_test` |
| `facility-month` | 处理工艺通路 | `10` | `15.77%` | `0.19%` | `0.03%` | `optional_mechanistic_evidence_candidate` | `audit_more_before_modeling` |
| `facility-month` | 设施复杂度通路 | `3` | `70.80%` | `25.14%` | `21.93%` | `main_screening_candidate` | `enter_model_admission_test` |
| `facility-month` | NOM/有机前体物通路 | `20` | `25.22%` | `0.20%` | `0.12%` | `optional_mechanistic_evidence_candidate` | `audit_more_before_modeling` |
| `facility-month` | 酸碱与缓冲条件通路 | `10` | `34.32%` | `0.72%` | `0.53%` | `optional_mechanistic_evidence_candidate` | `enter_model_admission_test` |
| `facility-month` | 消毒剂与残余消毒剂通路 | `17` | `17.72%` | `0.50%` | `0.45%` | `optional_mechanistic_evidence_candidate` | `audit_more_before_modeling` |
| `facility-month` | 监测覆盖度与证据质量通路 | `6` | `100.00%` | `38.10%` | `33.39%` | `evidence_quality_module_candidate` | `use_for_evidence_quality_only` |

## 7. 泄露风险判断

本轮审计没有把同周期同目标 DBP 结果字段加入候选预测输入。需要继续固定以下泄露边界：

- 同周期 `tthm_*` 摘要字段不得作为预测 `TTHM` 的输入。
- 同周期 `haa5_*` 摘要字段不得作为预测 `HAA5` 的输入。
- 同周期单项 THM 组分不得直接预测同周期 `TTHM`。
- 同周期单项 HAA 组分不得直接预测同周期 `HAA5`。
- 合规、纠正行动和事后监管响应变量在时间顺序未明确前不得作为前置预测输入。
- 监测覆盖度与证据质量变量可用于证据等级、完整性和可信度判断，但不能解释为导致 DBP 高风险的化学机制因素。

处理工艺、设施复杂度和结构背景通路目前泄露风险较低。消毒剂与残余消毒剂通路不属于同目标 DBP 结果，但其字段可能接近同周期运行状态，正式建模前仍需单独确认时间顺序和真实应用可获得性。

## 8. 每条通路的推荐框架角色

### 8.1 结构背景通路

推荐角色：`main_screening_candidate`

理由：两个层级均达到 `100.00%` 通路覆盖率，且第三层与 `TTHM/HAA5` 标签重叠率分别为 `76.99%` 和 `63.73%`。这些字段通常可在预测前获得，泄露风险低，适合进入后续主筛查模型准入测试。

### 8.2 处理工艺通路

推荐角色：第三层可作为 `main_screening_candidate` 的补充候选，第二层暂作为 `optional_mechanistic_evidence_candidate`。

理由：处理工艺字段有明确工程解释意义，但覆盖率只有约 `15%`，且第二层与目标标签重叠率很低。后续可作为主筛查候选中的可审计工程背景摘要，但不应在未完成缺失语义和应用可得性审计前直接扩展成核心主模型输入。

### 8.3 设施复杂度通路

推荐角色：`main_screening_candidate`

理由：第三层通路覆盖率为 `100.00%`，第二层为 `70.80%`，且泄露风险低。该通路适合作为系统结构复杂度和供水组织复杂度代理，优先进入后续主筛查输入组冻结。

### 8.4 NOM/有机前体物通路

推荐角色：`optional_mechanistic_evidence_candidate`

理由：该通路机制意义强，但第三层覆盖率只有 `7.59%`，第二层覆盖率虽为 `25.22%`，与目标标签重叠率仍偏低。当前不适合作为广覆盖主模型输入，更适合作为高信息样本或 reduced dataset 专题模块。

### 8.5 酸碱与缓冲条件通路

推荐角色：`optional_mechanistic_evidence_candidate`

理由：第三层覆盖率为 `39.18%`，与 `TTHM/HAA5` 标签重叠率分别为 `18.97%` 和 `16.62%`；第二层覆盖率为 `34.32%`。该通路可优先进入可选机制证据模块的准入测试，但应与广覆盖主筛查模型区分。

### 8.6 消毒剂与残余消毒剂通路

推荐角色：第三层为 `exploratory_future_module`，第二层为 `optional_mechanistic_evidence_candidate`

理由：该通路机制意义强，但第三层覆盖率只有 `3.47%`，与标签重叠率很低。第二层覆盖率提高到 `17.72%`，但仍需审计字段时间顺序、运行状态接近性和真实可获得性。当前不宜直接进入广覆盖主模型。

### 8.7 监测覆盖度与证据质量通路

推荐角色：`evidence_quality_module_candidate`

理由：该通路覆盖率高，但它反映的是观测完整性、监测强度和数据质量，不是化学机制。后续应进入证据等级、可信度和适用范围判定层，不应被解释为 DBP 生成机制因素。

## 9. 后续建模准入建议

优先进入 `V5.6` 主筛查模型准入测试的通路：

- `PWS-year` 结构背景通路
- `PWS-year` 设施复杂度通路
- `PWS-year` 可审计处理工艺摘要，但需保留缺失语义和应用可得性限制

优先进入可选机制证据模块准入测试的通路：

- `PWS-year` 酸碱与缓冲条件通路
- `facility-month` 酸碱与缓冲条件通路
- `facility-month` NOM/有机前体物通路，限于专题或高信息样本
- `facility-month` 消毒剂与残余消毒剂通路，需先完成时序和运行状态审计

仅用于证据质量模块的通路：

- `PWS-year` 和 `facility-month` 的监测覆盖度与证据质量通路

当前暂不进入正式预测输入的通路或模块：

- 同周期单项 THM 与单项 HAA 组分
- `bromate/chlorite`
- 微生物相关模块
- `ADWR compliance`
- `corrective actions`
- `cryptobinning`
- `phasechem`
- `rads`

这些模块后续可以作为字段存在性、覆盖率、时序和泄露边界专题审计对象，但不能在本轮直接纳入预测模型。

## 10. 对 V5 后续工作的建议

下一步建议启动 `V5.6 Main Screening Admission Test Design And Feature Set Freeze`，核心任务是把本轮 V5.5 的通路审计结果转化为明确的模型准入输入组，而不是立即训练复杂模型。

`V5.6` 应优先完成：

1. 冻结第一轮主筛查候选输入组：`baseline + structural background + facility complexity + audited treatment summary`。
2. 明确 `PWS-year` 主筛查模型的输入边界，禁止同周期目标结果、单项组分、合规和纠正行动类变量进入前置预测输入。
3. 固定证据质量模块字段用途，只用于证据等级、完整性和可信度判断。
4. 为酸碱与缓冲条件通路设计可选机制证据模块准入测试。
5. 对 NOM 和消毒剂/残余消毒剂通路继续做专题覆盖率、时序与标签重叠审计。

本轮结束后的最稳妥结论是：`PWS-year` 结构背景通路和设施复杂度通路已经具备进入主筛查模型准入测试的基础；酸碱与缓冲条件通路具备进入可选机制证据模块的基础；NOM 与消毒剂相关通路机制意义强但覆盖率、标签重叠和时序边界仍不足，暂不应写入广覆盖主模型。
