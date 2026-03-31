# V4 Training Protocol

- 更新时间：2026-03-31 13:10（Asia/Hong_Kong）
- 适用阶段：V4 正式机器学习阶段
- 当前主线对象：`TTHM`
- 当前正式输入表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V4_Chapter1_Part1_ML_Ready\V4_pws_year_ml_ready.csv`
- 当前统一读取入口：`D:\Project_DBPs_prediction_and_casual_analysis\scripts\io_v4_ml_ready.py`

## 1. 文档定位

本文件是 V4 阶段的总实验协议，用于统一约束后续 `TTHM` 主线机器学习实验的任务体系、样本体系、数据切分方式、特征制度、缺失处理边界、评价指标、结果记录制度与版本维护方式。

本文件不是某一次单独实验的运行记录，也不是某一个模型的超参数说明。它的作用是：

- 固定后续 V4 全阶段都应遵守的总规则
- 防止不同实验之间口径漂移
- 为后续每一次单独实验细则和对应脚本提供上位规则

## 2. 适用范围

当前本文件只约束：

- 第三层 `pwsid + year` 粒度的全国主模型线
- `TTHM` 主线
- 基于 `V4_pws_year_ml_ready.csv` 的建模实验

当前本文件不直接约束：

- 第二层 `facility-month` 机制补充线
- `HAA5` 平行主线
- 因果分析
- 纯描述性统计分析

后续若将 `HAA5` 或第二层主线纳入 V4，应新增对应协议，或在本文件中单独扩展新章节，而不是直接混写到当前 `TTHM` 总协议中。

## 3. V4 总体目标

V4 阶段的总体目标不是立刻追求最优模型分数，而是建立一套可复现、可比较、可逐步扩展的正式机器学习实验体系。

当前阶段目标包括：

- 把 `V4_pws_year_ml_ready.csv` 正式转化为可建模的训练 / 验证 / 测试工作流
- 固定 `TTHM` 主线的正式任务、样本层级、特征制度与评价指标
- 先跑通 `level1 + baseline` 全国主模型主线
- 再评估条件候选变量和增强变量是否带来稳定且可解释的增益

当前阶段明确不追求：

- 直接把高信息样本模型当作全国主线结论
- 直接把模型增益解释为因果机制发现
- 在训练制度尚未固定前反复进行复杂调参

## 4. 数据入口与 IO 规则

### 4.1 正式输入表

当前唯一正式输入表为：

- `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`

### 4.2 正式读取入口

后续所有 V4 建模脚本必须通过以下统一入口读取数据：

- `scripts/io_v4_ml_ready.py`

当前禁止后续训练脚本直接裸用：

```python
pd.read_csv(...)
```

原因：

- `CSV` 不保存 pandas dtype 元信息
- 若不经过统一 schema 恢复，标签列、二值状态列和整数计数列会发生类型漂移
- 类型漂移会直接影响后续特征处理、缺失处理和模型训练逻辑

### 4.3 当前正式 schema 含义

统一读取入口至少保证以下规则：

- `tthm_regulatory_exceed_label`、`tthm_warning_label` 读回后恢复为 `Int8`
- `has_*_process` 系列字段读回后恢复为 `Int8`
- `tthm_months_with_data`、`months_with_*`、`n_core_vars_available` 恢复为 `Int64`
- 标签缺失规则再次校验
- 主键唯一性再次校验

## 5. 正式任务体系

当前 V4 不再采用“阶段 A 探索、阶段 B 正式预测”的双阶段入口。  
当前正式任务体系直接固定为两个 `TTHM` 分类主任务和一个连续值回归补充任务。

### 5.1 任务 1：`tthm_regulatory_exceedance_prediction`

- 任务性质：法规超标预测
- 样本范围：所有 `level1` 可用样本
- 目标列：`tthm_regulatory_exceed_label`
- 正类定义：`tthm_sample_weighted_mean_ug_l >= 80`
- 负类定义：`tthm_sample_weighted_mean_ug_l < 80`

这个任务学习的是：

- 哪些系统-年份更容易跨过法规超标边界

这个任务回答的是：

- 哪些系统-年份更可能进入法规意义上的超标状态

### 5.2 任务 2：`tthm_anchored_risk_prediction`

- 任务性质：研究型锚点风险预测
- 样本范围：仅保留两端样本
- 目标列：`tthm_anchored_risk_label`
- 正类定义：`tthm_sample_weighted_mean_ug_l >= 80`
- 负类定义：`tthm_sample_weighted_mean_ug_l <= 40`
- 灰区处理：`40 < tthm_sample_weighted_mean_ug_l < 80` 不进入该任务训练

这个任务学习的是：

- 明显高端样本与明显低端样本之间的清晰差异模式

这个任务回答的是：

- 如果把灰区先拿掉，模型能否更稳定地识别高低两端样本

### 5.3 任务 3：`tthm_regression`

- 任务性质：连续值回归
- 样本范围：所有 `level1` 可用样本
- 目标列：`tthm_sample_weighted_mean_ug_l`

这个任务学习的是：

- 系统-年份 `TTHM` 连续水平的变化模式

这个任务回答的是：

- 在连续暴露尺度上，系统之间为何存在高低差异

### 5.4 当前任务优先级

当前建议的正式实验顺序为：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`
3. `tthm_regression`

