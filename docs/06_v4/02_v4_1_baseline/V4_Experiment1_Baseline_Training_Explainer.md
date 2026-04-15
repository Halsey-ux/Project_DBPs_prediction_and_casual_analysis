# V4 Experiment 1 Baseline Training Explainer

## 1. 文档目的

本文档用于把当前 `V4` 第一轮 baseline 机器学习实验的真实执行过程、关键代码逻辑、指标解读与常见概念问题固定下来，方便后续回看与项目交接。

本文档重点回答以下问题：

- 当前 `V4 Experiment 1` 到底做了什么
- 本地 `LogisticRegression` 训练是如何被触发的
- 数据是如何进入模型的
- 每一步代码逻辑在做什么
- 为什么训练前必须做 schema、标签、主键和缺失规则校验
- 当前实验结果应如何理解
- 当前版本保存了什么、没有保存什么

## 2. 当前实验定义

当前 `V4 Experiment 1` 指的是第三层 `PWS-year` 主线上的第一轮 baseline 分类实验。当前已经实际完成两个正式任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

它们都使用相同的第一版 baseline 输入特征 `X`：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

两个任务的 `Y` 分别是：

### 2.1 `tthm_regulatory_exceedance_prediction`

- `Y = tthm_regulatory_exceed_label`
- `1` 表示 `tthm_sample_weighted_mean_ug_l >= 80`
- `0` 表示 `tthm_sample_weighted_mean_ug_l < 80`

这个任务学的是：

- 系统-年份样本跨过法规超标边界的模式

### 2.2 `tthm_anchored_risk_prediction`

- 先筛样本：
  - `tthm_sample_weighted_mean_ug_l <= 40`
  - 或 `tthm_sample_weighted_mean_ug_l >= 80`
- `Y = tthm_anchored_risk_label`
- `1` 表示 `>= 80`
- `0` 表示 `<= 40`
- 中间 `40-80` 灰区不进入训练

这个任务学的是：

- 明显高端与明显低端之间的清晰差异模式

需要强调：

- `80 ug/L` 是联邦法规超标端
- `40 ug/L` 是研究中的 low-risk anchor，不是联邦法定低风险阈值

## 3. 本次实验的真实脚本入口

本次实验真正执行用到的脚本如下：

- `scripts/io_v4_ml_ready.py`
- `scripts/prepare_v4_tthm_model_inputs.py`
- `scripts/build_v4_tthm_splits.py`
- `scripts/v4_tthm_training_common.py`
- `scripts/train_v4_tthm_regulatory_baseline.py`
- `scripts/train_v4_tthm_anchored_baseline.py`

可以把它们理解成一条完整流水线：

1. 统一读取并校验 `ml_ready` 表
2. 生成 `group_by_pwsid` 切分
3. 构建具体任务数据集
4. 定义 baseline 预处理与模型
5. 训练 `LogisticRegression`
6. 计算指标
7. 写出结果表

## 4. 当前训练流程的代码逻辑

下面按真实执行顺序说明每一步在做什么。

### 4.1 读取稳定数据表

位置：

- `scripts/v4_tthm_training_common.py`
- `scripts/io_v4_ml_ready.py`

核心逻辑：

