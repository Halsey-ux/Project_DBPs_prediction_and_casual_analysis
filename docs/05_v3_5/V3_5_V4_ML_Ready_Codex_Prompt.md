# V3.5 阶段：为 V4 机器学习更新准备最终输入数据集的 Codex Prompt

## 你的角色

你现在是本项目的新一轮 Codex 执行者。你不是来重新讨论研究方向，也不是直接开始训练机器学习模型。你本轮任务的唯一重点是完成一次 **V3.5 过渡更新**，把当前已经完成的 V3 数据产品，进一步整理成可直接进入 V4 机器学习阶段的标准输入层。

你必须严格基于当前项目既有文档、既有脚本、既有数据口径执行，不得擅自改写研究边界，不得把二层和三层混成一个统一宽表，也不得绕过已固定的数据契约重新定义字段。

## 任务背景

当前项目已经完成：

- V2 阶段三层数据可用性审计
- V3 阶段两张主表原型构建：
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`
- V3 收尾阶段原始数据映射法则固化：
  - `docs/04_v3/V3_Raw_Data_Mapping_Rules.md`
- 第三层机器学习字段筛选规范：
  - `docs/04_v3/V3_PWS_Year_ML_Field_Selection_Protocol.md`

当前项目判断已经明确：

- 第三层 `V3_pws_year_master.csv` 是全国机器学习主线的正式起点
- 第二层 `V3_facility_month_master.csv` 继续作为机制补充线，不进入全国统一主模型
- 进入 V4 前，不应直接开始模型训练，而应先构建面向机器学习的标准输入数据集

因此，本轮更新命名为 **V3.5**。

## 本轮唯一核心目标

请你基于当前第三层主表，构建并输出：

- `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`

并同步生成该数据集的最小必要配套文档，使后续 V4 机器学习对话可以直接接手开始建模，而不需要再次回头讨论字段来源、目标变量定义、样本分层和基础清洗规则。

## 本轮必须遵守的研究与数据边界

### 1. 只处理第三层主表

本轮只围绕：

- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`

进行派生，不得把第二层与第三层横向拼接，也不得把二层字段直接混入本轮主数据集。

### 2. 第一轮只服务于 TTHM

本轮 `ml_ready` 数据集只为 `TTHM` 主线服务，不同时为 `HAA5` 建立联合标签体系。  
`HAA5` 可在文档中保留为后续可迁移对象，但本轮不作为主任务输出中心。

### 3. 主结果变量固定

本轮必须把以下字段固定为第三层主结果变量：

- `tthm_sample_weighted_mean_ug_l`

理由已经在项目既有讨论中明确：

- 它最符合第三层 `pwsid + year` 的年度系统粒度
- 它最适合作为全国主模型的连续结果变量
- 它可以同时支撑回归任务与基于阈值的分类任务

不得将多个 `tthm_*` 结果摘要同时设为并行主标签写入同一个第一轮建模目标体系。

### 4. 分类标签规则固定

本轮必须至少生成以下标签列：

- `tthm_regulatory_exceed_label`
  - 定义：当 `tthm_sample_weighted_mean_ug_l >= 80` 时取 `1`，否则取 `0`

可以额外生成以下预警标签列：

- `tthm_warning_label`
  - 定义：当 `tthm_sample_weighted_mean_ug_l >= 60` 时取 `1`，否则取 `0`

但必须在文档中明确：

- `80 ug/L` 是法规阈值口径
- `60 ug/L` 只是预警阈值，不得误写成法规阈值

### 5. 样本分层命名固定为 level1 / level2 / level3

不得再使用“档 1/2/3”的说法。必须在数据集和文档中统一使用：

- `level1`
- `level2`
- `level3`

并固定规则如下：

- `level1`
  - 条件：`tthm_sample_weighted_mean_ug_l` 非缺失
  - 用途：全国主模型样本

- `level2`
  - 条件：`level1` 且 `n_core_vars_available >= 2`
  - 用途：增强模型样本

- `level3`
  - 条件：`level1` 且 `n_core_vars_available >= 3`
  - 用途：高信息验证模型样本

必须在文档中明确：

- `level3 ⊂ level2 ⊂ level1`
- `TTHM + 4 个核心变量全齐` 的 60 条记录只作为补充检查，不单独定义为新的正式 level

### 6. 缺失值处理边界固定

本轮不进行复杂插补，不进行多重插补，不进行面向模型结果优化的缺失修补。

本轮只允许完成以下处理：

- 目标变量缺失样本剔除出对应任务
- 对核心连续变量增加缺失标记列
- 保留原始缺失状态
- 统一数值类型、分类类型、布尔类型

如果确有必要，可以在文档中预留“后续敏感性分析可做分组中位数插补”的说明，但本轮不得把插补后的值写成主版本字段覆盖原值。

### 7. 不允许目标泄漏

本轮生成 `ml_ready` 数据集时，必须显式区分：

- 保留在表中用于回查或后续分析的字段
- 可作为候选特征进入模型的字段
- 明确禁止入模的字段

所有与 `TTHM` 结果同源的摘要字段不得在第一轮 `TTHM` 模型中作为输入特征。

