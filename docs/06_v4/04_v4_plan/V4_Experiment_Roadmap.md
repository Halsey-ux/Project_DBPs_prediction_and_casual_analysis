# V4 Experiment Roadmap

## 1. 文档定位

本文档用于把 `V4` 阶段后续实验按照推进顺序正式冻结为版本化路线图。

本文档回答以下问题：

- `V4.1` 到底包含了什么
- `V4.2` 之后应该先做哪些实验
- 每一轮实验分别用什么样本层级
- 每一轮实验分别加入哪些 `X`
- 每一轮实验要回答什么问题
- 每一轮实验的结果如何判断是否进入下一轮
- 什么时候开始比较模型、什么时候开始调参、什么时候开始保存模型

本文档是 `V4` 的实验方案计划书，不是某一轮实验的运行日志。

## 2. 当前 V4 的总原则

后续 `V4` 实验统一遵守以下原则：

1. 先固定任务和切分制度，再逐步扩展特征，不直接在多个维度同时发散
2. 先做特征维度扩展，再做模型维度比较，最后才进入超参数优化
3. `level1` 用于全国主线 baseline
4. `level2` 用于增强变量主实验
5. `level3` 用于高信息、小样本、稳健性与专题实验
6. 真实环境/机制变量优先于质控/覆盖变量进入扩展序列
7. 质控/覆盖变量可以进入预测增强实验，但不直接作为环境机制解释依据
8. `has_*_process` 默认不进入第一轮主模型，只作为后续条件实验
9. 所有实验必须复用当前固定的 `group_by_pwsid` 切分制度
10. 所有实验都必须输出统一结果表，禁止只保留终端输出

## 3. 当前正式任务

当前 `V4` 默认沿两条主分类任务推进：

### 3.1 `tthm_regulatory_exceedance_prediction`

- `Y = tthm_regulatory_exceed_label`
- `1` 表示 `TTHM >= 80 ug/L`
- `0` 表示 `TTHM < 80 ug/L`

### 3.2 `tthm_anchored_risk_prediction`

- 先保留两端样本：
  - `TTHM <= 40 ug/L`
  - `TTHM >= 80 ug/L`
- `Y = tthm_anchored_risk_label`
- `1` 表示 `>= 80 ug/L`
- `0` 表示 `<= 40 ug/L`

说明：

- `80 ug/L` 是法规超标端
- `40 ug/L` 是研究型 low-risk anchor，不是法定低风险阈值

## 4. 样本层级使用规则

### 4.1 `level1`

- 定义：目标可用的全国主线样本
- 用途：第一轮主结果、baseline、主分类任务
- 当前定位：广覆盖主样本

### 4.2 `level2`

- 定义：在 `level1` 基础上，`n_core_vars_available >= 2`
- 用途：增强变量主实验
- 当前定位：中高信息增强样本

### 4.3 `level3`

- 定义：在 `level1` 基础上，`n_core_vars_available >= 3`
- 用途：高信息稳健性和专题实验
- 当前定位：高信息小样本验证层

## 5. 特征组分层

### 5.1 `baseline_default`

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

### 5.2 `mechanistic_core_stage1`

在 `baseline_default` 基础上增加：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

### 5.3 `mechanistic_core_stage2`

在 `mechanistic_core_stage1` 基础上增加：

- `toc_sample_weighted_mean_mg_l`
- `toc_missing_flag`

### 5.4 `mechanistic_core_stage3`

在 `mechanistic_core_stage2` 基础上增加：

- `free_chlorine_sample_weighted_mean_mg_l`
- `free_chlorine_missing_flag`

### 5.5 `qc_coverage_conditional`

