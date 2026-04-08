# V5.0 Facility-Month 可执行性判断说明

- 更新时间：2026-04-08 20:07（Asia/Hong_Kong）
- 对应阶段：`V5.0`
- 依据数据：
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_candidate_variable_coverage.csv`
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_complete_case_summary.csv`
  - `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/v5_0_facility_month_core_pattern_summary.csv`

## 1. 对 prompt 六个核心问题的正式回答

### 1.1 第二层 `facility-month` 能否形成一个比第三层内部第二级样本更接近环境过程的独立模块？

可以，但必须加上严格限定。

更准确的表述是：

- 第二层在数据对象和时间尺度上，天然比第三层内部第二级样本更接近设施级月度过程，因此具备独立模块价值。
- 但当前这份价值只能建立在受限变量链和受限样本上。
- 它还不能被写成“第二层已经形成成熟的正式水质宽表模型”。

因此，第二层当前成立的是：

- 一个可以独立存在的、偏机制支撑取向的高信息模块雏形。

而不是：

- 一个已经准备好无约束扩变量的第二层正式主模型。

### 1.2 第二层里五个候选变量的覆盖情况如何？

结论按与 `TTHM` 的真实重合度排序为：

1. `pH`：`9,796` 行
2. `free_chlorine`：`5,446` 行
3. `alkalinity`：`3,220` 行
4. `TOC`：`2,824` 行
5. `total_chlorine`：`2,385` 行

但研究判断不能只看 pairwise 行数，还要看它们接入正式链条后的 complete-case 收缩幅度。

### 1.3 哪些 pairwise 组合仍有可用性？

当前真正仍有解释价值的 pairwise 关系是：

- `TTHM + pH`
- `TTHM + alkalinity`
- `TTHM + TOC`
- `TTHM + free_chlorine`
- `TTHM + total_chlorine`

其中最值得保留为正式下一步的不是 pairwise 行数第二高的 `free_chlorine`，而是：

- `pH + alkalinity`

原因是：

- `pH + alkalinity` 的二变量 complete-case 为 `2,638` 行，是所有真正机制双变量组合中最稳定的一组。
- 它与 `V4` 第三层内部第二级样本已有证据方向一致。
- 它比氯残留变量更适合作为第二层“机制核心 stage1”。

### 1.4 哪些组合一旦要求 complete-case 就几乎不可训练？

已经可以明确收束的组合包括：

- `TTHM + pH + alkalinity + TOC`：仅 `37` 行
- `TTHM + pH + alkalinity + TOC + free_chlorine`：`0` 行
- `TTHM + pH + alkalinity + TOC + total_chlorine`：`0` 行

同时，第二层 baseline 若强行纳入详细 treatment 过程字段，也会立刻塌到：

- `2,699` 行

这说明当前不能把第二层写成：

- “baseline + 任意机制变量逐步叠加”的开放式主链

### 1.5 哪些变量值得进入后续正式实验，哪些应暂缓？

正式建议如下：

1. 进入 `V5.1` 的应是稳定结构字段组成的 `baseline_core`。
2. 进入 `V5.2` 的应是 `baseline + pH + alkalinity`。
3. `TOC` 暂不进入当前第二层正式主链，先保留为 reduced dataset 专题候选。
4. `free_chlorine` 与 `total_chlorine` 暂停进入第二层正式主链。

这里要特别说明：

- `free_chlorine` 的高阶 complete-case 行数虽然大于 `TOC`，但总体覆盖仍不到 `1%` 的 `TTHM` 月样本，而且更可能对应高度选择性的监测子集。
- `TOC` 在真正第二层下也还不够成熟，但它至少仍保留与既有机制路径一致的理论意义，因此更适合作为保留候选，而不是彻底删除。

### 1.6 第二层最终更适合承担什么角色？

当前最稳妥的判断是：

- 第二层更适合承担“机制支撑线为主、有限高信息增强为辅”的角色。

换言之，它不是完全只能做机制解释，也不是已经具备广义高信息增强主链的成熟条件，而是：

- 先以机制支撑线为主体建立正式定位；
- 再在非常有限的可执行子集上保留受控增强空间。

## 2. 对 `V5` 后续路径的直接影响

本轮 `V5.0` 实际上已经改写了原先过于线性的推进预期。

当前更合理的后续顺序应是：

1. 先固定 `V5.1 baseline`
2. 再执行 `V5.2 baseline + pH + alkalinity`
3. 完成 `V5.2` 后再决定是否保留 `V5.3`

其中 `V5.3` 不能再被默认写成：

- 下一步自然就是 `baseline + pH + alkalinity + TOC`

而应改成：

- 只有当 `V5.2` 后仍确认二层主链需要继续扩变量，且愿意接受 reduced dataset 设计时，才考虑把 `TOC` 作为专题增量变量重新评估。

## 3. 本轮总判断

`V5.0` 给出的不是“第二层失败”，而是更严格也更有价值的边界结论：

1. 第二层确实有必要独立成模块。
2. 第二层确实比第三层内部第二级样本更接近设施月度过程。
3. 但第二层当前只支持一条很短的正式增强链：`baseline -> baseline + pH + alkalinity`。
4. 任何继续扩到 `TOC`、`free_chlorine` 或 `total_chlorine` 的动作，都不能再被写成默认下一步，而应被视为需要额外审计支持的专题分支。
