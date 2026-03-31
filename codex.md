# codex.md

## 1. 项目背景

本项目服务于基于美国 EPA SYR4 数据集的论文研究。

当前论文重点是第一章：

- 将 SYR4 作为大规模真实世界监管监测数据集使用
- 聚焦受监管消毒副产物（DBPs），尤其是 `TTHM` 和 `HAA5`
- 构建系统级、可解释的风险识别与预测框架

本项目不把 SYR4 视为单厂精细工艺机理数据库，而是将其视为一个真实世界的数据训练场，用来识别高风险场景、筛选稳定驱动因素，并支撑后续实验章节的样品优选。

## 2. 总体目标

本项目的总体目标是支撑完整论文主线，包括：

- 基于 SYR4 的 DBP 风险识别与预测
- 关键驱动因素筛选与可解释分析
- 为后续靶向/准靶向筛查章节提供现实场景依据

## 3. 当前阶段目标

当前阶段目标是完成第一章第一部分从 V3 原型主表到 V4 机器学习输入层的过渡工作：

- 固定第三层 `TTHM` 主线的主结果变量、法规标签、预警标签与 `level1/level2/level3` 分层
- 产出可直接进入 V4 的 `V4_pws_year_ml_ready.csv`
- 完成机器学习输入层所需的最小必要文档、字段字典与基础清洗口径
- 为后续 V4 正式建模阶段划清输入边界、缺失处理边界与禁止误用规则

## 4. 目录结构

当前项目根目录：

- `D:\Project_DBPs_prediction_and_casual_analysis`

当前结构：

```text
D:\Project_DBPs_prediction_and_casual_analysis
├─ .git/
├─ .gitignore
├─ README.md
├─ codex.md
├─ docs/
├─ scripts/
├─ data_local/
└─ scratch/
```

当前与 DBP 主线直接相关的本地输出目录：

- `data_local/tthm_first_round/`
  - 历史第一轮本地结果目录
  - 旧版不符合当前要求的数据与结果已不再作为当前版本输入
- `data_local/V1_TTHM_strict_spearman_base_data/`
  - V1 严格样本级基线专用目录
  - 用于存放严格样本级母表、Spearman 输入表、清洗说明与结果报告
- `data_local/V2_Chapter1_Part1_DBP_Data_Foundation/`
  - V2 数据基础审计目录
  - 用于存放三层级可用性审计结果、关系摘要、变量覆盖统计与中文审计报告
- `data_local/V3_Chapter1_Part1_Prototype_Build/`
  - V3 原型主表目录
  - 用于存放 `V3_facility_month_master.csv`、`V3_pws_year_master.csv` 及相关摘要表
- `data_local/V4_Chapter1_Part1_ML_Ready/`
  - V3.5 机器学习输入层目录
  - 用于存放 `V4_pws_year_ml_ready.csv`

各目录作用：

- `docs/`
  - 项目说明
  - 研究设计
  - 数据逻辑文档
  - 项目状态文档
  - 第一章方法框架文档
- `scripts/`
  - 数据转换脚本
  - 合并脚本
  - 分析脚本
  - 建模脚本
- `data_local/`
  - 本地大文件
  - 仅本地使用，不纳入 Git
- `scratch/`
  - 临时目录
  - 测试/修复输出
  - 本地缓存类内容，不纳入 Git

## 5. 原始数据位置与数据情况

原始 SYR4 数据在本地其他路径，当前应视为只读输入源。

当前主要数据源路径：

- `D:\Syr4_Project\syr4_DATA_CSV`
- `D:\SYR4_Data\syr4_DATA_excel`

当前第一轮重点数据源：

