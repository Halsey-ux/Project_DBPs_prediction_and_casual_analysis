# V4 Project Status Summary

## 1. 文档目的

本文档用于总结当前 `V4` 阶段的项目状态、已完成工作、当前执行位置、关键产物与下一步任务，作为当前阶段的简明进展总览。

## 2. 当前阶段判断

当前项目已经正式进入 `V4` 机器学习执行阶段。

更准确地说，当前已经完成：

- `V4` 任务体系冻结
- `V4` 训练协议冻结
- `V4` 执行层脚本落地
- 第一轮 baseline 训练跑通

因此，当前状态已经不是“机器学习前准备”，而是：

- 已完成第一轮 baseline
- 正准备进入第二轮条件特征与增强实验

## 3. 当前 V4 的正式任务体系

当前 `V4` 已正式固定两个主分类任务：

### 3.1 `tthm_regulatory_exceedance_prediction`

- 目标：预测系统-年份是否达到 `TTHM >= 80 ug/L`
- 解释：学习法规超标边界模式

### 3.2 `tthm_anchored_risk_prediction`

- 目标：在 `TTHM <= 40 ug/L` 与 `TTHM >= 80 ug/L` 两端样本之间做分类
- 解释：学习明显低端与明显高端之间的清晰差异模式

其中：

- `80 ug/L` 是法规超标端
- `40 ug/L` 是研究型 low-risk anchor，不是联邦法定低风险标准

## 4. 当前 baseline 特征制度

当前第一版 baseline 默认输入 `X` 固定为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

当前不作为第一版 baseline 默认输入，但保留为后续候选的包括：

- `adjusted_total_population_served`
- `months_observed_any`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`
- 6 个 `has_*_process`
- `enhanced_default` 中的机制变量

## 5. 当前数据产品与样本规模

当前正式训练底表为：

- `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`

当前已确认：

- 总行数：`259,500`
- 总字段数：`38`
- `第一级样本`：`199,802`
- `第二级样本`：`26,975`
- `第三级样本`：`6,193`

当前法规标签样本：

- `tthm_regulatory_exceed_label = 1`：`5,618`

当前预警标签样本：

- `tthm_warning_label = 1`：`19,853`

## 6. 当前已完成的执行层脚本

当前 `V4` 训练链条已经具备以下核心脚本：

- `scripts/io_v4_ml_ready.py`
  - 统一读取 `ml_ready`，恢复 schema 和 dtype
- `scripts/prepare_v4_tthm_model_inputs.py`
  - 生成建模准备摘要
- `scripts/build_v4_tthm_splits.py`
  - 生成 `group_by_pwsid` 主切分
- `scripts/v4_tthm_training_common.py`
  - 封装 baseline 训练共用逻辑
- `scripts/train_v4_tthm_regulatory_baseline.py`
  - 训练法规任务 baseline
- `scripts/train_v4_tthm_anchored_baseline.py`
  - 训练锚点任务 baseline

## 7. 当前切分与训练状态

当前已经正式生成：

- `data_local/V4_Chapter1_Part1_Splits/v4_group_by_pwsid_master_split.csv`
- `data_local/V4_Chapter1_Part1_Splits/v4_tthm_regulatory_exceedance_level1_split_index.csv`
- `data_local/V4_Chapter1_Part1_Splits/v4_tthm_anchored_risk_level1_split_index.csv`

当前切分主方案为：

- `group_by_pwsid`

其含义是：

- 同一个 `pwsid` 的所有年份只能进入 `train / validation / test` 中的一个集合

## 8. 当前 baseline 训练结果

### 8.1 法规任务 baseline

任务：

- `tthm_regulatory_exceedance_prediction`

测试集结果：

- `PR-AUC = 0.068959`
- `ROC-AUC = 0.704565`
- `F1 = 0.102584`
- `Recall = 0.627962`
- `Precision = 0.055854`

阶段判断：

- 结果明显优于随机基线
- baseline 成立
- 但当前仍属于弱到中等的第一轮起点

### 8.2 锚点任务 baseline

任务：

- `tthm_anchored_risk_prediction`

测试集结果：

- `PR-AUC = 0.116178`
- `ROC-AUC = 0.745176`
- `F1 = 0.169400`
- `Recall = 0.630332`
- `Precision = 0.097848`

阶段判断：

- 锚点任务比法规任务更容易学习
- 当前结果验证了“边界更干净时模型更容易学”的方法判断

## 9. 当前 V4 的关键认识

截至目前，`V4` 最大的进展不是“模型已经很好”，而是：

- 训练链条已经打通
- baseline 已经建立
- 当前结果已经可以作为后续所有条件实验和增强实验的对照基线

因此，当前 `V4` 的方法状态是：

- 已经从“讨论设计”进入“可复现执行”

## 10. 当前仍然存在的边界

当前版本已经保存了：

- split 文件
- 建模准备摘要
- baseline 结果表

当前版本还没有保存：

- 单独落盘的训练好模型文件（如 `.joblib`）

因此，当前可以：

- 稳定复现实验

当前还不能直接：

- 从磁盘加载已训练模型去做新数据预测

## 11. 下一步任务

当前最合理的下一步包括：

1. 开始结构/覆盖条件特征对照实验
2. 开始 treatment 条件特征对照实验
3. 在 `第二级样本` 上启动 `enhanced_default` 机制变量实验
4. 补充统一结果汇总表
5. 在 baseline 和条件实验跑通后，再决定是否进入超参数优化与模型保存阶段

## 12. 一句话总结

当前 `V4` 已经完成正式机器学习执行链条和第一轮 baseline，项目正处在：

- “baseline 已建立，准备进入第二轮对照实验”

这一阶段。