原因：

- 法规超标任务最贴近论文主问题和监管语境
- 锚点任务适合作为边界更干净的补充分类实验
- 回归任务保留连续信息，但评价与解释口径不同，放在分类主线稳定后再展开更合理

## 6. 阈值口径与法规边界

### 6.1 高风险端

当前正式固定：

- `TTHM 80 ug/L` 为联邦法规 `MCL`

因此 `>= 80 ug/L` 可以直接作为法规超标端。

### 6.2 低风险锚点端

当前正式固定：

- `TTHM 40 ug/L` 不是联邦法规定义的低风险健康标准
- `TTHM 40 ug/L` 是参考 EPA Stage 2 DBPR 中 reduced monitoring / 40-30 certification 相关管理门槛后设定的研究型 low-risk anchor

因此：

- `<= 40 ug/L` 可以作为研究设计中的低风险锚点
- 但不得在文档、代码或结果中误写为“EPA 法规定义的低风险阈值”

### 6.3 当前阈值解释边界

必须明确：

- `>= 80` 是法规超标端
- `<= 40` 是研究型低风险锚点端
- `40–80` 是当前锚点任务中的灰区

## 7. 样本层级体系

### 7.1 `level1`

- 筛选条件：`level1_flag = 1`
- 定义：目标变量非缺失
- 当前数量：`199,802`
- 定位：全国广覆盖主线样本

`level1` 是当前第一版全国主模型的默认主线层级。

### 7.2 `level2`

- 筛选条件：`level2_flag = 1`
- 定义：在 `level1` 基础上，`n_core_vars_available >= 2`
- 当前数量：`26,975`
- 定位：增强模型与机制变量增益测试样本

### 7.3 `level3`

- 筛选条件：`level3_flag = 1`
- 定义：在 `level1` 基础上，`n_core_vars_available >= 3`
- 当前数量：`6,193`
- 定位：高信息稳健性检查样本

### 7.4 正式层级使用规则

- 主结果默认来自 `level1`
- 增强实验优先在 `level2` 上进行
- `level3` 优先用于稳健性、解释性与敏感性检查

当前禁止：

- 直接拿 `level2` 或 `level3` 结果替代 `level1` 全国主线结论
- 把极小高信息子样本写成全国主模型统一结论

## 8. 数据切分策略

### 8.1 当前正式主方案

V4 当前正式主切分方案固定为：

- `group_by_pwsid`

即：

- 同一个 `pwsid` 的所有年份记录必须整体进入同一个集合
- 不允许同一个 `pwsid` 同时出现在 train / validation / test 中

### 8.2 为什么采用 `group_by_pwsid`

原因如下：

