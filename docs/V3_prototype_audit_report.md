# V3_prototype_audit_report

- 更新时间：2026-03-26 22:31:36
- 二层主表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_facility_month_master.csv`
- 三层主表：`D:\Project_DBPs_prediction_and_casual_analysis\data_local\V3_Chapter1_Part1_Prototype_Build\V3_pws_year_master.csv`

## 1. 二层轻量审计

| 指标 | 结果 |
| --- | --- |
| 二层行数 | 1442728 |
| 二层主键重复数 | 0 |
| 二层 TTHM 行数 | 549730 |
| 二层 HAA5 行数 | 481761 |
| 二层 TTHM + 至少 2 个核心变量 | 3811 |
| 二层 TTHM + 至少 3 个核心变量 | 230 |
| 二层 TTHM + 4 个核心变量全齐 | 0 |

## 2. 三层轻量审计

| 指标 | 结果 |
| --- | --- |
| 三层行数 | 259500 |
| 三层主键重复数 | 0 |
| 三层 TTHM 行数 | 199802 |
| 三层 HAA5 行数 | 165379 |
| 三层 TTHM + 至少 2 个核心变量 | 26975 |
| 三层 TTHM + 4 个核心变量全齐 | 60 |

## 3. 与 V2 审计结论的一致性检查

| 层级 | 指标 | V2 | V3 | 一致性判断 |
| --- | --- | --- | --- | --- |
| facility_month | 并集行数/唯一键数 | 1442728 | 1442728 | 一致 |
| facility_month | TTHM 键数 | 549730 | 549730 | 一致 |
| facility_month | HAA5 键数 | 481761 | 481761 | 一致 |
| facility_month | TTHM + 核心变量至少 2 个 | 3811 | 3811 | 一致 |
| facility_month | TTHM + 核心四变量全齐 | 0 | 0 | 一致 |
| system_year | 并集行数/唯一键数 | 259500 | 259500 | 一致 |
| system_year | TTHM 键数 | 199802 | 199802 | 一致 |
| system_year | HAA5 键数 | 165379 | 165379 | 一致 |
| system_year | TTHM + 核心变量至少 2 个 | 26975 | 26975 | 一致 |
| system_year | TTHM + 核心四变量全齐 | 60 | 60 | 一致 |

## 4. 判断

- 二层 facility-month 原型表已经足够作为后续高风险场景内部分析和小模型机制分析的起点。理由是：TTHM 对应的二层键达到 549,730 个，且至少 2 个核心变量的交集单元达到 3,811 个。
- 但二层仍不适合被当作“全国统一全变量宽表”。原因是 TTHM + 4 个核心变量在二层仍然为 0，与 V2 结论完全一致。
- 三层 pws-year 原型表已经足够作为全国机器学习主表原型。理由是：TTHM 系统-年份单元达到 199,802 个，至少 2 个核心变量的系统-年份单元达到 26,975 个，且 TTHM + 4 个核心变量全齐已有 60 个。
- 下一步应优先进入第三层全国 ML 主表线。第二层机制/风险场景线应作为高信息补充线并行推进。

