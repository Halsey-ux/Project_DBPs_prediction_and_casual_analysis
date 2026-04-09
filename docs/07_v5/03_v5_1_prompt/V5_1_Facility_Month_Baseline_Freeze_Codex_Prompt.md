# V5.1 Facility-Month Baseline Freeze Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下文档：

- [V1_5_Update_Service_Scope_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/V1_5_Update_Service_Scope_Summary.md)
- [V5_Master_Plan.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/V5_Master_Plan.md)
- [V5_0_Facility_Month_Candidate_Coverage_And_Overlap_Audit_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/02_v5_0_execution/V5_0_Facility_Month_Candidate_Coverage_And_Overlap_Audit_Report.md)
- [V5_0_Facility_Month_Feasibility_Judgement.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/02_v5_0_execution/V5_0_Facility_Month_Feasibility_Judgement.md)
- [V5_0_Facility_Month_Baseline_And_Enhancement_Recommendations.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/02_v5_0_execution/V5_0_Facility_Month_Baseline_And_Enhancement_Recommendations.md)
- [V3_Facility_Month_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Dictionary.md)
- [V3_Facility_Month_Build_Notes.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Build_Notes.md)
- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_Phase_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/V4_Phase_Summary.md)
- [V4_Chapter1_Framework_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/V4_Chapter1_Framework_Summary.md)

## 1. 当前任务定位

你当前要执行的是 `V5.1` 更新。

`V5.1` 的正式主题是：

- `facility-month baseline freeze`

这一轮更新的核心目标不是直接扩大第二层变量链，也不是立即开始大规模模型比较，而是：

- 在真正第二层 `facility-month` 上正式固定第一版 baseline
- 固定样本口径、标签口径、切分口径与禁止误用规则
- 将 `V5.0` 的审计结论转化为一套可复现、可比较、可作为后续 `V5.2` 对照基线的实验制度

## 2. 必须接受的前序判断

在开始 `V5.1` 之前，你必须接受并沿用以下已确认判断：

1. `V5.0` 已经确认：第二层可以继续推进，但当前只支持一条很短的正式增强链。
2. `V5.0` 已经确认：真正第二层下最稳妥的第一轮正式增强组合是 `baseline + pH + alkalinity`。
3. `V5.0` 已经确认：`baseline + pH + alkalinity + TOC` 在真正第二层下 strict complete-case 仅 `37` 行，不能再被默认写成下一步必做主链。
4. `V5.0` 已经确认：`free_chlorine` 与 `total_chlorine` 当前都不适合作为第二层正式主链变量，应先暂停。
5. 第二层 `facility-month` 与第三层 `PWS-year` 内部第二级样本不是同一对象；`V5.1` 必须建立在真正第二层上，而不是借用第三层高信息子样本口径。

## 3. 本轮必须回答的核心问题

`V5.1` 至少必须回答以下问题：

1. 第二层第一版正式 baseline 的样本口径到底是什么？
2. 第二层第一版正式标签口径到底是什么？
3. 第二层第一版 baseline 应固定为哪些字段？
4. `has_treatment_summary` 是否进入第一版 baseline，还是只保留为条件候选？
5. `water_facility_type` 是否进入第一版 baseline，还是只作为对照项？
6. 第二层应该采用什么切分方式，才能尽量避免设施级/系统级泄漏？
7. 第二层 baseline 结果应输出到哪里，并如何为 `V5.2` 做对照准备？

## 4. 当前实验边界与解释要求

### 4.1 `V5.1` 是 baseline 冻结轮，不是扩变量轮

本轮的角色必须明确为：

- 第二层正式 baseline 制度固定
- 第二层第一版训练 / 验证 / 测试工作流落地
- 为 `V5.2 baseline + pH + alkalinity` 提供严格对照基线

当前不得预设：

- 第二层 baseline 一定已经足够强
- 第二层 baseline 一定要纳入所有结构背景字段
- 第二层 baseline 一定要引入 detailed treatment flags

### 4.2 必须固定在真正第二层 `facility-month`

本轮所有主检查对象固定为：

- 第二层 `facility-month`

不得把第三层 `PWS-year` 的切分、标签、特征制度直接照搬过来而不作说明。

### 4.3 必须保持与机制解释的边界

本轮 baseline 可以包含结构背景或信息可接入性字段，但必须明确：

- baseline 的作用是提供正式对照底座
- baseline 中的制度/记录代理特征不应被误写成环境机制变量

### 4.4 本轮的重点是“冻结制度”而不是“追求最好分数”

本轮若发现某些候选 baseline 字段虽然能提升一点分数，但会明显污染解释边界或缩小样本覆盖，不应自动纳入正式 baseline。

更稳妥的优先级是：

1. 样本覆盖稳定
2. 切分制度清楚
3. 口径可复现
4. 对后续增强实验可作为干净对照
5. 再考虑 baseline 分数

## 5. 本轮总体原则

