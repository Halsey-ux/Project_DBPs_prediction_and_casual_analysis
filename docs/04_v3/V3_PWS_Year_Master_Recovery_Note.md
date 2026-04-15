# V3_pws_year_master 恢复记录

## 1. 事件概况

- 发现时间：2026-04-15
- 异常文件：`data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`
- 异常状态：文件大小为 `0` 字节
- 文件系统显示的异常文件时间：`2026-04-01 09:18:46`
- 影响范围：该文件是第三层 `PWS-year` 原型主表，理论上应作为 V3.5、V4 和后续 V5 通路审计的第三层来源表之一

本次检查确认，除该文件外，项目业务数据目录中没有发现其他核心业务文件为 `0` 字节。`.codex_tmp` 与 `scratch/.codex_tmp` 中的 Python 包标记文件不属于项目数据损坏。

## 2. 恢复原则

本次没有直接从原始 SYR4 数据完整重跑 V3 全流程，而是采用受控恢复方式：

1. 保留当前 `0` 字节文件作为事故证据备份。
2. 使用未损坏的 `V3_facility_month_master.csv` 作为输入。
3. 复用原始 V3 构建脚本中的年度聚合逻辑，只重建 `V3_pws_year_master.csv`。
4. 不重新生成 `V3_facility_month_master.csv`，避免扩大改动范围。
5. 恢复后同时进行 V3 层级统计校验和 V4 下游一致性校验。

该方法符合 V3 文档中已经固定的规则：`V3_pws_year_master.csv` 是从第二层 `V3_facility_month_master.csv` 进一步聚合得到的年度主表，而不是从原始 SYR4 表重新建立一套平行口径。

## 3. 本次新增恢复脚本

新增脚本：

- `scripts/recover_v3_pws_year_master_from_facility_month.py`

脚本功能：

- 检查当前 `V3_pws_year_master.csv` 是否为 `0` 字节。
- 将当前异常文件备份为 `V3_pws_year_master.zero_byte_20260401_091846.csv`。
- 读取 `V3_facility_month_master.csv`。
- 调用 `build_v3_chapter1_part1_prototypes.py` 中的 `build_pws_year_master()` 和 `order_pws_year_columns()`。
- 先写入临时恢复文件 `V3_pws_year_master.recovered_tmp.csv`。
- 校验通过后再替换正式 `V3_pws_year_master.csv`。
- 生成本地校验报告 `V3_pws_year_master_recovery_validation.json`。

## 4. 恢复输出

正式恢复文件：

- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv`

异常备份文件：

- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.zero_byte_20260401_091846.csv`

本地校验报告：

- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master_recovery_validation.json`

上述 `data_local` 文件仅保留在本地，不纳入 GitHub。

## 5. V3 层级校验结果

恢复后的 `V3_pws_year_master.csv` 已通过以下校验：

| 指标 | 恢复后结果 | 预期记录 | 结论 |
|---|---:|---:|---|
| 行数 | `259,500` | `259,500` | 一致 |
| 字段数 | `130` | `130` | 一致 |
| `pwsid + year` 主键重复数 | `0` | `0` | 一致 |
| `TTHM` 系统-年份单元数 | `199,802` | `199,802` | 一致 |
| `HAA5` 系统-年份单元数 | `165,379` | `165,379` | 一致 |
| `TTHM + 至少 2 个核心变量` | `26,975` | `26,975` | 一致 |
| `TTHM + 4 个核心变量全齐` | `60` | `60` | 一致 |

这些结果与既有 V3 文档和 `codex.md` 中记录的第三层主表统计一致。

## 6. V4 下游一致性校验

为确认恢复后的年度主表与此前 V3.5/V4 实际使用版本一致，本次进一步使用恢复后的 `V3_pws_year_master.csv` 临时生成 V4 `ml_ready` 数据，并与现有正式文件进行逐列对齐检查：

- 现有正式文件：`data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
- 临时生成方式：复用 `build_v3_5_pws_year_ml_ready.py` 中的 `build_dataset()` 逻辑
- 对齐方式：按 `pwsid + year` 排序后逐列比较
- 比较结果：`frame_equal = true`

