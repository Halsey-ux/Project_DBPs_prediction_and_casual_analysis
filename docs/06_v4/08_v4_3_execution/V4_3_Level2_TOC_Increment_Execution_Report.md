# V4.3 Level2 TOC Increment 执行报告

- 更新时间：2026-04-03 12:07（Asia/Hong_Kong）
- 对应阶段：`V4.3`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_3/tthm_regulatory_exceedance_prediction/`
  - `data_local/V4_Chapter1_Part1_Experiments/V4_3/tthm_anchored_risk_prediction/`

## 1. 本轮任务定义

本轮执行的是 `V4.3 第二级样本 TOC increment`。目标不是更换模型，也不是提前做调参或树模型，而是在 `V4.2.1 第二级样本 mechanistic stage1` 的底座上，检验：

- 在 `baseline + pH + alkalinity + missing flags` 之外，`TOC + toc_missing_flag` 是否还能继续提供边际预测信息
- 这一增益是更像来自 `TOC` 数值本身，还是更像来自 `toc_missing_flag` 与样本筛选效应
- `V4.2` 已确认的结论，在扩展到 `TOC` 后是否保持稳定

本轮仍然只围绕第三层 `PWS-year` 主表展开，不引入第二层 `facility-month` 字段，不切换到 boosting，不进行超参数优化，也不保存模型文件。

## 2. 正式任务、样本层级与特征组

### 2.1 正式任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

### 2.2 样本层级

- 主实验固定为 `第二级样本`
- 不把 `第一级样本` 当作本轮主增强层级
- 不把 `第三级样本` 当作本轮主实验层级

### 2.3 本轮主特征组

`V4.3` 主增强组建立在 `V4.2.1` 基础上，并新增 `TOC`：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`
- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_sample_weighted_mean_mg_l`
- `toc_missing_flag`

本轮在代码中命名为：

- `mechanistic_stage2_toc_increment_v4_3_1`

## 3. 对照链与缺失处理

### 3.1 必保留对照链

本轮对每个任务至少保留以下版本：

1. `第二级样本 baseline reference`
2. `第二级样本 mechanistic stage1 reference`
3. `第二级样本 TOC increment`
4. `第二级样本 complete-case mechanistic stage1 reference`
5. `第二级样本 complete-case TOC increment`
6. `第二级样本 complete-case TOC increment no missing flags`

此外，补充执行了一个轻量敏感性检查：

- `baseline_without_n_facilities_sensitivity`

### 3.2 缺失处理规则

- 主实验版本：保留全部 `第二级样本` 样本，对数值变量做中位数填补，并显式保留 `ph_missing_flag`、`alkalinity_missing_flag`、`toc_missing_flag`
- complete-case 版本：仅保留 `pH + alkalinity + TOC` 同时非缺失的样本，再分别运行 stage1 reference 与 TOC increment
- no-missing-flags 敏感性版本：在与 complete-case TOC increment 完全相同的样本上，删除三列 missing flags，用于验证这些 flag 是否仅为常量列

## 4. 样本规模

### 4.1 `tthm_regulatory_exceedance_prediction`

- `第二级样本` 全样本：train `19,320`，validation `3,761`，test `3,894`
- `pH + alkalinity + TOC` complete-case：train `4,096`，validation `806`，test `733`

### 4.2 `tthm_anchored_risk_prediction`

- `第二级样本` 全样本：train `12,589`，validation `2,399`，test `2,513`
- `pH + alkalinity + TOC` complete-case：train `1,987`，validation `361`，test `318`

## 5. 结果总览

### 5.1 `tthm_regulatory_exceedance_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `第二级样本 baseline reference` | `第二级样本 + baseline` | 0.0652 | 0.7212 | 0.6641 | 0.1039 | 0.7395 | 0.6846 |
| `第二级样本 mechanistic stage1 reference` | `第二级样本 + pH + alkalinity + missing flags` | 0.0775 | 0.7586 | 0.6956 | 0.1941 | 0.7986 | 0.7020 |
| `第二级样本 TOC increment` | `第二级样本 + TOC + toc_missing_flag` | 0.1138 | 0.8020 | 0.7154 | 0.1877 | 0.8320 | 0.7642 |
| `第二级样本 complete-case mechanistic stage1 reference` | `pH + alkalinity + TOC` complete-case，但不加 `TOC` 入模 | 0.0925 | 0.7214 | 0.6622 | 0.0883 | 0.7776 | 0.7286 |
| `第二级样本 complete-case TOC increment` | `pH + alkalinity + TOC` complete-case，加入 `TOC` 入模 | 0.1071 | 0.8134 | 0.7349 | 0.3427 | 0.8592 | 0.7594 |
| `第二级样本 complete-case TOC increment no missing flags` | 与上一行同样本，但删除三列 missing flags | 0.1071 | 0.8134 | 0.7349 | 0.3427 | 0.8592 | 0.7594 |

关键观察：

- 相对 `V4.2.1`，`第二级样本 TOC increment` 在 validation 上全部主指标继续上升。
- 在 regulatory 任务的 test 集上，`ROC-AUC` 与 `balanced_accuracy` 继续上升，但 `PR-AUC` 从 `0.1941` 小幅降至 `0.1877`，因此不能把它写成“regulatory 任务所有主指标都稳定继续提升”。
- 在 `pH + alkalinity + TOC` complete-case 子集上，加入 `TOC` 后 test `PR-AUC` 从 `0.0883` 提升到 `0.3427`，说明 `TOC` 数值本身在已观测子样本中具有明显信息量。
- complete-case 去掉 missing flags 后结果与 complete-case TOC increment 完全一致，说明该子集中三列 missing flags 只是常量列。