- 主表：
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv`
- 重点参数表：
  - `PH.csv`
  - `TOTAL ALKALINITY.csv`
  - `TOTAL ORGANIC CARBON.csv`
  - `FREE RESIDUAL CHLORINE (1013).csv`

## 6. 技术栈

当前优先使用的技术栈：

- Python
- pandas
- numpy
- scipy
- scikit-learn
- xgboost / lightgbm（需要时）
- shap（需要时）
- PowerShell（本地文件检查与项目操作）
- Git + GitHub（项目管理）

## 7. 编码与项目管理规范

### 7.1 原始数据规范

- 原始数据只读
- 不允许原位覆盖本地源数据
- 不允许在原始数据目录中重命名文件

### 7.2 GitHub 管理范围

GitHub 主要管理：

- 脚本
- 文档
- 报告
- 配置
- 轻量级元数据
- 项目级说明文件

GitHub 不直接管理：

- 原始 SYR4 数据
- 大型中间分析表
- 大型临时输出
- 本地 scratch 结果

### 7.3 `codex.md` 维护规则

`codex.md` 是项目级长期说明书。

以下情况属于“重要更新”，需要同步更新 `codex.md`：

- 新增或修改脚本
- 重要文档更新
- 完成一轮数据处理
- 完成一轮分析或建模
- 项目结构发生重要调整

### 7.4 Git 提交规则

每次重要更新后，都应：

1. 更新 `codex.md`
2. 进行 Git commit
3. 推送到 GitHub

小型临时修改不要求立即 push，避免提交历史过碎。

协作确认规则：

- 每次完成项目修改后，Codex 需要先询问用户是否需要执行 Git 提交与推送
- 在用户明确同意前，不默认直接执行 `git commit` 或 `git push`
- 如用户仅要求完成本地修改，则保留修改结果并汇报状态，不自动推送 GitHub
- 在执行用户任何新指令前，Codex 必须先判断该指令是否合理、是否符合当前任务要求、以及是否违背 `codex.md` 中的项目规范；如存在冲突，应先向用户指出并澄清，再决定是否执行

### 7.5 提交标题规则

每次重要更新都应使用清晰、准确的 commit message，能够反映实际改动内容。

### 7.6 Markdown 文档语言规则

- 后续新增或更新的 `.md` 文件默认使用中文撰写
- 如需保留英文，应仅限于路径、字段名、代码标识符、技术术语或必要引用
- 自动生成的 Markdown 报告也应优先输出中文标题、中文说明和中文结论

## 8. 当前进展

当前项目已经完成：

- 将 SYR4 数据在本地转换为 CSV 和 Excel 形式
- 梳理了 SYR4 的主要数据模块和目录结构
- 理清了模板化监测表和特殊用途表的逻辑
- 明确了 paired microbes/disinfectant residual 文件的用途
- 完成了第一章初步研究设计
- 已通过 SSH 建立 GitHub 仓库连接并完成首次推送
- 已对项目根目录进行第一轮整理
- 已建立 `codex.md` 作为长期项目说明书
- 已完成第一轮 `TTHM` 主表与 4 张核心化学表的字段兼容性检查
- 已新增脚本 `scripts/build_tthm_first_round.py`
- 已新增脚本 `scripts/export_tthm_first_round_excel.py`
- 已新增脚本 `scripts/create_tthm_spearman_strict_dataset.py`
- 已新增脚本 `scripts/build_v1_tthm_strict_spearman_base_data.py`
- 已新增第一章方法文档 `docs/SYR4_第一章高风险场景定义框架.md`
- 已新增版本执行文档 `docs/V1_TTHM_strict_spearman_base_data_Codex_Prompt.md`
- 已明确第一章建议采用“样本级严格对齐 + 设施-月份高风险场景”并行的分层数据策略
- 已将当前项目修改版本名明确为 `V1_TTHM_strict_spearman_base_data`
- 已确认旧版 `tthm_first_round` 数据集与结果不符合当前 V1 要求，当前版本必须从原始 SYR4 数据重新构建
- 已明确 V1 版本输出不得再写入 `tthm_first_round`，而应统一写入 `data_local/V1_TTHM_strict_spearman_base_data/`
- 已从原始 SYR4 文件重新构建 `V1_tthm_strict_spearman_master.csv`
- 已生成原值版、轻度清洗稳健版和部分 log 版 Spearman 输入表与结果文件
- 已生成 `V1_tthm_strict_cleaning_notes.md` 和 `V1_tthm_spearman_report.md`
- 已确认 V1 严格样本级母表记录数为 `1,056,301`
- 已确认至少匹配到 1 个核心预测变量的严格样本数为 `16,352`，至少匹配到 2 个核心预测变量的样本数为 `2,246`
- 已确认 4 个核心预测变量在严格样本级下同时完整的记录数为 `0`
- 已完成第一层保守版 Spearman 结果计算，当前相关方向表现为：`TOC` 与 `TTHM` 中等正相关、`TOTAL ALKALINITY` 与 `TTHM` 中等负相关、`FREE RESIDUAL CHLORINE` 与 `TTHM` 弱负相关、`PH` 与 `TTHM` 相关性很弱
- 已新增脚本 `scripts/build_chapter1_part1_dbp_foundation.py`
- 已生成 V2 数据基础审计结果与中文审计报告
- 已新增文档 `docs/第一章第一部分_DBP数据基础与分析层级设计.md`
- 已正式完成第一章第一部分的结构化产出，包括目标定位、变量环境意义框架、核心表关系、三层级数据可用性比较、V1 正式定位与后续数据路线图
- 已确认严格样本级下 `TTHM + pH + 总碱度 + TOC + 游离余氯` 完整样本数仍为 `0`
- 已确认设施-月份级下上述核心四变量与 `TTHM` 的 pairwise 重合度有所改善，但完整共同非缺失单元仍为 `0`
- 已确认系统-年份级下 `TTHM + pH + 总碱度 + TOC + 游离余氯` 完整单元数为 `60`
- 已确认 `Paired TOC-Alkalinity` 仅与 `306` 个 `TTHM` 设施-月份键重合、与 `140` 个 `HAA5` 设施-月份键重合，更适合作为专题化 reduced dataset 而非通用主表
- 已明确 `HAA5` 应与 `TTHM` 平行纳入同一三层级分析框架，而不是后置补充
- 已完成 V3 第二层原型表 `V3_facility_month_master.csv`
- 已完成 V3 第三层原型表 `V3_pws_year_master.csv`
- 已新增文档 `docs/V3_facility_month_dictionary.md`
- 已新增文档 `docs/V3_facility_month_build_notes.md`
- 已新增文档 `docs/V3_pws_year_dictionary.md`
- 已新增文档 `docs/V3_pws_year_build_notes.md`
- 已新增文档 `docs/V3_prototype_audit_report.md`
- 已新增文档 `docs/V3_pws_year_ML字段筛选规范.md`
- 已明确：进入 V4 之前，V3 还需要完成一个最后的小更新，即用简洁直观的方式固定两张 V3 主表相对于原始 SYR4 数据的变量映射法则、缺失语义、样本分层规则与禁止误用规则
- 已新增一份专用 prompt 任务定义，用于指导新 Codex 会话专门完成上述 V3 收尾更新
- 已新增文档 `docs/V3_Raw Data Mapping Rules.md`
- 已正式固定 `V3_facility_month_master` 与 `V3_pws_year_master` 相对于原始 SYR4 的字段来源、聚合规则、缺失语义、样本分层规则与禁止误用规则
- 已明确第三层进入 V4 时应采用“全国主模型样本 / 加强模型样本 / 高信息模型样本”三档分层，并保留 `A_ready_for_national_ml` 作为更严格验收子集
- 已明确第二层继续作为机制分析与高信息小模型补充线，而不是替代第三层全国主表线
- 已明确在正式进入 V4 之前，需要增加一次 V3.5 过渡更新，用于构建第三层机器学习输入底座 `V4_pws_year_ml_ready.csv`
- 已明确 V3.5 只围绕第三层 `TTHM` 主线展开，先冻结主结果变量、标签规则、`level1/2/3` 分层、缺失标记与基础清洗口径
- 已新增 V3.5 专用执行文档 `docs/V3_5_V4_ML_Ready_Codex_Prompt.md`
- 已新增脚本 `scripts/build_v3_5_pws_year_ml_ready.py`
- 已生成 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 已新增文档 `docs/V3_5_pws_year_ml_ready_build_notes.md`
- 已新增文档 `docs/V3_5_pws_year_ml_ready_dictionary.md`
- 已正式固定第三层 `TTHM` 主结果变量为 `tthm_sample_weighted_mean_ug_l`
- 已正式固定 `tthm_regulatory_exceed_label`（`>=80 ug/L`）与 `tthm_warning_label`（`>=60 ug/L`）两类标签口径，并明确 `60 ug/L` 仅为预警阈值
- 已正式固定 `level1 / level2 / level3` 为第三层机器学习样本分层命名，且满足“`level3` 包含于 `level2`，`level2` 包含于 `level1`”
- 已为 `ph`、`alkalinity`、`toc`、`free_chlorine` 与 `total_chlorine` 增加缺失标记列，并保留原始缺失值不做覆盖式插补
- 已确认 `V4_pws_year_ml_ready.csv` 行数为 `259,500`、字段数为 `38`
- 已确认 `level1` 样本数为 `199,802`、`level2` 样本数为 `26,975`、`level3` 样本数为 `6,193`
- 已确认 `tthm_regulatory_exceed_label=1` 的系统-年份样本数为 `5,618`，`tthm_warning_label=1` 的系统-年份样本数为 `19,853`
- 已明确 `annual_match_quality_tier` 保留在 `ml_ready` 表内，但默认不进入第一版主模型特征

## 9. 最近一次更新

最后更新时间：2026-03-31 10:18（Asia/Hong_Kong）

最近更新内容：

- 新增脚本 `scripts/build_v3_5_pws_year_ml_ready.py`，用于从第三层 `V3_pws_year_master.csv` 派生 V3.5 机器学习输入层
- 新增本地输出 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 新增文档 `docs/V3_5_pws_year_ml_ready_build_notes.md` 与 `docs/V3_5_pws_year_ml_ready_dictionary.md`
- 正式固定第三层 `TTHM` 主结果变量为 `tthm_sample_weighted_mean_ug_l`
- 正式固定 `tthm_regulatory_exceed_label` 与 `tthm_warning_label`，并明确 `80 ug/L` 为法规阈值、`60 ug/L` 仅为预警阈值
- 正式固定 `level1 / level2 / level3` 样本分层、`ml_level_max` 最高层级标记与 5 个机制变量缺失标记列
- 完成基础清洗边界冻结：校验主键唯一、统一字段类型、保留原始缺失、禁止覆盖式插补、禁止目标缺失样本误写标签
- 确认 `V4_pws_year_ml_ready.csv` 行数为 `259,500`、字段数为 `38`，可被 pandas 稳定回读
- 同步更新 `codex.md`，将 V3.5 过渡更新正式记入项目级说明书
- 补强 `scripts/build_v3_5_pws_year_ml_ready.py` 的 CSV 回读校验：不再只检查行列一致，而是按显式 schema 回读并校验关键字段 dtype，防止标签列、treatment 二值列和整数计数列在后续 V4 阶段发生类型漂移
- 新增统一读取模块 `scripts/io_v4_ml_ready.py`，正式固定 V4 `ml_ready` 表的 schema、统一读取函数与类型校验入口，后续 V4 脚本不再直接裸用 `pd.read_csv`
- 已验证统一读取函数可将 `tthm_regulatory_exceed_label`、`tthm_warning_label`、`has_disinfection_process` 恢复为 `Int8`，并将 `tthm_months_with_data` 恢复为 `Int64`

对应提交：

- 待用户确认是否执行 Git 提交与推送

## 10. 下一步任务

下一步最具体的工作是：

- 基于 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv` 进入 V4 正式建模准备阶段
- 明确第一版 `TTHM` 年度模型的任务拆分：回归主模型、法规阈值分类模型与预警阈值分类模型
- 按 `level1 / level2 / level3` 三档样本分别制定训练/验证/测试切分、编码与缺失处理方案
- 先以 baseline 特征集启动全国主模型，再与增强特征集和默认不入模字段做对照实验
- 保持第二层 `facility-month` 机制线并行，但不与第三层全国主模型线混表

