# V5.1 Facility-Month Baseline 结果摘要

- 更新时间：2026-04-08 21:11（Asia/Hong_Kong）
- 对应阶段：`V5.1`

## 1. 最终固定的正式 baseline 字段集

第二层 `V5.1` 最终固定的正式 baseline 字段集是：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`

正式命名为：

- `baseline_core_minimal`

## 2. `has_treatment_summary` 是否进入正式 baseline

不进入。

理由是：

- 它与最小 baseline 相比没有形成稳定的 out-of-sample 增益
- validation `PR-AUC` 仅增加 `+0.00056`
- test `PR-AUC` 反而减少 `-0.00008`
- 它本质上更接近记录可用性代理，而不是第二层正式 baseline 应固定的核心结构字段

## 3. `water_facility_type` 是否进入正式 baseline

不进入。

理由是：

- 它在缩窄样本后表现更强，但 strict complete-case 样本明显收缩
- 总样本从 `549,646` 行下降到 `362,751` 行
- test 样本从 `78,669` 行下降到 `53,029` 行
- 因此它更适合作为条件性 baseline 对照，而不是第一版正式 baseline

## 4. detailed treatment flags 是否全部排除在 baseline 外

是。

理由是：

- `V5.0` 已确认它们的 strict complete-case 规模只有 `2,699` 行
- 当前不适合作为第二层正式 baseline 字段
- 同时缺失不能被解释为明确不存在，不应在 baseline 中被硬编码为 `0`

## 5. 第二层正式标签

第二层正式标签固定为：

- `is_tthm_high_risk_month`

定义为：

- `tthm_mean_ug_l >= 80 ug/L`

它与第三层年度任务的关系是：

- 共用同一个 `80 ug/L` 高风险边界
- 但第二层是“设施-月份高风险月识别”，第三层是“系统-年份年度风险识别”

## 6. 第二层正式切分

第二层正式切分固定为：

- `group_by_pwsid`

原因是：

- 它同时避免同一系统跨设施、跨月份泄漏
- 比 `group_by_pwsid + water_facility_id` 更严格

## 7. baseline 的 train / validation / test 结果

### 正式 baseline：`baseline_core_minimal`

| split | rows | positive_rows | PR-AUC | ROC-AUC | balanced_accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| train | 386,102 | 24,765 | 0.1707 | 0.7375 | 0.6764 |
| validation | 84,875 | 5,173 | 0.1924 | 0.7418 | 0.6800 |
| test | 78,669 | 5,130 | 0.1696 | 0.7305 | 0.6786 |

### `V5.2` 对照 reference：`baseline_core_minimal_stage1_reference`

| split | rows | positive_rows | PR-AUC | ROC-AUC | balanced_accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| train | 2,073 | 131 | 0.2506 | 0.8532 | 0.7887 |
| validation | 362 | 14 | 0.0935 | 0.6805 | 0.6775 |
| test | 203 | 19 | 0.3643 | 0.7765 | 0.7271 |

## 8. 是否可以继续进入 `V5.2`

可以。

当前理由是：

1. 第二层正式标签、正式切分与正式 baseline 已经固定。
2. `V5.2` 所需的同子样本 baseline reference 已经提前准备完成。
3. 当前最合理的下一步就是在完全相同的制度下测试：
   - `baseline_core_minimal`
   - `baseline_core_minimal + pH + alkalinity`
