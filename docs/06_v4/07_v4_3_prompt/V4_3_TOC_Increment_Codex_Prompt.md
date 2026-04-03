# V4.3 TOC Increment Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/06_v4_2_execution/V4_2_Level2_Mechanistic_Core_Stage1_Execution_Report.md)

## 1. 当前任务定位

你当前要执行的是 `V4.3` 更新。`V4.3` 的正式主题是：

- `level2 TOC increment`

这轮更新的核心目标不是更换模型，不是追求调参，也不是扩展到更多变量，而是：

- 在已经完成的 `V4.2` 基础上，检验 `TOC` 是否能够在 `pH + alkalinity` 的基础上继续带来稳定增量信息
- 继续保持严格的对照链，避免把样本筛选效应、缺失模式效应误写成变量真实增益
- 继续把 `V4` 保持在“可复现、可比较、可解释的逐步增强实验”轨道上

## 2. 必须继承的 V4.2 结论

在开始 `V4.3` 之前，你必须接受并沿用以下 `V4.2` 结论：

1. `V4.2.1` 已确认：在 `level2` 上加入 `pH + alkalinity + missing flags` 后，两条任务线都相对各自对照版获得稳定提升
2. `V4.2.2` 已确认：在 `pH + alkalinity` 完整子集上，这种提升仍然成立，说明增益不太可能仅由 missing pattern 驱动
3. `V4.2.2b` 已确认：在 complete-case 子集上删除 `ph_missing_flag` 和 `alkalinity_missing_flag` 后，结果与原 `V4.2.2` 完全一致，说明这两个 flag 在 complete-case 版本中只是冗余常量列
4. 因此，`V4.3` 的最自然起点不是重新从 baseline 做起，而是在 `V4.2.1` 的机制底座上检验 `TOC` 的边际增益

## 3. 当前实验体系是否存在需要改进的地方

你必须带着以下批判性判断进入 `V4.3`，而不是把当前体系视为无争议正确：

### 3.1 `level2` 不是纯机制样本

- `level2` 是“高信息样本”，不是随机抽样的独立研究样本
- 它的进入规则本身与变量可用性和数据完整性相关
- 因此，`level2` 上的提升只能解释为“在高信息样本中观测到的增益”，不能直接写成全国主线最终结论

### 3.2 缺失处理仍需保持谨慎

- `V4.2` 已经说明增益不太可能仅来自缺失模式
- 但这不等于已经完全排除样本选择偏差或监测制度偏差
- 因此 `V4.3` 仍必须保留 complete-case 对照和 missing-pattern 解释边界

### 3.3 baseline 仍有争议点

- `n_facilities_in_master` 更像系统结构代理变量，而不是纯机制变量
- 它当前可以保留在 baseline 中
- 但在文档表述上必须承认它属于“结构代理特征”，而非毫无争议的环境机制特征

### 3.4 当前评价体系还可以增强

- 主指标仍应优先使用 `PR-AUC` 和 `ROC-AUC`
- 但后续可以补充 `balanced_accuracy`、`specificity`、`MCC` 与 confusion matrix
- 本轮 `V4.3` 不强制一次性重构所有评价脚本，但至少要为后续升级留出清晰接口

## 4. 本轮总原则

1. 原始数据只读，不允许原位修改
2. 仅基于第三层 `V4_pws_year_ml_ready.csv` 执行
3. 统一通过 [io_v4_ml_ready.py](D:/Project_DBPs_prediction_and_casual_analysis/scripts/io_v4_ml_ready.py) 读取数据
4. 统一复用当前 `group_by_pwsid` 切分，不重新随机切分
5. 默认模型继续使用 `LogisticRegression`
6. 当前不做树模型、不做 boosting、不做超参数优化
7. 当前不保存模型文件
8. 所有新增或更新的 `.md` 文档必须使用中文
9. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)
10. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送

## 5. 本轮正式实验定义

### 5.1 主任务

本轮至少要继续跑两条正式任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

### 5.2 样本层级

本轮主实验固定为：

- `level2`

本轮不把 `level1` 当作主增强实验层级，不把 `level3` 当作主实验层级。

### 5.3 本轮主特征组

`V4.3` 的主增强版特征组应建立在 `V4.2.1` 基础上，并增量加入 `TOC`：

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

这组特征应命名为类似：

- `mechanistic_stage2_toc_increment`

你可以微调命名，但必须清晰表达“这是在 `V4.2.1` 底座上加入 `TOC` 的增量实验”。

## 6. 本轮必须保留的对照链

`V4.3` 最大的风险不是跑不出结果，而是对照不完整，导致无法解释 `TOC` 是否真的带来边际增益。因此本轮必须至少保留以下 4 组版本：

### 6.1 `level2 baseline reference`

定义：

- 样本：全部 `level2`
- 特征：仅 baseline 4 个特征

作用：

- 作为当前 `level2` 主对照
- 保证可以和 `V4.2.1`、`V4.3.1` 继续比较

### 6.2 `level2 mechanistic stage1 reference`

定义：

- 样本：全部 `level2`
- 特征：沿用 `V4.2.1`，即 `baseline + pH + alkalinity + missing flags`

作用：

- 它是 `V4.3` 最关键的直接参照物
- `V4.3` 的问题不是“比 baseline 强不强”，而是“比 `V4.2.1` 多出来的 `TOC` 有没有额外价值”

### 6.3 `level2 complete-case mechanistic stage1 reference`

定义：

- 样本：`pH + alkalinity + TOC` 同时非缺失的 complete-case 子集
- 特征：仍使用 `V4.2.1` 的特征组，不加入 `TOC`

