# V4.5 PWS-Year Structural Conditional Increment Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_3_Level2_TOC_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/08_v4_3_execution/V4_3_Level2_TOC_Increment_Execution_Report.md)
- [V4_4_Level2_Free_Chlorine_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/10_v4_4_execution/V4_4_Level2_Free_Chlorine_Increment_Execution_Report.md)
- [V4_4b_Total_Chlorine_Readiness_Audit_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/11_v4_4b_execution/V4_4b_Total_Chlorine_Readiness_Audit_Report.md)
- [V4_1_4_Update_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/V4_1_4_Update_Summary.md)

## 1. 当前任务定位

你当前要执行的是 `V4.5` 更新。`V4.5` 的正式主题是：

- `PWS-year structural conditional increment`

这一轮更新的核心目标不是继续往第三层主线里加入高稀疏机制变量，也不是切换模型、做树模型或提前进入超参数优化，而是：

- 在当前已经完成的 `baseline -> pH + alkalinity -> TOC -> free_chlorine -> total_chlorine readiness audit` 之后，回到第三层主线真正应回答的问题
- 检验一组覆盖率更高、结构意义更稳定的 `PWS-year` 条件特征，是否能为全国主线提供额外预测信息
- 明确这些特征带来的提升，究竟更像“全国主线风险画像增强”，还是更像“样本质量/观测覆盖代理信息”
- 继续把 `V4` 保持在“可复现、可比较、可解释的逐步增强实验”轨道上

## 2. 必须继承的前序结论

在开始 `V4.5` 之前，你必须接受并沿用以下已确认结论：

1. `V4.1` 已确认：`level1 + baseline_default` 可以作为第三层全国主线起点。
2. `V4.2` 已确认：在 `level2` 上加入 `pH + alkalinity + missing flags` 后，两条任务线都相对 baseline 获得稳定提升。
3. `V4.3` 已确认：`TOC` 是当前第三层主线上最可信的机制增强变量，尤其在 `anchored` 任务上增益明显。
4. `V4.4` 已确认：`free_chlorine` 在 full `level2` 上只带来弱边际增益，且无法稳健拆分数值信号、缺失模式信号与样本选择效应。
5. `V4.4b` 已确认：`total_chlorine` 当前不具备继续进入第三层正式增量实验的条件。
6. 因此，`V4.5` 的自然下一步不是继续推进高稀疏化学变量，而是检验 `PWS-year` 层级的结构/覆盖条件特征，看看全国主线还能否在不依赖极稀疏变量的情况下获得更稳健提升。

## 3. 当前实验体系仍需保持的批判性判断

你必须带着以下判断执行 `V4.5`，不能把结构条件特征的提升直接误写成环境机制结论：

### 3.1 `PWS-year` 主线的任务仍是全国风险识别

- 第三层 `PWS-year` 主表适合做全国主线风险识别与系统级风险画像。
- 它不适合作为精细工艺机制表，也不应被写成直接的形成机理模型。
- 因此，`V4.5` 的结论应定位为“全国主线可否用结构/覆盖信息进一步提升风险识别”，而不是“找到新的环境机制变量”。

### 3.2 新增特征更像结构代理或覆盖代理

本轮候选特征大多不是直接环境暴露变量，而是：

- 结构背景特征
- 观测覆盖特征
- 年度匹配质量标签

因此：

- 即便它们带来预测增益，也不能直接解释为环境机制发现
- 文档中必须明确区分“预测价值”和“机制意义”

### 3.3 `level1` 与 `level2` 的角色需要重新拉开

- 到目前为止，增强实验大多集中在 `level2`
- 但第三层真正的全国主线应优先回到 `level1`
- 因此 `V4.5` 应优先围绕 `level1` 正式主线展开，并在必要时补充 `level2` 对照，避免继续把高信息样本结果误写成全国主结论

### 3.4 主指标与辅助指标规则继续沿用

