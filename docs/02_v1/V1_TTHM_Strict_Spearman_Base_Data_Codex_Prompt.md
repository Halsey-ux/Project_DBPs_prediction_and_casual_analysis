# V1_TTHM_strict_spearman_base_data Codex Prompt

## 版本名

`V1_TTHM_strict_spearman_base_data`

## 执行指令

你现在要在项目 `D:\Project_DBPs_prediction_and_casual_analysis` 中执行版本：

`V1_TTHM_strict_spearman_base_data`

本版本只做第一层分析单元的数据整理、从原始 SYR4 数据重新严格对齐、轻度清洗、Spearman 输入表构建与保守版相关性分析准备。不要扩展到第二层场景级数据，不要直接进入复杂机器学习，不要直接进入因果分析。

### 1. 第一层分析单元定义

本版本的分析单元固定为样本级严格单元。

固定键：

- `PWSID`
- `WATER_FACILITY_ID`
- `SAMPLING_POINT_ID`
- `SAMPLE_COLLECTION_DATE`

第一层分析单元只允许严格样本级对齐。禁止混入 `facility_day` 或更宽松的匹配结果。

### 2. 数据起点与原始输入文件

本版本必须从原始 SYR4 数据重新构建 V1 数据集，不允许把已有中间产物当作默认起点直接沿用。

本版本的所有输出目录固定为：

- `D:\Project_DBPs_prediction_and_casual_analysis\data_local\V1_TTHM_strict_spearman_base_data\`

禁止将 V1 输出继续写入旧目录：

- `D:\Project_DBPs_prediction_and_casual_analysis\data_local\tthm_first_round\`

原始输入文件固定为：

- 主结果表：
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv`

- 第一轮必须对齐的核心参数表：
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\PH.csv`
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ALKALINITY.csv`
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_DBP_Related Parameters\TOTAL ORGANIC CARBON.csv`
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_Disinfectant Residuals\FREE RESIDUAL CHLORINE (1013).csv`

必须遵守以下判断：

1. 旧版 `tthm_first_round` 中间结果不符合当前版本要求，不得作为 V1 起点继续沿用。
2. `V1_TTHM_strict_spearman_base_data` 必须由原始 SYR4 文件重新严格对齐和处理后生成。
3. 如需核验旧版逻辑，只能作为历史参考，不得直接复用旧版数据文件。

### 3. 对齐规则

本版本只允许使用严格样本级对齐规则：

- `PWSID`
- `WATER_FACILITY_ID`
- `SAMPLING_POINT_ID`
- `SAMPLE_COLLECTION_DATE`

禁止使用以下回退或放宽规则：

- `facility_day`
- 同月匹配
- 同季度匹配
- 任何非严格样本级聚合结果

### 4. Spearman 分析的数据组织要求

必须区分：

- 母表
- Spearman 输入表

母表用于追溯、分层和后续扩展，允许保留键字段和背景字段。  
Spearman 输入表只保留真正进入相关分析的变量。

### 5. V1 母表必须保留的字段

#### 4.1 键字段

- `PWSID`
- `WATER_FACILITY_ID`
- `SAMPLING_POINT_ID`
- `SAMPLE_COLLECTION_DATE`

#### 4.2 核心水质变量

- `tthm_value`
- `log_tthm`
- `ph_value`
- `alkalinity_value`
- `toc_value`
- `free_chlorine_value`

#### 4.3 背景字段

以下字段保留在母表中，用于后续分层分析和扩展建模：

- `SYSTEM_TYPE`
- `SOURCE_WATER_TYPE`
- `WATER_FACILITY_TYPE`
- `SAMPLING_POINT_TYPE`
- `SAMPLE_TYPE_CODE`
- `RETAIL_POPULATION_SERVED`
- `ADJUSTED_TOTAL_POPULATION_SERVED`
- `year`
- `month`
- `quarter`

### 6. V1 Spearman 输入表的变量要求

第一轮直接进入 Spearman 的变量固定为：

- `tthm_value`
- `log_tthm`
- `ph_value`
- `alkalinity_value`
- `toc_value`
- `free_chlorine_value`

可选数值扩展变量：

