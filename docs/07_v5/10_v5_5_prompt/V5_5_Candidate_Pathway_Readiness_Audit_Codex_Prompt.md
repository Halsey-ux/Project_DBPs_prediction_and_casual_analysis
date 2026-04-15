# V5.5 Candidate Pathway Readiness Audit Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下文档：

- [V5_Master_Plan.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/V5_Master_Plan.md)
- [V5_4_Candidate_Pathway_Audit_And_Framework_Assembly_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/09_v5_4_execution/V5_4_Candidate_Pathway_Audit_And_Framework_Assembly_Protocol.md)
- [V5_3_Framework_Decision_Support_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/08_v5_3_execution/V5_3_Framework_Decision_Support_Definition.md)
- [V5_3_Framework_Input_Output_Examples.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/08_v5_3_execution/V5_3_Framework_Input_Output_Examples.md)
- [V5_3_Overall_Research_Framework_Status_And_Next_Steps.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/08_v5_3_execution/V5_3_Overall_Research_Framework_Status_And_Next_Steps.md)
- [V3_Facility_Month_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Dictionary.md)
- [V3_PWS_Year_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_PWS_Year_Dictionary.md)
- [V3_Raw_Data_Mapping_Rules.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Raw_Data_Mapping_Rules.md)
- [V5_2_Facility_Month_Mechanistic_Core_Stage1_Result_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Result_Summary.md)
- [V5_2b_Facility_Month_Sample_Framework_And_Boundary_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/07_v5_2b_execution/V5_2b_Facility_Month_Sample_Framework_And_Boundary_Summary.md)

## 1. 当前任务定位

你当前要执行的是 `V5.5` 更新。

`V5.5` 的正式主题是：

- `candidate pathway readiness audit`

这一轮更新的核心目标不是训练新模型，也不是继续扩展一个新的单变量增量实验，而是：

- 将 `V5.4` 已固定的候选信息通路审计与框架组装协议落地为第一轮可执行审计
- 基于当前已经构建的 V3 主表，梳理候选通路字段清单
- 分别在第三层 `PWS-year` 与第二层 `facility-month` 口径下审计候选通路的覆盖率、标签重叠、泄露风险和框架角色
- 输出一张后续建模准入判定表，明确哪些通路适合进入主筛查模型、哪些适合作为可选机制证据模块、哪些只适合作为证据质量或解释模块、哪些应暂缓或排除

## 2. 必须接受的前序判断

在开始 `V5.5` 之前，你必须接受并沿用以下已确认判断：

1. `V5.3` 已将本课题框架定义为面向环保局和水厂的分层风险证据与决策支持框架。
2. 该框架的主价值不是重复完整监管结果，而是在不完整监管数据条件下进行风险筛查、优先级排序与局部证据整合。
3. `V5.4` 已明确后续不能直接无边界扩变量，也不能把每个通路机械训练成一个独立模型后简单投票。
4. 最终框架应组织为三层：广覆盖主筛查模型、可选机制证据模块、证据整合与行动建议层。
5. `PWS-year` 第三层应优先承担广覆盖主筛查任务。
6. `facility-month` 第二层应优先承担局部机制证据与高信息补充任务。
7. 监测覆盖度与数据质量变量可用于证据等级和可信度判断，但不能直接解释为导致 DBP 高风险的化学机制因素。
8. 同周期同目标家族的 DBP 结果变量不得作为预测输入。
9. 原始 SYR4 数据始终只读，不允许原位修改。

## 3. 本轮必须回答的核心问题

`V5.5` 至少必须回答以下问题：

1. 当前 V3 主表中已经有哪些字段可以归入候选信息通路？
2. 每条候选通路在 `PWS-year` 层级和 `facility-month` 层级中的字段覆盖率如何？
3. 每条通路与 `TTHM` 标签和 `HAA5` 标签的重叠覆盖率如何？
4. 每条通路是否存在明显同周期目标泄露风险？
5. 每条通路在真实监管使用场景中是否可能作为前置输入获得？
6. 每条通路应被分配到什么框架角色：主筛查模型输入、可选机制证据模块、证据质量模块、结果谱系/解释模块、探索性专题模块或暂不纳入？
7. 哪些通路应优先进入后续模型准入测试，哪些通路只能作为专题或解释模块，哪些通路应暂缓？

## 4. 本轮审计范围

### 4.1 第一轮优先审计范围

本轮优先审计已经进入 V3 主表的通路，不要一开始就重新整合所有原始 SYR4 模块。

