# V4.4 Free Chlorine Increment Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/06_v4_2_execution/V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md)
- [V4_3_Level2_TOC_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/08_v4_3_execution/V4_3_Level2_TOC_Increment_Execution_Report.md)

## 1. 当前任务定位

你当前要执行的是 `V4.4` 更新。`V4.4` 的正式主题是：

- `第二级样本 free_chlorine increment`

这一轮更新的核心目标不是更换模型，不是做树模型，也不是提前进入超参数优化，而是：

- 在已经完成的 `V4.3` 底座上，检验 `free_chlorine` 是否能在 `pH + alkalinity + TOC` 之外继续带来边际预测信息
- 继续保留严格的对照链，避免把样本筛选效应、缺失模式效应误写成 `free_chlorine` 数值本身的真实增益
- 继续把 `V4` 保持在“可复现、可比较、可解释的逐步增强实验”轨道上

## 2. 必须继承的 `V4.2` 与 `V4.3` 结论

在开始 `V4.4` 之前，你必须接受并沿用以下已确认结论：

1. `V4.2.1` 已确认：在 `第二级样本` 上加入 `pH + alkalinity + missing flags` 后，两条任务线都相对 baseline 获得了稳定提升。
2. `V4.2.2` 已确认：在 `pH + alkalinity` complete-case 子集上，这种提升依然成立，说明增益不太可能仅由 `pH/alkalinity` 缺失模式驱动。
3. `V4.2.2b` 已确认：在 complete-case 子集上删除 `ph_missing_flag` 与 `alkalinity_missing_flag` 后，结果与 `V4.2.2` 完全一致，说明这两个 flag 在对应 complete-case 版本中只是常量列。
4. `V4.3` 已确认：在 `V4.2.1` 底座上加入 `TOC + toc_missing_flag` 后，`anchored` 任务获得了明显且稳定的边际增益，`regulatory` 任务则表现为部分稳定增益。
5. `V4.3` 还已确认：在 `pH + alkalinity + TOC` complete-case 子集上，删除缺失标记后结果与保留缺失标记完全一致，说明 complete-case 子集中的相关 missing flags 只是常量列。
6. 因此，`V4.4` 的最自然起点不是重新从 baseline 做起，而是基于 `V4.3` 的 `mechanistic_stage2_toc_increment` 底座检验 `free_chlorine` 的边际价值。

## 3. 当前实验体系仍需保持的批判性判断

你必须带着以下判断执行 `V4.4`，而不能把当前体系视为无争议的最终结论：

### 3.1 `第二级样本` 仍然只是高信息样本

- `第二级样本` 是高信息样本，不是全国随机抽样的独立研究样本。
- 它的进入规则本身与变量可用性和数据完整性相关。
- 因此，`第二级样本` 上的提升只能解释为“在高信息样本中观察到的增益”，不能直接写成全国主结论。

### 3.2 缺失处理必须继续谨慎

- `V4.2` 与 `V4.3` 已经说明增益不太可能仅由前序变量的 missing pattern 造成。
- 但这不等于已经完全排除样本选择偏差、监测制度偏差与 `free_chlorine` 专属缺失机制。
- 因此 `V4.4` 必须继续保留 complete-case 对照与 missing-pattern 解释边界。

### 3.3 baseline 中的 `n_facilities_in_master` 仍属结构代理特征

- 它当前可以继续保留在 baseline 中。
- 但文档叙述中必须承认它更像结构代理变量，而不是纯机制变量。
- `V4.4` 不需要把这一争议重新扩展成主线，只需延续这一边界。

### 3.4 评价体系可以继续沿用，但必须保留主次关系

- 主指标仍优先使用 `PR-AUC` 与 `ROC-AUC`。
- 可以继续保留 `balanced_accuracy`、`specificity`、`MCC` 与 confusion matrix 相关字段。
- 但本轮不要求重构整套评价框架，只要求沿用现有统一输出格式。

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

