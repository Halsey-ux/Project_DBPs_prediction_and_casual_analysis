# V5.2 Facility-Month Mechanistic Core Stage1 Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下文档：

- [V1_5_Update_Service_Scope_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/V1_5_Update_Service_Scope_Summary.md)
- [V5_Master_Plan.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/V5_Master_Plan.md)
- [V5_1_Facility_Month_Baseline_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/04_v5_1_execution/V5_1_Facility_Month_Baseline_Protocol.md)
- [V5_1_Facility_Month_Baseline_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/04_v5_1_execution/V5_1_Facility_Month_Baseline_Execution_Report.md)
- [V5_1_Facility_Month_Baseline_Result_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/04_v5_1_execution/V5_1_Facility_Month_Baseline_Result_Summary.md)
- [V5_0_Facility_Month_Candidate_Coverage_And_Overlap_Audit_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/02_v5_0_execution/V5_0_Facility_Month_Candidate_Coverage_And_Overlap_Audit_Report.md)
- [V5_0_Facility_Month_Feasibility_Judgement.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/02_v5_0_execution/V5_0_Facility_Month_Feasibility_Judgement.md)
- [V3_Facility_Month_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Dictionary.md)
- [V3_Facility_Month_Build_Notes.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Build_Notes.md)
- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/06_v4_2_execution/V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md)

## 1. 当前任务定位

你当前要执行的是 `V5.2` 更新。

`V5.2` 的正式主题是：

- `facility-month mechanistic core stage1`

这一轮更新的核心目标不是继续扩大第二层变量链，也不是同时展开多个任务，而是：

- 在真正第二层 `facility-month` 上正式测试 `baseline_core_minimal + pH + alkalinity`
- 在与 `V5.1` 完全一致的标签、切分和对照制度下，判断这条最短机制增强链是否具有稳定价值
- 形成第二层是否可以继续保留“机制支撑线”的第一轮正式证据

## 2. 必须接受的前序判断

在开始 `V5.2` 之前，你必须接受并沿用以下已确认判断：

1. `V5.1` 已经正式固定第二层任务为 `tthm_high_risk_month_prediction`。
2. `V5.1` 已经正式固定第二层标签为 `is_tthm_high_risk_month`，定义为 `tthm_mean_ug_l >= 80 ug/L`。
3. `V5.1` 已经正式固定第二层主切分为 `group_by_pwsid`。
4. `V5.1` 已经正式固定第一版 baseline 为 `baseline_core_minimal`，即 `month + state_code + system_type + source_water_type + retail_population_served + adjusted_total_population_served`。
5. `V5.1` 已经正式固定 `baseline_core_minimal_stage1_reference` 作为 `V5.2` 的同子样本 baseline 对照。
6. `V5.0` 已经确认：真正第二层下当前唯一值得进入正式增强链的最短组合是 `baseline + pH + alkalinity`。
7. `V5.0` 已经确认：`TOC`、`free_chlorine` 与 `total_chlorine` 当前都不应进入第二层正式主链。
8. 第二层 `facility-month` 与第三层 `PWS-year` 内部第二级样本不是同一对象；`V5.2` 必须建立在真正第二层上，而不是借用第三层高信息子样本口径。

## 3. 本轮必须回答的核心问题

`V5.2` 至少必须回答以下问题：

1. 在真正第二层 `facility-month` 上，`baseline_core_minimal + pH + alkalinity` 是否相对 `baseline_core_minimal_stage1_reference` 形成稳定增益？
2. 该增益在 `validation` 与 `test` 上是否方向一致？
3. `pH + alkalinity` 的增益更像是可重复的机制增强证据，还是只出现在极小子样本上的偶然波动？
4. 第二层是否已具备继续保留“机制支撑线”的第一轮正式证据？
5. `V5.3 TOC` 是否仍值得作为后续专题分支保留，还是应进一步收紧边界？

## 4. 当前实验边界与解释要求

### 4.1 `V5.2` 是最短机制增强链检验轮，不是扩变量轮

本轮角色必须明确为：

- 第二层最短机制增强链的正式检验
- `baseline_core_minimal` 与 `baseline_core_minimal + pH + alkalinity` 的直接对照
- 第二层机制支撑线是否成立的第一轮判断

当前不得预设：

- `pH + alkalinity` 一定带来稳定增益
- 第二层一定已经形成成熟的高信息增强模块
- 本轮结束后一定继续进入 `TOC`

### 4.2 必须固定在真正第二层 `facility-month`

本轮所有主检查对象固定为：

- 第二层 `facility-month`

不得把第三层 `PWS-year` 第二级样本中的结论直接搬过来当作第二层正式结论。

### 4.3 必须保持与 `V5.1` 制度完全对齐

本轮必须沿用：

- 同一任务
- 同一标签
- 同一切分
- 同一 baseline
- 同一 stage1 reference 子样本口径

不得重新改标签、重新改切分、重新定义 baseline，否则结果不能与 `V5.1` 直接比较。

### 4.4 本轮重点是“判断是否形成稳定增益”

