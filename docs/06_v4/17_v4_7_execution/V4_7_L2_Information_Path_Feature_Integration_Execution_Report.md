# V4.7 L2 Information Path Feature Integration 执行报告

- 更新时间：2026-04-03 19:23（Asia/Hong_Kong）
- 对应阶段：`V4.7`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_7/tthm_regulatory_exceedance_prediction/`
  - `data_local/V4_Chapter1_Part1_Experiments/V4_7/tthm_anchored_risk_prediction/`

## 1. 本轮任务定义

本轮执行的是 `V4.7 第二级样本 information path feature integration`。核心目的不是改写当前第三层 `第一级样本` 正式主模型，而是在第二层高信息样本 `第二级样本` 中，把两条已形成阶段性证据的信息通路放入同一套对照链中，回答以下问题：

- 水质特征通路相对 baseline 是否已经形成稳定增益
- 系统背景通路相对 baseline 是否仍然强势
- 两条信息通路合并后是否继续优于单通路版本
- 当系统背景通路已经进入模型后，`pH + alkalinity + TOC` 是否仍保留独立价值
- 当水质特征通路已经进入模型后，`structural + treatment` 是否仍提供附加价值

## 2. 为什么固定在 `第二级样本`

- `pH + alkalinity + TOC` 的主要证据基础本来就来自 `第二级样本`
- `第二级样本` 是当前项目定义的高信息样本层，更适合比较信息通路之间的互补与重叠
- `V4.7` 的角色是高信息样本中的探索性整合实验，不是重新争夺第三层全国正式主线

## 3. 两条信息通路与对照链定义

### 3.1 系统背景通路

当前定义为：

- `baseline + structural + treatment`

其中：

- `baseline`：`system_type`、`source_water_type`、`retail_population_served`、`n_facilities_in_master`
- `structural`：`months_observed_any`、`tthm_months_with_data`、`months_with_1plus_core_vars`、`months_with_2plus_core_vars`、`months_with_3plus_core_vars`、`n_core_vars_available`、`annual_match_quality_tier`
- `treatment`：`has_*_process` 六个 treatment summary 字段

### 3.2 水质特征通路

当前定义为：

- `baseline + pH + alkalinity + TOC`

具体字段为：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_missing_flag`

### 3.3 本轮实际运行版本

每条任务共运行 6 个 `第二级样本` 版本：

1. `baseline_default_reference`
2. `water_quality_reference_v4_7_1`
3. `system_background_reference_v4_7_1`
4. `structural_and_water_quality_v4_7_1`
5. `treatment_and_water_quality_v4_7_1`
6. `full_integration_v4_7_1`

其中前 4 项中的前 3 个单通路版本加 `full_integration` 构成主对照链；后 2 个版本用于拆分 `structural` 与 `treatment` 在合并模型中的相对作用。

## 4. 缺失处理方式

- 原始数据保持只读，不对主表做覆盖式改写
- `pH`、`alkalinity`、`TOC` 数值列在 pipeline 内使用中位数填补
- `ph_missing_flag`、`alkalinity_missing_flag`、`toc_missing_flag` 保留并进入模型
- `has_*_process` treatment 字段保留原始缺失，不把缺失覆盖成 `0`
- 类别变量沿用既有 one-hot 编码；全部实验继续复用既有 `group_by_pwsid` 切分

## 5. 样本规模

### 5.1 `tthm_regulatory_exceedance_prediction`

- train：`19,320`
- validation：`3,761`
- test：`3,894`

### 5.2 `tthm_anchored_risk_prediction`

- train：`12,589`
- validation：`2,399`
- test：`2,513`

## 6. 结果总览

### 6.1 `tthm_regulatory_exceedance_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.0652 | 0.7212 | 0.6641 | 0.1039 | 0.7395 | 0.6846 |
| `water_quality_reference_v4_7_1` | 0.1138 | 0.8020 | 0.7154 | 0.1877 | 0.8320 | 0.7642 |
| `system_background_reference_v4_7_1` | 0.0833 | 0.7801 | 0.7204 | 0.1783 | 0.8189 | 0.7560 |
| `structural_and_water_quality_v4_7_1` | 0.1209 | 0.8322 | 0.7690 | 0.2270 | 0.8527 | 0.7790 |
| `treatment_and_water_quality_v4_7_1` | 0.1270 | 0.7957 | 0.7326 | 0.2183 | 0.8374 | 0.7736 |
| `full_integration_v4_7_1` | 0.1345 | 0.8246 | 0.7494 | 0.2513 | 0.8567 | 0.7852 |

