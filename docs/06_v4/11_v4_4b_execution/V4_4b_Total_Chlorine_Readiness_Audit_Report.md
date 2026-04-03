# V4.4b Total Chlorine Readiness Audit 执行报告

- 更新时间：2026-04-03 14:08（Asia/Hong_Kong）
- 对应阶段：`V4.4b`
- 审计目标：在决定是否启动 `V4.5 total_chlorine increment` 之前，先评估 `total_chlorine` 在当前数据体系中的覆盖率、split 可执行性与 complete-case 可训练性
- 输入表：
  - `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv`
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 统一读取入口：
  - `scripts/io_v4_ml_ready.py`
  - `scripts/audit_v4_total_chlorine_readiness.py`
- 结果目录：
  - `data_local/V4_Chapter1_Part1_Experiments/V4_4b/total_chlorine_readiness_audit/`

## 1. 本轮任务定义

`V4.4b` 不是正式建模轮次，而是进入 `total_chlorine increment` 前的 readiness audit。目标不是直接训练模型，而是回答三个更基础的问题：

- `total_chlorine` 在 `PWS-year` 的 `level1 / level2 / level3` 中是否有足够覆盖率
- 在 `regulatory` 与 `anchored` 任务下，`pH + alkalinity + TOC + total_chlorine` complete-case 子集是否还能在既有 `group_by_pwsid` 切分中合法训练
- 如果第三层主线不可行，`facility-month` 是否至少为后续机制线保留了足够的变量重合度

## 2. 审计范围与口径

### 2.1 `PWS-year` 审计范围

本轮审计使用：

- `level1`
- `level2`
- `level3`

并重点检查以下列：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `total_chlorine_sample_weighted_mean_mg_l`

### 2.2 任务层级审计范围

继续沿用两条正式任务：

- `tthm_regulatory_exceedance_prediction`
- `tthm_anchored_risk_prediction`

并分别在：

- `level2`
- `level3`

下检查 complete-case 子集的 split 类别分布与 `LogisticRegression` 可训练性。

### 2.3 `facility-month` 审计范围

本轮额外检查第二层 `V3_facility_month_master.csv` 中：

- `tthm_mean_ug_l`
- `ph_mean`
- `alkalinity_mean_mg_l`
- `toc_mean_mg_l`
- `total_chlorine_mean_mg_l`

的重合情况，用于判断 `total_chlorine` 是否更适合作为第二层机制线专题变量，而不是第三层全国主模型增量变量。

## 3. `PWS-year` 覆盖率结果

| 层级 | 行数 | `total_chlorine` 非缺失 | 非缺失率 | `free_chlorine` 非缺失 | `free_chlorine` 非缺失率 | `pH + alkalinity + TOC + total_chlorine` complete-case |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `level1` | 199,802 | 783 | 0.39% | 3,547 | 1.78% | 36 |
| `level2` | 26,975 | 185 | 0.69% | 749 | 2.78% | 36 |
| `level3` | 6,193 | 152 | 2.45% | 618 | 9.98% | 36 |

关键观察：

- `total_chlorine` 在三个层级上的覆盖率都明显低于 `free_chlorine`。
- 即便限制到 `level3`，`total_chlorine` 非缺失率也只有 `2.45%`。
- `pH + alkalinity + TOC + total_chlorine` 的 complete-case 总行数在 `level1 / level2 / level3` 中都只有 `36` 行，说明这个变量的可用性不是简单通过升层就能解决。

## 4. 任务层级 complete-case 可训练性

| 任务 | 层级 | 总行数 | `total_chlorine` 非缺失 | 四变量 complete-case | train / validation / test | train 是否可合法训练 |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `regulatory` | `level2` | 26,975 | 185 | 36 | `29 / 2 / 5` | 否 |
| `regulatory` | `level3` | 6,193 | 152 | 36 | `29 / 2 / 5` | 否 |
| `anchored` | `level2` | 17,501 | 93 | 14 | `13 / 0 / 1` | 否 |
| `anchored` | `level3` | 3,071 | 71 | 14 | `13 / 0 / 1` | 否 |

更关键的是，四个任务层级的 complete-case split 都只剩负类：

- `regulatory level2`：`train={0:29}; validation={0:2}; test={0:5}`
- `regulatory level3`：`train={0:29}; validation={0:2}; test={0:5}`
- `anchored level2`：`train={0:13}; validation={}; test={0:1}`
- `anchored level3`：`train={0:13}; validation={}; test={0:1}`

这意味着：