本轮至少要继续跑两条正式任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

### 5.2 样本层级

本轮主实验固定为：

- `第二级样本`

本轮不把 `第一级样本` 当作主增强实验层级，也不把 `第三级样本` 当作主实验层级。

### 5.3 本轮主特征组

`V4.4` 的主增强特征组必须建立在 `V4.3` 基础上，并新增 `free_chlorine`：

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

这组特征应命名为类似：

- `mechanistic_stage3_free_chlorine_increment`

你可以微调命名，但必须清晰表达“这是在 `V4.3` 的 `TOC increment` 底座上加入 `free_chlorine` 的增量实验”。

## 6. 本轮必须保留的对照链

`V4.4` 的核心风险不是跑不出结果，而是对照不完整，导致无法解释 `free_chlorine` 是否真的带来边际增益。因此本轮至少必须保留以下 5 组版本：

### 6.1 `第二级样本 baseline reference`

定义：

- 样本：全部 `第二级样本`
- 特征：仅 baseline 4 个特征

作用：

- 作为当前 `第二级样本` 的最基础参照
- 保证可以与 `V4.2`、`V4.3`、`V4.4` 连续比较

### 6.2 `第二级样本 mechanistic stage1 reference`

定义：

- 样本：全部 `第二级样本`
- 特征：沿用 `V4.2.1`，即 `baseline + pH + alkalinity + missing flags`

作用：

- 作为 `V4.2` 的直接对照物
- 防止后续文档跳过 `stage1`

### 6.3 `第二级样本 TOC increment reference`

定义：

- 样本：全部 `第二级样本`
- 特征：沿用 `V4.3`，即 `baseline + pH + alkalinity + missing flags + TOC + toc_missing_flag`

作用：

- 这是 `V4.4` 最关键的直接参照物
- `V4.4` 的问题不是“比 baseline 强不强”，而是“比 `V4.3` 多出来的 `free_chlorine` 有没有额外价值”

### 6.4 `第二级样本 complete-case TOC increment reference`

定义：

- 样本：`pH + alkalinity + TOC + free_chlorine` 同时非缺失的 complete-case 子集
- 特征：仍然使用 `V4.3` 的 TOC increment 特征组，不加入 `free_chlorine`

作用：

- 固定住 `V4.4` complete-case 子样本
- 为 `free_chlorine` complete-case 版本提供直接参照

### 6.5 `第二级样本 complete-case free_chlorine increment`

定义：

- 样本：`pH + alkalinity + TOC + free_chlorine` 同时非缺失
- 特征：`V4.4` 主特征组

作用：

- 检查 `free_chlorine` 在完整观测子集上是否仍保留增益
- 避免把 `free_chlorine_missing_flag` 或 complete-case 筛选效应误写成 `free_chlorine` 数值增益

## 7. 需要执行的补充实验

### 7.1 complete-case 去掉 missing flags 的敏感性版本

如时间与计算成本允许，建议补一个与 `V4.3` 完全对应的版本：

- 样本：`pH + alkalinity + TOC + free_chlorine` complete-case 子集
- 特征：删除 `ph_missing_flag`、`alkalinity_missing_flag`、`toc_missing_flag`、`free_chlorine_missing_flag`

作用：

- 验证 complete-case 子集中的 missing flags 是否同样只是常量列
- 让后续文档表述更干净

### 7.2 如有余力，可保留 `baseline_without_n_facilities` 轻量参照

这不是 `V4.4` 的主线任务。

如果你已有复用好的实现，可以顺带保留：

- `baseline_with_n_facilities`
- `baseline_without_n_facilities`

但不能让这条支线喧宾夺主。

## 8. 缺失处理要求

### 8.1 主实验版本

对于 `V4.4` 主实验版本：

- 保留 `第二级样本` 样本
- 对数值变量做中位数填补
- 保留 `ph_missing_flag`
- 保留 `alkalinity_missing_flag`
- 保留 `toc_missing_flag`
- 保留 `free_chlorine_missing_flag`