1. 当前样本粒度为 `pwsid + year`
2. 同一系统不同年份之间高度相关
3. 若按行随机切分，容易造成同系统信息泄漏
4. `group_by_pwsid` 更能反映模型对“未见系统”的泛化能力

### 8.3 默认切分比例

建议当前默认比例固定为：

- train：`70%`
- validation：`15%`
- test：`15%`

### 8.4 随机性控制

后续正式切分脚本必须固定：

- 随机种子
- 切分版本号

### 8.5 补充稳健性方案

后续可增加：

- `time_split_by_year`

作为稳健性检查，但当前不作为默认主方案。

## 9. 特征制度

### 9.1 第一版默认 baseline 特征

当前第一版正式 baseline 输入 `X` 固定为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

这组变量共同特点是：

- 不直接泄漏目标
- 含义相对稳定
- 结构与环境解释边界较清楚

### 9.2 条件候选结构与覆盖特征

以下字段保留为 `conditional`，默认不进入第一版 baseline：

- `state_code`
- `adjusted_total_population_served`
- `months_observed_any`
- `tthm_months_with_data`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`

说明：

- `adjusted_total_population_served` 与 `retail_population_served` 高度相关，第一版不同时进入
- `months_*` 和 `n_core_vars_available` 更像观测覆盖 / 信息强度特征，不是核心环境机制变量
- 这些变量可能提升预测，但不应在第一版主解释模型中与环境结构变量混写

### 9.3 条件候选 treatment 特征

以下字段保留为 `conditional treatment features`：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

说明：

- 它们是年度 treatment 摘要信号，不是实时工艺运行状态
- 缺失很重，且缺失不等于“明确没有该工艺”
- 第一版 baseline 默认不纳入
- 仅在后续条件实验中测试是否带来稳定增益

### 9.4 增强机制特征

以下字段属于 `enhanced`，优先在 `level2` 上测试：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `free_chlorine_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_missing_flag`
- `free_chlorine_missing_flag`

### 9.5 增强条件候选

以下字段保留为增强条件候选：

- `total_chlorine_sample_weighted_mean_mg_l`
- `total_chlorine_missing_flag`
- `annual_match_quality_tier`

### 9.6 特征制度使用规则

- 第一轮正式实验：`level1 + baseline_default`
- 第二轮条件实验：`level1 + baseline_default + conditional`
- 第三轮增强实验：`level2 + baseline_default + enhanced_default`
- 第四轮补充实验：在增强实验基础上测试 `enhanced_conditional`

## 10. 缺失处理协议

### 10.1 当前默认原则

当前正式固定以下缺失处理边界：

- 保留原始缺失
- 使用显式缺失标记
- 不进行统一覆盖式填补
- treatment 缺失不得默认改写为 `0`

### 10.2 当前明确禁止

当前默认主线中禁止：

- 所有变量统一均值填补
- treatment 缺失统一填为 `0`
- 在未记录的情况下做多重插补
- 用“是否缺失”替代变量本身的全部解释

### 10.3 如后续进行插补实验

后续如确需尝试插补，必须满足：

1. 明确标记为附加实验，而不是默认主线
2. 与“保留原始缺失”的版本做直接对照
3. 在结果表中单独记录缺失处理策略

## 11. 训练前数据校验清单

每次正式训练前，至少完成以下检查：

1. 主键唯一
2. 统一通过 `io_v4_ml_ready.py` 读取
3. 标签列只包含 `0/1/NA`
4. 目标缺失样本标签必须为空
5. 整数计数列值域合理
6. split 划分互斥
7. 当前任务目标列未误入特征矩阵
8. 当前实验禁止字段未误入训练输入
9. 特征集名称、样本层级名称与协议一致

## 12. 模型优先级与实验顺序

当前建议的模型优先级如下：

### 第一轮

- `LogisticRegression`
- 用于 `tthm_regulatory_exceedance_prediction`
- 使用 `level1 + baseline_default`

### 第二轮

- `LogisticRegression`
- 用于 `tthm_anchored_risk_prediction`
- 使用 `level1 + baseline_default`

### 第三轮

- `Ridge` 或 `LinearRegression`
- 用于 `tthm_regression`

### 第四轮

- `RandomForest`
- `HistGradientBoosting`

### 第五轮

- `XGBoost` / `LightGBM`

当前原则是：

- 先跑简单、稳定、可解释的 baseline
- 再测试更复杂模型是否带来真实增益
- 不在训练制度尚未固定时直接进入复杂调参

## 13. 评价指标协议

### 13.1 分类任务

分类任务至少记录：

- `PR-AUC`
- `ROC-AUC`
- `F1`
- `Recall`
- `Precision`

当前正式要求：

- 不允许只报 `accuracy`
- 对类别不平衡任务，`PR-AUC` 必须进入主结果

### 13.2 回归任务

回归任务至少记录：

- `MAE`
- `RMSE`
- `R²`

## 14. Results Table Template

V4 阶段必须采用统一结果表模板记录实验结果。

### 14.1 结果表模板的作用

统一结果表模板用于：

- 横向比较不同任务、不同样本层、不同特征集和不同模型
- 防止实验记录口径漂移
- 为后续论文主结果表和补充结果表提供稳定来源

### 14.2 建议字段

后续每轮实验至少记录以下字段：

- `experiment_id`
- `task_name`
- `level_name`
- `feature_set`
- `split_strategy`
- `model_name`
- `target_column`
- `train_rows`
- `validation_rows`
- `test_rows`
- `positive_count_train`
- `positive_count_validation`
- `positive_count_test`
- `primary_metric_1_name`
- `primary_metric_1_value`
- `primary_metric_2_name`
- `primary_metric_2_value`
- `primary_metric_3_name`
- `primary_metric_3_value`
- `notes`
- `run_time`

### 14.3 当前正式任务名

当前结果表中的正式任务名应统一使用：

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`
- `tthm_regression`

