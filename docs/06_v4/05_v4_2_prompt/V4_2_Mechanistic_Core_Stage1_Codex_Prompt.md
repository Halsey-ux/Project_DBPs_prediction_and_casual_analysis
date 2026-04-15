# V4.2 Mechanistic Core Stage1 Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的所有要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_Experiment1_Baseline_Training_Explainer.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/02_v4_1_baseline/V4_Experiment1_Baseline_Training_Explainer.md)

## 1. 当前任务定位

当前需要执行的是 `V4.2` 大版本下的两个子更新：

- `V4.2.1` 主实验
- `V4.2.2` 补充稳健性实验

对应 `V4` 路线图中的：

- `L2 Stage1 Mechanistic Core`

这一轮实验的总目标是：

- 在已经完成的 `V4.1` baseline 基础上，测试最基础的两项核心水质变量是否带来稳定增益
- 当前只进入第一阶段机制变量扩展，不提前加入 `TOC`、`free_chlorine`、`total_chlorine`
- 当前不做模型家族比较
- 当前不做超参数优化
- 当前重点是把 `V4.2.1` 和 `V4.2.2` 的任务、样本、脚本和结果记录落成可复现版本

## 2. 本轮实验必须遵守的总规则

1. 原始数据只读，不允许原位修改
2. 只基于第三层 `V4_pws_year_ml_ready.csv` 执行，不把第二层 `facility-month` 字段混入
3. 统一通过 [io_v4_ml_ready.py](D:/Project_DBPs_prediction_and_casual_analysis/scripts/io_v4_ml_ready.py) 读取数据
4. 统一复用当前 `group_by_pwsid` 切分，不重新随机切分
5. 默认模型继续使用 `LogisticRegression`
6. 当前不进入超参数优化
7. 当前不保存模型文件，除非用户后续明确要求新增模型保存功能
8. 所有新增或更新的 `.md` 文档内容必须使用中文
9. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)
10. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送

## 3. 本轮正式实验定义

### 3.1 `V4.2.1` 主实验

`V4.2.1` 是当前这一轮的主实验版本，含义是：

- 在 `第二级样本` 上保留样本
- 在 baseline 基础上加入 `pH`、`alkalinity` 及对应 missing flag
- 默认采用缺失保留 + 数值填补 + missing flag 方案

### 3.2 `V4.2.2` 补充稳健性实验

`V4.2.2` 是当前这一轮的补充稳健性版本，含义是：

- 在 `第二级样本` 中，仅保留 `ph_sample_weighted_mean` 和 `alkalinity_sample_weighted_mean_mg_l` 同时非缺失的样本
- 在完整子集上重复当前两条正式任务
- 用于检查 `V4.2.1` 的增益是否主要来自缺失模式

### 3.3 样本层级

本轮主实验样本层级固定为：

- `第二级样本`

本轮不使用：

- `第一级样本` 作为主增强实验样本
- `第三级样本` 作为主实验样本

### 3.4 正式任务

本轮至少要跑两条主任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

### 3.5 本轮 X

在 `baseline_default` 基础上增加：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

所以 `V4.2.1` 的主实验 `X` 固定为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`
- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`

`V4.2.2` 的完整子集实验默认沿用同一组 `X`，但筛掉 `pH` 和 `alkalinity` 缺失的样本。

### 3.6 本轮 Y

#### 任务 1

- `Y = tthm_regulatory_exceed_label`

#### 任务 2

- `Y = tthm_anchored_risk_label`
- 仍然按 `<= 40` 和 `>= 80` 两端样本构造

## 4. 本轮缺失处理规则

`V4.2.1` 主实验不采用 complete-case 作为默认方案。当前主实验默认采用：

- 保留 `第二级样本` 样本
- 对数值变量做填补
- 保留 `ph_missing_flag`
- 保留 `alkalinity_missing_flag`

需要明确：

