# V4 TTHM Model Task Definition

- 更新时间：2026-03-31 13:10（Asia/Hong_Kong）
- 适用输入表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V4_Chapter1_Part1_ML_Ready\V4_pws_year_ml_ready.csv`
- 适用读取入口：`D:\Project_DBPs_prediction_and_casual_analysis\scripts\io_v4_ml_ready.py`
- 文档定位：正式固定 V4 阶段 `TTHM` 年度主线的任务拆分、样本层级、特征分组、评价指标与禁止误用规则

## 1. 目标

本文件用于把 V3.5 已生成的第三层 `ml_ready` 输入层进一步固定为 V4 正式建模入口，避免后续在建模过程中反复修改目标定义、样本口径或特征边界。

本文件不负责训练模型，也不覆盖原始 `ml_ready` 表。它的作用是：

- 固定正式任务名
- 固定 `X / Y` 定义
- 固定 `第一级样本 / 第二级样本 / 第三级样本` 的使用方式
- 固定 baseline / enhanced / conditional 特征制度
- 固定缺失处理和禁止误用边界

## 2. 输入边界

V4 的全国主模型只使用第三层系统-年份表：

- `V4_pws_year_ml_ready.csv`

当前阶段禁止把第二层 `facility-month` 字段横向并入第三层全国主模型输入层。

第二层继续保留为：

- 机制分析补充线
- 高信息小模型线
- 场景诊断线

但不作为当前全国主模型训练表。

## 3. 正式任务定义

### 3.1 任务 1：`tthm_regulatory_exceedance_prediction`

- 任务性质：法规超标分类
- 样本范围：全部 `第一级样本` 样本
- 目标列：`tthm_regulatory_exceed_label`
- 正类定义：`tthm_sample_weighted_mean_ug_l >= 80`
- 负类定义：`tthm_sample_weighted_mean_ug_l < 80`
- 当前正类数量：`5,618`
- 当前负类数量：`194,184`

该任务学到的是：

- 系统-年份跨过法规超标边界的统计模式

该任务回答的是：

- 哪些系统-年份更可能进入法规意义上的超标状态

### 3.2 任务 2：`tthm_anchored_risk_prediction`

- 任务性质：研究型锚点分类
- 样本范围：仅保留两端样本
- 目标列：`tthm_anchored_risk_label`
- 正类定义：`tthm_sample_weighted_mean_ug_l >= 80`
- 负类定义：`tthm_sample_weighted_mean_ug_l <= 40`
- 灰区处理：`40 < tthm_sample_weighted_mean_ug_l < 80` 不进入该任务训练

该任务学到的是：

- 明显高端样本和明显低端样本之间的清晰差异模式

该任务回答的是：

- 在去掉灰区后，模型是否能更稳定地识别高低两端

补充说明：

- `80 ug/L` 是法规阈值
- `40 ug/L` 是研究型 low-risk anchor
- `40 ug/L` 不是联邦法规定义的低风险健康阈值

### 3.3 任务 3：`tthm_regression`

- 任务性质：连续值回归
- 样本范围：全部 `第一级样本` 样本
- 目标列：`tthm_sample_weighted_mean_ug_l`

该任务学到的是：

- 年度系统级 `TTHM` 连续水平的变化模式

该任务回答的是：

- 系统之间为何存在连续浓度差异

## 4. 正式 X / Y 定义

### 4.1 `tthm_regulatory_exceedance_prediction`

#### Y

- `tthm_regulatory_exceed_label`

#### X：第一版 baseline 默认输入

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

### 4.2 `tthm_anchored_risk_prediction`

#### Y

- `tthm_anchored_risk_label`

#### 样本筛选

- 保留 `tthm_sample_weighted_mean_ug_l <= 40`
- 保留 `tthm_sample_weighted_mean_ug_l >= 80`
- 去掉中间灰区

#### X：第一版 baseline 默认输入

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

### 4.3 `tthm_regression`

#### Y

- `tthm_sample_weighted_mean_ug_l`

#### X：第一版 baseline 默认输入

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

## 5. 样本层级的正式使用方式

### 5.1 `第一级样本`

- 筛选条件：`level1_flag = 1`
- 当前样本数：`199,802`
- 定位：全国广覆盖主线样本
- 用途：第一版 baseline 主模型的默认训练范围

### 5.2 `第二级样本`

- 筛选条件：`level2_flag = 1`
- 当前样本数：`26,975`
- 定位：信息更高的增强模型样本
- 用途：测试机制变量和缺失模式变量是否带来稳定增益

### 5.3 `第三级样本`

- 筛选条件：`level3_flag = 1`
- 当前样本数：`6,193`
- 定位：高信息稳健性检查样本
- 用途：解释性检查、敏感性分析、稳健性验证

## 6. 特征分组

### 6.1 baseline_default

第一版正式 baseline 默认输入 `X` 固定为：

- `system_type`
- `source_water_type`
- `retail_population_served`
- `n_facilities_in_master`

### 6.2 structural_conditional

以下字段保留为结构/覆盖条件候选：

- `state_code`
- `adjusted_total_population_served`
- `months_observed_any`
- `tthm_months_with_data`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`

