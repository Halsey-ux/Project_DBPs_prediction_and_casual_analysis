# V4.6 PWS-Year Treatment Summary Increment 执行报告

- 更新时间：2026-04-03 17:01（Asia/Hong_Kong）
- 对应阶段：`V4.6`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_6/tthm_regulatory_exceedance_prediction/`
  - `data_local/V4_Chapter1_Part1_Experiments/V4_6/tthm_anchored_risk_prediction/`

## 1. 本轮任务定义

本轮执行的是 `V4.6 PWS-year treatment summary increment`。核心目标不是继续向第三层全国主线中加入新的高稀疏化学数值变量，也不是切换到树模型、boosting 或超参数优化，而是回答以下问题：

- 在 `第一级样本 baseline` 基础上，年度 treatment summary 特征是否已经具有独立预测价值
- 在控制 `V4.5 structural conditional` 特征后，treatment summary 是否仍保留额外增益
- 这类增益更适合被解释为系统工程背景信号、制度代理信息，还是可直接写成环境机制发现

本轮继续只围绕第三层 `PWS-year` 主表展开，不引入第二层 `facility-month` 字段，不保存模型文件。

## 2. 样本层级、特征组与缺失处理

### 2.1 正式任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

### 2.2 样本层级

- 主实验固定为 `第一级样本`
- 补充对照保留 `第二级样本`
- `第二级样本` 只用于补充解释，不替代全国主线结论

### 2.3 本轮 treatment summary 特征组

`V4.6` treatment summary 候选组为：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

代码中对应命名为：

- `treatment_summary_increment_v4_6_1`
- `structural_and_treatment_combined_v4_6_1`

### 2.4 保留的对照链

每个任务在 `第一级样本` 与 `第二级样本` 都保留以下四层版本：

1. `baseline_default_reference`
2. `structural_conditional_reference_v4_5_1`
3. `treatment_summary_increment_v4_6_1`
4. `structural_and_treatment_combined_v4_6_1`

这样可以区分两件事：

- treatment summary 单独加在 baseline 上是否有用
- treatment summary 在控制 `V4.5 structural conditional` 后是否仍有剩余增益

### 2.5 treatment 字段覆盖情况

在 `V4_pws_year_ml_ready.csv` 中：

- `第一级样本` 共 `199,802` 行，其中至少有 1 个 treatment summary 字段非缺失的行数为 `26,702`，占 `13.36%`
- `第一级样本` 有 `173,100` 行在 6 个 treatment summary 字段上全部缺失，占 `86.64%`
- `第二级样本` 共 `26,975` 行，其中至少有 1 个 treatment summary 字段非缺失的行数为 `19,266`，占 `71.43%`
- `第二级样本` 有 `7,709` 行在 6 个 treatment summary 字段上全部缺失，占 `28.57%`

这意味着：

- treatment summary 在 `第一级样本` 全国主样本上的覆盖率并不高
- 它在 `第二级样本` 高信息样本中的可用度明显更强，因此 `第二级样本` 中出现更大增益是可解释的

### 2.6 缺失处理与解释边界

- treatment 二值字段保留原始缺失，不在主表中覆盖式改写为 `0`
- 在模型 `pipeline` 中，这些字段按现有数值列规则进入中位数填补与标准化
- 这些变量只能解释为年度 treatment 摘要信号、系统工程背景信号或制度代理信息
- 即使带来预测增益，也不能被写成 DBP 环境机制发现

## 3. 样本规模

### 3.1 `tthm_regulatory_exceedance_prediction`

- `第一级样本`：train `140,580`，validation `29,692`，test `29,530`
- `第二级样本`：train `19,320`，validation `3,761`，test `3,894`

### 3.2 `tthm_anchored_risk_prediction`

- `第一级样本`：train `106,182`，validation `22,483`，test `22,126`
- `第二级样本`：train `12,589`，validation `2,399`，test `2,513`

## 4. 结果总览

### 4.1 `第一级样本` 全国主线

#### `tthm_regulatory_exceedance_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.0696 | 0.7218 | 0.6678 | 0.0690 | 0.7046 | 0.6578 |
| `structural_conditional_reference_v4_5_1` | 0.1003 | 0.8241 | 0.7598 | 0.1025 | 0.8149 | 0.7578 |
| `treatment_summary_increment_v4_6_1` | 0.0710 | 0.7273 | 0.6665 | 0.0688 | 0.7070 | 0.6579 |
| `structural_and_treatment_combined_v4_6_1` | 0.1021 | 0.8232 | 0.7603 | 0.1073 | 0.8159 | 0.7605 |

