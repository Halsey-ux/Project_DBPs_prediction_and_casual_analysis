# V5.6 Candidate Pathway Field Inventory And Coverage Audit Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下文档：

- [V5_Master_Plan.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/V5_Master_Plan.md)
- [V5_4_Candidate_Pathway_Audit_And_Framework_Assembly_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/09_v5_4_execution/V5_4_Candidate_Pathway_Audit_And_Framework_Assembly_Protocol.md)
- [V5_5_Candidate_Pathway_Readiness_Audit_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/11_v5_5_execution/V5_5_Candidate_Pathway_Readiness_Audit_Report.md)
- [V5_5_candidate_field_coverage.csv](D:/Project_DBPs_prediction_and_casual_analysis/data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/V5_5_candidate_field_coverage.csv)
- [V5_5_candidate_pathway_readiness_summary.csv](D:/Project_DBPs_prediction_and_casual_analysis/data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/V5_5_candidate_pathway_readiness_summary.csv)
- [V5_5_candidate_pathway_readiness_summary.json](D:/Project_DBPs_prediction_and_casual_analysis/data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/V5_5_candidate_pathway_readiness_summary.json)
- [V3_PWS_Year_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_PWS_Year_Dictionary.md)
- [V3_Facility_Month_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Dictionary.md)
- [V3_Raw_Data_Mapping_Rules.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Raw_Data_Mapping_Rules.md)
- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_Chapter1_Framework_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/V4_Chapter1_Framework_Summary.md)
- [V5_3_Framework_Decision_Support_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/08_v5_3_execution/V5_3_Framework_Decision_Support_Definition.md)

## 1. 当前任务定位

你当前要执行的是 `V5.6` 更新。

`V5.6` 的正式主题是：

- `Candidate Pathway Field Inventory And Coverage Audit`

这一轮更新的核心目标不是直接建模，也不是马上冻结最终主筛查输入组，而是把 `V5.5` 中仍然偏粗的通路 readiness audit 继续展开为字段级、字段-Y 对齐级、通路内部结构级和可训练性级的补充审计。

本轮应服务于一个更现实的问题：

> 在正式做先验因果-语义分析和主模型特征冻结之前，先把 SYR4 当前主表中到底有哪些字段、每个字段覆盖率如何、每个字段和 `TTHM/HAA5` 标签能否对齐、每条候选通路内部由哪些字段支撑、每条通路是否具备后续建模审计基础弄清楚。

本轮仍属于 `V5.6`，但其定位应从原先的“主筛查输入组冻结”前移为：

- 数据认识补全
- 候选通路字段盘点
- 字段级标签对齐审计
- 通路内部覆盖结构审计
- 通路 partial-case / complete-case 可训练性审计
- 为后续先验因果-语义分析和主筛查特征冻结提供更完整的事实基础

## 2. 为什么需要调整 V5.6 的重点

`V5.5` 已经完成了第一轮候选通路 readiness audit，但它仍然没有完全回答以下问题：

1. 当前 `SYR4` 派生主表中所有可见字段到底有哪些。
2. 每个字段各自与 `TTHM/HAA5` 标签的对齐情况如何。
3. 每条候选通路内部到底由哪些字段支撑。
4. 同一通路内部哪些字段是机制强度字段，哪些只是样本数、月份数、设施数或证据质量字段。
5. 每条通路的“任一字段覆盖率”是否掩盖了完整字段组合覆盖不足的问题。
6. 每条通路如果后续进入模型准入测试，complete-case、partial-case 或可插补样本基础是否足够。
7. 当前基于解释机制划分的候选通路是否需要在后续先验因果-语义分析中调整。

因此，`V5.6` 现在应先补完审查，而不是直接冻结主模型输入。

## 3. 必须接受的前序判断

在开始 `V5.6` 之前，你必须接受并沿用以下判断：

1. `V5.5` 是候选通路 readiness audit，不是完整 feature admission audit。
2. `V5.5` 没有训练模型，没有逐字段计算预测能力，也没有确定每个字段最终能否作为模型输入。
3. 当前通路划分仍应称为 `candidate pathway`，不是最终因果通路定稿。
4. 当前可以先按解释机制和监管语义组织候选通路，但必须允许后续先验因果-语义分析调整字段归属。
5. 本轮审计只回答数据可用性、字段-Y 对齐、通路内部覆盖结构和可训练性基础，不回答最终因果效应。
6. 原始 SYR4 数据始终只读，不允许原位修改。
7. 本轮不得直接训练正式模型，不得做树模型、boosting、超参数优化或多模型投票。
8. 本轮不得把同周期同目标 DBP 结果字段、单项组分、合规与纠正行动类变量作为前置预测输入。

