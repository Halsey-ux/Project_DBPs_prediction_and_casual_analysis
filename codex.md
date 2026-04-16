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
- 构建一个能够在监管数据不全面、不完整且具有时空异质性的现实条件下运行的 DBP 高风险场景分层预测框架
- 在广覆盖低信息条件下保持可用预测能力，并在高信息子样本中通过附加信息通路实现增强预测

## 3. 当前阶段目标

当前阶段目标已经从单条第三层主线增量验证，完成 `V5.5` 候选信息通路 readiness audit，并完成 `V5.6` 候选通路字段盘点、字段-Y 对齐与覆盖审计，进入先验因果-语义复核准备阶段：

- 将当前第三层正式主线重新表述为“基于美国 SYR4 的全国尺度 DBP 高风险场景正式主模型”，而不直接表述为通用全球模型
- 固定系统背景通路的当前正式版本，即第三层 `第一级样本` 上的 `baseline + structural + treatment`
- 固定水质特征通路的当前版本，即第三层 `PWS-year` 内部第二级样本上的 `baseline + pH + alkalinity + TOC`
- 将上述两条信息通路整合为同一分层预测框架中的互补部分，用于分别承担广覆盖风险识别与高信息水质增强预测/机制支撑
- 在不改变当前正式主模型定位的前提下，基于 `V5.5` 审计结果明确哪些候选通路具备覆盖率、标签重叠、可获得性和泄露边界上的后续准入基础
- 将项目总目标进一步明确为：不是追求单一万能模型，而是构建一个可在不同信息完整度下工作的分层预测框架
- 明确接受监管数据中的制度性缺失、变量覆盖不均衡与时空异质性是现实约束，并将其纳入框架设计而非视为异常噪音
- 继续区分“全国主线风险画像增强”“工程背景辅助增强”“水质增强预测”与“环境机制增强”的解释边界

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
- `data_local/V4_Chapter1_Part1_Experiments/`
  - V4 实验结果目录
  - 当前已按版本分层写入 `V4_3/tthm_regulatory_exceedance_prediction/` 与 `V4_3/tthm_anchored_risk_prediction/`
- `data_local/V5_Chapter1_Part1_Facility_Month_Module/`
  - V5 第二层 `facility-month` 模块结果目录
  - 当前已写入 `V5_0/`、`V5_1/`、`V5_2/`、`V5_5/` 与 `V5_6/`

各目录作用：