关键观察：

- treatment summary 单独加在 `baseline` 上几乎没有形成稳定提升，`test PR-AUC` 甚至略低于 baseline（`-0.0002`）
- 但把 treatment summary 加到 `V4.5 structural conditional` 之后，`validation PR-AUC` 仍提升 `+0.0018`，`test PR-AUC` 提升 `+0.0047`
- 因此在 `regulatory` 任务上，treatment summary 不足以单独构成新的主增强层，但作为 `V4.5` 之后的附加层有小幅稳定收益

#### `tthm_anchored_risk_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.1216 | 0.7642 | 0.7132 | 0.1162 | 0.7452 | 0.6999 |
| `structural_conditional_reference_v4_5_1` | 0.2183 | 0.8822 | 0.8074 | 0.1990 | 0.8732 | 0.8035 |
| `treatment_summary_increment_v4_6_1` | 0.1268 | 0.7683 | 0.7135 | 0.1183 | 0.7492 | 0.6987 |
| `structural_and_treatment_combined_v4_6_1` | 0.2228 | 0.8807 | 0.8063 | 0.2080 | 0.8742 | 0.8043 |

关键观察：

- treatment summary 单独加在 `baseline` 上只有小幅提升，`test PR-AUC` 仅增加 `+0.0022`
- 但在 `V4.5 structural conditional` 之后仍存在稳定剩余增益：`validation PR-AUC` 增加 `+0.0045`，`test PR-AUC` 增加 `+0.0090`
- `anchored` 是本轮 treatment summary 增益更清晰的任务

### 4.2 `第二级样本` 补充对照

#### `tthm_regulatory_exceedance_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.0652 | 0.7212 | 0.6641 | 0.1039 | 0.7395 | 0.6846 |
| `structural_conditional_reference_v4_5_1` | 0.0769 | 0.7868 | 0.7310 | 0.1735 | 0.8161 | 0.7481 |
| `treatment_summary_increment_v4_6_1` | 0.0824 | 0.7109 | 0.6276 | 0.1158 | 0.7495 | 0.6914 |
| `structural_and_treatment_combined_v4_6_1` | 0.0833 | 0.7801 | 0.7204 | 0.1783 | 0.8189 | 0.7560 |

关键观察：

- `第二级样本` 中 treatment summary 单独相对 baseline 已有一定增益，`test PR-AUC` 提升 `+0.0119`
- treatment summary 加到 structural conditional 后，`validation PR-AUC` 再提升 `+0.0064`，`test PR-AUC` 再提升 `+0.0048`
- 方向与 `第一级样本` 一致，但增幅更大

#### `tthm_anchored_risk_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_default_reference` | 0.1208 | 0.7681 | 0.7380 | 0.1858 | 0.7816 | 0.7292 |
| `structural_conditional_reference_v4_5_1` | 0.1852 | 0.8552 | 0.7941 | 0.3436 | 0.8698 | 0.7913 |
| `treatment_summary_increment_v4_6_1` | 0.1432 | 0.7740 | 0.7137 | 0.2123 | 0.7929 | 0.7378 |
| `structural_and_treatment_combined_v4_6_1` | 0.1980 | 0.8464 | 0.7967 | 0.3591 | 0.8750 | 0.8059 |

关键观察：

- 这是本轮 treatment summary 响应最强的补充版本
- 相对 `baseline`，treatment summary 单独的 `test PR-AUC` 提升 `+0.0265`
- 相对 `structural conditional`，combined 版本的 `validation PR-AUC` 再提升 `+0.0128`，`test PR-AUC` 再提升 `+0.0156`

## 5. 与 V4.1 至 V4.5 的对照解释

### 5.1 与 `V4.1 baseline` 的关系

- `V4.1` 固定了第三层全国主线的最小起点：`第一级样本 + baseline_default`
- `V4.6` 延续同一切分、同一模型、同一评价框架，因此与 `V4.1` 保持直接可比
- 本轮结果显示：treatment summary 单独相对 baseline 的增益有限，不足以像 `V4.5` 那样重新定义全国主线