- `RETAIL_POPULATION_SERVED`
- `ADJUSTED_TOTAL_POPULATION_SERVED`
- `log1p(RETAIL_POPULATION_SERVED)`
- `log1p(ADJUSTED_TOTAL_POPULATION_SERVED)`

以下字段禁止直接作为 Spearman 变量：

- `PWSID`
- `WATER_FACILITY_ID`
- `SAMPLING_POINT_ID`
- `SAMPLE_COLLECTION_DATE`
- `SYSTEM_TYPE`
- `SOURCE_WATER_TYPE`
- `WATER_FACILITY_TYPE`
- `SAMPLING_POINT_TYPE`
- `SAMPLE_TYPE_CODE`
- 所有匹配技术字段
- 所有追溯字段

这些字段只能用于：

- 数据追踪
- 分层分析
- 分组比较
- 后续机器学习中的类别特征

### 7. 关于标准化和 log 转换的明确要求

1. Spearman 分析阶段不做 Z-score 标准化。
2. 不允许对所有变量统一做 log 转换。
3. 必须同时保留 `tthm_value` 和 `log_tthm`。
4. `ph_value` 不做 log 转换。
5. `alkalinity_value`、`toc_value`、`free_chlorine_value` 可以在查看分布后增加 `log1p` 版本，但不得替换原值。
6. 人口变量如进入分析，必须同时提供原值和 `log1p` 版本。

### 8. 数据清洗要求

必须进行数据清洗，但只允许执行轻度、透明、保守的清洗流程。

执行要求如下：

1. 先保留原始严格版，不得直接覆盖。
2. 对关键变量缺失情况进行统计并单独报告。
3. 检查明显错误值、负值、单位异常和物理不合理值。
4. 对数值变量做分位数、极值、IQR 检查。
5. 先生成异常值标记，不得一开始大量删除记录。
6. 至少生成两版 Spearman 分析数据：
   - 原始严格版
   - 轻度清洗稳健性版

### 9. 参考文章的使用原则

可以借鉴文章 *Explainable and causal machine learning to investigate the spatiotemporal dynamics patterns of coastal water quality in Hong Kong* 的清洗思想，但不得机械照搬。

具体要求：

1. 借鉴其“先描述缺失、再检查异常、再做稳健性版本”的思路。
2. 不照搬其对长期月度连续监测数据的重度清洗流程。
3. 不在第一层严格样本级数据上直接进行大规模插补。
4. 不在 Spearman 阶段执行不必要的统一标准化。

### 10. 本版本必须输出的文件

围绕版本 `V1_TTHM_strict_spearman_base_data`，必须输出以下文件：

1. `data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_strict_spearman_master.csv`
2. `data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_spearman_input.csv`
3. 如有必要，`data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_spearman_input_log.csv`
4. `data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_strict_cleaning_notes.md`
5. `data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_spearman_results.csv`
6. `data_local/V1_TTHM_strict_spearman_base_data/V1_tthm_spearman_report.md`

如需生成 Excel，对应文件也必须以 `V1_` 前缀命名。

### 11. 报告中必须明确回答的问题

报告中必须明确写出：

1. 当前第一层严格样本级数据总记录数
2. 每个核心变量的非缺失记录数
3. 哪些变量进入 Spearman
4. 哪些变量留在母表但不进入 Spearman
5. 清洗规则是什么
6. 原值版和部分 log 版的 Spearman 结果是否稳定
7. 当前第一层结果能否作为后续第二层场景级分析的保守对照

### 12. 项目管理要求

1. 每次重要更新后，更新 `codex.md`
2. 所有 Markdown 文件必须使用中文
3. 原始 SYR4 数据始终只读
4. 大型中间结果只保留在本地，不进入 Git
5. 完成修改后，必须先询问用户是否需要执行 Git 提交与推送，不得默认提交

### 13. 最终目标

本版本的最终目标是：

从原始 SYR4 数据重新构建一个可追溯、严格样本级对齐、可直接用于保守版 Spearman 分析的 `V1_TTHM_strict_spearman_base_data` 基础数据版本，并将其作为后续高风险场景框架和第二层设施-月份分析的基线对照。