---

## V2_Chapter1_Part1_Mainline_Update

### 当前主线调整

- 当前已明确：整个大论文第一章的主线采用“方案 A”，即先做数据基础、变量环境意义、表结构关系、分层设计与数据可用性评估
- 当前已明确：风险场景识别（方案 B）不作为第一章总框架，而作为后续探究阶段嵌入到第一章主线之后的应用思想
- 当前已明确：第一章第一部分的任务不是直接建模，不是直接做因果分析，也不是直接做全国风险场景识别，而是为这些工作建立可信的数据基础和方法边界

### 第一章第一部分当前定义

第一章第一部分的主题为：

“基于 SYR4 数据集的 DBP 相关数据基础梳理、环境变量意义解释、跨表可拼接性评估与后续分析层级设计”。

这一部分当前需要完成的工作包括：

1. 明确 SYR4 中 DBP 研究范围
2. 梳理各核心变量的环境意义
3. 理清核心数据表之间的关系
4. 评估不同层级下的数据可拼接性与覆盖率
5. 明确后续机器学习和因果分析分别应建立在哪种数据层级上
6. 输出可直接写入论文或报告的结构化成果

### 当前必须遵守的研究判断

- SYR4 的优势在于全国尺度、真实监管场景、多层级结构、结果变量与机制变量并存
- SYR4 的劣势在于缺失严重且非随机、监测不是为研究设计、时间不连续、处理信息不完整
- 严格样本级四键对齐（PWSID + WATER_FACILITY_ID + SAMPLING_POINT_ID + SAMPLE_COLLECTION_DATE）适合作为保守基线和可拼接性审计，不适合作为后续主建模底表
- 后续主分析的数据方向已明确为两条：
  - 全国广覆盖主表：PWS-year
  - 高信息机制子样本：PWS-facility-month