第一轮至少覆盖以下通路：

| 通路 | 候选字段或字段组 | 优先层级 |
|---|---|---|
| 结构背景通路 | `system_type`、`source_water_type`、`retail_population_served`、`adjusted_total_population_served`、`state_code` | `PWS-year` 与 `facility-month` |
| 处理工艺通路 | `has_disinfection_process`、`has_filtration_process`、`has_adsorption_process`、`has_oxidation_process`、`has_chloramination_process`、`has_hypochlorination_process`、`treatment_process_record_count`、`n_treatment_process_names`、`n_treatment_objective_names`、`filter_type_list` | `PWS-year` 与 `facility-month` |
| 设施复杂度通路 | `water_facility_type`、`n_facilities_in_master`、`n_supplying_facilities`、`flow_record_count`、`water_facility_type_list` | `PWS-year` 与 `facility-month` |
| NOM/有机前体物通路 | `toc_*`、`doc_*`、`uv254_*`、`suva_*` | `PWS-year` 与 `facility-month` |
| 酸碱与缓冲条件通路 | `ph_*`、`alkalinity_*` | `PWS-year` 与 `facility-month` |
| 消毒剂与残余消毒剂通路 | `free_chlorine_*`、`total_chlorine_*`、`chloramine_*`、`plant_disinfectant_concentration_mean_mg_l`、`plant_ct_value_mean` | `PWS-year` 与 `facility-month` |
| 监测覆盖度与证据质量通路 | `n_result_vars_available`、`n_core_vars_available`、`n_extended_vars_available`、`n_mechanism_vars_available`、`source_module_count`、`match_quality_tier`、`annual_match_quality_tier`、`months_with_1plus_core_vars`、`months_with_2plus_core_vars`、`months_with_3plus_core_vars` | `PWS-year` 与 `facility-month` |

字段名应以实际主表字段为准。若某些候选字段只存在于其中一个层级，必须在审计表中明确标注。

### 4.2 本轮暂不重新整合的范围

以下原始模块本轮可以在报告中列为后续候选，但不得在未完成字段和时序审计前强行整合入主表或模型：

- 单项 THM 与单项 HAA 组分
- `bromate/chlorite`
- 微生物相关模块
- ADWR compliance
- corrective actions
- cryptobinning
- phasechem
- rads

如果你认为其中某个模块必须在本轮提前审计，必须先说明原因，并将其限定为“字段存在性与覆盖率盘点”，不得直接进入预测模型。

## 5. 审计指标要求

### 5.1 字段级审计

字段级审计表至少包含以下列：

- `layer`
- `pathway_name`
- `field_name`
- `field_exists`
- `non_missing_n`
- `total_n`
- `non_missing_rate`
- `field_type`
- `candidate_role`
- `leakage_risk_note`
- `remarks`

### 5.2 通路级审计

通路级审计表至少包含以下列：

- `layer`
- `pathway_name`
- `candidate_fields`
- `fields_existing_n`
- `any_field_non_missing_n`
- `total_n`
- `any_field_non_missing_rate`
- `tthm_label_overlap_n`
- `tthm_label_overlap_rate`
- `haa5_label_overlap_n`
- `haa5_label_overlap_rate`
- `application_availability_judgement`
- `leakage_risk_level`
- `mechanism_or_regulatory_interpretation`
- `recommended_framework_role`
- `next_step_recommendation`

### 5.3 覆盖率定义

本轮必须区分三类覆盖率：

1. 字段覆盖率：字段本身非缺失比例。
2. 标签重叠覆盖率：字段或通路非缺失且目标标签也可定义的比例。
3. 应用覆盖率判断：监管者或水厂在真实使用时是否大概率能提前提供该信息。

不能只用字段非缺失率替代标签重叠覆盖率。

## 6. 标签与泄露边界

本轮是审计任务，不是正式建模任务，但仍必须严格遵守泄露边界。

### 6.1 标签口径

本轮至少应审计与以下目标的重叠：

- `TTHM` 高风险标签
- `HAA5` 高风险标签

如果主表中已有对应高风险标签字段，应优先使用已有标签字段。若需要临时根据 `tthm_*` 或 `haa5_*` 摘要字段定义审计用标签，必须在报告中明确说明：该标签仅用于覆盖率和重叠率审计，不代表新增预测特征。

### 6.2 泄露控制

必须明确标记以下风险：