### 5.2 `tthm_anchored_risk_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `第二级样本 baseline reference` | `第二级样本 + baseline` | 0.1208 | 0.7681 | 0.7380 | 0.1858 | 0.7816 | 0.7292 |
| `第二级样本 mechanistic stage1 reference` | `第二级样本 + pH + alkalinity + missing flags` | 0.1416 | 0.8112 | 0.7636 | 0.3061 | 0.8412 | 0.7567 |
| `第二级样本 TOC increment` | `第二级样本 + TOC + toc_missing_flag` | 0.2353 | 0.8537 | 0.7645 | 0.3588 | 0.8790 | 0.8183 |
| `第二级样本 complete-case mechanistic stage1 reference` | `pH + alkalinity + TOC` complete-case，但不加 `TOC` 入模 | 0.1508 | 0.7454 | 0.6571 | 0.2020 | 0.8035 | 0.7283 |
| `第二级样本 complete-case TOC increment` | `pH + alkalinity + TOC` complete-case，加入 `TOC` 入模 | 0.2658 | 0.8609 | 0.7707 | 0.6040 | 0.9149 | 0.7939 |
| `第二级样本 complete-case TOC increment no missing flags` | 与上一行同样本，但删除三列 missing flags | 0.2658 | 0.8609 | 0.7707 | 0.6040 | 0.9149 | 0.7939 |

关键观察：

- `anchored` 是本轮 `TOC` 增益最清楚、最稳定的任务。
- 相对 `V4.2.1`，`第二级样本 TOC increment` 在 validation / test 的 `PR-AUC`、`ROC-AUC` 与 `balanced_accuracy` 都继续明显提升。
- 在 complete-case 子集上，加入 `TOC` 后 test `PR-AUC` 从 `0.2020` 提升到 `0.6040`，幅度很大，且 no-missing-flags 版本完全复现相同结果。
- 这说明在 `anchored` 任务上，本轮增益不能简单归因为缺失模式；`TOC` 数值本身大概率提供了额外区分信息。

## 6. 对 `V4.2` 的承接与解释

`V4.2` 已确认：

- `pH + alkalinity + missing flags` 相对 baseline 在 `第二级样本` 上有稳定增益
- 这种增益在 `pH + alkalinity` complete-case 子集上仍然成立
- 在 complete-case 子集上删除 `ph_missing_flag` 与 `alkalinity_missing_flag` 不改变结果

`V4.3` 在此基础上的结论是：

1. `TOC` 不是无效变量。无论是 regulatory 还是 anchored，validation 集都显示出正向增益；complete-case 子集也支持 `TOC` 数值本身存在信息量。
2. `TOC` 增益并不在所有任务上同样稳定。`anchored` 上表现非常强，而 `regulatory` 上的 full `第二级样本` test `PR-AUC` 没有继续上升，因此需要保留谨慎口径。
3. `toc_missing_flag` 不是 complete-case 增益来源。因为在 complete-case 子集上删除 missing flags 后结果完全不变。
4. `第二级样本` 仍然只是高信息样本，不是全国随机样本，因此本轮结论只能写成“在 `第二级样本` 高信息样本中观察到的增益”。

## 7. 轻量敏感性检查

本轮补充了 `baseline_without_n_facilities_sensitivity`：

- `regulatory`：validation `PR-AUC` 从 `0.0652` 降到 `0.0637`，test `PR-AUC` 从 `0.1039` 降到 `0.0993`
- `anchored`：validation `PR-AUC` 从 `0.1208` 降到 `0.1155`，test `PR-AUC` 从 `0.1858` 降到 `0.1761`

解释边界：

- `n_facilities_in_master` 对 baseline 表现有一定贡献
- 但它不是压倒性驱动项，因为去掉后只是小幅下降
- 后续文档应继续把它写成“结构代理特征”，而不是无争议的机制变量

## 8. 当前解释边界与争议点

- 不能把 `第二级样本` 的增益直接写成全国主模型已经稳定升级，更不能写成因果发现。
- `anchored` 任务上的 `TOC` 增益最稳定，但 `regulatory` 任务上的 full `第二级样本` test `PR-AUC` 没有继续提高，因此不能把本轮结论简化成“TOC 对所有主任务都稳定增益”。
- complete-case 结果说明 `TOC` 数值本身有信息，但 complete-case 也改变了样本构成，因此它仍然不是全国总体可泛化性的直接证据。
- 本轮新增的 `balanced_accuracy`、`specificity`、`MCC` 与 confusion matrix 字段仅用于补充理解，不改变 `PR-AUC` 与 `ROC-AUC` 仍是主要比较指标的原则。

## 9. 本轮结论

本轮可以明确写出的结论是：

1. `V4.3` 已完成，且 `TOC` 在 `第二级样本` 机制增强框架中不是冗余变量。
2. `TOC` 的边际增益主要体现在 `anchored` 任务上，并在 complete-case 子集上得到进一步支持。
3. 对于 `regulatory` 任务，`TOC` 提升了 validation 指标、test `ROC-AUC` 与 test `balanced_accuracy`，但没有带来更高的 full `第二级样本` test `PR-AUC`，因此应使用“部分稳定增益”而不是“稳定全面增益”的表述。
4. 当前结果足以支持按相同对照框架进入下一轮 `free_chlorine`，但必须保留 `V4.2.1`、`V4.3`、complete-case 与 no-missing-flags 的连续参照链。