## 本轮必须完成的具体任务

### 任务 1：构建 `V4_pws_year_ml_ready.csv`

请从第三层主表派生机器学习就绪数据集，输出到：

- `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`

该数据集至少应包含以下几类字段：

#### A. 主键与回查字段

- `pwsid`
- `year`

#### B. 主结果变量与标签字段

- `tthm_sample_weighted_mean_ug_l`
- `tthm_regulatory_exceed_label`
- 如可行，增加 `tthm_warning_label`

#### C. level 分层字段

- `level1_flag`
- `level2_flag`
- `level3_flag`

如你认为更清晰，也可以增加一个统一字符列，例如：

- `ml_level_max`

但不能替代三个布尔分层字段。

#### D. baseline 候选特征

至少纳入以下候选字段：

- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `n_facilities_in_master`
- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

#### E. 增强候选特征

至少纳入以下候选字段：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `free_chlorine_sample_weighted_mean_mg_l`

如字段在第三层表中存在且口径稳定，可额外纳入：

- `total_chlorine_sample_weighted_mean_mg_l`

#### F. 质控与覆盖字段

以下字段应保留在 `ml_ready` 中，用于后续样本筛选、模型对照和敏感性分析：

- `months_observed_any`
- `tthm_months_with_data`
- `months_with_1plus_core_vars`
- `months_with_2plus_core_vars`
- `months_with_3plus_core_vars`
- `n_core_vars_available`

以下字段可以保留在表内，但必须在文档中标记为“默认不进入第一版主模型特征”：

- `annual_match_quality_tier`

#### G. 缺失标记字段

至少为以下字段增加缺失标记：

- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_missing_flag`
- `free_chlorine_missing_flag`
- 如纳入总氯，则增加 `total_chlorine_missing_flag`

### 任务 2：完成基础数据清洗

请在生成 `V4_pws_year_ml_ready.csv` 的过程中，完成基础清洗，但不要越界到正式模型预处理阶段。

必须完成：

- 确认主键唯一
- 统一列类型
- 统一布尔字段表示
- 去除显然无效的目标缺失样本对应标签
- 检查数值字段是否存在明显类型错误
- 检查输出表是否可被 pandas 稳定读取

本轮不要完成：

- 训练集/验证集/测试集切分
- 标准化
- one-hot 编码后的最终训练矩阵
- 模型训练
- 复杂异常值裁剪

### 任务 3：输出最小必要文档

请在 `docs/` 下新增并输出至少两份中文文档：

#### 文档 A：`V3_5_pws_year_ml_ready_build_notes.md`

必须包括：

- 本轮目标
- 输入文件
- 输出文件
- 主结果变量定义
- 标签定义
- `level1 / level2 / level3` 规则
- 缺失标记生成规则
- 基础清洗规则
- 当前不做的事情

#### 文档 B：`V3_5_pws_year_ml_ready_dictionary.md`

必须包括：

- `V4_pws_year_ml_ready.csv` 的字段清单
- 每个字段的中文说明
- 字段类别
  - 主键/回查
  - 目标
  - 标签
  - level 分层
  - baseline 候选特征
  - 增强候选特征
  - 质控/覆盖
  - 缺失标记
- 是否建议进入第一版主模型
- 备注与禁用说明

### 任务 4：同步更新 `codex.md`

本轮属于重要更新。完成后必须同步更新项目根目录下的：

- `codex.md`

至少补充：

- V3.5 的定位
- 新增 `V4_pws_year_ml_ready.csv`
- 新增的 V3.5 文档
- 本轮完成了哪些清洗与字段冻结
- 下一步正式进入 V4 时将做什么

## 本轮明确禁止的事项

- 不得修改原始 SYR4 数据
- 不得把第二层和第三层直接拼接成一张统一表
- 不得在本轮启动正式机器学习训练
- 不得在本轮做复杂插补并覆盖主版本字段
- 不得把 `pwsid`、`system_name`、结果同源 `tthm_*` 摘要字段当作第一轮 `TTHM` 模型特征
- 不得把 `state_code` 直接写死为“必须入模”字段；它只能作为候选 baseline 特征保留，后续由模型对照实验决定是否纳入

## 你完成后必须汇报的内容

完成后，请明确汇报以下内容：

1. 新生成了哪些文件
2. `V4_pws_year_ml_ready.csv` 的行数和字段数
3. `level1 / level2 / level3` 的样本数
4. `tthm_regulatory_exceed_label` 的正负样本数
5. 是否生成了 `tthm_warning_label`
6. 哪些字段被保留为候选特征
7. 哪些字段被保留但明确标记为默认不入第一版主模型
8. 本轮没有做哪些事情，并说明这些属于 V4 正式建模阶段

## 本轮产出定位

请你始终记住，本轮不是为了追求模型成绩，而是为了把当前项目从“可信主表阶段”推进到“可直接进入机器学习阶段的数据输入层”。

本轮的最好结果不是训练出模型，而是交付出：

- 一张可复用、可追溯、可直接进入 V4 的 `V4_pws_year_ml_ready.csv`
- 一套与之匹配的最小必要中文说明文档
- 一次同步更新后的 `codex.md`