作用：

- 固定住 complete-case 子集样本
- 为 `V4.3` 的 complete-case 版本提供直接参照

### 6.4 `level2 complete-case TOC increment`

定义：

- 样本：`pH + alkalinity + TOC` 同时非缺失
- 特征：`V4.3` 主特征组

作用：

- 检查 `TOC` 在完整观测子集上是否仍保留增益
- 避免把 `toc_missing_flag` 或 complete-case 筛选效应误写成 `TOC` 数值增益

## 7. 需要执行的补充实验

### 7.1 complete-case 去掉 missing flags 的敏感性版本

如果时间与计算成本允许，建议补一个与 `V4.2.2b` 对应的版本：

- 样本：`pH + alkalinity + TOC` complete-case 子集
- 特征：删除 `ph_missing_flag`、`alkalinity_missing_flag`、`toc_missing_flag`

作用：

- 验证 complete-case 子集中的 missing flags 是否同样只是冗余常量列
- 让后续文档表述更干净

### 7.2 baseline 去掉 `n_facilities_in_master` 的小型敏感性检查

这个不是 `V4.3` 必做主线，但如果你有余力，建议补一个轻量检查：

- `baseline_with_n_facilities`
- `baseline_without_n_facilities`

作用：

- 排查 `n_facilities_in_master` 是否对 baseline 表现有过强影响
- 为后续 baseline 争议提供证据

## 8. 缺失处理要求

### 8.1 主实验版本

对于 `V4.3` 主实验版本：

- 保留 `level2` 样本
- 对数值变量做中位数填补
- 保留 `ph_missing_flag`
- 保留 `alkalinity_missing_flag`
- 保留 `toc_missing_flag`

### 8.2 complete-case 版本

对于 `V4.3` complete-case 版本：

- 仅保留 `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`

三者同时非缺失的样本。

你必须明确写清：

- 主实验版本允许缺失存在，并显式保留缺失模式信息
- complete-case 版本用于判断增益是否仍然成立
- 两者的关系与 `V4.2.1 / V4.2.2` 类似，但变量范围扩大到了 `TOC`

## 9. 结果判断标准

完成本轮后，至少要回答以下问题：

1. 在 `V4.2.1` 基础上加入 `TOC + toc_missing_flag` 后，是否带来稳定提升？
2. 提升主要体现在 `regulatory` 还是 `anchored` 任务上？
3. 在 `pH + alkalinity + TOC` 完整子集上，这个提升是否仍然存在？
4. 当前增益更像来自：
   - `TOC` 真实数值信号
   - `toc_missing_flag`
   - 样本选择效应
   - 三者混合
5. 新增 `TOC` 后，原有 `V4.2` 结论是否保持稳定？

## 10. 本轮明确禁止事项

本轮禁止：

1. 直接跳到 `free_chlorine`
2. 直接引入 `total_chlorine`
3. 直接切换树模型或 boosting 模型
4. 提前做超参数优化
5. 把 `level2` 结果直接写成全国主线最终结论
6. 把 `TOC` 的预测增益直接解释成机制定论或因果发现
7. 跳过 `mechanistic stage1 reference` 而只拿 `V4.3` 与 baseline 比较

## 11. 本轮输出要求

### 11.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/train_v4_tthm_regulatory_l2_toc_increment.py`
- `scripts/train_v4_tthm_anchored_l2_toc_increment.py`
- 如有必要，可扩展 `scripts/v4_tthm_training_common.py`

### 11.2 本地结果目录

本轮结果目录不再建议直接平铺写入旧的按任务目录，而应先在实验总目录下新增 `V4_3` 版本层，再在其下按任务分目录。

建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/V4_3/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/V4_3/tthm_anchored_risk_prediction/`

这样做的原因是：

- 将 `V4.2` 与 `V4.3` 的结果物理隔离，避免不同子版本结果混放
- 让结果目录结构与 `docs/06_v4` 下按版本分层的文档结构保持一致
- 便于后续继续扩展 `V4.4`、`V4.5` 等版本，而不是把所有实验都堆叠在同一任务目录下

因此：

- 目录负责表达 `V4.3`
- 文件名主要负责表达具体实验配置

并在文件名中明确体现：

- `level2`
- `toc_increment`
- `logistic_regression`

如有必要，也可以在文件名中保留 `V4.3`，但不强制，因为目录层已经承担了版本表达功能。

### 11.3 文档

至少新增一份 `V4.3` 中文执行文档，建议放在：

- `docs/06_v4/08_v4_3_execution/`

文档必须包括：

- 本轮任务定义
- 样本层级
- 特征组
- 对照链定义
- 缺失处理方式
- validation / test 结果
- 与 `V4.2` 的对照解释
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
   - `TOC` 是否带来边际增益
3. 向用户汇报：
   - `V4.3` 是否完成
   - 主实验结果
   - complete-case 稳健性结果
   - 是否建议进入下一轮 `free_chlorine`
4. 最后询问用户是否执行 Git 提交与推送

## 13. 一句话任务总结

当前请你执行 `V4.3`，明确目标为：

- 在 `V4.2.1` 的 `level2 mechanistic stage1` 底座上，加入 `TOC + toc_missing_flag`
- 继续跑 `tthm_regulatory_exceedance_prediction` 和 `tthm_anchored_risk_prediction`
- 同时保留 `mechanistic stage1 reference`、complete-case reference 和必要的敏感性检查
- 最终完成脚本、结果、中文文档和 `codex.md` 的同步更新
