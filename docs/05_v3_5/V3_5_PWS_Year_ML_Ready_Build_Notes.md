# V3.5 pws-year ML-ready 构建说明

- 更新时间：2026-03-30 22:04:45（Asia/Hong_Kong）
- 输入文件：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_pws_year_master.csv`
- 输出文件：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V4_Chapter1_Part1_ML_Ready\V4_pws_year_ml_ready.csv`

## 1. 本轮目标

- 仅基于第三层 `V3_pws_year_master.csv` 派生一张可直接进入 V4 机器学习阶段的数据输入层。
- 本轮只服务于 `TTHM` 主线，不把第二层 `facility-month` 字段横向拼入，也不启动正式模型训练。

## 2. 输出数据集概况

- 行数：`259500`
- 字段数：`38`
- `第一级样本` 样本数：`199802`
- `第二级样本` 样本数：`26975`
- `第三级样本` 样本数：`6193`
- `tthm_regulatory_exceed_label=1`：`5618`
- `tthm_regulatory_exceed_label=0`：`194184`
- `tthm_warning_label=1`：`19853`
- `tthm_warning_label=0`：`179949`
- `TTHM` 目标缺失行数：`59698`

## 3. 主结果变量定义

- 唯一连续型主结果变量固定为 `tthm_sample_weighted_mean_ug_l`。
- 它表示在 `pwsid + year` 粒度下的 TTHM 年度样本加权均值，单位为 `ug/L`。
- 本轮不把其他 `tthm_*` 摘要字段并列写成主标签体系。

## 4. 标签定义

- `tthm_regulatory_exceed_label`：当 `tthm_sample_weighted_mean_ug_l >= 80` 时记为 `1`，否则记为 `0`。
- `tthm_warning_label`：当 `tthm_sample_weighted_mean_ug_l >= 60` 时记为 `1`，否则记为 `0`。
- `80 ug/L` 是法规阈值；`60 ug/L` 只是预警阈值，不能写成法规阈值。
- 当目标变量缺失时，这两个标签均保持为空值，不把缺失样本误写为负类。

## 5. 第一级样本 / 第二级样本 / 第三级样本 规则

- `第一级样本`：`tthm_sample_weighted_mean_ug_l` 非缺失。
- `第二级样本`：满足 `第一级样本` 且 `n_core_vars_available >= 2`。
- `第三级样本`：满足 `第一级样本` 且 `n_core_vars_available >= 3`。
- 始终满足“`第三级样本` 包含于 `第二级样本`，`第二级样本` 包含于 `第一级样本`”。
- `TTHM + 4 个核心变量全齐` 的 `60` 条记录仍只作为补充检查，不单独定义为新的正式 level。
- 为避免与第一章“第一层 / 第二层 / 第三层”数据层级混淆，文档中统一使用“第一级样本 / 第二级样本 / 第三级样本”指代第三层 `PWS-year` 内部样本分层；内部字段名仍保持为 `level1_flag`、`level2_flag`、`level3_flag` 与 `ml_level_max`。

## 6. 保留字段口径

- baseline 候选特征：state_code、system_type、source_water_type、retail_population_served、adjusted_total_population_served、n_facilities_in_master、has_disinfection_process、has_filtration_process、has_adsorption_process、has_oxidation_process、has_chloramination_process、has_hypochlorination_process。
- 增强候选特征：ph_sample_weighted_mean、alkalinity_sample_weighted_mean_mg_l、toc_sample_weighted_mean_mg_l、free_chlorine_sample_weighted_mean_mg_l、total_chlorine_sample_weighted_mean_mg_l。
- 质控/覆盖字段保留在表内，用于样本筛选、模型对照和敏感性分析。
- `annual_match_quality_tier` 保留，但默认不进入第一版主模型特征。
- `state_code` 仅保留为 baseline 候选特征，后续是否纳入由模型对照实验决定。

## 7. 缺失标记生成规则

- 对 `ph`、`alkalinity`、`toc`、`free_chlorine` 和 `total_chlorine` 年度均值各生成一列缺失标记。
- 缺失标记为 `1` 表示该变量缺失，为 `0` 表示非缺失。
- 原始数值列保持原始缺失状态，不做覆盖式插补。

## 8. 基础清洗规则

- 校验输出主键 `pwsid + year` 唯一。
- 统一字符串字段、整数型字段、连续型字段和 0/1 布尔字段口径。
- treatment 二值字段仅在原表有值时保留为 `0/1`，没有 treatment 摘要时仍保留为空。
- 目标缺失样本不生成分类标签，同时 `level1_flag`、`level2_flag`、`level3_flag` 统一为 `0`。
- 输出后通过统一读取函数按显式 schema 再次回读，确认关键字段不会在回读阶段漂移为错误 dtype。

## 9. 本轮明确不做的事情

- 不切分训练集 / 验证集 / 测试集。
- 不做标准化、one-hot 编码、最终训练矩阵生成。
- 不做复杂插补、多重插补或面向模型性能优化的缺失修补。
- 不做异常值裁剪或正式模型训练。
- 不把 `system_name`、`pwsid`、`year` 或与目标同源的 `tthm_*` 摘要字段写入第一版 `TTHM` 模型特征。
