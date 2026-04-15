# V5.2 Facility-Month Mechanistic Core Stage1 结果摘要

- 更新时间：2026-04-09 09:45（Asia/Hong_Kong）
- 对应阶段：`V5.2`

## 1. 第二层 `V5.2` 正式增强版本字段集

本轮正式增强版本为：

- `baseline_core_minimal_plus_ph_alkalinity`

字段集固定为：

- `month`
- `state_code`
- `system_type`
- `source_water_type`
- `retail_population_served`
- `adjusted_total_population_served`
- `ph_mean`
- `alkalinity_mean_mg_l`

对照版本为：

- `baseline_core_minimal_stage1_reference`

## 2. 第二层 `V5.2` 样本口径

本轮正式比较固定在真正第二层 `facility-month` 的同子样本 complete-case 上：

- `tthm_mean_ug_l` 非缺失
- 正式 baseline 字段全部非缺失
- `ph_mean` 非缺失
- `alkalinity_mean_mg_l` 非缺失

样本规模为：

- train：`2,073`
- validation：`362`
- test：`203`

## 3. 结果总览

| 版本 | split | PR-AUC | ROC-AUC | balanced_accuracy |
| --- | --- | ---: | ---: | ---: |
| `baseline_core_minimal_stage1_reference` | validation | 0.0935 | 0.6805 | 0.6775 |
| `baseline_core_minimal_plus_ph_alkalinity` | validation | 0.0865 | 0.6819 | 0.6821 |
| `baseline_core_minimal_stage1_reference` | test | 0.3643 | 0.7765 | 0.7271 |
| `baseline_core_minimal_plus_ph_alkalinity` | test | 0.3937 | 0.7979 | 0.7361 |

## 4. 本轮五个核心回答

### 4.1 `pH + alkalinity` 是否形成稳定增益

未形成严格意义上的稳定增益。

原因是：

- `test` 上三项主指标都改善
- `validation` 上 `ROC-AUC` 与 `balanced_accuracy` 改善
- 但 `validation PR-AUC` 没有改善

因此最稳妥表述是：

- 出现了弱正向、但未完全稳定的正式证据

### 4.2 `validation` 与 `test` 是否方向一致

不完全一致。

一致部分：

- `ROC-AUC`
- `balanced_accuracy`

不一致部分：

- `PR-AUC`

### 4.3 第二层当前是否已具备第一轮正式机制支撑证据

是，但只能表述为：

- 有限的、弱正向的第一轮正式证据

不能表述为：

- 第二层机制增强链已经稳定成熟

### 4.4 第二层当前角色应如何表述

当前更适合继续固定为：

- 机制支撑线为主
- 有限高信息增强为辅

而不是：

- 已成熟的第二层宽表主模型

### 4.5 是否可以继续进入后续 `TOC` 专题分支

可以保留，但必须收紧边界。

更具体地说：

- `TOC` 仍可作为第二层 reduced dataset 专题候选
- 不应再被写成默认线性下一步
- 进入前应明确接受极强样本收缩和专题化设计

## 5. 一句话结论

`V5.2` 说明真正第二层 `facility-month` 上的 `baseline + pH + alkalinity` 不是无效链条，但当前证据仍然偏弱，足以支持保留“机制支撑线”，不足以支持直接把第二层写成稳定成熟的增强主链。