## 4. `V5.5` 已确认但仍需展开的结果

`V5.5` 已经确认了以下通路级结果：

| 层级 | 通路 | 通路覆盖率 | TTHM 标签重叠率 | HAA5 标签重叠率 | `V5.5` 推荐角色 |
|---|---:|---:|---:|---:|---|
| `PWS-year` | 结构背景通路 | `100.00%` | `76.99%` | `63.73%` | `main_screening_candidate` |
| `PWS-year` | 设施复杂度通路 | `100.00%` | `76.99%` | `63.73%` | `main_screening_candidate` |
| `PWS-year` | 处理工艺通路 | `15.21%` | `10.29%` | `9.13%` | `main_screening_candidate`，但需继续审计缺失语义 |
| `PWS-year` | 酸碱与缓冲条件通路 | `39.18%` | `18.97%` | `16.62%` | `optional_mechanistic_evidence_candidate` |
| `PWS-year` | NOM/有机前体物通路 | `7.59%` | `7.23%` | `7.11%` | `optional_mechanistic_evidence_candidate`，但不进主筛查 |
| `PWS-year` | 消毒剂与残余消毒剂通路 | `3.47%` | `1.90%` | `1.51%` | `exploratory_future_module` |
| `PWS-year` | 监测覆盖度与证据质量通路 | `100.00%` | `76.99%` | `63.73%` | `evidence_quality_module_candidate` |

本轮必须把这些通路级结果进一步拆成字段级和组合级审计。

## 5. 本轮必须回答的核心问题

`V5.6` 至少必须回答以下问题：

1. 当前 `V3_pws_year_master.csv`、`V3_facility_month_master.csv` 和必要时 `V4_pws_year_ml_ready.csv` 中到底有哪些字段。
2. 每个字段的非缺失率、唯一值数量、字段类型和示例值是什么。
3. 每个字段单独与 `TTHM` 标签可定义样本的重叠情况如何。
4. 每个字段单独与 `HAA5` 标签可定义样本的重叠情况如何。
5. 当前候选通路下实际匹配到哪些字段，哪些字段只存在于某一个层级。
6. 每条通路内部字段覆盖率排序如何。
7. 每条通路中哪些字段可能是机制强度字段，哪些字段只是监测覆盖或证据质量字段。
8. 每条通路的核心字段 complete-case 样本数是多少。
9. 每条通路的 partial-case 样本数是多少，例如至少 1 个、至少 2 个、至少 3 个候选字段非缺失。
10. 每条通路在 train / validation / test 口径下是否具备正负样本基础。如果当前没有正式 split，可以先输出未切分总体审计，并说明 split 审计需在下一轮补做。
11. 哪些通路已经有足够数据基础进入后续主筛查或机制模块的模型准入测试。
12. 哪些通路只适合后续先验因果-语义复核或专题审计。
13. 哪些字段需要在后续先验因果-语义分析中重点复核。

## 6. 候选通路初始框架

本轮可以沿用 `V5.5` 的候选通路框架，但必须明确这些仍是候选通路，不是最终因果通路定稿。

### 6.1 结构背景通路

候选字段包括但不限于：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `state_code`

### 6.2 设施复杂度通路

候选字段包括但不限于：

- `water_facility_type`
- `n_facilities_in_master`
- `n_supplying_facilities`
- `flow_record_count`
- `water_facility_type_list`

### 6.3 处理工艺通路

候选字段包括但不限于：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`
- `treatment_process_record_count`
- `n_treatment_process_names`
- `n_treatment_objective_names`
- `filter_type_list`

### 6.4 酸碱与缓冲条件通路

候选字段包括：

- `ph_*`
- `alkalinity_*`

### 6.5 NOM/有机前体物通路

候选字段包括：

- `toc_*`
- `doc_*`
- `uv254_*`
- `suva_*`

### 6.6 消毒剂与残余消毒剂通路

候选字段包括：

- `free_chlorine_*`
- `total_chlorine_*`
- `chloramine_*`
- `plant_disinfectant_concentration_mean_mg_l`
- `plant_ct_value_mean`

### 6.7 监测覆盖度与证据质量通路

候选字段包括：

- `n_result_vars_available`
- `n_outcome_vars_available`
- `n_core_vars_available`
- `n_extended_vars_available`
- `n_mechanism_vars_available`
- `source_module_count`
- `match_quality_tier`
- `annual_match_quality_tier`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`

