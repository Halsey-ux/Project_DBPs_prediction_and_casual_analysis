# V4.5 PWS-Year Structural Conditional Increment 执行报告

- 更新时间：2026-04-03 16:30（Asia/Hong_Kong）
- 对应阶段：`V4.5`
- 输入表：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 统一读取入口：`scripts/io_v4_ml_ready.py`
- 切分策略：复用既有 `group_by_pwsid`
- 模型：`LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_5/tthm_regulatory_exceedance_prediction/`
  - `data_local/V4_Chapter1_Part1_Experiments/V4_5/tthm_anchored_risk_prediction/`

## 1. 本轮任务定义

本轮执行的是 `V4.5 PWS-year structural conditional increment`。目标不是继续往第三层全国主线中加入高稀疏化学变量，也不是切换到树模型或超参数优化，而是回到第三层 `PWS-year` 全国主线真正需要回答的问题：

- 在 `level1 baseline` 基础上，结构/覆盖条件特征是否能稳定提升全国主线风险识别
- 这种提升更像来自系统结构与观测覆盖代理信息，还是来自可写成环境机制的信号
- 在 `level1` 主线和 `level2` 高信息子样本中，这组特征的响应方向是否一致

本轮继续只围绕第三层 `PWS-year` 主表展开，不引入第二层 `facility-month` 字段，不进入 treatment summary features、boosting、树模型或超参数优化，也不保存模型文件。

## 2. 正式任务、样本层级与特征组

### 2.1 正式任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

### 2.2 样本层级

- 主实验固定为 `level1`
- 补充对照为 `level2`
- 不把 `level2` 重新写回全国主线主结论

### 2.3 本轮主特征组

`V4.5` 主增强组建立在 `baseline_default` 之上，新增结构/覆盖条件特征：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`
- `months_observed_any`
- `tthm_months_with_data`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`
- `annual_match_quality_tier`

本轮在代码中命名为：

- `structural_conditional_increment_v4_5_1`

同时保留两个关键消融版本：

- `baseline_without_n_facilities_sensitivity`
- `structural_conditional_without_annual_match_quality_tier`

## 3. 对照链与缺失处理

### 3.1 保留的对照链

`level1` 主实验对每个任务保留以下 4 个版本：

1. `level1 baseline reference`
2. `level1 structural conditional increment`
3. `level1 baseline without n_facilities`
4. `level1 structural conditional without annual_match_quality_tier`

`level2` 补充对照对每个任务保留以下 3 个版本：

1. `level2 baseline reference`
2. `level2 structural conditional increment`
3. `level2 structural conditional without annual_match_quality_tier`

### 3.2 缺失处理规则

- 数值特征保留原始缺失，在模型 pipeline 中使用中位数填补
- 类别特征保留原始类别，在模型 pipeline 中使用众数填补并进行 one-hot 编码
- 不在 `ml_ready` 主表中覆盖式改写缺失值
- `annual_match_quality_tier` 作为年度匹配质量标签使用，不作为环境暴露变量解释

### 3.3 本轮可执行性边界

与 `free_chlorine`、`total_chlorine` 路线不同，本轮结构/覆盖条件特征在 `level1` 和 `level2` 中均接近满覆盖，因此：

- 不需要 complete-case 子集才能运行主实验
- 不存在因极端稀疏导致训练不可执行的问题
- 本轮结果更适合回答“全国主线是否值得引入结构/覆盖代理信息”，而不是机制变量能否通过稀疏数据稳健增益

## 4. 样本规模

### 4.1 `tthm_regulatory_exceedance_prediction`

- `level1`：train `140,580`，validation `29,692`，test `29,530`
- `level2`：train `19,320`，validation `3,761`，test `3,894`

### 4.2 `tthm_anchored_risk_prediction`

- `level1`：train `106,182`，validation `22,483`，test `22,126`
- `level2`：train `12,589`，validation `2,399`，test `2,513`

## 5. 结果总览

### 5.1 `level1` 全国主线