- 同周期 `tthm_*` 摘要字段不得作为预测 `TTHM` 的输入。
- 同周期 `haa5_*` 摘要字段不得作为预测 `HAA5` 的输入。
- 同周期单项 THM 组分不得直接预测同周期 `TTHM`。
- 同周期单项 HAA 组分不得直接预测同周期 `HAA5`。
- 合规、纠正行动和事后监管响应变量在时间顺序未明确前，不得作为前置预测输入。

## 7. 建议脚本与输出目录

### 7.1 建议新增脚本

建议新增脚本：

- `scripts/audit_v5_5_candidate_pathway_readiness.py`

脚本应尽量模块化，至少包括：

- 读取 `V3_facility_month_master.csv` 与 `V3_pws_year_master.csv`
- 定义候选通路字段映射
- 自动检查字段是否存在
- 计算字段级覆盖率
- 计算通路级任一字段非缺失覆盖率
- 计算与 `TTHM/HAA5` 审计标签的重叠覆盖率
- 输出字段级和通路级 CSV
- 输出轻量 JSON 或文本摘要，便于报告引用

### 7.2 本地输出目录

本轮本地结果建议写入：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/`

该目录用于保存轻量审计输出。不得写入原始 SYR4 数据目录。

### 7.3 建议输出文件

至少输出：

- `V5_5_candidate_field_coverage.csv`
- `V5_5_candidate_pathway_readiness_summary.csv`
- `V5_5_candidate_pathway_readiness_summary.json`

如输出文件较大，应仅保留本地，并在文档中说明路径和用途；不要把大型结果文件纳入 GitHub。

## 8. 建议新增文档

本轮至少新增：

- `docs/07_v5/11_v5_5_execution/V5_5_Candidate_Pathway_Readiness_Audit_Report.md`

报告必须使用中文，并至少包含：

1. 本轮任务定位。
2. 输入数据与层级。
3. 候选通路字段清单。
4. 字段级覆盖率结果摘要。
5. 通路级覆盖率与标签重叠结果摘要。
6. 泄露风险判断。
7. 每条通路的推荐框架角色。
8. 后续建模准入建议。
9. 哪些通路暂不应进入模型。
10. 对 V5 后续工作的建议。

如果你修改 `V5_Master_Plan.md` 或其他项目文档，必须同步说明修改理由。

## 9. 本轮结果判定规则

本轮结束时，每条通路必须尽量给出明确归属，不应只写“有待进一步研究”。

可用归属包括：

- `main_screening_candidate`
- `optional_mechanistic_evidence_candidate`
- `evidence_quality_module_candidate`
- `outcome_profile_or_explanation_only`
- `exploratory_future_module`
- `defer_or_exclude`

建议下一步动作包括：

- `enter_model_admission_test`
- `audit_more_before_modeling`
- `use_for_evidence_quality_only`
- `use_for_explanation_only`
- `defer_to_future_raw_module_audit`
- `exclude_from_predictive_inputs`

## 10. 明确禁止事项

本轮禁止：

1. 直接训练通路模型。
2. 直接训练多模型投票框架。
3. 直接做树模型、boosting 或超参数优化。
4. 将监测覆盖度变量解释为化学机制因素。
5. 使用同周期同目标 DBP 结果变量作为预测输入。
6. 在未审计时序和泄露风险前整合合规、纠正行动或事后监管响应变量。
7. 将第二层 `facility-month` 与第三层 `PWS-year` 内部样本等级混写。
8. 跳过 `codex.md` 更新。
9. 未经用户确认直接执行 Git commit 或 push。

## 11. 完成后的汇报要求

完成后请至少向用户汇报：

1. 新增或修改了哪些脚本和文档。
2. V5.5 审计使用了哪些输入表。
3. 哪些通路覆盖率较高，适合优先进入后续模型准入测试。
4. 哪些通路机制意义强但覆盖率不足，只适合作为可选机制模块或专题模块。
5. 哪些通路存在泄露风险，只能作为解释或后续审计对象。
6. 下一步建议进入哪一条 V5.6 任务。
7. 是否需要执行 Git 提交并推送到 GitHub，并给出清晰 commit message。

## 12. 当前阶段一句话总结

`V5.5` 的任务不是建模，而是把 `V5.4` 固定的候选信息通路审计协议落地为第一轮可执行审计：明确 SYR4 当前主表中哪些通路有足够覆盖率、足够标签重叠、可控泄露风险和明确框架角色，从而为后续模型准入测试和最终框架搭建提供依据。
