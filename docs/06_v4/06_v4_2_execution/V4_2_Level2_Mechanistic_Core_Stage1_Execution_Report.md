# V4.2 Level2 Mechanistic Core Stage1 执行报告

- 更新时间：2026-04-02 22:46（Asia/Hong_Kong）
- 对应阶段：`V4.2`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`

## 1. 本轮任务定位

本轮执行的是 `V4.2` 下的两项正式更新：

- `V4.2.1`：在 `第二级样本` 上执行 `baseline + pH + alkalinity + missing flags`
- `V4.2.2`：在 `第二级样本` 中仅保留 `pH` 与 `alkalinity` 同时非缺失的完整子集，重复对应稳健性实验

本轮仍只围绕第三层 `PWS-year` 主表展开，不引入第二层 `facility-month` 字段，不切换树模型，不进行超参数优化，也不保存模型文件。

## 2. 样本、特征与缺失处理

### 2.1 正式任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

### 2.2 样本层级

- `V4.2.1` 固定使用 `第二级样本`
- `V4.2.2` 仍以 `第二级样本` 为母集，但仅保留 `ph_sample_weighted_mean` 与 `alkalinity_sample_weighted_mean_mg_l` 同时非缺失的记录

`第二级样本` 总样本数为 `26,975`。其中：

- `pH` 缺失行数：`10,047`
- `alkalinity` 缺失行数：`1,529`
- `pH / alkalinity` 任一缺失行数：`11,503`
- `pH + alkalinity` 完整子集行数：`15,472`
- 完整子集占 `第二级样本` 比例：`57.36%`

### 2.3 特征制度

第一组对照特征：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

`V4.2.1` / `V4.2.2` 的增强特征：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

因此本轮正式增强版 `X` 为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`
- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

### 2.4 缺失处理规则

- `V4.2.1`：保留 `第二级样本` 样本，不做 complete-case；数值变量走中位数填补，保留 `pH` 与 `alkalinity` 的 missing flag
- `V4.2.2`：先筛出 `pH + alkalinity` 完整子集，再跑同一组增强特征；此时 missing flag 理论上退化为常量列，仅保留为口径一致
- `V4.2.2b`：在与 `V4.2.2` 完全相同的 complete-case 子集上，显式删除 `ph_missing_flag` 与 `alkalinity_missing_flag`，用于验证常量列是否会影响结果

### 2.5 为解释增益而增加的对照

为了区分“新增变量本身的价值”和“样本筛选/缺失模式带来的表面提升”，本轮额外补了两个解释性对照版本：

- `level2_baseline_reference`
- `level2_complete_case_baseline_reference`

此外，本轮还补了一个纯实现层面的敏感性检查：

- `mechanistic_stage1_complete_case_no_missing_flags`

这两个对照不是新的主实验结论来源，但它们是判断 `V4.2` 提升来源所必需的参照。

## 3. 结果总览

### 3.1 `tthm_regulatory_exceedance_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Test PR-AUC | Test ROC-AUC |
| --- | --- | ---: | ---: | ---: | ---: |
| `V4.1 baseline` | `第一级样本 + baseline_default` | 0.0696 | 0.7218 | 0.0690 | 0.7046 |
| `第二级样本 baseline reference` | `第二级样本 + baseline_default` | 0.0652 | 0.7212 | 0.1039 | 0.7395 |
| `V4.2.1` | `第二级样本 + mechanistic_stage1` | 0.0775 | 0.7586 | 0.1941 | 0.7986 |
| `第二级样本 complete-case baseline reference` | `第二级样本 complete-case + baseline_default` | 0.0815 | 0.7213 | 0.1115 | 0.7452 |
| `V4.2.2` | `第二级样本 complete-case + mechanistic_stage1` | 0.1298 | 0.7902 | 0.1781 | 0.8221 |
| `V4.2.2b` | `第二级样本 complete-case + mechanistic_stage1 without missing flags` | 0.1298 | 0.7902 | 0.1781 | 0.8221 |

关键信息：

- `V4.2.1` 相对 `第二级样本 baseline reference` 的测试集增益为：`PR-AUC +0.0902`、`ROC-AUC +0.0591`
- `V4.2.2` 相对 `第二级样本 complete-case baseline reference` 的测试集增益为：`PR-AUC +0.0666`、`ROC-AUC +0.0769`
- `V4.2.2b` 与 `V4.2.2` 的 validation / test 指标完全一致，说明 complete-case 子集中的两个 missing flag 确实只是常量列，不会改变当前逻辑回归结果
- `V4.2.1` 相对 `V4.1 baseline` 的测试集增益为：`PR-AUC +0.1252`、`ROC-AUC +0.0940`

### 3.2 `tthm_anchored_risk_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Test PR-AUC | Test ROC-AUC |
| --- | --- | ---: | ---: | ---: | ---: |
| `V4.1 baseline` | `第一级样本 + baseline_default` | 0.1216 | 0.7642 | 0.1162 | 0.7452 |
| `第二级样本 baseline reference` | `第二级样本 + baseline_default` | 0.1208 | 0.7681 | 0.1858 | 0.7816 |
| `V4.2.1` | `第二级样本 + mechanistic_stage1` | 0.1416 | 0.8112 | 0.3061 | 0.8412 |
| `第二级样本 complete-case baseline reference` | `第二级样本 complete-case + baseline_default` | 0.0950 | 0.7362 | 0.1854 | 0.7744 |
| `V4.2.2` | `第二级样本 complete-case + mechanistic_stage1` | 0.1660 | 0.8275 | 0.2830 | 0.8716 |
| `V4.2.2b` | `第二级样本 complete-case + mechanistic_stage1 without missing flags` | 0.1660 | 0.8275 | 0.2830 | 0.8716 |

