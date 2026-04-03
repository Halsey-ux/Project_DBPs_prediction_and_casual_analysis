# V4.6 PWS-Year Treatment Summary Increment Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_5_PWS_Year_Structural_Conditional_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/13_v4_5_execution/V4_5_PWS_Year_Structural_Conditional_Increment_Execution_Report.md)
- [V4_4_Level2_Free_Chlorine_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/10_v4_4_execution/V4_4_Level2_Free_Chlorine_Increment_Execution_Report.md)
- [V4_4b_Total_Chlorine_Readiness_Audit_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/11_v4_4b_execution/V4_4b_Total_Chlorine_Readiness_Audit_Report.md)

## 1. 当前任务定位

你当前要执行的是 `V4.6` 更新。`V4.6` 的正式主题是：

- `PWS-year treatment summary increment`

这一轮更新的核心目标不是继续追加高稀疏化学变量，也不是切换模型、做树模型或超参数优化，而是：

- 在已经完成 `V4.5 structural conditional increment` 之后，继续检验第三层全国主线是否还能从 treatment summary 特征中获得额外预测信息
- 明确 treatment summary 特征的增益，究竟是独立于 `V4.5` 结构/覆盖条件特征的系统工程背景信号，还是主要重复已有代理信息
- 保持第三层全国主线的实验体系仍然处于“可复现、可比较、可解释的逐步增强实验”轨道

## 2. 必须继承的前序结论

在开始 `V4.6` 之前，你必须接受并沿用以下已确认结论：

1. `V4.1` 已确认：`level1 + baseline_default` 可以作为第三层全国主线起点。
2. `V4.3` 已确认：`TOC` 是当前第三层主线上最可信的机制增强变量，但其主要证据来自 `level2` 机制增强链。
3. `V4.4` 已确认：`free_chlorine` 在 full `level2` 上只有弱边际增益，且数值信号与缺失模式信号无法稳健拆分。
4. `V4.4b` 已确认：`total_chlorine` 当前不具备继续进入第三层正式增量实验的条件。
5. `V4.5` 已确认：结构/覆盖条件特征在 `level1` 全国主线上对 `regulatory` 与 `anchored` 两条任务都带来明显且稳定的预测提升，且主体增益来自覆盖计数与结构条件特征本身，而不是单个 `annual_match_quality_tier`。
6. 因此，`V4.6` 的自然下一步不是继续推进高稀疏水化学变量，而是检验 treatment summary 特征在控制 `baseline` 与 `structural conditional` 后，是否仍提供独立增益。

## 3. 当前实验体系仍需保持的批判性判断

你必须带着以下判断执行 `V4.6`，不能把 treatment summary 特征的提升直接误写成环境机制结论：

### 3.1 第三层主线仍是全国风险识别

- 第三层 `PWS-year` 主表适合做全国主线风险识别与系统级风险画像。
- 它不适合作为精细工艺运行机制表，也不应被写成直接的 DBP 形成机理模型。
- 因此，`V4.6` 的结论应定位为“全国主线是否能从 treatment summary 中获得额外预测增强”，而不是“发现新的处理机制变量”。

### 3.2 treatment summary 更像系统工程背景代理

本轮候选特征不是实时运行状态，也不是全年连续工艺强度指标，而是年度摘要型 treatment 存在性信号：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

因此：

- 即便它们带来预测增益，也不能直接解释为环境机制发现
- 文档中必须明确区分“预测价值”“工程背景价值”与“机制意义”

### 3.3 不能跳过 `V4.5` 对照链

- `V4.5` 已经证明结构/覆盖条件特征能显著提升第三层全国主线表现
- 因此 `V4.6` 不能只跑 `baseline + treatment`，否则无法判断 treatment 的增益是否独立存在
- 必须保留 `baseline`、`structural conditional reference`、`treatment increment`、`structural + treatment combined` 四层对照链

### 3.4 `level1` 与 `level2` 的角色继续区分

- 主实验仍优先围绕 `level1` 全国主线展开
- 如有必要，可补 `level2` 对照，但不得重新让 `level2` 替代全国主线结论

### 3.5 主指标与辅助指标规则继续沿用

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

本轮主实验固定为：

- `level1`

如有必要，可补一个 `level2` 对照版本，但不得让 `level2` 重新替代全国主线。

### 5.3 本轮 treatment 特征组

`V4.6` 的 treatment summary 特征组默认候选为：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

这组特征应命名为类似：

- `treatment_summary_increment_v4_6_1`

你可以微调命名，但必须清晰表达“这是在第三层全国主线对照框架中测试 treatment summary 特征独立增量价值的实验”。

## 6. 本轮必须保留的对照链

`V4.6` 的核心风险不是跑不出结果，而是误把 treatment summary 的工程背景代理信号写成机制发现，或误把其增益与 `V4.5` 的结构/覆盖代理信号混在一起。因此本轮至少必须保留以下 4 组 `level1` 版本：

### 6.1 `level1 baseline reference`

定义：

- 样本：全部 `level1`
- 特征：仅 baseline 4 个特征

作用：

- 作为第三层全国主线最基础参照
- 保证可与 `V4.1` 连续比较

### 6.2 `level1 structural conditional reference`

定义：

- 样本：全部 `level1`
- 特征：沿用 `V4.5 structural_conditional_increment_v4_5_1`

作用：

- 作为 `V4.6` 的正式上位参照
- 用于判断 treatment 增益是否独立于 `V4.5` 已确认的结构/覆盖条件增益