1. 原始数据只读，不允许原位修改。
2. 优先复用已有第二层主表，不重建底表。
3. 所有新增或更新的 `.md` 文档必须使用中文。
4. 必须先冻结 baseline 制度，再进入 `V5.2` 正式增强实验。
5. 当前仍不做树模型、boosting、复杂调参。
6. 当前模型优先继续使用可解释、轻量、可复现的基线模型。
7. 当前不进行跨州、跨年份、跨系统类型泛化性外推。
8. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)。
9. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送。

## 6. 本轮正式任务定义

### 6.1 主任务

本轮必须完成以下主任务：

1. 基于 `V5.0` 结果正式定义第二层第一版 baseline 候选字段集。
2. 明确第二层第一版默认 baseline 与条件 baseline 的区别。
3. 明确第二层任务标签定义，并写清楚与第三层标签的关系与差异。
4. 设计并固定第二层正式切分策略。
5. 落地第二层 baseline 训练脚本与统一结果记录模板。
6. 运行第二层 baseline 正式实验，输出 train / validation / test 结果。
7. 输出第二层 baseline 制度文档、执行报告与结果摘要。

### 6.2 baseline 字段决策要求

本轮至少必须对以下字段作出明确去留判断：

1. `month`
2. `state_code`
3. `system_type`
4. `source_water_type`
5. `retail_population_served`
6. `adjusted_total_population_served`
7. `has_treatment_summary`
8. `water_facility_type`
9. `has_disinfection_process`
10. `has_filtration_process`
11. `has_adsorption_process`
12. `has_oxidation_process`
13. `has_chloramination_process`
14. `has_hypochlorination_process`

### 6.3 至少应比较的 baseline 版本

本轮至少应比较以下版本：

1. `baseline_core_minimal`
   - 必须尽量只包含最稳定、覆盖最高、解释边界最清楚的基础字段
2. `baseline_core_with_has_treatment_summary`
   - 用于判断 `has_treatment_summary` 是否值得保留在正式 baseline 中
3. `baseline_core_plus_water_facility_type`
   - 用于判断 `water_facility_type` 是否值得进入正式 baseline

如你发现某个版本明显不合理，可以明确指出并调整，但必须给出理由。

### 6.4 标签与任务要求

本轮必须明确第二层正式 baseline 的任务定义。

默认建议：

- 主任务优先围绕 `is_tthm_high_risk_month`

但你必须明确回答：

1. 该标签是否应直接作为 `V5.1` 正式 baseline 标签？
2. 若沿用它，应如何解释其与第三层年度任务的关系？
3. 若不沿用它，应改成什么口径，且理由是什么？

### 6.5 切分要求

本轮必须对第二层切分给出明确方案，并说明为什么这样做。

至少必须讨论以下问题：

1. 是否应按 `pwsid` 分组切分？
2. 是否应按 `pwsid + water_facility_id` 分组切分？
3. 是否会出现同一设施不同月份泄漏到 train / test 的问题？
4. 当前最稳妥的正式主切分是什么？

必须把最终方案写成确定语气，并落实为正式切分脚本。

## 7. 输入、输出与目录要求

### 7.1 输入

本轮优先使用：

- 第二层原型主表 `V3_facility_month_master.csv`
- `V5.0` 审计结果文档
- 第二层字段字典与构建说明
- 第三层 `V4` 训练协议，仅作为制度参考，不可直接混写

### 7.2 输出目录

本轮所有结果应统一写入新的本地目录，建议命名为：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/`

如目录不存在，应按项目规范新建，但不得写回原始数据路径。

### 7.3 输出文档

本轮至少应新增：

1. 第二层 baseline 协议文档
2. 第二层 baseline 执行报告
3. 第二层 baseline 结果摘要文档

如你新增训练脚本、切分脚本或结果表模板，也必须写入文档。

## 8. 结果汇报要求

完成后请至少汇报以下内容：

1. 第二层 `V5.1` 最终固定的正式 baseline 字段集是什么
2. `has_treatment_summary` 是否进入正式 baseline，理由是什么
3. `water_facility_type` 是否进入正式 baseline，理由是什么
4. detailed treatment flags 是否全部排除在 baseline 外，理由是什么
5. 第二层正式标签采用什么定义
6. 第二层正式切分采用什么定义
7. 第二层 baseline 的 train / validation / test 结果如何
8. 第二层 baseline 是否足够稳定，可以继续进入 `V5.2`

## 9. 明确禁止事项

当前禁止：

1. 在 `V5.1` 中直接开始 `pH + alkalinity` 增强实验
2. 未固定切分与标签口径就直接比较多个模型
3. 把 `has_treatment_summary` 误写成环境机制变量
4. 把 detailed treatment flags 在缺失状态下强行改写为 `0`
5. 跳过 `codex.md` 更新
6. 未经用户确认直接执行 Git commit 或 push

## 10. 当前阶段一句话总结

`V5.1` 的任务不是继续扩变量，而是把真正第二层 `facility-month` 的第一版正式 baseline 冻结下来：明确样本、标签、切分、字段与解释边界，形成一个可复现、可比较、可供 `V5.2` 对照的正式起点。

