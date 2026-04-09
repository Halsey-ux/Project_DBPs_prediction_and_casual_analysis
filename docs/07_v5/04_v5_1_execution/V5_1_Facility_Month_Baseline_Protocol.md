# V5.1 Facility-Month Baseline 协议

- 更新时间：2026-04-08 21:11（Asia/Hong_Kong）
- 对应阶段：`V5.1`
- 输入主表：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 本地结果目录：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/`

## 1. 文档定位

本协议用于正式冻结第二层 `facility-month` 的第一版 baseline 制度，固定以下内容：

- 正式任务与标签口径
- 正式样本口径
- 正式切分制度
- 正式 baseline 字段集
- 条件性 baseline 对照字段
- 为 `V5.2 baseline + pH + alkalinity` 预留的同子样本 baseline reference

本协议不是增强变量实验文档，也不是树模型或调参文档。

## 2. 正式任务定义

`V5.1` 的正式任务固定为：

- `tthm_high_risk_month_prediction`

正式标签固定为：

- `is_tthm_high_risk_month`

其定义为：

- 当 `tthm_mean_ug_l >= 80 ug/L` 时取 `1`
- 当 `tthm_mean_ug_l < 80 ug/L` 时取 `0`

解释边界：

- 这是第二层 `facility-month` 的月度高风险识别任务
- 它与第三层 `pws-year` 的 `tthm_regulatory_exceed_label` 共享同一个 `80 ug/L` 风险边界
- 但二者不是同一任务对象
- 第二层预测的是“设施-月份是否达到高风险月”
- 第三层预测的是“系统-年份是否达到年度超标状态”

## 3. 正式样本口径

`V5.1` 正式样本池固定为：

- `tthm_mean_ug_l` 非缺失的 `facility-month` 记录

正式 baseline 采用严格 complete-case 口径：

- 只保留正式 baseline 特征全部非缺失的记录

本轮最终正式 baseline 的 complete-case 规模为：

- `549,646` 行

这相当于全部 `TTHM` 月样本 `549,730` 行中的 `99.98%`，说明第二层 baseline 样本覆盖稳定，可以作为正式起点。

## 4. 字段制度

### 4.1 正式 baseline 字段

第二层 `V5.1` 最终冻结的正式 baseline 字段集为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`

这组字段构成“最小稳定结构 baseline”，原因是：

- 覆盖率最高
- 解释边界最清楚
- 不直接混入明显的记录可用性代理
- 可以为 `V5.2` 提供更干净的对照底座

### 4.2 条件性对照字段

以下字段保留为条件性 baseline 对照，不进入第一版正式 baseline：

| 字段 | `V5.1` 决定 | 理由 |
| --- | --- | --- |
| `has_treatment_summary` | 不进入正式 baseline | 与最小 baseline 相比没有形成稳定的 out-of-sample 增益，而且它本质上是记录可用性指示字段。 |
| `water_facility_type` | 不进入正式 baseline | 虽然在收缩样本后分数更高，但 strict complete-case 样本只剩 `362,751` 行，不能作为第一版正式 baseline。 |

### 4.3 暂停字段

以下字段全部排除在正式 baseline 外：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

原因是：

- 它们的 `TTHM` complete-case 行数只有 `2,699`
- 只占全部 `TTHM` 月样本的约 `0.49%`
- 它们更适合保留为后续专题变量，而不是第一版正式 baseline

同时必须明确：

- detailed treatment flags 不得因缺失而被强行改写为 `0`
- `has_treatment_summary` 只能解释为“treatment 摘要记录是否可用”，不能误写为环境机制变量

## 5. 正式切分制度

`V5.1` 正式主切分固定为：

- `group_by_pwsid`

切分比例固定为：

- train：`70%`
- validation：`15%`
- test：`15%`

随机控制固定为：

- `random_seed = 42`
- `split_version = v001`

不采用 `group_by_pwsid + water_facility_id` 作为正式主切分的原因是：

- 它只能阻断同一设施跨月份泄漏
- 但仍允许同一系统的不同设施分散到不同集合
- 第二层 baseline 包含系统级结构信息，若同一 `pwsid` 被拆开，会引入系统级泄漏风险

因此本轮正式切分必须使用更严格的：

- 同一 `pwsid` 下所有设施、所有月份整体进入同一集合

## 6. 正式对照链

`V5.1` 至少保留以下四个对照版本：

1. `baseline_core_minimal`
2. `baseline_core_with_has_treatment_summary`
3. `baseline_core_plus_water_facility_type`
4. `baseline_core_minimal_stage1_reference`

其中：

- 前三项用于决定正式 baseline 字段制度
- 第四项只用于给 `V5.2 baseline + pH + alkalinity` 提供同子样本 baseline reference

`baseline_core_minimal_stage1_reference` 的额外样本限制是：

- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失

## 7. 输出制度

本轮新增脚本固定为：

- `scripts/io_v5_facility_month.py`
- `scripts/build_v5_1_facility_month_splits.py`
- `scripts/v5_facility_month_training_common.py`
- `scripts/train_v5_1_facility_month_baseline.py`

本轮核心本地输出固定为：

- `v5_1_group_by_pwsid_master_split.csv`
- `v5_1_tthm_high_risk_month_split_index.csv`
- `v5_1_split_strategy_comparison.csv`
- `v5_1_baseline_feature_sets.csv`
- `v5_1_baseline_experiment_results.csv`

## 8. 本轮协议结论

`V5.1` 的核心不是继续扩变量，而是把真正第二层的第一版制度冻结下来。  
本轮正式冻结结果为：

- 正式任务：`tthm_high_risk_month_prediction`
- 正式标签：`is_tthm_high_risk_month`
- 正式切分：`group_by_pwsid`
- 正式 baseline：`month + state_code + system_type + source_water_type + retail_population_served + adjusted_total_population_served`
- `has_treatment_summary` 仅保留为条件性对照字段
- `water_facility_type` 仅保留为条件性对照字段
- detailed treatment flags 全部排除在正式 baseline 外
- `V5.2` 必须沿用本轮固定的标签、切分与 baseline reference 制度