- `docs/`
  - `00_overview/`：项目概览、README、数据目录与项目状态说明
  - `01_design/`：第一章总体设计与高风险场景框架
  - `02_v1/`：V1 严格样本级 prompt 与相关说明
  - `03_v2/`：V2 第一章第一部分数据基础审计 prompt
  - `04_v3/`：V3 原型主表、字段映射与字段筛选规范
  - `05_v3_5/`：V3.5 `ml_ready` 构建说明、字典与执行 prompt
  - `06_v4/`：V4 文档总目录
    - `01_protocol/`：V4 任务定义与训练协议
    - `02_v4_1_baseline/`：V4.1 baseline 执行与摘要
    - `03_v4_1_learning_support/`：V4.1 面向理解的解释型文档
    - `04_v4_plan/`：V4 后续实验路线图与计划书
    - `05_v4_2_prompt/`：V4.2 机制核心 stage1 的 Codex 执行 prompt
    - `06_v4_2_execution/`：V4.2 执行报告
    - `07_v4_3_prompt/`：V4.3 TOC 增量实验的 Codex 执行 prompt
    - `08_v4_3_execution/`：V4.3 执行报告
    - `09_v4_4_prompt/`：V4.4 free_chlorine 增量实验的 Codex 执行 prompt
    - `10_v4_4_execution/`：V4.4 执行报告
    - `11_v4_4b_execution/`：V4.4b 执行报告
    - `12_v4_5_prompt/`：V4.5 结构/覆盖条件增量实验 prompt
    - `13_v4_5_execution/`：V4.5 执行报告
    - `14_v4_6_prompt/`：V4.6 treatment summary 增量实验 prompt
    - `15_v4_6_execution/`：V4.6 执行报告
    - `16_v4_7_prompt/`：V4.7 信息通路整合实验 prompt
    - `17_v4_7_execution/`：V4.7 执行报告
    - `V4_1_4_Update_Summary.md`：V4 阶段更新总览
    - `V4_Phase_Summary.md`：V4 阶段总结
    - `V4_Chapter1_Framework_Summary.md`：第一章框架型总结
  - `07_v5/`：V5 第二层 `facility-month` 高信息增强 / 机制支撑模块规划目录
    - `01_v5_0_prompt/`：V5.0 第二层可执行性审计 prompt
    - `02_v5_0_execution/`：V5.0 执行文档
    - `03_v5_1_prompt/`：V5.1 第二层 baseline 冻结 prompt
    - `04_v5_1_execution/`：V5.1 第二层 baseline 协议、执行报告与结果摘要
    - `05_v5_2_prompt/`：V5.2 第二层机制核心 stage1 prompt
    - `06_v5_2_execution/`：V5.2 第二层机制核心 stage1 协议、执行报告与结果摘要
    - `07_v5_2b_execution/`：V5.2b 第二层样本制度收束、专题分支重定义与后续计划
    - `08_v5_3_execution/`：V5.3 第二层框架决策支持定义与输入输出示例
    - `09_v5_4_execution/`：V5.4 候选信息通路审计与框架组装协议
    - `10_v5_5_prompt/`：V5.5 候选信息通路 readiness audit 的 Codex 执行 prompt
    - `11_v5_5_execution/`：V5.5 候选信息通路 readiness audit 执行报告
    - `12_v5_6_prompt/`：V5.6 候选通路字段盘点、字段-Y 对齐与覆盖审计 prompt
    - `13_v5_6_execution/`：V5.6 候选通路字段盘点、覆盖审计、数据可用性决策摘要与先验因果-语义复核清单
    - `V5_Master_Plan.md`：V5 总体计划
  - `V1_5_Update_Service_Scope_Summary.md`：V1-V5 大版本服务范围说明
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
- 已新增第一章方法文档 `docs/01_design/SYR4_Chapter1_High_Risk_Scenario_Framework.md`
- 已新增版本执行文档 `docs/02_v1/V1_TTHM_Strict_Spearman_Base_Data_Codex_Prompt.md`
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
- 已新增文档 `docs/01_design/Chapter1_Part1_DBP_Data_Foundation_and_Analysis_Layer_Design.md`
- 已正式完成第一章第一部分的结构化产出，包括目标定位、变量环境意义框架、核心表关系、三层级数据可用性比较、V1 正式定位与后续数据路线图
- 已确认严格样本级下 `TTHM + pH + 总碱度 + TOC + 游离余氯` 完整样本数仍为 `0`
- 已确认设施-月份级下上述核心四变量与 `TTHM` 的 pairwise 重合度有所改善，但完整共同非缺失单元仍为 `0`
- 已确认系统-年份级下 `TTHM + pH + 总碱度 + TOC + 游离余氯` 完整单元数为 `60`
- 已确认 `Paired TOC-Alkalinity` 仅与 `306` 个 `TTHM` 设施-月份键重合、与 `140` 个 `HAA5` 设施-月份键重合，更适合作为专题化 reduced dataset 而非通用主表
- 已明确 `HAA5` 应与 `TTHM` 平行纳入同一三层级分析框架，而不是后置补充
- 已完成 V3 第二层原型表 `V3_facility_month_master.csv`
- 已完成 V3 第三层原型表 `V3_pws_year_master.csv`
- 已新增文档 `docs/04_v3/V3_Facility_Month_Dictionary.md`
- 已新增文档 `docs/04_v3/V3_Facility_Month_Build_Notes.md`
- 已新增文档 `docs/04_v3/V3_PWS_Year_Dictionary.md`
- 已新增文档 `docs/04_v3/V3_PWS_Year_Build_Notes.md`
- 已新增文档 `docs/04_v3/V3_Prototype_Audit_Report.md`
- 已新增文档 `docs/04_v3/V3_PWS_Year_ML_Field_Selection_Protocol.md`
- 已明确：进入 V4 之前，V3 还需要完成一个最后的小更新，即用简洁直观的方式固定两张 V3 主表相对于原始 SYR4 数据的变量映射法则、缺失语义、样本分层规则与禁止误用规则
- 已新增一份专用 prompt 任务定义，用于指导新 Codex 会话专门完成上述 V3 收尾更新
- 已新增文档 `docs/04_v3/V3_Raw_Data_Mapping_Rules.md`
- 已正式固定 `V3_facility_month_master` 与 `V3_pws_year_master` 相对于原始 SYR4 的字段来源、聚合规则、缺失语义、样本分层规则与禁止误用规则
- 已明确第三层进入 V4 时应采用“全国主模型样本 / 加强模型样本 / 高信息模型样本”三档分层，并保留 `A_ready_for_national_ml` 作为更严格验收子集
- 已明确第二层继续作为机制分析与高信息小模型补充线，而不是替代第三层全国主表线
- 已明确在正式进入 V4 之前，需要增加一次 V3.5 过渡更新，用于构建第三层机器学习输入底座 `V4_pws_year_ml_ready.csv`
- 已明确 V3.5 只围绕第三层 `TTHM` 主线展开，先冻结主结果变量、标签规则、`第一级样本/2/3` 分层、缺失标记与基础清洗口径
- 已新增 V3.5 专用执行文档 `docs/05_v3_5/V3_5_V4_ML_Ready_Codex_Prompt.md`
- 已新增脚本 `scripts/build_v3_5_pws_year_ml_ready.py`
- 已生成 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 已新增文档 `docs/05_v3_5/V3_5_PWS_Year_ML_Ready_Build_Notes.md`
- 已新增文档 `docs/05_v3_5/V3_5_PWS_Year_ML_Ready_Dictionary.md`
- 已正式固定第三层 `TTHM` 主结果变量为 `tthm_sample_weighted_mean_ug_l`
- 已正式固定 `tthm_regulatory_exceed_label`（`>=80 ug/L`）与 `tthm_warning_label`（`>=60 ug/L`）两类标签口径，并明确 `60 ug/L` 仅为预警阈值
- 已正式固定 `第一级样本 / 第二级样本 / 第三级样本` 为第三层机器学习样本分层命名，且满足“`第三级样本` 包含于 `第二级样本`，`第二级样本` 包含于 `第一级样本`”
- 已明确第三层内部“第一级样本 / 第二级样本 / 第三级样本”与第一章“第一层 / 第二层 / 第三层”是两套不同概念，后续文档应避免混写
- 已为 `ph`、`alkalinity`、`toc`、`free_chlorine` 与 `total_chlorine` 增加缺失标记列，并保留原始缺失值不做覆盖式插补
- 已确认 `V4_pws_year_ml_ready.csv` 行数为 `259,500`、字段数为 `38`
- 已确认 `第一级样本` 样本数为 `199,802`、`第二级样本` 样本数为 `26,975`、`第三级样本` 样本数为 `6,193`
- 已确认 `tthm_regulatory_exceed_label=1` 的系统-年份样本数为 `5,618`，`tthm_warning_label=1` 的系统-年份样本数为 `19,853`
- 已明确 `annual_match_quality_tier` 保留在 `ml_ready` 表内，但默认不进入第一版主模型特征
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l2_toc_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l2_toc_increment.py`
- 已扩展 `scripts/v4_tthm_training_common.py`，使其支持版本化结果目录，并补充 `balanced_accuracy`、`specificity`、`MCC` 与 confusion matrix 指标输出
- 已完成 `V4.3 第二级样本 TOC increment` 的两条正式任务执行，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_3/`
- 已新增中文执行报告 `docs/06_v4/08_v4_3_execution/V4_3_Level2_TOC_Increment_Execution_Report.md`
- 已确认 `TOC` 在 `anchored` 任务上带来明显且稳定的边际增益
- 已确认 `TOC` 在 `regulatory` 任务上带来部分稳定增益：validation 与 complete-case 结果改善明显，test `ROC-AUC` 与 `balanced_accuracy` 提升，但 full `第二级样本` test `PR-AUC` 未继续上升
- 已确认 `pH + alkalinity + TOC` complete-case 子集上删除 missing flags 后结果与保留 flags 完全一致，说明相关 flags 在该子集内只是常量列
- 已完成 `baseline_without_n_facilities` 轻量敏感性检查，并确认 `n_facilities_in_master` 对 baseline 有一定贡献但不是压倒性驱动项
- 已新增文档 `docs/06_v4/09_v4_4_prompt/V4_4_Free_Chlorine_Increment_Codex_Prompt.md`
- 已将 `V4.4` 的正式方向固定为：在 `V4.3 TOC increment` 底座上检验 `free_chlorine + free_chlorine_missing_flag` 的边际增益
- 已明确 `V4.4` 必须保留 `第二级样本 baseline reference`、`mechanistic stage1 reference`、`TOC increment reference`、complete-case reference 和 no-missing-flags 敏感性检查
- 已明确 `V4.4` complete-case 的筛选口径必须扩展为 `pH + alkalinity + TOC + free_chlorine` 同时非缺失
- 已明确 `V4.4` 暂不进入 `total_chlorine`、树模型和超参数优化，继续沿用逐步增强实验路线
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l2_free_chlorine_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l2_free_chlorine_increment.py`
- 已扩展 `scripts/v4_tthm_training_common.py`，使其在 complete-case 子集出现单一类别 split 时输出可执行性说明而不是直接报错中断
- 已完成 `V4.4 第二级样本 free_chlorine increment` 的两条正式任务执行，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_4/`
- 已新增中文执行报告 `docs/06_v4/10_v4_4_execution/V4_4_Level2_Free_Chlorine_Increment_Execution_Report.md`
- 已确认 `free_chlorine` 在 full `第二级样本` 上对 `regulatory` 与 `anchored` 两条任务都带来方向一致但幅度很小的边际增益
- 已确认 `free_chlorine` 在 `第二级样本` 中覆盖率极低：`regulatory` 任务可用观测仅 `749 / 26,975`，`anchored` 任务可用观测仅 `540 / 17,501`
- 已确认 `pH + alkalinity + TOC + free_chlorine` complete-case 子集在 `group_by_pwsid` 切分后，`regulatory` 与 `anchored` 的 train split 都只剩负类，因此无法合法训练 `LogisticRegression`
- 已明确 `V4.4` 当前不能像 `V4.2` 与 `V4.3` 那样通过 complete-case 结果稳健地区分 `free_chlorine` 数值信号与缺失模式信号
- 已明确当前不建议直接进入 `V4.5 total_chlorine increment`，应先审计 `total_chlorine` 在 `第二级样本` 与 `facility-month` 口径下的覆盖率和可执行性
- 已新增脚本 `scripts/audit_v4_total_chlorine_readiness.py`
- 已完成 `V4.4b total_chlorine readiness audit`，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_4b/total_chlorine_readiness_audit/`
- 已新增中文执行报告 `docs/06_v4/11_v4_4b_execution/V4_4b_Total_Chlorine_Readiness_Audit_Report.md`
- 已确认 `total_chlorine` 在 `PWS-year` 中的覆盖率低于 `free_chlorine`：`第二级样本` 仅 `185 / 26,975`，`第三级样本` 仅 `152 / 6,193`
- 已确认 `pH + alkalinity + TOC + total_chlorine` complete-case 在 `regulatory` 与 `anchored` 的 `第二级样本 / 第三级样本` 四个任务层级中全部只剩负类，因此没有任何一个版本具备合法训练 `LogisticRegression` 的条件
- 已确认 `facility-month` 下 `TTHM + total_chlorine` 重合行数为 `2,385`，高于第三层，但 `TTHM + pH + alkalinity + TOC + total_chlorine` 全齐行数仍为 `0`
- 已明确 `V4.4b` 的正式结论是：暂停 `V4.5 total_chlorine increment`，把 `total_chlorine` 从第三层主线待增量变量调整为第二层机制专题候选变量
- 已新增总结文档 `docs/V1_4_Update_Summary.md`
- 已对 `V1` 至 `V4.4b` 的数据处理、主表构建、建模主线、关键结论、方法边界与风险点进行了系统中文总结
- 已明确当前阶段最稳妥的总判断是：`TOC` 是第三层主线上最可信的机制增强变量，`free_chlorine` 只有弱边际增益，`total_chlorine` 当前不适合继续进入第三层正式增量实验
- 已新增文档 `docs/06_v4/12_v4_5_prompt/V4_5_PWS_Year_Structural_Conditional_Increment_Codex_Prompt.md`
- 已将 `V4.5` 的正式方向固定为：在第三层 `PWS-year` 全国主线 baseline 基础上测试结构/覆盖条件特征的增量价值
- 已明确 `V4.5` 应优先回到 `第一级样本` 主线，而不是继续默认以 `第二级样本` 替代全国主样本
- 已明确 `V4.5` 的结论必须区分“预测增强”与“环境机制解释”，不得把结构/覆盖特征的增益误写成机制发现
- 已新增脚本 `scripts/v4_5_structural_conditional_common.py`
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l1_structural_conditional_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l1_structural_conditional_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l2_structural_conditional_reference.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l2_structural_conditional_reference.py`
- 已完成 `V4.5 PWS-year structural conditional increment` 的两条正式主任务与 `第二级样本` 补充对照，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_5/`
- 已新增中文执行报告 `docs/06_v4/13_v4_5_execution/V4_5_PWS_Year_Structural_Conditional_Increment_Execution_Report.md`
- 已确认结构/覆盖条件特征在 `第一级样本` 全国主线上对 `regulatory` 与 `anchored` 两条任务都带来明显且稳定的预测提升
- 已确认 `anchored` 是本轮提升更强的任务：`第一级样本` 上 validation `PR-AUC` 从 `0.1216` 升至 `0.2183`，test `PR-AUC` 从 `0.1162` 升至 `0.1990`
- 已确认 `regulatory` 也出现稳定增益：`第一级样本` 上 validation `PR-AUC` 从 `0.0696` 升至 `0.1003`，test `PR-AUC` 从 `0.0690` 升至 `0.1025`
- 已确认去掉 `annual_match_quality_tier` 后结果仍明显高于 baseline，说明主体增益来自结构/覆盖计数特征本身，而不是单个年度质量标签
- 已确认 `annual_match_quality_tier` 在 `第一级样本` 与 `第二级样本` 上都提供小幅但一致的附加增益，但它只能被解释为年度匹配质量标签，不能被解释为环境机制变量
- 已确认 `n_facilities_in_master` 仍有轻微贡献，但不是压倒性驱动项；`第一级样本 baseline` 去掉该变量后，`regulatory` 与 `anchored` 的 test `PR-AUC` 仅分别下降约 `0.0020` 与 `0.0028`
- 已确认 `第一级样本` 与 `第二级样本` 对同一组结构/覆盖条件特征的响应方向一致，但 `第二级样本` 的绝对 test `PR-AUC` 增益更大
- 已明确 `V4.5` 的最稳妥结论是：结构/覆盖条件特征值得纳入第三层全国主线正式预测模型，但其学术定位应是“风险画像增强”或“观测制度代理增强”，而不是“机制增强”
- 已新增文档 `docs/06_v4/14_v4_6_prompt/V4_6_PWS_Year_Treatment_Summary_Increment_Codex_Prompt.md`
- 已将 `V4.6` 的正式方向固定为：在 `第一级样本` 全国主线中测试 treatment summary 特征在 `baseline` 与 `V4.5 structural conditional` 对照框架下的独立增量价值
- 已明确 `V4.6` 必须至少保留 `baseline reference`、`structural conditional reference`、`treatment summary increment` 与 `structural + treatment combined` 四层对照链
- 已明确 `V4.6` 中的 treatment summary 特征只能被解释为系统工程背景或制度代理信号，不能被误写成环境机制发现
- 已新增脚本 `scripts/v4_6_treatment_summary_common.py`
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l1_treatment_summary_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l1_treatment_summary_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l2_treatment_summary_increment.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l2_treatment_summary_increment.py`
- 已完成 `V4.6 PWS-year treatment summary increment` 的两条 `第一级样本` 正式主任务与两条 `第二级样本` 补充对照，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_6/`
- 已新增中文执行报告 `docs/06_v4/15_v4_6_execution/V4_6_PWS_Year_Treatment_Summary_Increment_Execution_Report.md`
- 已确认 treatment summary 特征单独相对 `baseline` 的收益有限，在 `第一级样本 regulatory` 上几乎没有稳定独立价值
- 已确认 treatment summary 特征在控制 `V4.5 structural conditional` 后仍保留小而稳定的剩余增益，且 `anchored` 强于 `regulatory`
- 已确认 `第一级样本` 与 `第二级样本` 对 treatment summary 的响应方向一致，但 `第二级样本` 增益更强，这与 treatment 字段在 `第二级样本` 中覆盖率更高相一致
- 已明确 `V4.6` 的最稳妥定位是“工程背景辅助增强”或“制度代理辅助增强”，而不是“环境机制增强”
- 已明确当前更建议先阶段性收束第三层全国主线，把 `baseline`、`V4.5 structural conditional` 与 `V4.6 treatment combined` 的定位关系固定下来
- 已新增文档 `docs/06_v4/16_v4_7_prompt/V4_7_L2_Information_Path_Feature_Integration_Codex_Prompt.md`
- 已将 `V4.7` 的正式方向固定为：在第三层 `PWS-year` 内部第二级样本中探索性检验系统背景通路与水质特征通路的特征合并效果
- 已明确 `V4.7` 的核心问题不是直接改写当前正式主模型，而是判断两条信息通路在高信息样本中是互补、部分重叠还是大部分重复
- 已明确 `V4.7` 必须至少保留 `baseline reference`、`water-quality reference`、`system-background reference` 与 `full integration` 四层对照链
- 已新增文档 `docs/06_v4/V4_Phase_Summary.md`
- 已新增文档 `docs/06_v4/V4_Chapter1_Framework_Summary.md`
- 已新增文档 `docs/V1_5_Update_Service_Scope_Summary.md`
- 已新增目录 `docs/07_v5/`
- 已新增文档 `docs/07_v5/V5_Master_Plan.md`
- 已新增目录 `docs/07_v5/01_v5_0_prompt/`
- 已新增文档 `docs/07_v5/01_v5_0_prompt/V5_0_Facility_Month_Readiness_Audit_Codex_Prompt.md`
- 已对 `V4` 阶段当前主要进展、核心结论、信息通路框架思路、优点、风险、后续方向与最终框架目标进行了系统中文总结
- 已新增一份面向第一章主线的框架型总结文档，用于统一第三层正式主模型、第二层高信息增强模型与 `V4.7` 整合证据之间的角色关系
- 已新增一份 `V1-V5` 大版本服务范围说明文档，用于统一 `V1` 至 `V5` 的主线职责与递进关系
- 已新增 `V5` 总体计划文档，正式将 `V5` 定位为第二层 `facility-month` 高信息增强 / 机制支撑模块构建阶段
- 已新增脚本 `scripts/v4_7_information_path_integration_common.py`
- 已新增脚本 `scripts/train_v4_tthm_regulatory_l2_information_path_integration.py`
- 已新增脚本 `scripts/train_v4_tthm_anchored_l2_information_path_integration.py`
- 已完成 `V4.7 L2 information path feature integration` 的两条正式任务，结果统一写入 `data_local/V4_Chapter1_Part1_Experiments/V4_7/`
- 已新增中文执行报告 `docs/06_v4/17_v4_7_execution/V4_7_L2_Information_Path_Feature_Integration_Execution_Report.md`
- 已确认在 `第二级样本` 中，水质特征通路与系统背景通路相对 baseline 都形成稳定增益
- 已确认 `full integration` 在 `regulatory` 与 `anchored` 两条任务上都明显优于单独的水质特征通路和系统背景通路版本
- 已确认当系统背景通路已经进入模型后，`pH + alkalinity + TOC` 仍保留显著独立增量价值；反之系统背景通路在控制水质特征通路后也仍提供附加价值
- 已确认 `structural` 在合并框架中仍强于 `treatment`，但 `treatment` 不是零贡献
- 已明确 `V4.7` 最适合作为高信息样本中的信息通路互补证据，而不是直接改写第三层 `第一级样本` 正式主模型定位
- 已明确当前项目的最终目标应表述为：在不全面、不完整、具有时空异质性的监管数据条件下，构建可在不同信息完整度下运行的 DBP 高风险场景分层预测框架
- 已明确“EPA 监管数据本身不完整”不是削弱框架价值的理由，反而强化了本项目面向真实监管场景建模的现实意义
- 已明确制度性缺失与变量信息密度不均衡不会否定项目方向，但会决定框架的设计边界、解释边界与正式主模型的变量取舍逻辑
- 已明确当前最稳妥的目标不是追求一个在所有缺失模式下都同样最优的单一统一模型，而是建立“广覆盖主模型 + 高信息增强模型 + 探索性整合证据”的框架体系
- 已新增脚本 `scripts/train_v5_2_facility_month_mechanistic_core_stage1.py`
- 已完成 `V5.2 facility-month mechanistic core stage1` 正式实验，结果统一写入 `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_2/`
- 已新增中文文档 `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Protocol.md`
- 已新增中文文档 `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Execution_Report.md`
- 已新增中文文档 `docs/07_v5/06_v5_2_execution/V5_2_Facility_Month_Mechanistic_Core_Stage1_Result_Summary.md`
- 已确认 `V5.2` 与 `V5.1 baseline_core_minimal_stage1_reference` 使用完全同一批 `facility-month` complete-case 样本：train `2,073`、validation `362`、test `203`
- 已确认 `baseline_core_minimal + pH + alkalinity` 在 `test` 上相对同子样本 baseline 带来一致增益：`PR-AUC +0.0294`、`ROC-AUC +0.0215`、`balanced_accuracy +0.0090`
- 已确认 `baseline_core_minimal + pH + alkalinity` 在 `validation` 上仅 `ROC-AUC` 与 `balanced_accuracy` 轻微改善，而 `PR-AUC` 从 `0.0935` 下降到 `0.0865`，因此当前证据仍不足以写成“稳定增益”
- 已明确 `V5.2` 的最稳妥结论是：第二层当前具备有限、弱正向的第一轮正式机制支撑证据，但仍不应被写成已经成熟的第二层增强主链
- 已明确 `TOC` 仍可保留为第二层 reduced dataset 专题候选，但不能再被默认写成 `V5.2` 之后的线性主链下一步
- 已新增文档 `docs/07_v5/07_v5_2b_execution/V5_2b_Facility_Month_Sample_Framework_And_Boundary_Summary.md`
- 已新增文档 `docs/07_v5/07_v5_2b_execution/V5_3_TOC_Reduced_Dataset_Branch_Design.md`
- 已新增文档 `docs/07_v5/07_v5_2b_execution/V5_2b_Facility_Month_Follow_Up_Action_Plan.md`
- 已在 `V5_Master_Plan.md` 中正式补入 `V5.2b`，用于收束第二层样本制度、模块边界与 `V5.3` 专题分支定义
- 已明确 `V5` 当前尚未形成 `V4` 式正式三级样本制度，而是更适合维持“正式任务样本池 + 专题 complete-case 子样本池”的双层制度
- 已明确 `V5.0` 的 `match_quality_tier` 当前只能解释为第二层信息密度审计标签，不能直接等价写成 `V4` 式正式训练样本等级
- 已明确 `V5.3` 当前应重定义为 `TOC reduced dataset` 专题分支，而不是第二层正式主链的默认线性下一步
- 已新增文档 `docs/07_v5/08_v5_3_execution/V5_3_Framework_Decision_Support_Definition.md`
- 已新增文档 `docs/07_v5/08_v5_3_execution/V5_3_Framework_Input_Output_Examples.md`
- 已正式将 `V5.3` 更新为框架决策支持定义轮，用于固定整个分层框架的现实问题、输入输出逻辑和使用场景
- 已明确该框架的主价值不是重复完整监管结果，而是在不完整监管数据条件下进行风险筛查、优先级排序与局部证据整合
- 已明确第三层 `PWS-year` 应固定为广覆盖主筛查层，第二层 `facility-month` 应固定为局部场景支撑层
- 已明确面向环保局和水厂的最终输出不应只是单一高风险标签，而应包括综合风险等级、证据来源与建议动作
- 已将 `TOC reduced dataset` 从 `V5.3` 的默认主题下沉为后续专题子分支候选
- 已新增文档 `docs/07_v5/08_v5_3_execution/V5_3_Overall_Research_Framework_Status_And_Next_Steps.md`
- 已将当前整体课题思路总结为：基于 `SYR4` 真实监管数据，构建一个在信息不完整条件下生成多层级高风险证据、并服务于优先级排序、重点复核和补充监测决策的分层风险支持框架
- 已明确已完成工作在整体目标中的位置：数据基础与层级设计、第三层广覆盖主筛查线、第二层局部支撑线、框架语义与决策支持定义
- 已明确下一步优先级：先定义风险证据整合层输出规则，再决定是否启动 `TOC reduced dataset` 专题审计，随后再设计因果分析后续嵌套模块
- 已新增文档 `docs/07_v5/09_v5_4_execution/V5_4_Candidate_Pathway_Audit_And_Framework_Assembly_Protocol.md`
- 已正式将 `V5.4` 定义为候选信息通路审计与框架组装协议轮，用于固定通路准入、通路分级、模型组装、泄露控制和三层框架组织规则
- 已明确后续 V5 更新应按协议逐条审计候选通路，而不是直接把每个通路机械训练成独立模型或简单投票
- 已在 `V5_Master_Plan.md` 中补充 `V5.4` 协议定位与 `V5.5+` 候选通路逐条审计计划
- 已新增文档 `docs/07_v5/10_v5_5_prompt/V5_5_Candidate_Pathway_Readiness_Audit_Codex_Prompt.md`
- 已将 `V5.5` 的下一轮执行任务定义为候选信息通路 readiness audit，用于把 `V5.4` 协议落地为字段清单、覆盖率、标签重叠、泄露风险和框架角色判定表
- 已新增脚本 `scripts/audit_v5_5_candidate_pathway_readiness.py`
- 已完成 `V5.5 candidate pathway readiness audit`，结果统一写入 `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_5/`
- 已新增中文执行报告 `docs/07_v5/11_v5_5_execution/V5_5_Candidate_Pathway_Readiness_Audit_Report.md`
- 已确认当前 `V3_pws_year_master.csv` 为 `0` 字节，本轮未原位修改该文件，而是从 `V3_facility_month_master.csv` 按 `pwsid + year` 临时上卷形成第三层审计视图
- 已确认 `PWS-year` 结构背景通路和设施复杂度通路覆盖率均为 `100.00%`，与 `TTHM` 标签重叠率均为 `76.99%`，与 `HAA5` 标签重叠率均为 `63.73%`，适合优先进入后续主筛查模型准入测试
- 已确认 `PWS-year` 酸碱与缓冲条件通路覆盖率为 `39.18%`，与 `TTHM` 标签重叠率为 `18.97%`，与 `HAA5` 标签重叠率为 `16.62%`，适合作为优先可选机制证据模块候选
- 已确认 NOM/有机前体物通路和消毒剂与残余消毒剂通路机制意义较强，但标签重叠率和时序边界不足，当前更适合作为专题审计或可选机制模块，不应直接进入广覆盖主模型
- 已确认监测覆盖度与证据质量通路应进入证据质量模块，不能解释为导致 DBP 高风险的化学机制因素
- 已新增脚本 `scripts/recover_v3_pws_year_master_from_facility_month.py`
- 已完成 `V3_pws_year_master.csv` 受控恢复：从未损坏的 `V3_facility_month_master.csv` 复用原始 V3 年度聚合逻辑重建第三层主表
- 已将原 `0` 字节异常文件备份为本地文件 `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.zero_byte_20260401_091846.csv`
- 已生成本地校验报告 `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master_recovery_validation.json`
- 已新增恢复记录文档 `docs/04_v3/V3_PWS_Year_Master_Recovery_Note.md`
- 已确认恢复后的 `V3_pws_year_master.csv` 行数 `259,500`、字段数 `130`、主键重复数 `0`，并与历史 V3 关键统计一致
- 已确认使用恢复后的 `V3_pws_year_master.csv` 临时生成的 V4 `ml_ready` 与现有 `V4_pws_year_ml_ready.csv` 逐列逐行一致
- 已在恢复后重新运行 `scripts/audit_v5_5_candidate_pathway_readiness.py`，当前 V5.5 本地审计输出已读取正式恢复后的 `V3_pws_year_master.csv`
- 已更新 `docs/07_v5/11_v5_5_execution/V5_5_Candidate_Pathway_Readiness_Audit_Report.md`，说明初次临时上卷口径与恢复后正式主表重跑状态
- 已检索 `docs/06_v4/` 下 V4 阶段所有相关文档，确认恢复后的 `V3_pws_year_master.csv` 可派生出与 V4 文档记录一致的样本层级、正类数量和 treatment 覆盖统计
- 已在 `docs/04_v3/V3_PWS_Year_Master_Recovery_Note.md` 中补充 V4 文档交叉校验结果
- 已新增脚本 `scripts/audit_local_project_data_integrity.py`
- 已完成本地项目数据完整性审计，生成报告 `docs/00_overview/Local_Project_Data_Integrity_Audit_Report_2026_04_15.md`
- 已确认 `data_local/` 共检查 `167` 个文件，三个关键本地数据集 `V3_facility_month_master.csv`、`V3_pws_year_master.csv`、`V4_pws_year_ml_ready.csv` 均通过预期行数和字段数校验
- 已确认当前正式业务数据未发现新的 0 字节损坏文件；唯一 0 字节文件为已保留的事故证据备份 `V3_pws_year_master.zero_byte_20260401_091846.csv`
- 已确认原始 CSV 数据目录 `D:\Syr4_Project\syr4_DATA_CSV` 存在且未发现 0 字节文件；历史记录中的 `D:\SYR4_Data\syr4_DATA_excel` 当前不存在，需视为非当前可用输入路径
- 已再次确认 `data_local/` 大型本地数据和原始 SYR4 数据不应直接提交到 GitHub，GitHub 仅建议备份脚本、文档、配置、数据字典和轻量审计报告
- 已新增脚本 `scripts/audit_legacy_root_imports_cleanup.py`
- 已完成 `legacy_root_imports` 清理审计，生成报告 `docs/00_overview/Legacy_Root_Imports_Cleanup_Audit_Report_2026_04_15.md`
- 已确认 `docs/**/legacy_root_imports/` 下共有 `10` 个 legacy 文件，其中 `3` 个为内容完全重复的可删除候选，`4` 个需要人工复核，`3` 个仅 legacy 存在并建议暂时保留
- 已按用户确认删除 `3` 个完全重复的 legacy 副本，仅保留正式位置文件；其余 `7` 个 legacy 文件未删除，仍需人工复核或暂时保留
- 已新增文档 `docs/07_v5/12_v5_6_prompt/V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Codex_Prompt.md`
- 已将下一轮 `V5.6` 任务从直接冻结主筛查输入组前移为：基于 `V5.5` readiness audit 结果，补完候选通路字段盘点、字段-Y 对齐、通路内部覆盖结构和 complete/partial-case 可训练性审计
- 已明确 `V5.6` 仍不是建模轮，也不是最终因果通路定稿轮，而是为后续先验因果-语义分析、通路字段重组和主筛查特征组冻结提供数据事实基础的审计轮
- 已新增脚本 `scripts/audit_v5_6_candidate_pathway_field_inventory.py`
- 已完成 `V5.6 Candidate Pathway Field Inventory And Coverage Audit`，本地结果写入 `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_6/`
- 已新增中文执行文档目录 `docs/07_v5/13_v5_6_execution/`
- 已生成 `V5_6_all_field_inventory.csv`、`V5_6_field_label_alignment.csv`、`V5_6_candidate_pathway_field_map.csv`、`V5_6_pathway_internal_coverage_summary.csv`、`V5_6_pathway_complete_partial_case_summary.csv` 和 `V5_6_candidate_pathway_field_inventory_summary.json`
- 已新增中文报告 `V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Report.md`、`V5_6_Pathway_Data_Availability_Decision_Summary.md` 和 `V5_6_Causal_Semantic_Review_Todo_List.md`
- 已确认本轮使用 `V3_pws_year_master.csv`、`V3_facility_month_master.csv` 与 `V4_pws_year_ml_ready.csv`；其中 `V4_pws_year_ml_ready.csv` 仅作为 TTHM 主线字段对照表，不用于 HAA5 可训练性判断
- 已确认 `PWS-year` 结构背景通路和设施复杂度通路具备较好的数据覆盖基础；处理工艺通路在修正摘要/覆盖标记口径后仍为约 `15.21%` 通路覆盖率；酸碱与缓冲条件通路为可选机制证据模块候选；NOM 与消毒剂相关通路完整组合和标签重叠基础不足，更适合专题审计或先验语义复核
- 已明确下一步不应立即冻结主筛查输入组，而应先进入先验因果-语义分析，重点复核结果字段、样本数/月份数/设施数、证据质量字段、消毒剂时序边界以及水质强度字段与监测覆盖字段的拆分

## 9. 最近一次更新

最后更新时间：2026-04-15 20:00（Asia/Hong_Kong）

最近更新内容：

- 已完成 `V5.6 Candidate Pathway Field Inventory And Coverage Audit`
- 已新增脚本 `scripts/audit_v5_6_candidate_pathway_field_inventory.py`
- 已读取 `V3_pws_year_master.csv`、`V3_facility_month_master.csv` 与 `V4_pws_year_ml_ready.csv` 完成全字段 inventory、字段-Y 对齐、候选通路字段展开、通路内部覆盖结构和 complete/partial-case 样本基础审计
- 已生成本地结果目录 `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_6/`
- 已输出 `V5_6_all_field_inventory.csv`、`V5_6_field_label_alignment.csv`、`V5_6_candidate_pathway_field_map.csv`、`V5_6_pathway_internal_coverage_summary.csv`、`V5_6_pathway_complete_partial_case_summary.csv` 和 `V5_6_candidate_pathway_field_inventory_summary.json`
- 已新增中文执行文档目录 `docs/07_v5/13_v5_6_execution/`
- 已新增 `V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Report.md`、`V5_6_Pathway_Data_Availability_Decision_Summary.md` 和 `V5_6_Causal_Semantic_Review_Todo_List.md`
- 已确认 `PWS-year` 全字段数为 `130`，`facility-month` 全字段数为 `98`，`V4_pws_year_ml_ready` 字段数为 `38`
- 已确认 `PWS-year` 结构背景通路和设施复杂度通路的任意字段覆盖率均为 `100.00%`，与 `TTHM/HAA5` 标签重叠率分别为 `76.99%` 和 `63.73%`
- 已确认 `PWS-year` 处理工艺通路在修正摘要/覆盖标记口径后任意字段覆盖率为 `15.21%`，与 `TTHM/HAA5` 标签重叠率分别为 `10.29%` 和 `9.13%`
- 已确认 `PWS-year` 酸碱与缓冲条件通路任意字段覆盖率为 `39.18%`，NOM/有机前体物通路为 `7.59%`，消毒剂与残余消毒剂通路为 `3.47%`
- 已确认 `facility-month` NOM、酸碱和消毒剂相关通路虽有机制意义，但与同周期 `TTHM/HAA5` 的直接字段-Y 重叠明显有限，后续更适合专题审计、高信息子样本分析或先验语义复核
- 已明确结果谱系字段、样本数/月份数/设施数、match quality、缺失标记、消毒剂字段和合规/纠正行动类字段均需进入后续先验因果-语义复核清单
- 已同步更新 `codex.md`

对应提交：

- 最近已推送提交：`008afd0`（`Audit legacy root imports cleanup`）
- 建议本次提交信息：`feat: add V5.6 pathway field inventory audit`
- 本次提交范围建议包括 V5.6 审计脚本、V5.6 中文执行文档和 `codex.md` 更新；`data_local/V5_6/` 本地 CSV/JSON 结果按当前 `.gitignore` 保留在本地，不默认提交
- 本次更新尚未提交，待用户确认是否执行 Git 提交与推送

补充更新：
- 更新时间：2026-04-16（Asia/Hong_Kong）
- 更新内容概述：按用户要求补充 `V5_6_Candidate_Pathway_Field_Inventory_And_Coverage_Audit_Report.md`，新增 `7.1 通路字段明细与 n>=1/2/3 标签对齐结果`，逐通路列出具体字段、每个字段与 `TTHM/HAA5` 的覆盖率和对齐条数，并补充整条通路在 `n>=1`、`n>=2`、`n>=3` 口径下的总体可用条数、覆盖率和标签对齐条数。
- 对应 commit 信息：尚未提交；建议提交信息为 `docs: expand V5.6 pathway alignment details`。
## 10. 下一步任务

下一步最具体的工作是：

- 基于 `docs/07_v5/13_v5_6_execution/V5_6_Causal_Semantic_Review_Todo_List.md` 启动下一轮先验因果-语义分析，重点复核泄露风险、时序边界、应用可得性、机制强度字段与监测覆盖字段的拆分
- `V5.5` 审计已在恢复后重新运行；后续如继续修改 V5.5 脚本或通路定义，应继续使用恢复后的正式 `V3_pws_year_master.csv`
- 若用户确认执行 Git 备份，应仅提交脚本、文档、配置和轻量审计报告，不提交 `data_local/` 大型本地数据、原始 SYR4 数据、`scratch/` 或事故 0 字节备份文件
- 如需继续清理冗余文件，应只处理 `Legacy_Root_Imports_Cleanup_Audit_Report_2026_04_15.md` 中剩余的 `needs_manual_review` 和 `legacy_only_keep_until_reviewed` 文件，且必须先人工比较内容差异再决定迁移、合并或删除
- 基于 `V5.6` 字段审计结果，形成字段准入/暂缓/仅证据质量/仅解释的决策表
- 主筛查候选输入组冻结应放在 `V5.6` 字段审计和后续先验因果-语义复核之后执行，不应在尚未完成泄露风险和语义归属复核时直接定稿
- split 口径下的 train / validation / test 正负样本基础审计需在模型准入测试或特征冻结前补做
- 继续保留本地 `V3_pws_year_master.zero_byte_20260401_091846.csv` 和恢复校验 JSON 作为事故记录，不纳入 GitHub
- 继续禁止同周期同目标 DBP 结果字段、单项组分、合规与纠正行动类变量作为前置预测输入
- 暂不进入树模型、超参数优化或多模型简单投票，先完成模型准入输入组冻结和泄露边界固化

## 11. 当前框架判断

当前项目对第三层及相关高信息样本分析的最新统一表述为：

- 当前项目不再单纯追求一个固定输入的万能统一模型，而是逐步构建“基于不同信息通路的 DBP 高风险场景分层预测框架”
- 该框架的现实目标不是在所有缺失模式下寻找一个同样最优的单一模型，而是在不同信息完整度下保持可用预测能力，并在高信息条件下实现进一步增强
- 框架设计的出发点是：EPA 级别监管数据本身就不全面、不完整且具有明显时空异质性，因此模型应适应这种现实条件，而不是预设完整观测场景
- 该框架当前已经形成两条核心信息通路：系统背景通路依托第三层 `第一级样本` 的 `baseline + structural + treatment`，水质特征通路当前主要依托第三层 `PWS-year` 内部第二级样本上的 `baseline + pH + alkalinity + TOC`
- 系统背景通路当前主要承担美国全国尺度的广覆盖风险识别任务，其最稳妥定位是“基于美国 SYR4 的全国尺度 DBP 高风险场景正式主模型”
- 水质特征通路当前主要承担高信息样本下的水质增强预测与机制支撑任务，其价值在于提供更接近环境过程的补充证据
- 当前对制度性缺失的判断是：缺失模式本身可能携带制度代理信息，因此它不会自动削弱模型价值，但要求项目在解释时明确区分风险识别价值与环境机制解释价值
- 当前对变量覆盖不均衡的判断是：项目价值不在于强行纳入尽可能多的监管参数，而在于识别哪些核心稳定特征足以支持广覆盖预测，哪些附加变量值得在高信息子样本中作为增强层保留
- `V4.7` 已进一步表明：在 `第二级样本` 高信息样本中，两条信息通路合并后能形成更强预测表现，且双方在控制对方后仍保留独立价值
- 因此当前框架下，两条信息通路更适合被视为互补部分，而不是必须二选一保留的竞争模型
- `V4.7` 的最稳妥定位仍是高信息样本中的探索性整合证据，而不是新的全国正式主模型结论
- 当前最稳妥的总体表述是：本项目正在基于美国 `SYR4` 数据，构建一个能够在不完整且时空异质的监管数据条件下运行的 DBP 高风险场景分层预测框架原型，其中全国正式主模型、高信息增强模型与探索性整合证据分别承担不同角色
- `V5.4` 已进一步明确：后续通路筛选应先按机制解释、覆盖率、标签重叠覆盖率、应用可获得性、泄露风险、增量价值、稳定性和决策可解释性进行准入审计，再决定是否进入正式框架
- 当前框架不应被实现为多个通路模型的简单平均或投票，而应组织为“广覆盖主筛查模型 + 可选机制证据模块 + 证据整合与行动建议层”
- 监测覆盖度和数据质量变量应优先服务于证据等级、完整性和可信度判断，而不应被直接解释为导致 DBP 高风险的化学机制因素
- 同周期同目标家族的 DBP 结果变量和组分变量不得作为预测输入；单项 DBP、合规、纠正行动等信息只有在用途、时间顺序和泄露边界清楚后，才能进入解释或后续专题模块

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
- `docs/04_v3/V3_Facility_Month_Dictionary.md`
- `docs/04_v3/V3_Facility_Month_Build_Notes.md`

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
- `docs/04_v3/V3_PWS_Year_Dictionary.md`
- `docs/04_v3/V3_PWS_Year_Build_Notes.md`
- `docs/04_v3/V3_Prototype_Audit_Report.md`

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

- `docs/04_v3/V3_Raw_Data_Mapping_Rules.md` 已完成两张 V3 主表相对于原始 SYR4 的字段来源与聚合规则固化
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
- `docs/05_v3_5/V3_5_PWS_Year_ML_Ready_Build_Notes.md`
- `docs/05_v3_5/V3_5_PWS_Year_ML_Ready_Dictionary.md`
- `scripts/build_v3_5_pws_year_ml_ready.py`

当前状态：
- 行数：`259,500`
- 字段数：`38`
- 主键重复数：`0`
- `第一级样本` 样本数：`199,802`
- `第二级样本` 样本数：`26,975`
- `第三级样本` 样本数：`6,193`
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