补充说明：

- `adjusted_total_population_served` 与 `retail_population_served` 高度相关，第一版默认不同时进入
- `months_*` 和 `n_core_vars_available` 主要反映观测覆盖和信息强度，不是核心环境机制变量

### 6.3 treatment_conditional

以下字段保留为 treatment 条件候选：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

补充说明：

- 它们是年度 treatment 摘要信号，不是实时运行状态
- 缺失很重
- 缺失不等于“明确没有该工艺”
- 第一版 baseline 默认不纳入

### 6.4 enhanced_default

以下字段属于增强机制特征：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `free_chlorine_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_missing_flag`
- `free_chlorine_missing_flag`

### 6.5 enhanced_conditional

以下字段保留为增强条件候选：

- `total_chlorine_sample_weighted_mean_mg_l`
- `total_chlorine_missing_flag`
- `annual_match_quality_tier`

## 7. 当前数据风险的正式解释

### 7.1 法规任务类别不平衡明显

- 法规超标正类比例较低
- 因此不能只看 `accuracy`
- 必须同时看 `PR-AUC`、`Recall` 和 `Precision`

### 7.2 增强机制变量缺失严重

主要增强变量缺失率很高，因此：

- 不能把增强变量直接视为默认全国主线特征
- 更合理的策略是先建 `第一级样本 + baseline`，再在 `第二级样本` 上测试增强增益

### 7.3 treatment 布尔字段解释风险高

6 个 `has_*_process` 字段具有一定工程背景意义，但语义不够干净：

- 不是全年持续运行状态
- 不是严格工艺确认字段
- 更像低维存在性信号

因此它们更适合作为后续条件实验，而不是第一版 baseline 核心输入。

### 7.4 观测覆盖特征可能主导模型

`months_*` 和 `n_core_vars_available` 之类变量可能让模型先学到：

- 哪些系统监测更多
- 哪些系统信息更完整

而不一定先学到真正稳定的环境机制。

因此这类变量默认不进入第一版环境解释型 baseline。

## 8. 缺失处理边界

当前阶段正式固定以下边界：

- 连续型机制变量保留原始缺失
- 使用缺失标记显式暴露缺失模式
- 不做统一均值填补
- 不做多重插补
- 不把 treatment 缺失直接覆盖成 `0`

## 9. 评价指标

### 9.1 回归任务

至少固定以下指标：

- `MAE`
- `RMSE`
- `R²`

### 9.2 分类任务

至少固定以下指标：

- `ROC-AUC`
- `PR-AUC`
- `F1`
- `Recall`
- `Precision`

补充说明：

- 法规任务尤其不能只报准确率
- 由于正类比例偏低，`PR-AUC` 比单独 `ROC-AUC` 更重要

## 10. 实验顺序

当前建议固定为以下顺序：

1. `第一级样本 + baseline_default`  
   用于建立全国主线 baseline

2. `第一级样本 + baseline_default + structural_conditional`  
   测试结构/覆盖变量是否带来稳定增益

3. `第一级样本 + baseline_default + treatment_conditional`  
   测试 treatment 摘要信号是否带来稳定增益

4. `第二级样本 + baseline_default + enhanced_default`  
   测试机制变量是否真正提升结果

5. `第三级样本 + baseline_default + enhanced_default`  
   只用于稳健性和解释性检查

## 11. 禁止误用规则

1. 禁止把 `pwsid`、`year` 直接作为模型特征
2. 禁止把当前目标同源的 `tthm_*` 摘要字段送回模型
3. 禁止把 `facility-month` 级字段横向拼入当前全国主模型
4. 禁止把 treatment 缺失默认改写为 `0`
5. 禁止把 `40 ug/L` 写成法定低风险阈值
6. 禁止在没有对照实验的情况下把条件特征或增强特征结果直接写成主结论

## 12. 当前最短结论

V4 当前最重要的不是立刻堆复杂特征，而是：

- 固定正式任务名
- 固定正式 `X / Y`
- 先跑 `第一级样本 + baseline_default`
- 再把结构/覆盖、treatment 和机制变量放到明确对照框架里测试