- 主指标仍优先使用 `PR-AUC` 与 `ROC-AUC`
- 辅助保留 `balanced_accuracy`、`specificity`、`MCC` 与 confusion matrix 字段
- 当前不重构整套评价框架，只要求继续沿用现有统一输出格式

## 4. 本轮总原则

1. 原始数据只读，不允许原位修改。
2. 仅基于第三层 `V4_pws_year_ml_ready.csv` 执行。
3. 统一通过 [io_v4_ml_ready.py](D:/Project_DBPs_prediction_and_casual_analysis/scripts/io_v4_ml_ready.py) 读取数据。
4. 统一复用当前 `group_by_pwsid` 切分，不重新随机切分。
5. 默认模型继续使用 `LogisticRegression`。
6. 当前不做树模型、不做 boosting、不做超参数优化。
7. 当前不保存模型文件。
8. 所有新增或更新的 `.md` 文档必须使用中文。
9. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)。
10. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送。

## 5. 本轮正式实验定义

### 5.1 主任务

本轮至少继续跑两条正式任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

### 5.2 样本层级

本轮主实验优先固定为：

- `level1`

如有必要，可补一个 `level2` 对照版本，但不得让 `level2` 重新替代全国主线。

### 5.3 本轮主特征组

`V4.5` 的主增强特征组必须建立在 `baseline_default` 之上，并新增一组结构/覆盖条件特征。默认候选组为：

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

这组特征应命名为类似：

- `structural_conditional_increment_v4_5_1`

你可以微调命名，但必须清晰表达“这是在第三层全国主线 baseline 基础上增加结构/覆盖条件特征的增量实验”。

## 6. 本轮必须保留的对照链

`V4.5` 的核心风险不是跑不出结果，而是把结构代理变量的贡献误写成环境机制提升。因此本轮至少必须保留以下 5 组版本：

### 6.1 `level1 baseline reference`

定义：

- 样本：全部 `level1`
- 特征：仅 baseline 4 个特征

作用：

- 作为第三层全国主线最基础参照
- 保证可与 `V4.1` 连续比较

### 6.2 `level1 structural conditional increment`

定义：

- 样本：全部 `level1`
- 特征：`baseline + structural conditional features`

作用：

- 回答结构/覆盖条件特征是否能在全国主线上带来额外预测信息

### 6.3 `level1 baseline without n_facilities`

定义：

- 样本：全部 `level1`
- 特征：`baseline` 去掉 `n_facilities_in_master`

作用：

- 继续跟踪 `n_facilities_in_master` 作为结构代理特征的贡献边界
- 防止后续把 `structural conditional increment` 的增益都误归因到单个结构计数字段

### 6.4 `level1 structural conditional without annual_match_quality_tier`

定义：

- 样本：全部 `level1`
- 特征：`baseline + months_* + n_core_vars_available`，但不加入 `annual_match_quality_tier`

作用：

- 分开观察“年度质量分层标签”与“纯覆盖计数特征”各自的贡献
- 避免把标签化摘要变量和原始计数特征混在一起解释

### 6.5 `level2 structural conditional reference`（可选但推荐）

定义：

- 样本：全部 `level2`
- 特征：与 `level1 structural conditional increment` 相同

作用：

- 用于对比高信息样本与全国主样本下，结构条件特征的增益是否一致
- 但只作为补充解释线，不取代 `level1` 主结果

## 7. 本轮需要回答的核心问题

完成本轮后，至少要回答以下问题：

1. 在 `level1 baseline` 基础上加入结构/覆盖条件特征后，是否带来稳定提升？
2. 这种提升主要体现在 `regulatory` 还是 `anchored` 任务上？
3. 提升是否主要由 `annual_match_quality_tier` 带动，还是来自更基础的覆盖计数特征？
4. `n_facilities_in_master` 是否继续表现为重要结构代理变量？
5. `level1` 与 `level2` 对同一组结构条件特征的响应是否一致？
6. 当前结果是否支持把结构/覆盖条件特征纳入全国主线正式模型，还是只适合作为解释辅助线？

