# V5.0 Facility-Month 候选变量覆盖率与重合度审计报告

- 更新时间：2026-04-08 20:07（Asia/Hong_Kong）
- 对应阶段：`V5.0`
- 审计对象：真正第二层 `facility-month`
- 输入文件：
  - `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv`
- 执行脚本：
  - `scripts/build_v5_0_facility_month_readiness_audit.py`
- 本地结果目录：
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/`

## 1. 本轮任务定位

`V5.0` 的任务不是直接进入第二层正式建模，而是先回答三个更基础的问题：

1. 真正第二层 `facility-month` 下，哪些候选水质变量与 `TTHM` 还有实际重合度。
2. 哪些组合一旦进入 strict complete-case，样本规模会立刻塌缩到不再适合作为正式主链。
3. 第二层下一步到底应保留哪些变量、暂停哪些变量，并据此重新定义 `V5.1` 至 `V5.3` 的边界。

## 2. 审计范围与口径

本轮以 `TTHM` 月均值非缺失行作为第二层结果样本池，核心检查变量为：

- `pH`
- `alkalinity`
- `TOC`
- `free_chlorine`
- `total_chlorine`

同时额外检查第二层 baseline 候选结构字段：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `water_facility_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `has_treatment_summary`
- 各类 treatment 过程二值字段

本轮 `TTHM` 月样本总数为 `549,730`，其中 `is_tthm_high_risk_month=1` 的高风险月数为 `35,068`。

## 3. 候选变量覆盖率结果

| 变量 | 总体非缺失行数 | 总体非缺失率 | 与 `TTHM` 重合行数 | `TTHM` 内重合率 | 重合子集高风险正例数 | 重合子集高风险率 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pH` | 275,174 | 19.07% | 9,796 | 1.78% | 383 | 3.91% |
| `free_chlorine` | 215,741 | 14.95% | 5,446 | 0.99% | 355 | 6.52% |
| `alkalinity` | 299,981 | 20.79% | 3,220 | 0.59% | 193 | 5.99% |
| `TOC` | 363,849 | 25.22% | 2,824 | 0.51% | 111 | 3.93% |
| `total_chlorine` | 49,676 | 3.44% | 2,385 | 0.43% | 195 | 8.18% |

这里最需要强调的不是“总体非缺失率”，而是“与 `TTHM` 在真正第二层上的重合率”：

- `pH` 是当前第二层里与 `TTHM` 重合度最高的机制变量。
- `free_chlorine` 的 pairwise 重合行数高于 `alkalinity` 与 `TOC`，但它的总体覆盖仍不足 `1%` 的 `TTHM` 月样本。
- `TOC` 虽然总体非缺失行数最高，但与 `TTHM` 真正重合的月样本并不多。
- `total_chlorine` 总体覆盖最弱，不能被当作第二层正式主链变量。

## 4. Prompt 要求的必做组合检查

| 组合 | complete-case 行数 | `TTHM` 内比例 | 高风险正例数 |
| --- | ---: | ---: | ---: |
| `TTHM + pH` | 9,796 | 1.78% | 383 |
| `TTHM + alkalinity` | 3,220 | 0.59% | 193 |
| `TTHM + TOC` | 2,824 | 0.51% | 111 |
| `TTHM + free_chlorine` | 5,446 | 0.99% | 355 |
| `TTHM + total_chlorine` | 2,385 | 0.43% | 195 |
| `TTHM + pH + alkalinity` | 2,638 | 0.48% | 164 |
| `TTHM + pH + alkalinity + TOC` | 37 | 0.01% | 1 |
| `TTHM + pH + alkalinity + TOC + free_chlorine` | 0 | 0.00% | 0 |
| `TTHM + pH + alkalinity + TOC + total_chlorine` | 0 | 0.00% | 0 |

这张表给出的边界非常清楚：

- 真正能作为第二层第一轮正式增强起点的唯一可行组合是 `TTHM + pH + alkalinity`。
- 一旦把 `TOC` 接到 `pH + alkalinity` 后面，strict complete-case 直接掉到 `37` 行。
- 两条含 `TOC + chlorine` 的五变量组合在真正第二层下已经完全归零。

## 5. 二层内部模式结构

`TTHM` 月样本内部按四个核心变量 `pH / alkalinity / TOC / free_chlorine` 的可用模式看，最关键的结果是：

- `532,485` 行，也就是 `96.86%` 的 `TTHM` 月样本，完全没有这四个核心变量。
- `6,155` 行只有 `pH`。
- `5,225` 行只有 `free_chlorine`。
- `2,410` 行是 `pH + alkalinity`，这是当前最主要的二层机制双变量模式。
- `191` 行是 `pH + alkalinity + free_chlorine`。
- `37` 行是 `pH + alkalinity + TOC`。
- `230` 行总计达到了 `3+` 个核心变量，占全部 `TTHM` 月样本仅 `0.04%`。

这说明第二层并不存在一个可直接复用的“高信息宽表”。当前更像是少数可用机制链条散落在大量 `outcome-only` 月样本中。

## 6. Match Quality 结果

按 `match_quality_tier` 看，`TTHM` 月样本分布为：

- `D_outcome_only`：`532,485`
- `C_outcome_plus_1_core`：`13,434`
- `B_outcome_plus_2_core`：`3,581`
- `A_outcome_plus_3plus_core`：`230`

这进一步说明：

- 第二层大部分月样本只能支撑结果观测，不能支撑机制增强。
- 真正能进入“二层机制增强”讨论的样本，本质上只是一小块高信息子集。

## 7. 本轮直接结论

1. 第二层当前最值得保留的候选机制变量是 `pH` 与 `alkalinity`。
2. `TOC` 在真正第二层下仍有学术意义，但 strict complete-case 已塌缩到 `37` 行，当前不足以直接进入正式主链。
3. `free_chlorine` 与 `total_chlorine` 都不适合作为当前第二层正式主链变量；它们只能保留为后续小范围专题变量候选。
4. 第二层当前可以形成一个受限但真实的机制增强入口，但不能被误写成已经成熟的多变量高信息宽表。