- `第二级样本` 不等于 `pH` 和 `alkalinity` 一定都完整
- `V4.2.1` 允许 `pH` / `alkalinity` 在 `第二级样本` 中仍然存在缺失
- missing flag 的作用是让模型知道这些变量原本哪些行缺失

`V4.2.2` 则采用完整子集稳健性规则：

- 在 `第二级样本` 中，只保留 `pH` 和 `alkalinity` 同时非缺失的样本
- 不再依赖这两项变量的缺失保留来构造主分析样本

## 5. 本轮补充稳健性实验

除 `V4.2.1` 主实验外，本轮必须增加：

- `V4.2.2`

该实验定义为：

- 在 `第二级样本` 中，仅保留 `ph_sample_weighted_mean` 和 `alkalinity_sample_weighted_mean_mg_l` 同时非缺失的样本

这一补充实验的作用是：

- 检查 `V4.2.1` 的增益是否主要来自缺失模式
- 检查在完整观测子集上，结论是否仍然成立

注意：

- `V4.2.2` 是补充稳健性实验
- 不是本轮默认主结果来源

## 6. 本轮输出要求

本轮至少应新增以下输出：

### 6.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/train_v4_tthm_regulatory_l2_mechanistic_stage1.py`
- `scripts/train_v4_tthm_anchored_l2_mechanistic_stage1.py`
- 如有必要，可补充一个共用函数或训练公共逻辑扩展脚本

### 6.2 本地结果目录

建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/tthm_anchored_risk_prediction/`

并在文件名中明确体现：

- `第二级样本`
- `mechanistic_stage1`
- `V4.2.1` 和 `V4.2.2`
- `logistic_regression`

### 6.3 文档

至少新增一份 `V4.2` 说明文档，内容包括：

- 本轮任务定义
- 样本层级
- 特征组
- 缺失处理方式
- `V4.2.1` 与 `V4.2.2` 的区别
- validation / test 结果
- 和 `V4.1` baseline 的对照结论

文档建议位置：

- `docs/06_v4/06_v4_2_execution/`

## 7. 本轮结果判断标准

本轮完成后，需要至少回答这些问题：

1. `V4.2.1` 在 `第二级样本` 上加入 `pH + alkalinity + missing flag` 后，是否较 `V4.1` baseline 有稳定提升
2. 提升主要体现在哪个任务上：
   - `regulatory`
   - `anchored`
3. `V4.2.2` 完整子集版本和 `V4.2.1` 缺失保留版本是否方向一致
4. 当前增益更像来自：
   - 真实变量值
   - 缺失模式
   - 两者混合

## 8. 本轮禁止事项

本轮明确禁止：

1. 直接加入 `TOC`
2. 直接加入 `free_chlorine`
3. 直接加入 `total_chlorine`
4. 直接切换到树模型或 boosting 模型
5. 提前做超参数优化
6. 把 `第二级样本` 结果直接写成全国主线最终结论
7. 把 `V4.2.1` 中缺失保留版的提升直接写成“明确机制发现”

## 9. 完成后的收尾要求

完成本轮后，请务必：

1. 更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)
2. 在 `codex.md` 中记录：
   - 更新时间
   - 本轮实验名称
   - 新增脚本
   - 新增文档
   - 主结果摘要
   - 是否完成 `V4.2.2` 补充稳健性实验
3. 向用户汇报：
   - 本轮实验是否跑通
   - `V4.2.1` 主实验结果
   - `V4.2.2` 补充实验结果
   - 对下一轮 `V4.3` 的建议
4. 最后询问用户是否执行 Git 提交与推送

## 10. 一句话任务总结

当前请你执行 `V4.2`，并明确区分两个子更新：

- `V4.2.1`：在 `第二级样本` 上，用 `baseline + pH + alkalinity + missing flags` 跑两条正式任务的 `LogisticRegression` 增强实验
- `V4.2.2`：在 `第二级样本` 的 `pH + alkalinity` 完整子集上，重复对应稳健性版本实验

完成脚本、结果、文档和 `codex.md` 同步更新。