- `months_observed_any`
- `tthm_months_with_data`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`

### 5.6 `treatment_conditional`

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

### 5.7 `enhanced_conditional_high_missing`

- `total_chlorine_sample_weighted_mean_mg_l`
- `total_chlorine_missing_flag`
- `annual_match_quality_tier`

## 6. 统一执行规则

每一轮实验都默认遵守以下规则：

### 6.1 切分规则

- 统一使用 `group_by_pwsid`
- 统一复用当前已生成的 train / validation / test
- 非明确说明，不重新随机切分

### 6.2 默认模型规则

在进入模型比较阶段前，默认模型固定为：

- `LogisticRegression`

### 6.3 缺失处理规则

在使用增强变量时，默认优先采用：

- 数值列填补
- 显式 missing flag

只有在完整子集稳健性实验中，才单独改为 complete-case 版本。

### 6.4 输出规则

每一轮实验至少输出：

- 结果表 `csv`
- 当前实验所用特征清单
- 当前实验的样本量与正类数量
- validation/test 指标
- 实验版本说明

## 7. V4 版本化实验路线

下面按版本顺序固定后续推进路线。

### 7.1 `V4.1` 已完成：Baseline Start

#### 目标

建立全国主线第一轮 baseline，并打通正式训练链条。

#### 样本层级

- `level1`

#### 任务

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

#### X

- `baseline_default`

#### 模型

- `LogisticRegression`

#### 当前已知结果

- regulatory test `PR-AUC = 0.068959`
- regulatory test `ROC-AUC = 0.704565`
- anchored test `PR-AUC = 0.116178`
- anchored test `ROC-AUC = 0.745176`

#### 当前结论

- baseline 已成立
- 锚点任务比法规任务更容易学习
- 可以进入后续特征扩展实验

---

### 7.2 `V4.2`：L2 Stage1 Mechanistic Core

#### 目标

测试最基础的两项核心水质变量是否带来稳定增益。

#### 样本层级

- 主实验：`level2`

#### 任务

- 优先先跑 `tthm_regulatory_exceedance_prediction`
- 再跑 `tthm_anchored_risk_prediction`

#### X

- `baseline_default`
- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

#### 为什么加 missing flag

因为 `pH` 和 `alkalinity` 在 `level2` 中仍可能存在缺失。  
当前默认不是只保留完整样本，而是：

- 保留 `level2` 样本
- 对数值做填补
- 用 missing flag 告诉模型哪些值原本缺失

#### 同轮补充稳健性检查

建议同时补一个完整子集版：

- 只保留 `pH` 和 `alkalinity` 同时非缺失的 `level2` 子集

#### 回答的问题

- 最基础的两项核心水质变量是否能稳定提升 baseline？
- 提升主要来自变量值本身，还是主要来自缺失模式？

#### 进入下一轮的条件

- 至少一个主任务在 validation/test 上相对 `V4.1` 有稳定提升
- 结果不会因为样本骤减而完全失真

---

### 7.3 `V4.3`：L2 Stage2 Add TOC

#### 目标

测试 `TOC` 作为有机前体变量是否带来额外增益。

#### 样本层级

- 主实验：`level2`

#### X

- `V4.2` 全部特征
- `toc_sample_weighted_mean_mg_l`
- `toc_missing_flag`

#### 同轮补充稳健性检查

建议补一个完整子集版：

- 只保留 `pH`、`alkalinity`、`TOC` 同时非缺失的 `level2` 子集

#### 回答的问题

- `TOC` 是否在已有 `pH + alkalinity` 的基础上继续带来增益？
- 增益是否只发生在缺失模式层，而不是变量值层？

#### 进入下一轮的条件

- `TOC` 加入后至少一个主任务继续有稳定增益
- 若增益非常弱，可考虑保留为 conditional，不再继续堆叠

---

### 7.4 `V4.4`：L2 Stage3 Add Free Chlorine

#### 目标

测试与消毒过程更相关的 `free_chlorine` 是否还能提升模型。

#### 样本层级

- 主实验：`level2`

#### X

- `V4.3` 全部特征
- `free_chlorine_sample_weighted_mean_mg_l`
- `free_chlorine_missing_flag`

#### 同轮补充稳健性检查

建议补一个完整子集版：

- 只保留 `pH`、`alkalinity`、`TOC`、`free_chlorine` 同时非缺失的 `level2` 子集

#### 回答的问题

- 当加入更接近消毒过程的变量后，模型是否还能进一步提升？
- 提升是来自真实水质信息，还是主要来自缺失模式？

#### 进入下一轮的条件

- 结果较 `V4.3` 仍有明确增益
- 或至少在 anchored 任务上体现出更清晰边界

---

### 7.5 `V4.5`：L1 QC and Coverage Conditional

#### 目标

在全国主线样本上测试质控/覆盖变量是否带来预测增益。

#### 样本层级

- `level1`

#### X

- `baseline_default`
- `qc_coverage_conditional`

#### 解释边界

这一轮实验的目的是评估预测增益，不是做环境机制解释。  
这些变量只能解释为：

- 观测覆盖
- 信息完整度
- 数据可用性模式

不能解释为：

- 真实化学机制

#### 回答的问题

- 质控/覆盖变量是否能显著提升风险预测？
- 它们的增益相对真实水质变量增益，哪个更强？

#### 进入下一轮的条件

- 若预测增益明显，则保留这组变量为“预测增强模型”专用输入
- 但不自动升级为主解释模型输入

---

### 7.6 `V4.6`：L1 Treatment Conditional

#### 目标

测试 treatment 摘要信号是否具有额外预测价值。

#### 样本层级

- `level1`

#### X

- `baseline_default`
- `treatment_conditional`

#### 解释边界

`has_*_process` 是年度 treatment 摘要信号，不是实时运行状态。  
缺失不等于明确没有工艺。

#### 回答的问题

- 低维 treatment 信号是否带来稳定增益？
- 它们的增益是否足够稳定，值得保留为补充预测变量？

#### 进入下一轮的条件

- 若稳定增益明显，可保留进预测增强模型
- 若不稳定，则仅保留在表中，不进入后续主实验

---

### 7.7 `V4.7`：L2 Mechanistic Core vs QC Comparison

#### 目标

直接比较“真实机制变量增益”和“质控/覆盖变量增益”。

#### 样本层级

- `level2`

#### 设计

至少比较以下 3 组：

1. `baseline_default + mechanistic_core_stage3`
2. `baseline_default + qc_coverage_conditional`
3. `baseline_default + mechanistic_core_stage3 + qc_coverage_conditional`

#### 回答的问题

- 模型提升到底更依赖真实水质变量，还是更依赖信息覆盖变量？
- 如果两者同时加入，增益来源结构如何变化？

#### 解释规则

- 若 `qc_coverage` 增益明显大于机制变量，不应把这一轮结果写成“化学机制发现”

---

### 7.8 `V4.8`：L3 High-Information Sensitivity

#### 目标

在高信息样本中做更高强度稳健性检查。

#### 样本层级

- `level3`

#### X

优先使用：

- `baseline_default`
- `mechanistic_core_stage3`

若样本允许，再试：

- `enhanced_conditional_high_missing`

#### 回答的问题

- 在更高信息的小样本里，前面 `L2` 上的增强结论还成立吗？
- 更完整的增强变量组合是否在高信息层才表现出真正价值？

#### 解释规则

- `L3` 结果只作高信息验证，不替代全国主线结论

---

### 7.9 `V4.9`：Model Family Comparison

#### 目标

在已经较稳定的特征组上比较模型家族，而不是继续只用 `LogisticRegression`。

#### 前提

只有当 `V4.2` 至 `V4.8` 基本跑通后，才进入本轮。

#### 候选模型

1. `LogisticRegression`
2. `RandomForest`
3. `HistGradientBoosting`
4. 需要时再进入 `XGBoost` / `LightGBM`

#### 对比方式

固定：

- 同一任务
- 同一 level
- 同一特征组
- 同一 split

只改变模型。

#### 回答的问题

- 当前问题是否主要需要线性模型即可
- 更复杂模型是否带来真实增益

---

### 7.10 `V4.10`：Hyperparameter Tuning and Model Persistence

#### 目标

在较优任务、较优特征组、较优模型家族上做正式调参与模型保存。

#### 进入条件

必须满足以下条件后才能进入：

1. baseline 已稳定
2. 关键特征组已比较清楚
3. 模型家族比较已完成
4. 已能明确选出阶段最佳候选模型

#### 当前调参优先级

优先调：

- `LogisticRegression` 的 `C`、`class_weight`、决策阈值

后续再调：

- 树模型深度
- boosting 学习率
- 正则和采样参数

#### 模型保存规则

从本轮开始，阶段最佳模型应正式保存。

建议至少保存：

- 模型文件（如 `.joblib`）
- 特征清单
- split 文件版本
- 结果表
- 当前脚本版本说明

#### 回答的问题

- 当前阶段最佳模型到底是哪一个
- 是否值得冻结为正式 V4 主模型版本

## 8. 当前推荐推进顺序

当前建议严格按以下顺序推进：

1. `V4.1` 已完成
2. `V4.2`
3. `V4.3`
4. `V4.4`
5. `V4.5`
6. `V4.6`
7. `V4.7`
8. `V4.8`
9. `V4.9`
10. `V4.10`

## 9. 当前最重要的执行判断

当前阶段最不应该做的是：

- 同时换任务、换特征、换模型、换超参数

当前最应该坚持的是：

- 一次只改变一个主要因素
- 每轮实验都保留和上一轮的清晰对照
- 把真实机制变量和质控/覆盖变量分开解释

## 10. 一句话总结

当前 `V4` 后续路线应按：

- `V4.1` baseline 起点
- `V4.2 - V4.4` 真实核心水质变量递进增强
- `V4.5 - V4.6` 质控/覆盖与 treatment 条件实验
- `V4.7 - V4.8` 增益归因与高信息稳健性检查
- `V4.9 - V4.10` 模型比较、调参与模型保存

这一顺序逐步推进，而不是一开始就全面发散。