### 6.8 结果谱系/解释候选通路

本轮可以只做字段存在性和覆盖率盘点，不得进入预测输入：

- 同周期 `tthm_*`
- 同周期 `haa5_*`
- 单项 THM 组分
- 单项 HAA 组分
- `bromate/chlorite`

### 6.9 合规与纠正行动响应候选通路

本轮可以只做字段存在性和覆盖率盘点，不得进入预测输入：

- compliance 类字段
- violation 类字段
- corrective action 类字段
- 事后监管响应类字段

## 7. 必须新增或修改的脚本

建议新增脚本：

- `scripts/audit_v5_6_candidate_pathway_field_inventory.py`

脚本应尽量模块化，至少包括：

1. 读取 `V3_pws_year_master.csv`
2. 读取 `V3_facility_month_master.csv`
3. 必要时读取 `V4_pws_year_ml_ready.csv`，用于对照已进入 V4 正式主线的字段
4. 自动生成全字段 inventory
5. 按候选通路规则匹配字段
6. 计算每个字段的非缺失数和非缺失率
7. 计算每个字段与 `TTHM/HAA5` 标签可定义样本的重叠数和重叠率
8. 计算每条候选通路内部字段覆盖率排序
9. 计算每条通路的任意字段覆盖率
10. 计算每条通路核心字段 complete-case 覆盖率
11. 计算每条通路 partial-case 覆盖率，例如至少 1 个、2 个、3 个字段非缺失
12. 输出 CSV/JSON 摘要
13. 不训练任何模型

## 8. 审计指标要求

### 8.1 全字段 inventory

至少输出以下列：

- `layer`
- `source_table`
- `field_name`
- `field_type`
- `non_missing_n`
- `total_n`
- `non_missing_rate`
- `unique_n`
- `example_values`
- `name_pattern`
- `is_known_candidate_field`
- `candidate_pathway_guess`
- `remarks`

### 8.2 字段-Y 对齐表

至少输出以下列：

- `layer`
- `field_name`
- `candidate_pathway_guess`
- `non_missing_n`
- `total_n`
- `non_missing_rate`
- `tthm_label_available_n`
- `field_and_tthm_label_n`
- `field_and_tthm_label_rate`
- `haa5_label_available_n`
- `field_and_haa5_label_n`
- `field_and_haa5_label_rate`
- `preliminary_use_note`
- `needs_causal_semantic_review`

注意：这里是每个字段单独与标签对齐，不是通路整体对齐。

### 8.3 候选通路字段展开表

至少输出以下列：

- `layer`
- `pathway_name`
- `field_name`
- `matched_by`
- `field_exists`
- `non_missing_n`
- `non_missing_rate`
- `field_and_tthm_label_n`
- `field_and_haa5_label_n`
- `preliminary_field_subtype`
- `remarks`

`preliminary_field_subtype` 可以先粗分为：

- `possible_mechanism_intensity`
- `possible_monitoring_coverage`
- `possible_evidence_quality`
- `possible_outcome_or_label`
- `possible_context_or_structure`
- `needs_review`

这只是预分类，不是最终因果定稿。

### 8.4 通路内部覆盖结构表

至少输出以下列：

- `layer`
- `pathway_name`
- `field_count`
- `fields_existing_n`
- `any_field_non_missing_n`
- `any_field_non_missing_rate`
- `top_coverage_fields`
- `low_coverage_fields`
- `possible_mechanism_fields_n`
- `possible_monitoring_coverage_fields_n`
- `tthm_label_overlap_n`
- `tthm_label_overlap_rate`
- `haa5_label_overlap_n`
- `haa5_label_overlap_rate`

### 8.5 通路 complete-case / partial-case 审计表

至少输出以下列：

