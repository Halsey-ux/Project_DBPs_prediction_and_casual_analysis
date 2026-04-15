# V5.2 Facility-Month Mechanistic Core Stage1 协议

- 更新时间：2026-04-09 09:45（Asia/Hong_Kong）
- 对应阶段：`V5.2`
- 输入主表：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 复用切分：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/v5_1_group_by_pwsid_master_split.csv`
- 本地结果目录：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/`

## 1. 文档定位

本协议用于正式冻结第二层 `facility-month` 的 `V5.2 mechanistic core stage1` 制度。

本轮目标不是继续扩展第二层变量链，而是严格在 `V5.1` 已冻结制度下，检验：

- `baseline_core_minimal_stage1_reference`
- `baseline_core_minimal_plus_ph_alkalinity`

二者在真正第二层 `facility-month` 上是否形成稳定且值得保留的机制支撑证据。

## 2. 必须沿用的前序制度

`V5.2` 必须完整沿用以下 `V5.1` 冻结结果：

- 正式任务：`tthm_high_risk_month_prediction`
- 正式标签：`is_tthm_high_risk_month`
- 标签定义：`tthm_mean_ug_l >= 80 ug/L`
- 正式主切分：`group_by_pwsid`
- 随机控制：`random_seed = 42`
- 切分版本：`v001`
- 正式 baseline：`baseline_core_minimal`

本轮不得：

- 重定义标签
- 重建切分
- 改写 baseline 字段
- 以第三层 `PWS-year` 第二级样本结论替代真正第二层判断

## 3. 正式样本口径

本轮正式实验的母集固定为：

- `tthm_mean_ug_l` 非缺失的 `facility-month` 记录

`V5.2 stage1` 完整子样本固定为同时满足以下条件的记录：

- `tthm_mean_ug_l` 非缺失
- `month` 非缺失
- `state_code` 非缺失
- `system_type` 非缺失
- `source_water_type` 非缺失
- `retail_population_served` 非缺失
- `adjusted_total_population_served` 非缺失
- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失

该子样本总规模为：

- `2,638` 行

切分后固定为：

- train：`2,073` 行，正例 `131`
- validation：`362` 行，正例 `14`
- test：`203` 行，正例 `19`

必须明确：

- `baseline_core_minimal_stage1_reference` 与 `baseline_core_minimal_plus_ph_alkalinity` 使用完全同一批样本
- 本轮默认不引入 missing flags
- 不把 `TOC`、`free_chlorine`、`total_chlorine` 带入本轮正式主链

## 4. 正式特征制度

### 4.1 同子样本 baseline 对照

`baseline_core_minimal_stage1_reference` 固定字段为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`

### 4.2 正式增强版本

`baseline_core_minimal_plus_ph_alkalinity` 固定字段为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `ph_mean`
- `alkalinity_mean_mg_l`

本轮不加入：

- `ph_missing_flag`
- `alkalinity_missing_flag`
- `TOC`
- 任意氯残留字段

原因是：

- `V5.2` 目标是先检验第二层最短机制增强链
- 在 complete-case 子样本上，额外 missing flags 不是维持口径一致的必要条件
- 默认应保持特征制度最小化，避免把解释边界再次混宽

## 5. 模型与实现制度

本轮模型固定为：

- `LogisticRegression(class_weight="balanced", max_iter=4000, random_state=42, solver="lbfgs")`

预处理固定为：

- 数值变量：中位数填补 + 标准化
- 类别变量：众数填补 + one-hot 编码

但由于本轮样本已经是 strict complete-case：

- 实际不会发生 `ph_mean` 与 `alkalinity_mean_mg_l` 的缺失填补
- baseline 对照与增强版只在是否纳入两个水质数值字段上不同

## 6. 正式输出制度

本轮新增脚本固定为：

- `scripts/train_v5_2_facility_month_mechanistic_core_stage1.py`

本轮核心本地输出固定为：

- `v5_2_mechanistic_core_stage1_experiment_results.csv`
- `v5_2_mechanistic_core_stage1_feature_sets.csv`
- `v5_2_mechanistic_core_stage1_metric_comparison.csv`
- `v5_2_mechanistic_core_stage1_sample_summary.csv`

本轮中文文档输出固定为：

- `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Protocol.md`
- `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Execution_Report.md`
- `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Result_Summary.md`

## 7. 本轮协议判断边界

本轮必须回答，但不得越界：

1. `baseline_core_minimal + pH + alkalinity` 是否相对同子样本 baseline 形成增益
2. 该增益在 `validation` 与 `test` 上是否方向一致
3. 第二层当前是否已具备保留“机制支撑线”的第一轮正式证据
4. `TOC` 是否还值得保留为后续专题分支

本轮不得直接写成：

- 第二层已经形成成熟高信息宽表模型
- `pH + alkalinity` 已被证明是因果机制
- `V5.3 TOC` 必然是默认下一步

## 8. 本轮协议结论

`V5.2` 的正式任务不是扩变量，而是在真正第二层 `facility-month` 上，用与 `V5.1` 完全一致的制度，干净地比较：

- 同子样本 baseline reference
- `baseline + pH + alkalinity`

并据此判断第二层“机制支撑线”是否具备继续保留的最低正式证据。