#### `tthm_regulatory_exceedance_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level1 baseline reference` | 0.0696 | 0.7218 | 0.6678 | 0.0690 | 0.7046 | 0.6578 |
| `level1 structural conditional increment` | 0.1003 | 0.8241 | 0.7598 | 0.1025 | 0.8149 | 0.7578 |
| `level1 baseline without n_facilities` | 0.0700 | 0.7204 | 0.6678 | 0.0670 | 0.7032 | 0.6575 |
| `level1 structural conditional without annual_match_quality_tier` | 0.0978 | 0.8219 | 0.7566 | 0.0954 | 0.8128 | 0.7565 |

关键观察：

- 相对 `level1 baseline`，结构/覆盖条件特征在 validation 与 test 的三项主指标上都明显提升。
- `validation PR-AUC` 提升 `+0.0307`，`test PR-AUC` 提升 `+0.0336`，不是边际波动级别。
- 去掉 `annual_match_quality_tier` 后，结果仍显著优于 baseline，说明增益不只是由年度质量标签单独驱动。
- 加回 `annual_match_quality_tier` 后，`test PR-AUC` 仍进一步提升 `+0.0072`，表明它有小幅但稳定的附加贡献。

#### `tthm_anchored_risk_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level1 baseline reference` | 0.1216 | 0.7642 | 0.7132 | 0.1162 | 0.7452 | 0.6999 |
| `level1 structural conditional increment` | 0.2183 | 0.8822 | 0.8074 | 0.1990 | 0.8732 | 0.8035 |
| `level1 baseline without n_facilities` | 0.1226 | 0.7613 | 0.7132 | 0.1134 | 0.7435 | 0.7000 |
| `level1 structural conditional without annual_match_quality_tier` | 0.2110 | 0.8799 | 0.8054 | 0.1891 | 0.8724 | 0.8038 |

关键观察：

- `anchored` 是本轮 `level1` 主线中提升最强的任务。
- 相对 `level1 baseline`，`validation PR-AUC` 提升 `+0.0968`，`test PR-AUC` 提升 `+0.0829`。
- 去掉 `annual_match_quality_tier` 后，结果仍明显高于 baseline，说明主要增益来自更基础的结构/覆盖计数特征。
- `annual_match_quality_tier` 仍提供额外帮助，尤其在 `PR-AUC` 上有一致增益，但它不是全部提升来源。

### 5.2 `level2` 补充对照

#### `tthm_regulatory_exceedance_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level2 baseline reference` | 0.0652 | 0.7212 | 0.6641 | 0.1039 | 0.7395 | 0.6846 |
| `level2 structural conditional increment` | 0.0769 | 0.7868 | 0.7310 | 0.1735 | 0.8161 | 0.7481 |
| `level2 structural conditional without annual_match_quality_tier` | 0.0757 | 0.7820 | 0.7309 | 0.1659 | 0.8127 | 0.7474 |

#### `tthm_anchored_risk_prediction`