本轮不是追求最优分数，而是回答：

1. 增益是否存在
2. 增益是否稳定
3. 增益是否值得保留为第二层正式机制支撑证据

更稳妥的优先级是：

1. 制度一致
2. 对照干净
3. 结果方向稳定
4. 解释边界清楚
5. 再讨论分数高低

## 5. 本轮总体原则

1. 原始数据只读，不允许原位修改。
2. 优先复用 `V5.1` 已经生成的读取、切分与训练框架。
3. 所有新增或更新的 `.md` 文档必须使用中文。
4. 必须在同子样本上保留 `baseline_core_minimal_stage1_reference` 对照。
5. 当前仍不做树模型、boosting、复杂调参。
6. 当前模型优先继续使用可解释、轻量、可复现的基线模型。
7. 当前不进行跨州、跨年份、跨系统类型泛化性外推。
8. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)。
9. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送。

## 6. 本轮正式任务定义

### 6.1 主任务

本轮必须完成以下主任务：

1. 基于 `V5.1` 已固定制度，正式定义第二层 `mechanistic core stage1` 特征集。
2. 明确 `pH + alkalinity` 的 complete-case 样本口径，并与 `baseline_core_minimal_stage1_reference` 保持完全一致。
3. 落地第二层 `baseline + pH + alkalinity` 训练脚本与统一结果记录模板。
4. 运行第二层正式实验，输出 train / validation / test 结果。
5. 明确 `pH + alkalinity` 是否形成稳定增益，并写清楚对第二层角色定位的影响。
6. 输出第二层 `V5.2` 协议文档、执行报告与结果摘要。

### 6.2 特征集要求

本轮至少必须明确以下两个版本：

1. `baseline_core_minimal_stage1_reference`
   - 必须严格沿用 `V5.1` 已冻结版本
   - 不允许改字段，不允许改子样本口径
2. `baseline_core_minimal_plus_ph_alkalinity`
   - 在上述 baseline 上加入：
     - `ph_mean`
     - `alkalinity_mean_mg_l`

如你发现需要加入 missing flags 才能维持口径一致，必须先说明理由；默认不允许自动扩展为更多字段。

### 6.3 样本口径要求

本轮正式增强版本必须在以下子样本上运行：

- `tthm_mean_ug_l` 非缺失
- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失
- 正式 baseline 字段全部非缺失

必须保证：

- 增强版本与 `baseline_core_minimal_stage1_reference` 使用完全同一批样本

### 6.4 结果判断要求

本轮必须明确回答：

1. `validation` 与 `test` 上 `PR-AUC` 是否都改善
2. `validation` 与 `test` 上 `ROC-AUC` 是否都改善
3. `balanced_accuracy` 是否方向一致
4. 若部分指标改善、部分指标不改善，应如何解释
5. 当前证据是否足以支持继续推进第二层机制支撑线

## 7. 输入、输出与目录要求

### 7.1 输入

本轮优先使用：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/` 下的切分文件与 baseline 结果
- 第二层原型主表 `V3_facility_month_master.csv`
- `V5.1` baseline 协议、执行报告与结果摘要
- `V5.0` 审计结果文档
- `V4.2` 机制核心 stage1 执行报告，仅作为比较思路参考，不可直接混写

### 7.2 输出目录

本轮所有结果应统一写入新的本地目录，建议命名为：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/`

如目录不存在，应按项目规范新建，但不得写回原始数据路径。

### 7.3 输出文档

本轮至少应新增：

1. 第二层 `V5.2` 协议文档
2. 第二层 `V5.2` 执行报告
3. 第二层 `V5.2` 结果摘要文档

如你新增训练脚本、结果表模板或对照表，也必须写入文档。

## 8. 结果汇报要求

完成后请至少汇报以下内容：

1. 第二层 `V5.2` 正式增强版本采用的字段集是什么
2. 第二层 `V5.2` 使用的样本口径是什么
3. `baseline_core_minimal_stage1_reference` 与 `baseline_core_minimal + pH + alkalinity` 的 train / validation / test 结果如何
4. `pH + alkalinity` 是否形成稳定增益
5. 第二层当前是否已具备第一轮正式机制支撑证据
6. 是否可以继续进入后续 `TOC` 专题分支评估

## 9. 明确禁止事项

当前禁止：

1. 在 `V5.2` 中直接开始 `TOC` 增量实验
2. 未沿用 `V5.1` 已固定标签、切分与 reference 就直接比较结果
3. 把 `pH + alkalinity` 的预测增益直接写成因果机制证明
4. 把第二层结果误写成第三层全国主模型结论
5. 跳过 `codex.md` 更新
6. 未经用户确认直接执行 Git commit 或 push

## 10. 当前阶段一句话总结

`V5.2` 的任务不是继续扩第二层变量链，而是在真正第二层 `facility-month` 上，用与 `V5.1` 完全一致的制度，正式检验最短机制增强链 `baseline_core_minimal + pH + alkalinity` 是否能形成稳定且值得保留的第二层机制支撑证据。