摘要指标如下：

| 指标 | 临时重建结果 | 现有 V4 文件 | 结论 |
|---|---:|---:|---|
| 行数 | `259,500` | `259,500` | 一致 |
| 字段数 | `38` | `38` | 一致 |
| `level1` 样本数 | `199,802` | `199,802` | 一致 |
| `level2` 样本数 | `26,975` | `26,975` | 一致 |
| `level3` 样本数 | `6,193` | `6,193` | 一致 |
| `tthm_regulatory_exceed_label=1` | `5,618` | `5,618` | 一致 |
| `tthm_warning_label=1` | `19,853` | `19,853` | 一致 |
| 逐列逐行比较 | `true` | `true` | 一致 |

因此，恢复后的 `V3_pws_year_master.csv` 与此前用于 V3.5/V4 的版本在下游建模输入层面保持一致。

## 7. 对后续工作的影响

本次恢复后，后续 V5.5 候选信息通路 readiness audit 可以继续使用正式恢复后的 `V3_pws_year_master.csv`，不再需要依赖从 `V3_facility_month_master.csv` 临时派生的替代口径。

建议：

- 后续如果已经基于空文件状态运行过 V5.5 审计，应重新运行一次 V5.5 审计脚本。
- 后续文档中如引用 V3 第三层主表，应使用恢复后的正式文件。
- 本次异常应在 `codex.md` 中记录，作为重要数据恢复事件。

## 8. V4 文档交叉校验

恢复后进一步检索了 `docs/06_v4/` 下 V4 阶段所有 Markdown 文档中关于 `V3_pws_year_master`、`V4_pws_year_ml_ready.csv`、第三层样本等级和关键样本统计的描述。

检索结论如下：

- V4 阶段正式训练入口统一为 `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`。
- V4 文档直接提到 `V3_pws_year_master` 的位置主要是阶段总结中对 V3/V3.5 产物的概括；V4 正式建模文档不直接读取 `V3_pws_year_master.csv`。
- 因此，本次一致性校验的核心是确认：恢复后的 `V3_pws_year_master.csv` 能否重新派生出与 V4 文档记录完全一致的 `V4_pws_year_ml_ready.csv`。

已确认以下 V4 文档记录与当前恢复后数据一致：

| V4 文档描述 | V4 文档记录 | 恢复后校验结果 | 结论 |
|---|---:|---:|---|
| `V4_pws_year_ml_ready.csv` 总行数 | `259,500` | `259,500` | 一致 |
| `第一级样本` | `199,802` | `199,802` | 一致 |
| `第二级样本` | `26,975` | `26,975` | 一致 |
| `第三级样本` | `6,193` | `6,193` | 一致 |
| `tthm_regulatory_exceed_label = 1` | `5,618` | `5,618` | 一致 |
| `tthm_warning_label = 1` | `19,853` | `19,853` | 一致 |
| `第一级样本` 至少 1 个 treatment summary 字段非缺失 | `26,702` | `26,702` | 一致 |
| `第一级样本` 6 个 treatment summary 字段全部缺失 | `173,100` | `173,100` | 一致 |
| `第二级样本` 至少 1 个 treatment summary 字段非缺失 | `19,266` | `19,266` | 一致 |
| `第二级样本` 6 个 treatment summary 字段全部缺失 | `7,709` | `7,709` | 一致 |

因此，恢复后的 `V3_pws_year_master.csv` 不仅与 V3/V3.5 记录一致，也与 V4 所有核心样本层级和下游特征覆盖描述一致。

## 9. 当前结论

`V3_pws_year_master.csv` 已完成受控恢复。恢复依据来自未损坏的 `V3_facility_month_master.csv` 和原始 V3 年度聚合逻辑。恢复后的 V3 关键统计与历史文档记录一致，并且由其临时生成的 V4 `ml_ready` 数据与现有正式 V4 文件逐列一致。

因此，本次恢复可以视为成功，不改变此前 V3.5、V4 和 V5 已形成的主要结论。
