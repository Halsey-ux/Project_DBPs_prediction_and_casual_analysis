# V3.5 pws-year ML-ready 字段字典

- 更新时间：2026-03-30 22:04:45（Asia/Hong_Kong）
- 对应数据集：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V4_Chapter1_Part1_ML_Ready\V4_pws_year_ml_ready.csv`

| 字段名 | 字段类别 | 中文说明 | 是否建议进入第一版主模型 | 备注与禁用说明 |
| --- | --- | --- | --- | --- |
| `pwsid` | 主键/回查 | 公共供水系统唯一编号。 | 不适用 | 保留用于索引、回查和结果回写，禁止直接作为模型特征。 |
| `year` | 主键/回查 | 系统年度主键。 | 不适用 | 保留用于分年回查与时间切分，禁止直接作为模型特征。 |
| `tthm_sample_weighted_mean_ug_l` | 目标 | 第三层 TTHM 年度样本加权均值，单位为 ug/L。 | 不适用 | 本轮固定为唯一连续型主结果变量。 |
| `tthm_regulatory_exceed_label` | 标签 | 当 TTHM 年度样本加权均值大于等于 80 ug/L 时记为 1，否则记为 0。 | 不适用 | 80 ug/L 为法规阈值；目标缺失时标签留空。 |
| `tthm_warning_label` | 标签 | 当 TTHM 年度样本加权均值大于等于 60 ug/L 时记为 1，否则记为 0。 | 不适用 | 60 ug/L 仅作为预警阈值，不能写成法规阈值；目标缺失时标签留空。 |
| `level1_flag` | level 分层 | 标记是否满足第一级样本：TTHM 目标非缺失。 | 不适用 | 内部字段名保留为 `level1_flag`；对应人类可读叫法为“第一级样本”。 |
| `level2_flag` | level 分层 | 标记是否满足第二级样本：在第一级样本基础上 `n_core_vars_available >= 2`。 | 不适用 | 内部字段名保留为 `level2_flag`；对应人类可读叫法为“第二级样本”。 |
| `level3_flag` | level 分层 | 标记是否满足第三级样本：在第一级样本基础上 `n_core_vars_available >= 3`。 | 不适用 | 内部字段名保留为 `level3_flag`；第三级样本包含于第二级样本。 |
| `ml_level_max` | level 分层 | 记录每条记录当前可达到的最高 level。 | 不适用 | 内部字段名保留为 `ml_level_max`；便于后续直接筛选第一级样本 / 第二级样本 / 第三级样本 / `not_ml_ready`。 |
| `state_code` | baseline 候选特征 | 州代码。 | 条件 | 保留为 baseline 候选特征，但不能在文档中写成“必须入模”。 |
| `system_type` | baseline 候选特征 | 供水系统类型。 | 是 | 适合作为第一版主模型的低维结构背景变量。 |
| `source_water_type` | baseline 候选特征 | 原水类型。 | 是 | 适合作为第一版主模型的结构背景变量。 |
| `retail_population_served` | baseline 候选特征 | 零售服务人口。 | 是 | 反映系统规模。 |
| `adjusted_total_population_served` | baseline 候选特征 | 调整后总服务人口。 | 是 | 提供规模的补充口径。 |
| `n_facilities_in_master` | baseline 候选特征 | 该系统当年进入第三层主表聚合的设施数。 | 是 | 反映系统年度设施覆盖范围。 |
| `has_disinfection_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在消毒工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `has_filtration_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在过滤工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `has_adsorption_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在吸附工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `has_oxidation_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在氧化工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `has_chloramination_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在氯胺化工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `has_hypochlorination_process` | baseline 候选特征 | 年度 treatment 摘要中是否存在次氯化工艺。 | 是 | 保留原始缺失；有值时统一用 0/1 表示。 |
| `ph_sample_weighted_mean` | 增强候选特征 | 年度 pH 样本加权均值。 | 是 | 核心机制变量。 |
| `alkalinity_sample_weighted_mean_mg_l` | 增强候选特征 | 年度总碱度样本加权均值，单位为 mg/L。 | 是 | 核心机制变量。 |
| `toc_sample_weighted_mean_mg_l` | 增强候选特征 | 年度 TOC 样本加权均值，单位为 mg/L。 | 是 | 核心机制变量。 |
| `free_chlorine_sample_weighted_mean_mg_l` | 增强候选特征 | 年度游离余氯样本加权均值，单位为 mg/L。 | 是 | 核心机制变量。 |
| `total_chlorine_sample_weighted_mean_mg_l` | 增强候选特征 | 年度总氯样本加权均值，单位为 mg/L。 | 条件 | 保留为增强模型候选特征，不默认进入第一版全国主模型。 |
| `months_observed_any` | 质控/覆盖 | 该系统当年有任意数据的月份数。 | 是 | 反映年度监测覆盖。 |
| `tthm_months_with_data` | 质控/覆盖 | 该系统当年有 TTHM 数据的月份数。 | 条件 | 更适合作为样本质控和敏感性分析字段。 |
| `months_with_1plus_core_vars` | 质控/覆盖 | 至少 1 个核心机制变量有数据的月份数。 | 是 | 反映低门槛机制覆盖。 |
| `months_with_2plus_core_vars` | 质控/覆盖 | 至少 2 个核心机制变量有数据的月份数。 | 是 | 反映中等信息强度。 |
| `months_with_3plus_core_vars` | 质控/覆盖 | 至少 3 个核心机制变量有数据的月份数。 | 是 | 反映高信息强度。 |
| `n_core_vars_available` | 质控/覆盖 | 年度层可用核心机制变量数量。 | 是 | 同时用于样本分层和覆盖控制。 |
| `annual_match_quality_tier` | 质控/覆盖 | V3 第三层既有的年度匹配质量分层。 | 否 | 保留用于样本筛选、对照和敏感性分析，默认不进入第一版主模型。 |
| `ph_missing_flag` | 缺失标记 | 当年度 pH 均值缺失时记为 1，否则记为 0。 | 是 | 保留原始缺失，同时显式暴露缺失模式。 |
| `alkalinity_missing_flag` | 缺失标记 | 当年度总碱度均值缺失时记为 1，否则记为 0。 | 是 | 保留原始缺失，同时显式暴露缺失模式。 |
| `toc_missing_flag` | 缺失标记 | 当年度 TOC 均值缺失时记为 1，否则记为 0。 | 是 | 保留原始缺失，同时显式暴露缺失模式。 |
| `free_chlorine_missing_flag` | 缺失标记 | 当年度游离余氯均值缺失时记为 1，否则记为 0。 | 是 | 保留原始缺失，同时显式暴露缺失模式。 |
| `total_chlorine_missing_flag` | 缺失标记 | 当年度总氯均值缺失时记为 1，否则记为 0。 | 条件 | 仅在增强模型引入总氯时一并使用。 |

## 附加说明

- 第一版 `TTHM` 主模型明确禁止把与目标同源的 `tthm_monthly_median_median_ug_l`、`tthm_monthly_max_max_ug_l`、`tthm_monthly_p90_p90_ug_l`、`tthm_high_risk_*` 系列字段作为输入特征。
- `system_name`、各类字符串列表摘要字段和结果同源摘要字段不进入本轮 `ml_ready` 输出表。
- `annual_match_quality_tier` 虽然保留在表内，但文档口径固定为“默认不进入第一版主模型”。
- `state_code` 固定为候选特征，不写成“必须入模”。