### 8.2 complete-case 版本

对于 `V4.4` complete-case 版本：

- 仅保留以下 4 个变量同时非缺失的样本：
  - `ph_sample_weighted_mean`
  - `alkalinity_sample_weighted_mean_mg_l`
  - `toc_sample_weighted_mean_mg_l`
  - `free_chlorine_sample_weighted_mean_mg_l`

你必须明确写清：

- 主实验版本允许缺失存在，并显式保留缺失模式信息
- complete-case 版本用于判断 `free_chlorine` 的增益是否仍然成立
- 两者关系与 `V4.3` 类似，只是 complete-case 的变量范围扩大到了 `free_chlorine`

## 9. 结果判断标准

完成本轮后，至少要回答以下问题：

1. 在 `V4.3` 基础上加入 `free_chlorine + free_chlorine_missing_flag` 后，是否带来稳定提升？
2. 提升主要体现在 `regulatory` 还是 `anchored` 任务上？
3. 在 `pH + alkalinity + TOC + free_chlorine` complete-case 子集上，这个提升是否仍然存在？
4. 当前增益更像来自：
   - `free_chlorine` 真实数值信号
   - `free_chlorine_missing_flag`
   - 样本选择效应
   - 三者混合
5. 新增 `free_chlorine` 后，`V4.2` 与 `V4.3` 结论是否保持稳定？

## 10. 本轮明确禁止事项

本轮禁止：

1. 直接引入 `total_chlorine`
2. 直接跳到树模型或 boosting 模型
3. 提前做超参数优化
4. 把 `第二级样本` 结果直接写成全国主线最终结论
5. 把 `free_chlorine` 的预测增益直接解释成机制定论或因果发现
6. 跳过 `TOC increment reference`，只拿 `V4.4` 与 baseline 比较
7. 把 `free_chlorine_missing_flag` 带来的效应未经检验就写成 `free_chlorine` 数值本身的贡献

## 11. 本轮输出要求

### 11.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/train_v4_tthm_regulatory_l2_free_chlorine_increment.py`
- `scripts/train_v4_tthm_anchored_l2_free_chlorine_increment.py`
- 如有必要，可扩展 `scripts/v4_tthm_training_common.py`

### 11.2 本地结果目录

本轮结果目录应继续沿用“先按版本、再按任务”结构，建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/V4_4/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/V4_4/tthm_anchored_risk_prediction/`

目录层负责表达 `V4.4`。

文件名应尽量明确体现：

- `第二级样本`
- `free_chlorine_increment`
- `logistic_regression`

### 11.3 文档

至少新增一份 `V4.4` 中文执行文档，建议放在：

- `docs/06_v4/10_v4_4_execution/`

文档必须包括：

- 本轮任务定义
- 样本层级
- 特征组
- 对照链定义
- 缺失处理方式
- validation / test 结果
- 与 `V4.2`、`V4.3` 的对照解释
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
   - `free_chlorine` 是否带来边际增益
3. 向用户汇报：
   - `V4.4` 是否完成
   - 主实验结果
   - complete-case 稳健性结果
   - 是否建议进入下一轮 `total_chlorine` 或其他变量
4. 最后询问用户是否执行 Git 提交与推送

## 13. 一句话任务总结

当前请你执行 `V4.4`，明确目标为：

- 在 `V4.3` 的 `第二级样本 TOC increment` 底座上加入 `free_chlorine + free_chlorine_missing_flag`
- 继续跑 `tthm_regulatory_exceedance_prediction` 和 `tthm_anchored_risk_prediction`
- 同时保留 `baseline reference`、`mechanistic stage1 reference`、`TOC increment reference`、`complete-case reference` 和必要的 no-missing-flags 敏感性检查
- 最终完成脚本、结果、中文文档和 `codex.md` 的同步更新
