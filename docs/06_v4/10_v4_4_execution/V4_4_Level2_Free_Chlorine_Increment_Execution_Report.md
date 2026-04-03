# V4.4 Level2 Free Chlorine Increment 执行报告

- 更新时间：2026-04-03 13:54（Asia/Hong_Kong）
- 对应阶段：`V4.4`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_4/tthm_regulatory_exceedance_prediction/`
  - `data_local/V4_Chapter1_Part1_Experiments/V4_4/tthm_anchored_risk_prediction/`

## 1. 本轮任务定义

本轮执行的是 `V4.4 level2 free_chlorine increment`。目标不是切换模型，不是提前做树模型或超参数优化，而是在 `V4.3 level2 TOC increment` 的底座上检验：

- 在 `baseline + pH + alkalinity + TOC + missing flags` 之外，`free_chlorine + free_chlorine_missing_flag` 是否还能继续提供边际预测信息
- 这一增益更像来自 `free_chlorine` 数值本身，还是更像来自 `free_chlorine_missing_flag` 与样本筛选效应
- `V4.2` 与 `V4.3` 已确认的结论，在扩展到 `free_chlorine` 后是否仍然稳定

本轮仍然只围绕第三层 `PWS-year` 主表展开，不引入第二层 `facility-month` 字段，不进入 `total_chlorine`、boosting、树模型或超参数优化，也不保存模型文件。

## 2. 正式任务、样本层级与特征组

### 2.1 正式任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

### 2.2 样本层级

- 主实验固定为 `level2`
- 不把 `level1` 当作本轮主增强层级
- 不把 `level3` 当作本轮主实验层级

### 2.3 本轮主特征组

`V4.4` 主增强组建立在 `V4.3` 基础上，并新增 `free_chlorine`：

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
- `free_chlorine_sample_weighted_mean_mg_l`
- `free_chlorine_missing_flag`

本轮在代码中命名为：

- `mechanistic_stage3_free_chlorine_increment_v4_4_1`

## 3. 对照链与缺失处理

### 3.1 保留的对照链

本轮对每个任务保留以下版本：

1. `level2 baseline reference`
2. `level2 mechanistic stage1 reference`
3. `level2 TOC increment reference`
4. `level2 free_chlorine increment`
5. `level2 complete-case TOC increment reference`
6. `level2 complete-case free_chlorine increment`
7. `level2 complete-case free_chlorine increment no missing flags`

此外，沿用一个轻量敏感性检查：

- `baseline_without_n_facilities_sensitivity`

### 3.2 缺失处理规则

- 主实验版本：保留全部 `level2` 样本，对数值变量做中位数填补，并显式保留 `ph_missing_flag`、`alkalinity_missing_flag`、`toc_missing_flag`、`free_chlorine_missing_flag`
- complete-case 版本：仅保留 `pH + alkalinity + TOC + free_chlorine` 同时非缺失的样本，再分别运行 TOC increment reference 与 free_chlorine increment
- no-missing-flags 敏感性版本：在与 complete-case free_chlorine increment 完全相同的样本上，删除四列 missing flags

### 3.3 本轮新增的容错处理

`free_chlorine` 在 `level2` 中缺失极重。为了避免 complete-case 版本因为切分后只剩单一类别而直接报错，本轮扩展了 `scripts/v4_tthm_training_common.py`：

- 当 validation 或 test split 只有单一类别时，保留可计算指标，并把 `PR-AUC` / `ROC-AUC` 记为 `NA`
- 当 train split 只有单一类别时，不强行训练模型，而是在结果表中保留样本规模、类别计数与 `not_run_due_to_single_class_train_split` 说明

这一步不是为了“挽救结果”，而是为了如实记录该对照链在当前数据口径下的可执行性边界。

## 4. 样本规模与 `free_chlorine` 可用性

### 4.1 主实验样本规模

#### `tthm_regulatory_exceedance_prediction`

- `level2` 全样本：train `19,320`，validation `3,761`，test `3,894`
- `pH + alkalinity + TOC + free_chlorine` complete-case：train `49`，validation `6`，test `5`

#### `tthm_anchored_risk_prediction`

- `level2` 全样本：train `12,589`，validation `2,399`，test `2,513`
- `pH + alkalinity + TOC + free_chlorine` complete-case：train `22`，validation `4`，test `2`

### 4.2 `free_chlorine` 可用性

- `regulatory level2`：共 `26,975` 行，其中 `free_chlorine` 仅 `749` 行非缺失，占比约 `2.78%`
- `anchored level2`：共 `17,501` 行，其中 `free_chlorine` 仅 `540` 行非缺失，占比约 `3.09%`

这说明 `V4.4` 的核心约束不是模型本身，而是 `free_chlorine` 在 `PWS-year level2` 中的极低覆盖率。

## 5. 结果总览

### 5.1 `tthm_regulatory_exceedance_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level2 baseline reference` | `level2 + baseline` | 0.0652 | 0.7212 | 0.6641 | 0.1039 | 0.7395 | 0.6846 |
| `level2 mechanistic stage1 reference` | `level2 + pH + alkalinity + missing flags` | 0.0775 | 0.7586 | 0.6956 | 0.1941 | 0.7986 | 0.7020 |
| `level2 TOC increment reference` | `level2 + TOC + toc_missing_flag` | 0.1138 | 0.8020 | 0.7154 | 0.1877 | 0.8320 | 0.7642 |
| `level2 free_chlorine increment` | `level2 + free_chlorine + free_chlorine_missing_flag` | 0.1144 | 0.8048 | 0.7149 | 0.1880 | 0.8341 | 0.7687 |
| `level2 complete-case TOC increment reference` | `pH + alkalinity + TOC + free_chlorine` complete-case，但不加 `free_chlorine` 入模 | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |
| `level2 complete-case free_chlorine increment` | 同上样本，加入 `free_chlorine` 入模 | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |
| `level2 complete-case free_chlorine increment no missing flags` | 同上样本，删除四列 missing flags | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |

关键观察：

- 相对 `V4.3` 的 TOC increment 参考版本，`free_chlorine` 在 validation / test 的 `PR-AUC` 与 `ROC-AUC` 都是小幅上升。
- `test balanced_accuracy` 也从 `0.7642` 升至 `0.7687`，但 `validation balanced_accuracy` 从 `0.7154` 微降至 `0.7149`。
- 因此，本轮不能把 `regulatory` 写成“强而稳定的全面提升”，更合适的表述是“非常小幅、方向上大体正向的边际增益”。

### 5.2 `tthm_anchored_risk_prediction`

| 版本 | 样本说明 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level2 baseline reference` | `level2 + baseline` | 0.1208 | 0.7681 | 0.7380 | 0.1858 | 0.7816 | 0.7292 |
| `level2 mechanistic stage1 reference` | `level2 + pH + alkalinity + missing flags` | 0.1416 | 0.8112 | 0.7636 | 0.3061 | 0.8412 | 0.7567 |
| `level2 TOC increment reference` | `level2 + TOC + toc_missing_flag` | 0.2353 | 0.8537 | 0.7645 | 0.3588 | 0.8790 | 0.8183 |
| `level2 free_chlorine increment` | `level2 + free_chlorine + free_chlorine_missing_flag` | 0.2366 | 0.8562 | 0.7721 | 0.3605 | 0.8807 | 0.8201 |
| `level2 complete-case TOC increment reference` | `pH + alkalinity + TOC + free_chlorine` complete-case，但不加 `free_chlorine` 入模 | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |
| `level2 complete-case free_chlorine increment` | 同上样本，加入 `free_chlorine` 入模 | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |
| `level2 complete-case free_chlorine increment no missing flags` | 同上样本，删除四列 missing flags | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |

关键观察：

- 相对 `V4.3` 的 TOC increment 参考版本，`anchored` 在 validation / test 的三项主指标全部继续上升。
- 但绝对增幅也非常有限：validation `PR-AUC` 仅增加 `0.0013`，test `PR-AUC` 仅增加 `0.0017`。
- 这说明 `free_chlorine` 在 `anchored` 任务上的边际增益比 `regulatory` 略更整齐，但仍然只是弱增益，不是类似 `TOC` 的强增量。

## 6. complete-case 结果为何没有数值

本轮并非“漏跑” complete-case，而是 complete-case 在当前口径下无法合法训练：

- `regulatory` complete-case：train `49`、validation `6`、test `5`，其中 train 与 validation 全为负类
- `anchored` complete-case：train `22`、validation `4`、test `2`，其中 train 与 validation 全为负类

在这种情况下，继续强行训练 `LogisticRegression` 会违反最基本的二分类前提。因此本轮把 complete-case 版本明确记录为：

- 已完成样本筛选与可执行性检查
- 因 train split 为单一类别而未运行正式训练
- 在结果表与说明文档中保留样本规模和类别分布

这意味着 `V4.4` 无法像 `V4.2` 与 `V4.3` 那样，通过 complete-case 版本去验证“去掉缺失模式解释后，数值增益是否仍然存在”。

