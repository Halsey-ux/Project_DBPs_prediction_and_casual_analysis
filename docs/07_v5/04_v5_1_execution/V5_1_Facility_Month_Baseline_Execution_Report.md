# V5.1 Facility-Month Baseline 执行报告

- 更新时间：2026-04-08 21:11（Asia/Hong_Kong）
- 对应阶段：`V5.1`
- 输入主表：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 本地结果目录：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/`

## 1. 本轮执行目标

本轮不是扩变量实验，而是正式冻结第二层 `facility-month` 的 baseline 制度。  
本轮需要回答的核心问题是：

1. 第二层正式 baseline 到底采用哪些字段
2. `has_treatment_summary` 是否进入正式 baseline
3. `water_facility_type` 是否进入正式 baseline
4. 正式切分到底按 `pwsid` 还是按 `pwsid + water_facility_id`
5. `V5.2` 应该基于什么 baseline reference 做对照

## 2. 正式任务与切分

### 2.1 正式任务

正式任务固定为：

- `tthm_high_risk_month_prediction`

正式标签固定为：

- `is_tthm_high_risk_month = 1{tthm_mean_ug_l >= 80 ug/L}`

### 2.2 切分比较

本轮比较了两种候选切分：

1. `group_by_pwsid`
2. `group_by_pwsid + water_facility_id`

正式结论为：

- 采用 `group_by_pwsid`

原因不是因为它分数更高，而是因为它更严格地避免系统级泄漏。  
`group_by_pwsid + water_facility_id` 虽然可以阻断同一设施跨月份泄漏，但同一系统的不同设施仍可能分散到不同集合。

### 2.3 正式切分样本量

#### 正式目标样本池

| split | rows | positive_rows | positive_rate | groups |
| --- | ---: | ---: | ---: | ---: |
| train | 384,477 | 24,363 | 0.0634 | 27,451 |
| validation | 80,363 | 5,124 | 0.0638 | 5,882 |
| test | 84,890 | 5,581 | 0.0657 | 5,883 |

#### `V5.2` 同子样本 baseline reference 池

| split | rows | positive_rows | positive_rate |
| --- | ---: | ---: | ---: |
| train | 1,942 | 117 | 0.0602 |
| validation | 365 | 19 | 0.0521 |
| test | 331 | 28 | 0.0846 |

## 3. baseline 字段对照结果

### 3.1 三个 baseline 版本

| feature_set | train_rows | validation_rows | test_rows | validation PR-AUC | test PR-AUC | validation ROC-AUC | test ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_core_minimal` | 386,102 | 84,875 | 78,669 | 0.1924 | 0.1696 | 0.7418 | 0.7305 |
| `baseline_core_with_has_treatment_summary` | 386,102 | 84,875 | 78,669 | 0.1929 | 0.1696 | 0.7426 | 0.7301 |
| `baseline_core_plus_water_facility_type` | 256,492 | 53,230 | 53,029 | 0.2323 | 0.1990 | 0.7605 | 0.7480 |

### 3.2 对 `has_treatment_summary` 的判断

`has_treatment_summary` 与最小 baseline 使用相同样本规模，因此它的比较是直接可比的。

相对 `baseline_core_minimal`：

- validation `PR-AUC` 仅增加 `+0.00056`
- test `PR-AUC` 反而减少 `-0.00008`
- test `ROC-AUC` 也没有形成稳定提升

因此本轮正式判断为：

- `has_treatment_summary` 不进入第一版正式 baseline

理由是：

1. 没有形成稳定的 out-of-sample 增益
2. 它本质上更接近记录可用性代理，而不是结构环境变量
3. `V5.1` 的目标是先冻结一个解释边界更干净的 baseline，而不是吸收所有可能的制度代理特征

### 3.3 对 `water_facility_type` 的判断

`water_facility_type` 在 strict complete-case 子集上确实表现出更高分数，但必须同时看到它带来的样本收缩：

- test `PR-AUC` 相对最小 baseline 提升 `+0.02934`
- 但 test 行数从 `78,669` 降到 `53,029`
- 只保留了最小 baseline test 样本的约 `67.41%`

对应到总样本口径：

- `TTHM` complete-case 从 `549,646` 行下降到 `362,751` 行

因此本轮正式判断为：

- `water_facility_type` 不进入第一版正式 baseline

理由不是“它没有预测价值”，而是：

1. 它的收益建立在明显更窄的样本覆盖上
2. `V5.1` 当前优先级是建立广覆盖、制度稳定、可复现的 baseline
3. 它更适合保留为条件性 baseline 或后续专题对照项

### 3.4 对 detailed treatment flags 的判断

本轮不把以下字段带入正式 baseline：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

依据 `V5.0` 审计：

- 它们的 strict complete-case 规模只有 `2,699` 行
- 只占全部 `TTHM` 月样本约 `0.49%`

因此它们不具备成为第一版正式 baseline 的样本基础。

## 4. 最终冻结结果

第二层 `V5.1` 最终冻结的正式 baseline 为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`

这组字段的正式命名固定为：

- `baseline_core_minimal`

## 5. `V5.2` 对照 reference

为了给 `V5.2 baseline + pH + alkalinity` 提供干净对照，本轮同时运行了：

- `baseline_core_minimal_stage1_reference`

它只使用最终正式 baseline 特征，但样本限制在：

- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失

该 reference 的结果为：

| split | rows | positive_rows |
| --- | ---: | ---: |
| train | 2,073 | 131 |
| validation | 362 | 14 |
| test | 203 | 19 |

对应主要指标：

- validation `PR-AUC`：`0.0935`
- test `PR-AUC`：`0.3643`
- validation `ROC-AUC`：`0.6805`
- test `ROC-AUC`：`0.7765`

因此 `V5.2` 可以在完全相同的切分、完全相同的子样本上，直接比较：

- `baseline_core_minimal_stage1_reference`
- `baseline_core_minimal + pH + alkalinity`

## 6. 本轮结论

1. 第二层第一版正式 baseline 已经可以冻结下来，样本覆盖稳定，不需要再回到 `V5.0` 重新审计。
2. `has_treatment_summary` 不进入正式 baseline，因为它没有形成稳定外推增益，而且会把记录可用性代理混入正式底座。
3. `water_facility_type` 不进入正式 baseline，因为它建立在明显收缩的 complete-case 子集上，更适合保留为条件性对照。
4. detailed treatment flags 全部排除在第一版正式 baseline 外。
5. 第二层正式主切分必须固定为 `group_by_pwsid`。
6. `V5.2` 现在可以在同子样本上继续测试 `baseline + pH + alkalinity`，不需要再额外补制度。