### 5.2 与 `V4.5 structural conditional` 的关系

- `V4.5` 已证明结构/覆盖条件特征是第三层全国主线中最强、最稳定的预测增强层
- `V4.6` 进一步证明：在 `V4.5` 之后，treatment summary 仍有小到中等幅度的剩余增益
- 但这层增益明显小于 `V4.5` 本身，因此 treatment summary 更适合被定位为附加增强，而不是新的核心主线

### 5.3 与 `V4.3 TOC`、`V4.4 free_chlorine`、`V4.4b total_chlorine` 的关系

- `TOC` 仍是当前最可信的机制增强变量，但其主要证据来自 `第二级样本`
- `free_chlorine` 在 `第二级样本` 上只有弱边际增益，且难以区分数值信号和缺失模式信号
- `total_chlorine` 当前不适合继续进入第三层正式增量实验
- 与这些结果相比，`V4.6 treatment summary` 更像是工程背景辅助增强，而不是机制增强

## 6. 对核心问题的回答

### 6.1 在 `第一级样本 baseline` 基础上加入 treatment summary 后，是否带来稳定提升

不充分。

- `regulatory` 几乎没有稳定提升
- `anchored` 有轻微提升，但幅度较小

因此 treatment summary 不适合作为跳过 `V4.5` 的独立主增强层。

### 6.2 treatment summary 在控制 `V4.5 structural conditional` 后是否仍有增益

有，而且方向稳定。

- `第一级样本 regulatory`：`test PR-AUC` 从 `0.1025` 升到 `0.1073`
- `第一级样本 anchored`：`test PR-AUC` 从 `0.1990` 升到 `0.2080`
- `第二级样本` 两个任务也都继续上升

因此可以认为 treatment summary 与 `V4.5 structural conditional` 并非完全重复。

### 6.3 增益主要体现在哪条任务上

主要体现为：

- `anchored` 强于 `regulatory`
- `第二级样本` 强于 `第一级样本`

这与 treatment 字段在高信息样本中的覆盖率更高相一致。

### 6.4 这类增益更像什么

更像：

- 系统工程背景信号
- 年度工艺存在性摘要
- 与观测制度、系统配置相关的代理信息

不像：

- 可直接写成 DBP 生成机制的环境变量发现

### 6.5 `第一级样本` 与 `第二级样本` 对 treatment summary 的响应方向是否一致

一致。

- 两个任务在两个层级上都表现为 `combined > structural reference`
- 只是 `第二级样本` 的增益更强、更容易被看见

### 6.6 当前是否支持把 treatment summary 纳入第三层正式模型

支持，但应限定为：

- `V4.5 structural conditional` 之后的辅助增强层
- 以预测表现为目标时可纳入 `combined` 正式版本
- 以论文解释清晰度为目标时，应把它写成“工程背景辅助增强”或“制度代理辅助增强”

不应把它写成：

- 与 `TOC` 同性质的机制增强
- 替代 `V4.5 structural conditional` 的主结论

## 7. 当前最稳妥的结论与下一步建议

本轮可以明确写出的结论是：

1. `V4.6` 已完成，treatment summary 在第三层 `PWS-year` 全国主线中不构成新的独立主增强层。
2. treatment summary 单独相对 baseline 的收益有限，尤其在 `第一级样本 regulatory` 上几乎没有独立价值。
3. 但在控制 `V4.5 structural conditional` 后，treatment summary 仍提供小而稳定的剩余增益，且在 `anchored` 与 `第二级样本` 上更明显。
4. 因此 treatment summary 可被纳入第三层正式预测模型的扩展版，但更适合写成“工程背景辅助增强”，不应写成“机制增强”。

关于下一步，更建议：

1. 先阶段性收束第三层全国主线，把 `baseline`、`V4.5 structural conditional`、`V4.6 treatment combined` 的定位关系固定下来。
2. 若需要正式给出第三层最佳预测版，可采用 `baseline + structural conditional + treatment summary` 的 combined 版本。
3. 若需要强调学术解释边界，应继续把机制发现主证据保留在 `第二级样本 TOC` 路线，而不是把 `V4.6` 写成机制结果。