- 当前没有任何一个 `level2/level3 + total_chlorine complete-case` 组合具备合法训练 `LogisticRegression` 的条件
- 问题不只是“样本太少”，而是正类在 complete-case 里已经完全消失

## 5. 缺失模式与 observed subset 诊断

### 5.1 observed 与 missing 的正类比例

| 任务 | `total_chlorine` observed | `total_chlorine` missing | observed 正类率 | missing 正类率 |
| --- | ---: | ---: | ---: | ---: |
| `regulatory level2` | 185 | 26,790 | 1.62% | 3.86% |
| `anchored level2` | 93 | 17,408 | 3.23% | 5.93% |

这说明：

- 与 `free_chlorine` 一样，`total_chlorine` 的缺失模式本身也带有强结构信息
- 但它比 `free_chlorine` 更糟，因为 observed subset 的规模进一步缩小

### 5.2 observed subset 中的数值分布

在 `level2 observed subset` 中：

- `regulatory`：负类 `182` 行，正类仅 `3` 行
- `anchored`：负类 `90` 行，正类仅 `3` 行

并且这 `3` 个正类样本的 `total_chlorine` 均值反而低于 observed 负类均值：

- `regulatory`：负类均值约 `1.452 mg/L`，正类均值约 `1.072 mg/L`
- `anchored`：负类均值约 `1.495 mg/L`，正类均值约 `1.072 mg/L`

这一步不能被过度解释成稳定反向关系，因为：

- 正类只有 `3` 个
- 该子集规模太小，无法提供可靠的方向性证据

它真正说明的是：当前 observed subset 根本不足以支撑稳健的第三层正式增量实验。

## 6. `facility-month` 审计结果

`V3_facility_month_master.csv` 的关键结果如下：

| 指标 | 数值 |
| --- | ---: |
| 总行数 | 1,442,728 |
| `TTHM` 非缺失行数 | 549,730 |
| `total_chlorine` 非缺失行数 | 49,676 |
| `TTHM + total_chlorine` 重合行数 | 2,385 |
| `TTHM + pH + alkalinity + TOC + total_chlorine` 全齐行数 | 0 |
| `TTHM + pH + alkalinity + TOC + free_chlorine` 全齐行数 | 0 |

这说明：

- `facility-month` 下 `total_chlorine` 的重合度明显高于 `PWS-year level2/level3`
- 但它仍然不足以形成“`TTHM + 三个核心变量 + total_chlorine` 全齐”的通用机制宽表
- 因此它更像第二层可做专题 reduced dataset 的候选变量，而不是第三层全国主模型的下一轮自然增量变量

## 7. 对 `V4.5` 的建议

本轮给出的正式建议是：

- 当前不应直接启动 `V4.5 total_chlorine increment`

原因不是单一的一条，而是三条同时成立：

1. `total_chlorine` 在 `PWS-year level2` 的非缺失率只有 `0.69%`，比 `free_chlorine` 更低。
2. 在 `level2 / level3` 下，所有 `total_chlorine` complete-case 版本的 train split 都只剩单一类别，完全不具备合法训练条件。
3. 即便退回 `facility-month`，它也只适合作为重合度有限的专题 reduced dataset 候选，而不是直接接入现有第三层主线。

## 8. 当前更合理的下一步

比起进入 `V4.5`，当前更合理的后续路径是：

1. 把 `V4.4b` 固定为一个“阻止无效增量实验”的正式审计节点。
2. 不再把 `total_chlorine` 视作第三层主线的自然下一步。
3. 如果还想继续追踪氯残留信号，应优先考虑第二层专题化 reduced dataset 方案，而不是第三层全国主模型方案。
4. 如果仍坚持在第三层继续做变量增量，更适合先转向覆盖率更高的其他候选变量，而不是在当前口径下重复氯残留变量实验。

## 9. 本轮结论

`V4.4b` 可以明确写出的结论是：

1. `total_chlorine` 在当前 `PWS-year` 主线中比 `free_chlorine` 更不适合进入正式增量实验。
2. `level2` 与 `level3` 下的 `total_chlorine complete-case` 在两个正式任务中全部不可训练，不具备进入 `V4.5` 的最基本条件。
3. `facility-month` 虽然保留了比第三层更高的重合度，但仍然只支持专题 reduced dataset 候选，不支持把 `total_chlorine` 直接推进为第三层主模型的下一轮增强变量。
4. 因此，`V4.4b` 的正式建议是：暂停 `V4.5 total_chlorine increment`，把 `total_chlorine` 从“第三层主线待增量变量”调整为“第二层机制专题候选变量”。
