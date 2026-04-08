# V5.0 Facility-Month Baseline 与增强链建议

- 更新时间：2026-04-08 20:07（Asia/Hong_Kong）
- 对应阶段：`V5.0`
- 结论来源：
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_baseline_candidate_summary.csv`
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_baseline_set_readiness.csv`
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_recommendation_summary.csv`

## 1. 第二层第一版 baseline 的建议定义

当前建议把第二层第一版 baseline 固定为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `has_treatment_summary`

这组字段的主要理由是：

- 与 `TTHM` 同时可用的行数为 `549,646`，占全部 `TTHM` 月样本的 `99.98%`
- 它们构成了第二层最稳定、最不依赖高信息子样本的结构背景底座
- 它们不会像详细 treatment 过程字段那样在一开始就把样本压缩到不可用

## 2. 第二层 baseline 的条件性保留字段

`water_facility_type` 当前建议保留为条件性 baseline 候选，而不是第一版必选字段。

原因是：

- 一旦把它纳入 strict complete-case，样本会从 `549,646` 降到 `362,751`
- 这仍然是可用规模，但会明显收缩样本覆盖
- 因此它更适合在 `V5.1` 中作为对照项，而不是提前写死进主 baseline

## 3. 当前不应进入第一版 baseline 的字段

以下字段当前都不应进入第二层第一版 baseline：

- `has_disinfection_process`
- `has_filtration_process`
- `has_adsorption_process`
- `has_oxidation_process`
- `has_chloramination_process`
- `has_hypochlorination_process`

原因一致：

- 每个字段与 `TTHM` 同时可用的行数都只有 `2,699`
- 对应覆盖率仅 `0.49%`
- 一旦强行纳入 baseline，会把第二层 baseline 从“广覆盖结构底座”直接压缩成“极小专题子样本”

## 4. 对 `V5.1`、`V5.2`、`V5.3` 的正式建议

### 4.1 `V5.1`

建议继续推进，但范围应收敛为：

- 固定第二层 `baseline_core`
- 固定样本口径
- 固定标签口径
- 固定切分与禁止误用规则

不建议在 `V5.1` 中提前混入：

- 详细 treatment 过程字段
- `free_chlorine`
- `total_chlorine`

### 4.2 `V5.2`

建议作为第二层第一轮正式增强链启动：

- `baseline + pH + alkalinity`

理由是：

- `TTHM + pH + alkalinity` complete-case 共有 `2,638` 行
- 其中高风险正例为 `164`
- 这是当前真正第二层下唯一具备相对稳定样本支撑的机制核心组合

### 4.3 `V5.3`

不建议按原始计划直接写成：

- `baseline + pH + alkalinity + TOC` 正式增量实验

当前更合理的写法应改为：

- `TOC` 的第二层 reduced dataset 可执行性专题审计

原因是：

- `TTHM + pH + alkalinity + TOC` strict complete-case 仅 `37` 行
- 高风险正例仅 `1` 行
- 这不足以支撑一个稳妥的第二层正式主链增量实验

## 5. 对氯残留变量的建议

当前对两个氯残留变量的正式建议都是：

- 暂停进入第二层正式主链

分别说明如下：

### 5.1 `free_chlorine`

- `TTHM + free_chlorine` 虽有 `5,446` 行重合
- 但 `TTHM + pH + alkalinity + free_chlorine` 只剩 `191` 行
- 它更像受选择性监测驱动的高偏样本，不适合在当前阶段写成正式下一步

### 5.2 `total_chlorine`

- `TTHM + total_chlorine` 仅 `2,385` 行
- `TTHM + pH + alkalinity + total_chlorine` 仅 `125` 行
- 整体覆盖弱于 `free_chlorine`，更不适合进入第二层主链

## 6. 对 `V5_Master_Plan` 的调整建议

这轮 `V5.0` 的结果意味着原先那种线性的版本链需要加一个前提条件：

1. `V5.1` 继续推进
2. `V5.2` 继续推进
3. `V5.3` 只有在 `V5.2` 后仍确认值得扩变量时才保留

因此，`V5.3` 当前不应被视为“默认必做的正式下一步”，而应被视为：

- 一项需要二次放行的专题分支

## 7. 本轮建议的一句话总结

第二层当前最稳妥的正式链条不是“baseline 后不断自然扩变量”，而是先把 `baseline` 固定下来，再用 `pH + alkalinity` 建立一个受控、可解释、样本尚未塌缩的机制核心入口；`TOC` 与氯残留变量都暂不具备直接进入第二层正式主链的条件。