- `layer`
- `pathway_name`
- `candidate_field_count`
- `complete_case_n_all_candidate_fields`
- `complete_case_rate_all_candidate_fields`
- `partial_case_n_at_least_1`
- `partial_case_rate_at_least_1`
- `partial_case_n_at_least_2`
- `partial_case_rate_at_least_2`
- `partial_case_n_at_least_3`
- `partial_case_rate_at_least_3`
- `tthm_overlap_complete_case_n`
- `haa5_overlap_complete_case_n`
- `training_feasibility_note`

如果某条通路字段数少于 2 或 3，对应 partial-case 指标应明确标注为不适用。

## 9. 建议输出目录与文件

本轮本地结果建议写入：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_6/`

至少输出：

- `V5_6_all_field_inventory.csv`
- `V5_6_field_label_alignment.csv`
- `V5_6_candidate_pathway_field_map.csv`
- `V5_6_pathway_internal_coverage_summary.csv`
- `V5_6_pathway_complete_partial_case_summary.csv`
- `V5_6_candidate_pathway_field_inventory_summary.json`

本轮新增中文执行文档建议写入：

- `docs/07_v5/13_v5_6_execution/`

至少新增：

- `V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Report.md`
- `V5_6_Pathway_Data_Availability_Decision_Summary.md`
- `V5_6_Causal_Semantic_Review_Todo_List.md`

## 10. 本轮报告必须包含的内容

执行报告必须使用中文，并至少包含：

1. 本轮任务定位：说明本轮是数据认识补全和候选通路字段审计，不是最终建模。
2. 输入数据说明：列明使用了哪些主表、各自行数和字段数。
3. 全字段 inventory 总结：说明每个层级共有多少字段、多少字段高覆盖、多少字段低覆盖。
4. 候选通路字段展开：逐条通路说明实际匹配到哪些字段。
5. 字段-Y 对齐总结：说明哪些字段单独与 `TTHM/HAA5` 标签对齐较好，哪些对齐不足。
6. 通路内部覆盖结构：说明每条通路由哪些高覆盖字段支撑，哪些字段只是低覆盖补充。
7. complete-case / partial-case 可训练性：说明每条通路如果后续建模，完整组合与部分组合样本基础如何。
8. 当前能确定的结论：哪些通路有足够数据基础，哪些通路只是专题候选。
9. 当前不能确定的结论：明确本轮仍不判断最终字段准入、不判断因果效应、不判断模型增量性能。
10. 后续先验因果-语义分析待复核清单：列出最需要复核的字段类型和通路。
11. 下一步建议：说明是否应进入先验因果-语义分析，还是还需要补充原始模块字段盘点。

执行报告还必须单独设置“术语解释与读法说明”小节。该小节必须用面向项目使用者的中文解释所有本轮报告中反复出现的特殊名词，不能只给公式或英文缩写。至少解释以下概念：

1. 非缺失率：说明它表示某个字段在某张表中有有效记录的比例。例如，如果 `pH` 字段在 `259,500` 个 `PWS-year` 单元中有 `100,000` 个非空值，则非缺失率约为 `38.54%`。同时必须说明非缺失率高只代表字段数据较完整，不代表该字段一定适合作为模型输入。
2. 字段-Y 重叠率：说明它表示某个字段非缺失且目标标签 `TTHM` 或 `HAA5` 同时可用的样本比例。例如，如果某个消毒剂字段本身有记录，但只有很少样本同时拥有 `TTHM` 标签，则它对 `TTHM` 模型训练的直接可用样本基础仍然有限。
3. 通路覆盖率：说明它表示某条候选通路内至少一个字段可用的样本比例，或者在特定定义下若干关键字段可用的比例。报告必须明确采用的是“任意字段覆盖率”“关键字段覆盖率”还是“完整组合覆盖率”，避免把不同口径混在一起。
4. complete-case：说明它表示某个候选特征组合中的所有必需字段在同一样本中都非缺失。报告必须说明 complete-case 样本少时，整条通路不适合直接作为完整特征组训练。
5. partial-case：说明它表示某条通路中只有部分字段可用，但仍可能通过单字段、子组合、缺失指示、分层建模或专题审计方式使用。报告必须说明 partial-case 可以支持探索或局部模型，但不能等同于完整通路可训练。
6. 候选通路：说明它是当前基于解释机制、监管语义和字段名称暂时组织出来的字段集合，不是最终因果通路，也不是最终模型特征组。
7. 字段准入：说明它指某个字段是否允许进入后续模型或解释模块，需要综合覆盖率、字段-Y 对齐、时间顺序、泄露风险、解释语义、稳定性和增量价值，而不是只看一个统计指标。
8. 泄露风险：说明它指字段可能直接或间接包含目标结果、同周期结果、监管响应或后验信息，从而让模型在训练中“偷看答案”。报告必须举例说明 DBP 结果字段、合规/违规字段、纠正行动字段为何需要后续复核。

术语解释必须结合本轮实际输出中的至少 3 个具体例子来解释读法。优先从 `V5.5` 已发现的典型情况中选择例子，例如：

- 结构背景通路和设施复杂度通路覆盖率高，但仍需要判断它们是风险画像变量、工程背景变量，还是机制变量。
- NOM 通路字段可能更接近机制解释，但覆盖率和字段-Y 重叠不足，因此不应直接承担全国主筛查主力输入。
- 消毒剂与残余消毒剂通路具有明确机制意义，但字段-Y 重叠样本很少，因此更适合作为专题审计或高信息子样本分析候选。
- 监测覆盖度、样本数、设施数、match quality 等字段可能对风险识别有帮助，但更可能属于证据质量或监测强度变量，不应误解释为导致 DBP 的化学机制因素。

报告最后的结论部分必须再次用通俗语言说明：本轮的“可用”“覆盖较好”“对齐较好”只代表数据审计意义上的可用基础，不等于已经证明该字段有预测价值、因果作用或稳定模型增量。

## 11. 本轮必须避免的误读

报告中必须明确：

1. 非缺失率高不等于字段一定可以作为模型输入。
2. 标签重叠率高不等于字段有预测价值。
3. 通路任意字段覆盖率高不等于整条通路完整可训练。
4. 样本数、月份数、设施数等字段可能更像监测覆盖或证据质量，不应自动放入机制通路。
5. 本轮不回答最终因果机制。
6. 本轮不回答模型是否有稳定增量性能。
7. 本轮的通路仍是候选通路，后续先验因果-语义分析可以调整字段归属。

## 12. 对后续先验因果-语义分析的衔接要求

本轮结束时必须输出一份待复核清单，用于下一轮先验因果-语义分析。清单至少包括：

- 所有结果字段和目标代理字段
- 所有样本数、月份数、设施数、source module count、match quality 类字段
- 所有合规、违规、纠正行动、监管响应类字段
- 所有消毒剂与残余消毒剂字段，特别是可能存在同周期时序模糊的字段
- NOM 通路中浓度/强度字段与监测覆盖字段的拆分建议
- 酸碱通路中浓度/强度字段与监测覆盖字段的拆分建议

## 13. 对 `codex.md` 的更新要求

本轮属于重要更新。完成后必须同步更新项目根目录：

- `codex.md`

更新内容至少包括：

- 当前阶段推进到 `V5.6` 候选通路字段盘点与覆盖审计
- 新增脚本、执行报告和本地输出路径
- 本轮对 `V5.5` 的补充作用
- 当前仍未完成的先验因果-语义分析任务
- 下一步是否进入先验因果-语义分析或主筛查特征冻结
- 对应 commit 信息占位

## 14. 完成后的汇报要求

完成后请至少向用户汇报：

1. 新增或修改了哪些脚本、文档和本地输出。
2. 本轮使用了哪些输入表。
3. 全字段 inventory 的核心发现。
4. 每条候选通路内部字段覆盖结构的核心发现。
5. 哪些字段或通路与 `TTHM/HAA5` 标签对齐较好。
6. 哪些通路完整组合可训练性不足，只能做 partial-case 或专题审计。
7. 哪些字段需要后续先验因果-语义分析复核。
8. 下一步建议做什么。
9. 是否需要执行 Git 提交并推送到 GitHub，并给出清晰 commit message。

## 15. 当前阶段一句话总结

`V5.6` 的任务不是直接冻结主模型输入，也不是建模，而是把 `V5.5` 的候选通路 readiness audit 展开为更完整的字段盘点、字段-Y 对齐、通路内部覆盖结构和可训练性审计；本轮完成后，项目才能更有依据地进入先验因果-语义分析、通路字段重组和主筛查特征组冻结。