- 机器学习和因果分析不能共用同一套口径直接硬做，必须分层设计
- 当前阶段重点是建立可信数据产品和研究边界，而不是寻找最强相关性

### 当前第一章的分层框架

#### 第一层：严格样本级

键：
- PWSID + WATER_FACILITY_ID + SAMPLING_POINT_ID + SAMPLE_COLLECTION_DATE

定位：
- 保守基线
- 可拼接性审计
- sanity check

#### 第二层：设施-月份级

键：
- PWSID + WATER_FACILITY_ID + year + month

定位：
- 机制分析主层级
- 后续高风险场景内部聚合层级
- 受约束因果分析候选底表

#### 第三层：系统-年份级

键：
- PWSID + year

定位：
- 全国机器学习主表
- 全国风险识别主层级
- 系统级异质性分析主层级

### 对 V1 工作的当前定位

- V1_TTHM_strict_spearman_base_data 当前正式定位为：
  - 严格样本级保守基线
  - 样本级可拼接性审计
  - 第一层 sanity check
- 它的价值在于证明：在严格样本级口径下，SYR4 中 TTHM 与其他核心变量的跨表重合度有限
- 它的局限在于：不能直接承担后续多变量主建模任务，也不能直接代表后续分层分析的主数据底表

### 当前进展与下一步