## 15. 命名与输出规范

后续实验命名应尽量标准化，例如：

- `task-level-feature-model-split-v001`

后续至少应输出：

- 训练结果表
- 主要指标摘要表
- 当前实验使用的特征清单
- 当前实验使用的 split 索引说明

## 16. 解释边界与禁止误读规则

当前必须明确以下边界：

1. 模型分数提升不等于因果机制证明
2. 缺失模式变量带来的增益不能直接解释为真实环境驱动机制发现
3. `level2` 或 `level3` 的增强结果不能直接替代 `level1` 全国主线结论
4. `tthm_regulatory_exceedance_prediction` 的负类是“未达到法规超标”，不等于法定低风险
5. `tthm_anchored_risk_prediction` 中的 `<= 40 ug/L` 是研究型 low-risk anchor，不是联邦法规定义的低风险健康阈值
6. `60 ug/L` 只可写成预警阈值，不可写成法规阈值

## 17. 版本维护规则

以下变更属于 V4 阶段的重要更新，需要同步更新 `codex.md`：

- 新增或修改训练协议
- 新增或修改切分脚本
- 新增或修改正式训练脚本
- 新增结果表模板或输出目录
- 固定新的主结果任务
- 新增重要建模结论

每次重要更新后，应：

1. 更新 `codex.md`
2. 记录本次协议或实验制度变更
3. 询问是否执行 Git commit 与 push

## 18. 当前下一步执行清单

按当前协议，后续建议顺序为：

1. 新增正式 split 脚本，固定 `group_by_pwsid`
2. 生成 train / validation / test 索引
3. 完成 `tthm_regulatory_exceedance_prediction` 的 baseline 训练脚本
4. 完成 `tthm_anchored_risk_prediction` 的 baseline 训练脚本
5. 在 `level2` 上测试增强变量是否带来稳定增益

## 19. 当前最短结论

V4 当前不应直接进入无制度的自由调参阶段，而应：

- 先固定总协议
- 先固定切分
- 先跑 `level1 + baseline`
- 再做条件候选和增强实验
- 把所有增益都放在明确对照框架下解释