| 版本 | Validation PR-AUC | Validation ROC-AUC | Validation Balanced Accuracy | Test PR-AUC | Test ROC-AUC | Test Balanced Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level2 baseline reference` | 0.1208 | 0.7681 | 0.7380 | 0.1858 | 0.7816 | 0.7292 |
| `level2 structural conditional increment` | 0.1852 | 0.8552 | 0.7941 | 0.3436 | 0.8698 | 0.7913 |
| `level2 structural conditional without annual_match_quality_tier` | 0.1824 | 0.8495 | 0.7877 | 0.3310 | 0.8667 | 0.7831 |

关键观察：

- `level2` 与 `level1` 的响应方向一致，两条任务都出现清晰正向增益。
- `level2` test `PR-AUC` 的绝对提升幅度更大，说明结构/覆盖条件特征在高信息子样本中的区分度更强。
- 但这不能被改写成“`level2` 更代表全国主线”，它仍只是补充对照线。

## 6. 与 `V4.1` 至 `V4.4b` 的对照解释

### 6.1 与 `V4.1 baseline` 的关系

- `V4.1` 的作用是把 `level1 + baseline_default` 固定为第三层全国主线起点。
- `V4.5` 沿用同一主线起点，因此与 `V4.1` 保持了直接可比性。
- 本轮确认：全国主线不依赖高稀疏化学变量，也能通过结构/覆盖条件特征获得显著预测增强。

### 6.2 与 `V4.2`、`V4.3`、`V4.4` 的关系

- `V4.2` 至 `V4.4` 的核心对象是 `level2` 上的机制增强顺序验证。
- `V4.3` 已说明 `TOC` 是当前最可信的机制增强变量；`V4.4` 已说明 `free_chlorine` 只有弱边际增益；`V4.4b` 已暂停 `total_chlorine` 第三层主线实验。
- `V4.5` 没有推翻这些判断，而是回答了另一个不同层面的问题：在不继续推进高稀疏化学变量的情况下，全国主线是否还能通过结构/覆盖条件信息得到稳定增强。

### 6.3 当前最合理的整体判断

- 如果比较“可解释的机制增强”，`TOC` 仍是当前最重要的机制变量结果。
- 如果比较“全国主线的稳定预测增强”，`V4.5` 的结构/覆盖条件特征带来的提升更强、更稳定，也更容易执行。
- 但两者的学术意义不同：`TOC` 更接近机制线，`V4.5` 更接近风险画像增强和观测制度代理增强。

## 7. 对关键问题的回答

### 7.1 在 `level1 baseline` 基础上加入结构/覆盖条件特征后，是否带来稳定提升

是。两条任务在 validation 与 test 上均呈现明显正向提升，且不是只发生在单一指标或单一切分上的偶然波动。

### 7.2 提升主要体现在 `regulatory` 还是 `anchored`

两条任务都提升，但 `anchored` 的提升更强、更整齐。`regulatory` 也有稳定改善，但幅度略低于 `anchored`。

### 7.3 提升是否主要由 `annual_match_quality_tier` 带动

不是。去掉 `annual_match_quality_tier` 后，结果仍远高于 baseline，说明主体增益来自覆盖计数与结构条件特征本身。`annual_match_quality_tier` 提供的是额外但次一级的附加贡献。

### 7.4 `n_facilities_in_master` 是否继续表现为重要结构代理变量

它仍有贡献，但贡献很小。`level1 baseline` 去掉 `n_facilities_in_master` 后，`test PR-AUC` 仅下降约 `0.0020`（regulatory）和 `0.0028`（anchored），说明它不是主导本轮结果的压倒性驱动项。

### 7.5 `level1` 与 `level2` 的响应是否一致

一致。两条任务在两个层级上都呈现正向增益，且 `annual_match_quality_tier` 在两个层级上都表现为“小幅但一致的附加贡献”。

### 7.6 当前结果是否支持纳入第三层正式模型

支持，但应限定为：

- 第三层全国主线的正式预测增强层
- 风险画像与观测覆盖代理信息层

不应把它们写成：

- 环境机制变量层
- 因果解释层
- 与 `TOC` 同性质的机制增强结论

## 8. 当前解释边界与争议点

- 不能把 `annual_match_quality_tier` 写成环境暴露变量或真实水质变量。
- 不能把覆盖计数特征带来的增益直接写成 DBP 形成机理发现。
- 不能因为 `level2` 提升更大，就反向把 `level2` 当作全国主线结论主体。
- 不能把“预测上有用”与“机制上可信”混写成同一种结论。

## 9. 本轮结论与下一步建议

本轮可以明确写出的结论是：

1. `V4.5` 已完成，且结构/覆盖条件特征在第三层 `PWS-year` 全国主线 `level1` 上为两条任务都带来了明显且稳定的预测提升。
2. 这种提升在 `anchored` 任务上更强，在 `regulatory` 任务上也足够清晰，不属于边际噪声。
3. 主体增益并不主要来自 `annual_match_quality_tier` 单独一列，而是来自更基础的结构/覆盖计数特征；`annual_match_quality_tier` 只是在此基础上再提供小幅附加收益。
4. 这些特征值得纳入第三层全国主线正式预测模型，但应被写成“结构/覆盖条件增强”或“风险画像增强”，而不是机制增强。

关于下一步，当前更建议：

1. 先收束第三层全国主线的阶段性结论，把 `baseline`、`TOC`、`free_chlorine`、`total_chlorine readiness audit` 和 `V4.5 structural conditional` 的边界统一写清
2. 把 treatment summary features increment 作为可选后续补充实验，而不是默认立刻进入的主线步骤
3. 若后续仍继续推进 treatment summary features，必须继续保留 `level1 baseline reference`、结构/覆盖条件对照链与解释边界，避免把多个代理层混写成机制层