- 当前已完成：围绕第一章整体路线的重新梳理，并明确“方案 A 为主、方案 B 为辅”的整体课题框架
- 当前已完成：第一章第一部分的正式结构化产出，包括变量环境意义、核心表关系、三层级可用性比较、V1 学术定位、后续数据路线图、论文提纲与执行清单
- 当前新增：已形成独立的 V2_ 开头 prompt 文档，并已据此完成第一章第一部分的执行与审计
- 下一步将进入：`PWS-year` 全国主表原型构建、`PWS-facility-month` 机制表原型构建，以及 treatment 解释变量摘要化

---

## V3_Chapter1_Part1_Prototype_Build_Update

### 当前定位

- V3 阶段已经把第二层和第三层从审计结论正式落地为两张可复用的原型主表
- V3 收尾所需的原始数据映射法则、缺失语义、样本分层规则与禁止误用规则已经固定完成
- 当前项目已从 V3 原型主表阶段进入 V3.5 机器学习输入层阶段，为 V4 正式建模做准备

### V3 主要产物

#### 1. 第二层原型表：`V3_facility_month_master`

键：
- `pwsid + water_facility_id + year + month`

文件：
- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- `docs/V3_facility_month_dictionary.md`
- `docs/V3_facility_month_build_notes.md`

