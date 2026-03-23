# codex.md

## 1. 项目背景

本项目服务于基于美国 EPA SYR4 数据集的博士论文研究。

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

当前阶段目标是完成第一轮 `TTHM` 分析流程搭建：

- 以 `TOTAL TRIHALOMETHANES (TTHM).csv` 为主结果表
- 对齐少量第一轮最关键的 DBP 相关参数
- 构建可用于 Spearman 分析和第一轮机器学习的 analysis-ready 数据集

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

当前与第一轮 `TTHM` 构建直接相关的本地输出目录：

- `data_local/tthm_first_round/`
  - `tthm_corechem_dataset.csv`
  - `tthm_baseline_clean.csv`
  - `tthm_corechem_merge_report.md`
  - `tthm_field_audit.csv`
  - `tthm_missingness_summary.csv`
  - `tthm_match_summary.csv`
  - `tthm_predictor_combinations.csv`

各目录作用：

- `docs/`
  - 项目说明
  - 研究设计
  - 数据逻辑文档
  - 项目状态文档
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
- 第一轮准备对齐的参数表：
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

### 7.5 提交标题规则

每次重要更新都应使用清晰、准确的 commit message，能够反映实际改动内容。

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
- 已在本地生成第一轮 `TTHM` analysis-ready 数据集与 merge 报告
- 已确认当前数据足以进入 pairwise Spearman 分析与受限版 baseline 机器学习，但不足以直接支持 4 个核心化学变量同时完整的完整案例模型

## 9. 最近一次更新

最后更新时间：2026-03-23 15:20（Asia/Hong_Kong）

最近更新内容：

- 完成第一轮 `TTHM` 分析数据集构建脚本 `scripts/build_tthm_first_round.py`
- 完成 `TTHM` 与 `PH`、`TOTAL ALKALINITY`、`TOTAL ORGANIC CARBON`、`FREE RESIDUAL CHLORINE` 的两级匹配
- 生成本地输出目录 `data_local/tthm_first_round/` 及其 CSV/Markdown 报告
- 明确当前匹配覆盖率较低，适合做首轮 Spearman 和受限版 baseline ML，不适合作为高覆盖终版分析库

对应提交：

- `build first-round TTHM core chemistry dataset`

## 10. 下一步任务

下一步最具体的工作是：

- 基于 `tthm_corechem_dataset.csv` 开始首轮 pairwise Spearman 分析
- 对 `tthm_baseline_clean.csv` 评估可用于 baseline ML 的特征组合与缺失处理策略
- 评估是否有必要在下一轮放宽匹配规则，或补充少量高价值变量
- 在保持“小而干净”的前提下决定第二轮是否加入少量处理工艺或水质背景变量
