# V5.2 Facility-Month Mechanistic Core Stage1 执行报告

- 更新时间：2026-04-09 09:45（Asia/Hong_Kong）
- 对应阶段：`V5.2`
- 输入主表：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 复用切分：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_1/v5_1_group_by_pwsid_master_split.csv`
- 本地结果目录：`data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/`

## 1. 本轮执行目标

本轮不是继续扩展第二层变量链，而是在真正第二层 `facility-month` 上正式检验最短机制增强链：

- `baseline_core_minimal_stage1_reference`
- `baseline_core_minimal_plus_ph_alkalinity`

本轮要回答的核心问题是：

1. `pH + alkalinity` 相对同子样本 baseline 是否形成增益
2. 该增益在 `validation` 与 `test` 上是否方向一致
3. 当前证据是否足以支持继续保留第二层“机制支撑线”
4. `TOC` 是否还能保留为后续专题分支，而不是默认主链下一步

## 2. 样本、特征与制度对齐

### 2.1 正式任务

- `tthm_high_risk_month_prediction`
- `is_tthm_high_risk_month = 1{tthm_mean_ug_l >= 80 ug/L}`

### 2.2 同子样本 complete-case 口径

本轮严格使用与 `V5.1 stage1 reference` 完全一致的 complete-case 子样本：

- `tthm_mean_ug_l` 非缺失
- 正式 baseline 字段全部非缺失
- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失

样本规模为：

| split | rows | positive_rows | positive_rate |
| --- | ---: | ---: | ---: |
| train | 2,073 | 131 | 0.0632 |
| validation | 362 | 14 | 0.0387 |
| test | 203 | 19 | 0.0936 |

这与 `V5.1 baseline_core_minimal_stage1_reference` 完全一致，说明：

- 本轮制度对齐成功
- 本轮比较没有混入额外样本漂移

### 2.3 特征制度

同子样本 baseline 对照：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`

正式增强版本：

- 上述 6 个 baseline 字段
- `ph_mean`
- `alkalinity_mean_mg_l`

本轮未加入 missing flags，原因是：

- prompt 明确要求默认不自动扩字段
- 本轮已经是 strict complete-case 子样本
- 当前最重要的是先判断两个机制核心数值字段本身是否值得保留

## 3. 结果总览

### 3.1 两个正式版本的 train / validation / test 结果

| feature_set | split | rows | positive_rows | PR-AUC | ROC-AUC | balanced_accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `baseline_core_minimal_stage1_reference` | train | 2,073 | 131 | 0.2506 | 0.8532 | 0.7887 |
| `baseline_core_minimal_stage1_reference` | validation | 362 | 14 | 0.0935 | 0.6805 | 0.6775 |
| `baseline_core_minimal_stage1_reference` | test | 203 | 19 | 0.3643 | 0.7765 | 0.7271 |
| `baseline_core_minimal_plus_ph_alkalinity` | train | 2,073 | 131 | 0.2815 | 0.8637 | 0.7952 |
| `baseline_core_minimal_plus_ph_alkalinity` | validation | 362 | 14 | 0.0865 | 0.6819 | 0.6821 |
| `baseline_core_minimal_plus_ph_alkalinity` | test | 203 | 19 | 0.3937 | 0.7979 | 0.7361 |

### 3.2 相对同子样本 baseline 的增量

| split | 指标 | baseline reference | `+ pH + alkalinity` | delta |
| --- | --- | ---: | ---: | ---: |
| validation | PR-AUC | 0.0935 | 0.0865 | -0.0070 |
| validation | ROC-AUC | 0.6805 | 0.6819 | +0.0013 |
| validation | balanced_accuracy | 0.6775 | 0.6821 | +0.0045 |
| test | PR-AUC | 0.3643 | 0.3937 | +0.0294 |
| test | ROC-AUC | 0.7765 | 0.7979 | +0.0215 |
| test | balanced_accuracy | 0.7271 | 0.7361 | +0.0090 |

## 4. 结果解释

### 4.1 `PR-AUC` 是否在 validation 与 test 上都改善

否。

结果为：

- validation：`0.0935 -> 0.0865`
- test：`0.3643 -> 0.3937`

这说明按 prompt 中最严格的“稳定增益”标准看：