当前状态：
- 行数：`1,442,728`
- 字段数：`98`
- 主键重复数：`0`
- `TTHM` 非缺失单元：`549,730`
- `HAA5` 非缺失单元：`481,761`
- `TTHM + 至少 2 个核心变量`：`3,811`
- `TTHM + 4 个核心变量全齐`：`0`

当前定位：
- 用作后续高风险场景内部分析和小模型机制分析的起点
- 不作为全国统一全变量宽表
- 更适合模块化变量集、pairwise 或小模型策略

#### 2. 第三层原型表：`V3_pws_year_master`

键：
- `pwsid + year`

文件：
- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`
- `docs/V3_pws_year_dictionary.md`
- `docs/V3_pws_year_build_notes.md`
- `docs/V3_prototype_audit_report.md`

当前状态：
- 行数：`259,500`
- 字段数：`130`
- 主键重复数：`0`
- `TTHM` 系统-年份单元：`199,802`
- `HAA5` 系统-年份单元：`165,379`
- `TTHM + 至少 2 个核心变量`：`26,975`
- `TTHM + 4 个核心变量全齐`：`60`

当前定位：
- 用作全国机器学习主表原型
- 适合先做广覆盖 baseline 和分层主模型
- 不适合承担细粒度机制解释

### V3 当前方法判断

- 第一层 strict_sample 继续保留为保守基线和可拼接性审计层，不进入主建模
- 第二层 facility-month 已经足够作为机制分析起点，但不能被误写成完整多变量宽表
- 第三层 pws-year 已经足够作为全国机器学习主表原型，但进入 V4 前仍需先固定字段映射法则和数据契约
- 当前最重要的不是立刻追求模型性能，而是先确保两张主表相对于原始 SYR4 的字段来源、聚合规则、缺失语义和误用边界被明确记录

### V3 收尾状态

- `docs/V3_Raw Data Mapping Rules.md` 已完成两张 V3 主表相对于原始 SYR4 的字段来源与聚合规则固化
- 已固定单位、缺失值语义、样本分层规则与禁止误用规则
- V3 已正式收尾完成，后续工作已切换到 V3.5 `ml_ready` 派生表构建与 V4 模型任务定义

---

## V3_5_V4_ML_Ready_Update

### 当前定位

- V3.5 阶段的目标不是直接追求模型性能，而是把第三层原型主表整理成可直接进入 V4 的机器学习输入层
- 本阶段只围绕第三层 `TTHM` 主线展开，不把第二层 `facility-month` 字段混入全国主模型输入表
- 本阶段已经完成主结果变量、标签规则、样本分层、缺失标记和基础清洗边界的冻结

### V3.5 主要产物

#### 1. 第三层机器学习输入表：`V4_pws_year_ml_ready`

键：
- `pwsid + year`

文件：
- `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- `docs/V3_5_pws_year_ml_ready_build_notes.md`
- `docs/V3_5_pws_year_ml_ready_dictionary.md`
- `scripts/build_v3_5_pws_year_ml_ready.py`

当前状态：
- 行数：`259,500`
- 字段数：`38`
- 主键重复数：`0`
- `level1` 样本数：`199,802`
- `level2` 样本数：`26,975`
- `level3` 样本数：`6,193`
- `tthm_regulatory_exceed_label=1`：`5,618`
- `tthm_warning_label=1`：`19,853`

### 当前方法判断

- 第三层 `ml_ready` 输入层已经具备进入 V4 正式建模的最小必要条件
- `tthm_sample_weighted_mean_ug_l` 已被固定为唯一连续型主结果变量，避免多目标并列造成口径漂移
- `annual_match_quality_tier` 保留在表中，但默认不进入第一版主模型
- `state_code` 仅作为候选 baseline 特征保留，不提前写死为必须入模变量
- treatment 二值字段保留原始缺失，不在 V3.5 阶段用 0 强行覆盖未知状态

### V4 进入条件

- 下一步可以围绕 `V4_pws_year_ml_ready.csv` 开始训练/验证/测试切分、编码、缺失处理和 baseline 建模
- V4 阶段仍需继续遵守禁止目标泄漏、禁止同源 `tthm_*` 摘要字段回灌模型、禁止把第二层机制线混成第三层全国宽表等规则