### 6.2 `tthm_anchored_risk_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.1208 | 0.7681 | 0.7380 | 0.1858 | 0.7816 | 0.7292 |
| `water_quality_reference_v4_7_1` | 0.2353 | 0.8537 | 0.7645 | 0.3588 | 0.8790 | 0.8183 |
| `system_background_reference_v4_7_1` | 0.1980 | 0.8464 | 0.7967 | 0.3591 | 0.8750 | 0.8059 |
| `structural_and_water_quality_v4_7_1` | 0.2564 | 0.8851 | 0.8194 | 0.4495 | 0.9023 | 0.8307 |
| `treatment_and_water_quality_v4_7_1` | 0.2649 | 0.8444 | 0.7851 | 0.4402 | 0.8839 | 0.8139 |
| `full_integration_v4_7_1` | 0.2875 | 0.8761 | 0.8125 | 0.5176 | 0.9076 | 0.8389 |

## 7. 关键判断

### 7.1 两条信息通路都明显强于 baseline

- 在 `regulatory` 中，水质特征通路相对 baseline 的 test `PR-AUC` 提升 `+0.0838`，系统背景通路提升 `+0.0744`
- 在 `anchored` 中，水质特征通路相对 baseline 的 test `PR-AUC` 提升 `+0.1730`，系统背景通路提升 `+0.1734`
- 这说明两条通路在 `第二级样本` 中都已形成稳定增强层，而不是只有一条通路有效

### 7.2 `full integration` 在两个任务上都继续优于单通路版本

- `regulatory` 中，`full integration` 的 test `PR-AUC=0.2513`，高于 `water_quality=0.1877` 与 `system_background=0.1783`
- `anchored` 中，`full integration` 的 test `PR-AUC=0.5176`，高于 `water_quality=0.3588` 与 `system_background=0.3591`
- 这说明两条信息通路在高信息样本中不是大部分重复，合并后仍能形成明显增益

### 7.3 水质特征通路在控制系统背景通路后仍保留独立价值

- `regulatory` 中，`full integration` 相对 `system_background` 的 test `PR-AUC` 再提升 `+0.0730`
- `anchored` 中，`full integration` 相对 `system_background` 的 test `PR-AUC` 再提升 `+0.1584`
- 因此 `pH + alkalinity + TOC` 不是被系统背景通路完全吸收掉的重复信息

### 7.4 系统背景通路在控制水质特征通路后也仍提供附加价值

- `regulatory` 中，`full integration` 相对 `water_quality` 的 test `PR-AUC` 再提升 `+0.0636`
- `anchored` 中，`full integration` 相对 `water_quality` 的 test `PR-AUC` 再提升 `+0.1588`
- 因此结构/coverage/treatment 也不是水质通路进入后就失去作用

### 7.5 `structural` 仍然比 `treatment` 更强，但 `treatment` 不是零贡献

- `regulatory` 中，`structural_and_water_quality` 的 test `PR-AUC=0.2270`，高于 `treatment_and_water_quality=0.2183`
- `anchored` 中，`structural_and_water_quality` 的 test `PR-AUC=0.4495`，也高于 `treatment_and_water_quality=0.4402`
- `full integration` 相对 `structural_and_water_quality` 仍继续上升，说明 `treatment` 还有剩余信息；但 `full integration` 相对 `treatment_and_water_quality` 的增幅更大，说明 `structural` 仍是更强的系统背景层

### 7.6 `V4.7` 不改写当前正式主模型定位

- `V4.7` 的证据来自 `第二级样本` 高信息样本，不应直接改写成全国正式主模型结论
- 当前更稳妥的写法是：`V4.7` 支持系统背景通路与水质特征通路在高信息样本中具有明显互补性
- 第三层 `第一级样本 baseline + structural + treatment` 仍然是当前全国尺度正式主模型的最稳妥表述

## 8. 对核心问题的回答

1. 在 `第二级样本` 中，水质特征通路相对 baseline 已形成稳定增益。
2. 在 `第二级样本` 中，系统背景通路相对 baseline 同样形成稳定增益，但在 `regulatory` 上略弱于水质通路，在 `anchored` 上与水质通路接近。
3. `full integration` 在两个任务上都明显优于两个单通路版本。
4. 当系统背景通路已进入模型后，`pH + alkalinity + TOC` 仍保留值得强调的独立增量价值。
5. 当水质特征通路已进入模型后，`structural + treatment` 仍继续提供附加价值。
6. 两条信息通路之间更像“明显互补且存在部分重叠”，而不是“大部分重复”。
7. `V4.7` 更适合作为框架内的探索性整合证据，而不是新的正式主模型结论。

## 9. 本轮最稳妥结论

- `V4.7` 已完成，并在两个 `第二级样本` 正式任务上得到了方向一致的结果。
- 高信息样本中的最佳版本是 `full integration`，说明系统背景通路与水质特征通路合并后确实更强。
- `TOC` 等水质变量在控制系统背景通路后仍保留显著独立价值；反过来，系统背景特征在控制水质通路后也未被替代。
- 当前更应把 `V4.7` 写成“信息通路互补的探索性证据”，而不是“新的统一正式主模型已经建立”。