## 7. 对增益来源的补充诊断

### 7.1 缺失模式信号非常强

在 full `level2` 样本中，`free_chlorine` 的缺失占绝大多数：

- `regulatory`：`26,226 / 26,975` 行缺失
- `anchored`：`16,961 / 17,501` 行缺失

而且在两个任务里，“`free_chlorine` 缺失”的样本正类比例都明显高于“`free_chlorine` 有观测”的样本。这说明 `free_chlorine_missing_flag` 很可能承载了相当强的样本结构信息。

### 7.2 数值本身并非完全没有信息

在 `free_chlorine` 有观测的极小子样本里，正类样本的 `free_chlorine` 平均值高于负类样本：

- `regulatory observed subset`：负类均值约 `1.060 mg/L`，正类均值约 `1.571 mg/L`
- `anchored observed subset`：负类均值约 `0.998 mg/L`，正类均值约 `1.571 mg/L`

此外，在 full `level2` 主实验的 logistic 回归中：

- `free_chlorine_sample_weighted_mean_mg_l` 的标准化系数略高于 `free_chlorine_missing_flag`
- 但这个判断只建立在非常少的正类观测上：两个任务的 observed subset 都只有 `6` 个正类

### 7.3 因此更合理的解释是“混合来源”

本轮最稳妥的判断不是“`free_chlorine` 数值本身已被清晰验证”，而是：

- `free_chlorine` 可能包含一定数值信息
- `free_chlorine_missing_flag` 与样本选择结构也明显提供了信息
- 由于 complete-case 无法训练，当前无法把这两部分信号彻底拆开

## 8. 对 `V4.2` 与 `V4.3` 的承接

`V4.4` 没有推翻前两轮结论，反而强化了当前路线的边界：

1. `V4.2` 已说明 `pH + alkalinity + missing flags` 相对 baseline 有稳定增益，这一结论仍成立。
2. `V4.3` 已说明 `TOC` 在 `anchored` 任务上有明显且稳定的边际增益，在 `regulatory` 任务上则是部分稳定增益，这一判断仍是当前机制增强链条中最重要的实质性提升。
3. `V4.4` 表明在 `TOC` 之后继续加入 `free_chlorine`，只能带来很有限的进一步改善，而且当前无法通过 complete-case 把这种改善稳健地归因到数值本身。

## 9. 当前解释边界与争议点

- 不能把 `level2` 的结果写成全国主线最终结论。
- 不能把 `free_chlorine` 的小幅预测增益直接写成机制发现，更不能写成因果发现。
- 不能把本轮完整主实验的小幅提升简单改写为“`free_chlorine` 明确带来稳定强增益”。
- 不能把 observed subset 中极少数正类样本上的数值差异过度外推为稳健结论。
- complete-case 无法训练意味着：当前没有证据排除 `free_chlorine_missing_flag` 与样本选择效应对增益的主导作用。

## 10. 本轮结论与下一步建议

本轮可以明确写出的结论是：

1. `V4.4` 已完成，且 `free_chlorine + free_chlorine_missing_flag` 在 full `level2` 上为两条任务都带来了方向一致但幅度很小的边际增益。
2. 这类增益在 `anchored` 任务上略更整齐，在 `regulatory` 任务上则更弱。
3. 由于 `free_chlorine` 覆盖率极低，四变量 complete-case 子集在 train split 中只剩单一类别，导致本轮无法复现 `V4.2` / `V4.3` 那种 complete-case 稳健性验证。
4. 因此，当前最稳妥的表述不是“`free_chlorine` 数值信号已被稳健确认”，而是“`free_chlorine` 在当前 `PWS-year level2` 口径下显示出弱边际增益，但该增益很可能是数值信息、缺失模式信息与样本选择结构的混合产物”。

是否建议直接进入下一轮 `total_chlorine`：

- 当前不建议立刻按同样主线进入 `V4.5 total_chlorine increment`

原因是：

- `free_chlorine` 这一轮的增益幅度已经很小
- 最关键的稳健性检查被数据稀疏性直接阻断
- 如果 `total_chlorine` 覆盖率没有显著好于 `free_chlorine`，继续按同一口径推进，极可能只会重复同类问题

更合理的下一步优先级是：

1. 先把 `V4.4` 作为“弱增益但高缺失约束”的正式结论固定下来
2. 再单独审计 `total_chlorine` 在 `level2` 与 `facility-month` 口径下的非缺失覆盖率与正类分布
3. 只有在覆盖率和可执行性明显优于 `free_chlorine` 时，再决定是否启动 `V4.5`