关键信息：

- `V4.2.1` 相对 `第二级样本 baseline reference` 的测试集增益为：`PR-AUC +0.1203`、`ROC-AUC +0.0596`
- `V4.2.2` 相对 `第二级样本 complete-case baseline reference` 的测试集增益为：`PR-AUC +0.0975`、`ROC-AUC +0.0972`
- `V4.2.2b` 与 `V4.2.2` 的 validation / test 指标完全一致，说明 complete-case anchored 子集里的两个 missing flag 也是纯冗余列
- `V4.2.1` 相对 `V4.1 baseline` 的测试集增益为：`PR-AUC +0.1899`、`ROC-AUC +0.0960`

## 4. 本轮结论

### 4.1 `V4.2.1` 是否带来稳定提升

是。

两条正式任务线上，`V4.2.1` 都同时优于：

- `V4.1 baseline`
- 对应的 `第二级样本 baseline reference`

这说明把 `pH + alkalinity + missing flags` 纳入 `第二级样本` 后，提升不是单一指标上的偶然波动，而是 `PR-AUC` 与 `ROC-AUC` 都出现了同向改善。

### 4.2 提升主要体现在哪条任务线上

当前提升更明显地体现在 `tthm_anchored_risk_prediction` 上。

从测试集看：

- `anchored` 的 `V4.2.1` 相对 `第二级样本 baseline reference` 提升到 `PR-AUC 0.3061`
- `regulatory` 的 `V4.2.1` 相对 `第二级样本 baseline reference` 提升到 `PR-AUC 0.1941`

这表明 `pH` 与总碱度对于区分“高端样本 vs 低端锚点样本”的帮助，比对单纯法规超标边界的帮助更强。

### 4.3 `V4.2.2` 是否与 `V4.2.1` 同方向

是。

`V4.2.2` 在两条任务线上都继续优于各自的 complete-case baseline 对照：

- `regulatory`：`PR-AUC 0.1115 -> 0.1781`
- `anchored`：`PR-AUC 0.1854 -> 0.2830`

因此，`V4.2.1` 的提升不能简单归因为“保留了缺失模式以后模型更容易猜中”。

### 4.4 当前增益更像来自什么

当前证据更支持：

- `pH` 与 `alkalinity` 的真实数值信号是主要来源
- 缺失模式可能提供了附加信息
- 但不能把这轮结果直接写成明确机制发现

理由是：

- 如果增益主要来自 missing pattern，那么在 `V4.2.2` complete-case 子集上，对照增益应明显消失
- 但当前 `V4.2.2` 相对 complete-case baseline 仍保留显著提升
- 同时 `V4.2.1` 与 `V4.2.2` 的结果方向一致，说明信号并不依赖单一缺失处理路径

更稳妥的表述是：本轮结果说明 `pH` 与总碱度在 `第二级样本` 样本内具有可复现的预测增益，但仍属于预测层面的机制增强证据，而不是因果机制结论。

### 4.5 `V4.2.2` 中是否应删除 missing flag

从当前补充实验看，答案是：

- 对当前 `LogisticRegression + complete-case` 实现而言，可以删除
- 但保留在正式 `V4.2.2` 记录中也没有造成数值偏差

原因是：

- 在 complete-case 子集内，`ph_missing_flag` 与 `alkalinity_missing_flag` 对所有行都等于 `0`
- 新增的 `V4.2.2b` 在两条任务线上都与 `V4.2.2` 完全同分
- 这说明保留这两列的唯一作用是与 `V4.2.1` 保持特征口径一致，而不是改变模型行为

因此，后续文档解释可以明确写成：

- `V4.2.2` 正式版保留 missing flag 是为了与 `V4.2.1` 保持协议一致
- `V4.2.2b` 证明删除这两个常量列后结果不变
- 所以 `V4.2.2` 的提升可以视为来自 `pH` 与总碱度真实数值信号，而不是来自 complete-case 子集中的 missing flag

## 5. 本轮产物

### 5.1 新增脚本

- `scripts/train_v4_tthm_regulatory_l2_mechanistic_stage1.py`
- `scripts/train_v4_tthm_anchored_l2_mechanistic_stage1.py`
- `scripts/v4_tthm_training_common.py` 已扩展为支持任意特征组、`第二级样本` 样本和 complete-case 对照

### 5.2 本地结果文件

- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_baseline_reference_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_mechanistic_stage1_v4_2_1_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_complete_case_baseline_reference_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_mechanistic_stage1_complete_case_v4_2_2_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_mechanistic_stage1_complete_case_no_missing_flags_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/level2_mechanistic_stage1_experiment_summary.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_baseline_reference_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_mechanistic_stage1_v4_2_1_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_complete_case_baseline_reference_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_mechanistic_stage1_complete_case_v4_2_2_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_mechanistic_stage1_complete_case_no_missing_flags_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/level2_mechanistic_stage1_experiment_summary.csv`

## 6. 对下一步 `V4.3` 的建议

下一步可以进入 `TOC` 增量实验，但建议继续保持当前做法：

- 仍以 `第二级样本` 为主实验层
- 先保留 `V4.2.1` 的 `pH + alkalinity + missing flags` 作为固定底座
- 新增 `TOC` 与 `toc_missing_flag`
- 继续保留 baseline 对照和 complete-case 对照，避免把样本筛选效应误写成变量增益

在进入 `free_chlorine` 之前，优先把 `TOC` 的边际增益与口径稳定性先跑清楚。