- `PR-AUC` 还没有形成 validation 与 test 同向改善

### 4.2 `ROC-AUC` 是否在 validation 与 test 上都改善

是。

结果为：

- validation：`0.6805 -> 0.6819`
- test：`0.7765 -> 0.7979`

但也必须看到：

- validation 端提升幅度非常小
- 当前证据更像“轻微正向”而不是“强稳定提升”

### 4.3 `balanced_accuracy` 是否方向一致

是。

结果为：

- validation：`0.6775 -> 0.6821`
- test：`0.7271 -> 0.7361`

这说明加入 `pH + alkalinity` 后，模型在 0.5 阈值下的整体判别平衡性略有改善。

### 4.4 指标不完全一致时应如何解释

当前最合理的解释是：

1. `pH + alkalinity` 带来的信号更偏向提高排序与阈值判别的整体区分度，但尚未稳定转化为 `PR-AUC` 的双集合同向提升。
2. 模型在 validation 与 test 上都表现出更高的 `specificity` 与 `precision`，但 `recall` 有所下降，说明增强版更保守。
3. 在 validation 集中，正例只有 `14` 个；test 集中，正例只有 `19` 个。`PR-AUC` 在这种小正例样本下波动会明显放大。

更具体地看：

- validation：`tp 10 -> 9`，`fp 125 -> 97`
- test：`tp 14 -> 13`，`fp 52 -> 39`

也就是说，增强版主要是：

- 显著减少误报
- 同时略微减少召回

因此它更像是“更谨慎的风险识别器”，而不是在所有目标函数上都无条件变强。

### 4.5 `pH + alkalinity` 是否形成稳定增益

当前结论是：

- 形成了有限、偏正向的增益信号
- 但尚未形成可以直接写成“稳定成立”的强证据

原因是：

- `test` 上三项核心指标都改善
- `validation` 上 `ROC-AUC` 与 `balanced_accuracy` 改善
- 但 `validation PR-AUC` 未同步改善

所以本轮最稳妥的表述应是：

- 第二层 `baseline + pH + alkalinity` 已出现第一轮正式正向信号
- 但这个信号仍然受极小 complete-case 子样本限制
- 它支持“保留机制支撑线”，但不足以支持“第二层增强链已稳定成熟”

## 5. 对第二层角色定位的影响

### 5.1 第二层是否具备继续保留“机制支撑线”的第一轮正式证据

具备，但证据等级应表述为：

- 有限的、弱正向的第一轮正式证据

不能表述为：

- 已经形成稳定成熟的第二层正式增强主链

### 5.2 是否可以直接进入 `TOC`

当前不应把 `TOC` 写成默认下一步。

更稳妥的判断是：

- `TOC` 仍可保留为第二层 reduced dataset 专题候选
- 但前提是明确接受极强样本收缩，并重新做专题化边界设计
- 在 `V5.2` 只有弱正向证据的前提下，不宜直接把 `V5.3` 写成线性主链延续

## 6. 本轮产物

### 6.1 新增脚本

- `scripts/train_v5_2_facility_month_mechanistic_core_stage1.py`

### 6.2 本地结果文件

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/v5_2_mechanistic_core_stage1_experiment_results.csv`
- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/v5_2_mechanistic_core_stage1_feature_sets.csv`
- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/v5_2_mechanistic_core_stage1_metric_comparison.csv`
- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/v5_2_mechanistic_core_stage1_sample_summary.csv`

## 7. 本轮结论

1. `V5.2` 已严格在真正第二层 `facility-month` 上完成，且制度与 `V5.1` 完全对齐。
2. `baseline_core_minimal_plus_ph_alkalinity` 与 `baseline_core_minimal_stage1_reference` 使用完全同一批样本，比较成立。
3. `test` 上 `PR-AUC`、`ROC-AUC` 与 `balanced_accuracy` 均改善，说明第二层最短机制增强链并非完全无效。
4. 但 `validation PR-AUC` 没有同步改善，因此当前还不能把这条链写成“稳定成立”。
5. 第二层当前可以继续保留“机制支撑线”，但应明确为受限、弱正向、需收敛解释边界的正式证据。
6. `TOC` 仍可保留为专题分支候选，但不应再被默认写成主链下一步。