1. 从 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv` 读取数据
2. 按显式 schema 恢复列 dtype
3. 校验主键、标签、计数列和缺失规则

这一层不是简单的 `pd.read_csv`，而是：

- 先把 `CSV` 恢复成“项目定义的正式数据表”
- 再允许后续训练使用

#### 为什么这一步必须做

因为 `CSV` 不保存 pandas dtype。回读后如果不校验，容易发生以下问题：

- 标签列从 `0/1/空` 漂成 `float64`
- 计数列从整数语义漂成浮点列
- 缺失值语义被破坏
- 主键重复混入训练集

#### 例子 1：标签列被改坏

原本正确语义应为：

- `1` = 超标
- `0` = 未超标
- 空 = 无法打标签

如果训练前不检查，后续处理可能把空标签错误填成 `0`。这样模型会把本来没有标签的样本学成负类，导致训练目标被污染。

#### 例子 2：计数列被改坏

像 `months_with_1plus_core_vars` 这类列，本意应为整数个数。如果后续处理让它出现 `3.5` 这类值，而训练前没有整数校验，模型就会在不真实的计数状态上学习。

#### 例子 3：缺失值规则被改坏

像 `has_*_process` 本意是：

- `1` = 明确有
- `0` = 明确无
- 空 = 不知道

如果训练前没有校验，而后续有人直接 `fillna(0)`，模型就会把“不知道”误学成“明确无”。

#### 例子 4：主键重复

如果 `pwsid + year` 重复出现，模型会把同一个样本重复学习，导致样本权重错误，评估也会失真。

所以这一步本质上是在保证：

- 进入模型的，仍然是“你定义的那张数据表”
- 而不是一张在回读和处理中已经变味的数据表

### 4.2 合并 split 信息

位置：

- `scripts/v4_tthm_training_common.py`

核心逻辑：

1. 读取 `v4_group_by_pwsid_master_split.csv`
2. 将 `split=train/validation/test` 按 `pwsid` 合并回 `ml_ready`

这里采用的是：

- `group_by_pwsid`

意思是：

- 同一个 `pwsid` 的所有年份只能属于同一个集合

这样做是为了防止同一系统不同年份同时进入训练集和测试集，从而造成虚高结果。

### 4.3 构造具体任务数据集

位置：

- `scripts/v4_tthm_training_common.py`

#### 法规任务

逻辑是：

1. 只保留 `第一级样本`
2. 只保留有 `tthm_regulatory_exceed_label` 的样本
3. 把 `tthm_regulatory_exceed_label` 复制成统一的 `target_value`

这样后续训练代码就不需要再区分原始标签列名，统一都用：

- `target_value`

#### 锚点任务

逻辑是：

1. 根据 `tthm_sample_weighted_mean_ug_l` 动态生成锚点标签
2. 只保留 `<=40` 和 `>=80` 两端样本
3. 把动态标签写成 `target_value`

### 4.4 取出 baseline 的 `X`

位置：

- `scripts/io_v4_ml_ready.py`
- `scripts/v4_tthm_training_common.py`

当前第一版 baseline `X` 固定为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

取出 `X` 的逻辑是：

1. 从任务数据集中只选择这 4 列
2. 数值列转为 `float`
3. 类别列保持为类别对象
4. 把 `pd.NA` 统一转成 `np.nan`

### 4.5 构建预处理和模型 pipeline

位置：

- `scripts/v4_tthm_training_common.py`

这一步把“数据预处理”和“模型训练”绑定成一个整体。

#### 数值列处理

- `retail_population_served`
- `n_facilities_in_master`

逻辑：

1. 缺失值用中位数填补
2. 做标准化

#### 类别列处理

- `system_type`
- `source_water_type`

逻辑：

1. 缺失值用最常见值填补
2. 做 one-hot 编码

#### 模型本体

当前模型为：

- `LogisticRegression`

参数包括：

- `class_weight="balanced"`
- `max_iter=2000`
- `random_state=42`
- `solver="lbfgs"`

其中：

- `class_weight="balanced"` 是为了对抗类别不平衡
- `max_iter=2000` 是训练最大迭代次数上限

### 4.6 真正开始训练

位置：

- `scripts/train_v4_tthm_regulatory_baseline.py`
- `scripts/train_v4_tthm_anchored_baseline.py`

核心动作是：

- `model.fit(X_train, y_train)`

在当前代码里表现为：

1. 取训练集 `train_df`
2. 用 `prepare_feature_frame(train_df)` 准备训练输入
3. 用 `train_df["target_value"]` 作为训练目标
4. 调用 `fit()` 开始训练

这一步就是机器学习真正开始的地方。

## 5. 本地训练时，电脑在做什么

当前 `LogisticRegression` 训练是完全在本地电脑上完成的，主要消耗：

- CPU
- 内存

当前没有使用 GPU，也不是在云端训练。

你可以把当前流程理解成：

- Python 调用 `scikit-learn`
- `scikit-learn` 在本地 CPU 上对训练数据做数值优化
- 学出一组内部参数

## 6. 训练时长是如何控制的

当前最直接的训练控制参数是：

- `max_iter=2000`

它表示：

- 允许模型最多迭代 2000 次来寻找更优参数

这不意味着一定会跑满 2000 次。通常是：

- 如果提前收敛，会更早结束
- 如果未收敛，到 2000 次会强制停止

训练时长还受以下因素影响：

- 训练样本量
- 特征数量
- 电脑 CPU 性能
- 预处理复杂度

对于当前这轮 baseline 来说：

- 特征只有 4 个
- 模型是 LogisticRegression
- 因此总体属于比较轻量的训练

## 7. 训练好以后，如何判断结果

当前训练脚本会在 validation 和 test 上计算：

- `PR-AUC`
- `ROC-AUC`
- `F1`
- `Recall`
- `Precision`

### 7.1 当前法规任务结果

- task: `tthm_regulatory_exceedance_prediction`
- test `PR-AUC = 0.068959`
- test `ROC-AUC = 0.704565`
- test `F1 = 0.102584`
- test `Recall = 0.627962`
- test `Precision = 0.055854`

解释：

- `ROC-AUC` 明显高于 `0.5`，说明模型不是乱猜
- `PR-AUC` 明显高于法规任务的正类比例基线，说明 baseline 已经学到有效信号
- 但 `Precision` 仍然较低，说明当前误报较多
- 这是一轮合格的 baseline，不是最终强模型

### 7.2 当前锚点任务结果

- task: `tthm_anchored_risk_prediction`
- test `PR-AUC = 0.116178`
- test `ROC-AUC = 0.745176`
- test `F1 = 0.169400`
- test `Recall = 0.630332`
- test `Precision = 0.097848`

解释：

- 锚点任务比法规任务更容易学
- 这是因为灰区被排除后，边界更干净
- 当前结果验证了锚点任务设计在方法上是成立的

## 8. 训练完成后，当前版本保存了什么

当前版本已经保存：

- 切分结果
- baseline 实验结果表
- 相关准备摘要

当前已保存到本地的典型文件包括：

- `data_local/V4_Chapter1_Part1_Splits/v4_group_by_pwsid_master_split.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/baseline_default_logistic_regression_results.csv`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/baseline_default_logistic_regression_results.csv`