## 8. 缺失处理要求

### 8.1 数值特征

对于本轮中的数值特征：

- 保留原始缺失
- 在模型 pipeline 中使用中位数填补
- 不在主表中覆盖式改写缺失值

### 8.2 类别特征

对于本轮中的类别特征：

- 保留原始类别
- 在模型 pipeline 中按现有规则处理

### 8.3 关于 `annual_match_quality_tier`

- 它可以进入本轮条件增强实验
- 但文档中必须明确说明：它是年度匹配质量标签，不是环境暴露变量
- 即使它带来明显提升，也不能被写成环境机制发现

## 9. 结果判断标准

完成本轮后，至少要给出以下判断：

1. 结构/覆盖条件特征是否值得纳入第三层全国主线正式模型？
2. 它们的提升是否会明显超过现有 `baseline`？
3. 这些增益更像来自真正可泛化的系统结构信息，还是更像观测制度代理信息？
4. 相比前几轮机制增强实验，本轮结果是否更适合写成“预测辅助增强”，而不是“机制增强”？
5. 当前是否应先进入 treatment summary features 增量实验，还是先收束第三层主线结论？

## 10. 本轮明确禁止事项

本轮禁止：

1. 重新把高稀疏变量（如 `DOC`、`SUVA`、`UV254`、`chloramine`）直接塞进第三层正式实验
2. 在本轮中同时切换树模型、boosting 或超参数优化
3. 把结构/覆盖特征带来的提升写成环境机制发现
4. 把 `level2` 结果重新写成全国主线主结论
5. 跳过 `baseline reference`，直接只比较增强版本
6. 混淆 `annual_match_quality_tier` 与真实环境质量变量

## 11. 本轮输出要求

### 11.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/train_v4_tthm_regulatory_l1_structural_conditional_increment.py`
- `scripts/train_v4_tthm_anchored_l1_structural_conditional_increment.py`
- 如有必要，可扩展 `scripts/v4_tthm_training_common.py`

如补充 `level2` 对照，也可新增对应脚本，但应保持命名清晰。

### 11.2 本地结果目录

本轮结果目录应继续沿用“先按版本、再按任务”结构，建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/V4_5/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/V4_5/tthm_anchored_risk_prediction/`

目录层负责表达 `V4.5`。

文件名应尽量明确体现：

- `level1`
- `structural_conditional_increment`
- `logistic_regression`

### 11.3 文档

至少新增一份 `V4.5` 中文执行文档，建议放在：

- `docs/06_v4/13_v4_5_execution/`

文档必须包括：

- 本轮任务定义
- 样本层级
- 特征组
- 对照链定义
- 缺失处理方式
- validation / test 结果
- 与 `V4.1` 至 `V4.4b` 的对照解释
- 当前仍存在哪些解释边界与争议点

## 12. 完成后的收尾要求

完成本轮后，必须：

1. 更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)
2. 在 `codex.md` 中记录：
   - 更新时间
   - 本轮实验名称
   - 新增脚本
   - 新增文档
   - 关键结果摘要
   - 结构/覆盖条件特征是否值得纳入第三层正式主线
3. 向用户汇报：
   - `V4.5` 是否完成
   - 主实验结果
   - `level1` 与 `level2` 是否出现明显差异
   - 是否建议进入下一轮 treatment summary increment 或收束第三层主线
4. 最后询问用户是否执行 Git 提交与推送

## 13. 一句话任务总结

当前请你执行 `V4.5`，明确目标为：

- 在第三层 `PWS-year` 全国主线 baseline 基础上加入结构/覆盖条件特征
- 继续跑 `tthm_regulatory_exceedance_prediction` 和 `tthm_anchored_risk_prediction`
- 保留严格对照链，区分 baseline、结构条件增强、质量标签贡献与结构代理贡献
- 最终完成脚本、本地结果、中文执行文档和 `codex.md` 的同步更新