### 6.3 `level1 treatment summary increment`

定义：

- 样本：全部 `level1`
- 特征：`baseline + treatment summary features`

作用：

- 回答 treatment summary 在不加入 `V4.5 structural conditional` 时是否已有独立预测价值

### 6.4 `level1 structural + treatment combined`

定义：

- 样本：全部 `level1`
- 特征：`baseline + structural conditional features + treatment summary features`

作用：

- 回答 treatment summary 在控制 `V4.5` 结构/覆盖条件特征后是否仍有增益
- 识别 treatment 增益是否主要重复已有结构/覆盖代理信息

### 6.5 建议补充的 `level2` 对照

如资源允许，建议补一个 `level2 structural + treatment combined reference`：

- 样本：全部 `level2`
- 特征：与 `level1 structural + treatment combined` 相同

作用：

- 用于对比高信息样本与全国主样本下，treatment summary 的边际增益是否一致
- 但只作为补充解释线，不取代 `level1` 主结果

## 7. 本轮需要回答的核心问题

完成本轮后，至少要回答以下问题：

1. 在 `level1 baseline` 基础上加入 treatment summary 特征后，是否带来稳定提升？
2. treatment summary 的增益，在加入 `V4.5 structural conditional` 后是否仍然存在？
3. 这种增益主要体现在 `regulatory` 还是 `anchored` 任务上？
4. treatment summary 的提升更像系统工程背景信息，还是更像观测制度代理信息的重复表达？
5. `level1` 与 `level2` 对 treatment summary 的响应方向是否一致？
6. 当前结果是否支持把 treatment summary 特征纳入第三层全国主线正式模型，还是只适合作为补充解释线？

## 8. 缺失处理要求

### 8.1 关于 treatment 二值字段

对于 `has_*_process` 系列字段：

- 保留原始缺失
- 不允许把缺失直接覆盖成 `0`
- 不允许把缺失简单解释为“没有该工艺”
- 在模型 pipeline 中按现有二值字段处理规则执行

### 8.2 数值与类别特征

- 基线与结构/覆盖条件特征中的数值列继续使用中位数填补
- 类别列继续沿用现有 pipeline 规则处理
- 不在主表中覆盖式改写缺失值

### 8.3 关于解释边界

- treatment summary 可以进入条件增强实验
- 但文档中必须明确说明：它们是年度 treatment 摘要信号，不是实时运行强度指标
- 即使带来明显提升，也不能被写成环境机制发现

## 9. 结果判断标准

完成本轮后，至少要给出以下判断：

1. treatment summary 特征是否值得纳入第三层全国主线正式模型？
2. 它们的提升是否明显超过 `baseline`，以及是否独立于 `V4.5 structural conditional`？
3. 它们更像来自系统工程背景信号，还是更像对已有结构/覆盖代理信息的重复表达？
4. 相比 `V4.5`，本轮结果是否更适合写成“工程背景辅助增强”，而不是“机制增强”？
5. 当前是否应继续推进第三层主线补充实验，还是先收束第三层全国主线结论？

## 10. 本轮明确禁止事项

本轮禁止：

1. 重新把高稀疏化学变量直接塞进第三层正式实验
2. 在本轮中同时切换树模型、boosting 或超参数优化
3. 把 treatment summary 特征带来的提升写成环境机制发现
4. 把 `level2` 结果重新写成全国主线主结论
5. 跳过 `level1 structural conditional reference`，直接只比较 `baseline + treatment`
6. 把 treatment 缺失直接覆盖为 `0`

## 11. 本轮输出要求

### 11.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/train_v4_tthm_regulatory_l1_treatment_summary_increment.py`
- `scripts/train_v4_tthm_anchored_l1_treatment_summary_increment.py`
- 如有必要，可扩展 `scripts/v4_tthm_training_common.py`

如补充 `level2` 对照，也可新增对应脚本，但应保持命名清晰。

### 11.2 本地结果目录

本轮结果目录应继续沿用“先按版本、再按任务”结构，建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/V4_6/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/V4_6/tthm_anchored_risk_prediction/`

目录层负责表达 `V4.6`。

文件名应尽量明确体现：

- `level1`
- `treatment_summary_increment`
- `logistic_regression`

### 11.3 文档

至少新增一份 `V4.6` 中文执行文档，建议放在：

- `docs/06_v4/15_v4_6_execution/`

文档必须包括：

- 本轮任务定义
- 样本层级
- 特征组
- 对照链定义
- 缺失处理方式
- validation / test 结果
- 与 `V4.1` 至 `V4.5` 的对照解释
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
   - treatment summary 特征是否值得纳入第三层正式主线
3. 向用户汇报：
   - `V4.6` 是否完成
   - 主实验结果
   - treatment 增益在控制 `V4.5 structural conditional` 后是否仍存在
   - 是否建议继续补充第三层实验或先收束第三层主线
4. 最后询问用户是否执行 Git 提交与推送

## 13. 一句话任务总结

当前请你执行 `V4.6`，明确目标为：

- 在第三层 `PWS-year` 全国主线 `level1` 上测试 treatment summary 特征的独立增量价值
- 继续跑 `tthm_regulatory_exceedance_prediction` 和 `tthm_anchored_risk_prediction`
- 保留严格对照链，区分 baseline、`V4.5 structural conditional reference`、treatment summary 增强和 structural+treatment combined
- 最终完成脚本、本地结果、中文执行文档和 `codex.md` 的同步更新