## 9. 当前版本没有保存什么

当前训练脚本没有把“训练好的模型对象”单独落盘保存。

也就是说：

- 当前保存了结果表
- 没有保存 `.joblib` 或 `.pkl` 形式的模型文件

这意味着：

- 当前可以稳定复现实验
- 但不能直接从磁盘加载一个已经训练好的模型对象来做新预测

如果后续需要复用训练好的模型，应增加：

- `joblib.dump(model, model_path)`
- `joblib.load(model_path)`

这将会是后续执行层可以继续补的一层功能。

## 10. 当前版本如何复现实验

如果当前想重现实验结果，最直接的方法是重新运行训练脚本：

- `python scripts/train_v4_tthm_regulatory_baseline.py`
- `python scripts/train_v4_tthm_anchored_baseline.py`

由于以下条件已经固定：

- 数据表固定
- split 固定
- baseline 特征固定
- 随机种子固定

所以当前实验具备良好的可复现性。

## 11. 当前 V4 Experiment 1 的阶段判断

截至目前，V4 已经完成的不是“机器学习准备工作”，而是：

- 正式训练入口已搭建完成
- 第一轮 baseline 已经真实跑通
- 已形成两条正式任务的第一版 test 结果

所以当前最准确的阶段判断是：

- `V4 Experiment 1` 已完成 baseline 执行
- 下一步应进入条件特征对照实验与 `第二级样本 + enhanced` 增益实验

## 12. 当前最重要的认识

本次 `V4 Experiment 1` 最大的意义不是“分数已经很好”，而是：

- 正式任务定义已经落地
- 训练脚本链条已经打通
- 基础 baseline 已建立
- 后续所有条件实验和增强实验都可以以这轮结果为对照

这意味着项目已经从“讨论设计”进入到“可复现建模执行”阶段。
