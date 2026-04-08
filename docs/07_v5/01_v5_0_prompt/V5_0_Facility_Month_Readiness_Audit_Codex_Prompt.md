# V5.0 Facility-Month Readiness Audit Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下文档：

- [V1_5_Update_Service_Scope_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/V1_5_Update_Service_Scope_Summary.md)
- [V5_Master_Plan.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/07_v5/V5_Master_Plan.md)
- [V3_Facility_Month_Dictionary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Dictionary.md)
- [V3_Facility_Month_Build_Notes.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/04_v3/V3_Facility_Month_Build_Notes.md)
- [V4_Phase_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/V4_Phase_Summary.md)
- [V4_Chapter1_Framework_Summary.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/V4_Chapter1_Framework_Summary.md)

## 1. 当前任务定位

你当前要执行的是 `V5.0` 更新。

`V5.0` 的正式主题是：

- `facility-month readiness audit`

这一轮更新的核心目标不是直接开始第二层正式建模，也不是延续第三层 `PWS-year` 的局部性能优化，而是：

- 回到第一章真正的第二层 `facility-month`
- 对第二层候选变量的覆盖率、重合度与可执行性进行系统审计
- 明确第二层这一轮到底要回答什么问题
- 为后续 `V5.1 baseline`、`V5.2 机制核心`、`V5.3 TOC 增量` 建立边界

## 2. 必须接受的前序判断

在开始 `V5.0` 之前，你必须接受并沿用以下已确认判断：

1. `V4` 的核心任务已经是第三层 `PWS-year` 正式主线构建，而不是第二层 `facility-month` 的正式通路构建。
2. 当前第三层正式主模型的最稳妥表述是：第三层 `PWS-year` 第一级样本上的 `baseline + structural + treatment`。
3. 当前 `baseline + pH + alkalinity + TOC` 的最主要实证证据，来自第三层 `PWS-year` 内部第二级样本，而不是真正的第二层 `facility-month` 正式模块。
4. `V5` 的任务不是无边界寻找更多新通路，而是验证并构建真正第二层 `facility-month` 的高信息增强 / 机制支撑模块。
5. `V5.0` 的首要问题不是模型性能，而是变量边界、可执行性与后续正式实验是否值得开展。

## 3. 本轮必须回答的核心问题

`V5.0` 至少必须回答以下问题：

1. 第二层 `facility-month` 是否有条件形成一个比第三层内部第二级样本更接近环境过程的水质增强模块？
2. 在第二层里，`pH`、`alkalinity`、`TOC`、`free_chlorine`、`total_chlorine` 各自覆盖率如何？
3. 在第二层里，哪些变量 pairwise 重合仍然可用？
4. 哪些组合一旦要求 complete-case，就几乎没有可训练样本？
5. 哪些变量值得进入后续正式实验，哪些变量应在当前阶段暂停？
6. 第二层后续更适合承担“机制支撑线”“高信息增强线”，还是两者兼有？

## 4. 当前实验边界与解释要求

### 4.1 `V5.0` 是可执行性审计，不是正式建模

本轮的角色必须明确为：

- 第二层候选变量可执行性审计
- 第二层正式实验前的边界固定
- 第二层 baseline 与增强链设计前的准备工作

当前不得预设：

- 第二层一定能形成成熟正式模型
- 第二层一定优于第三层内部第二级样本
- 第二层一定要继续纳入全部候选变量

### 4.2 必须固定在真正第二层 `facility-month`

本轮所有主检查对象固定为：

- 第二层 `facility-month`

不得把第三层 `PWS-year` 内部第二级样本结果重新包装成第二层结果。

### 4.3 必须保持与第三层证据的区分

本轮应明确区分：

- 第一章第二层：`facility-month`
- 第三层内部高信息子样本：`PWS-year` 内部第二级样本

当前第二层工作的目标，是判断自己能否形成独立模块，而不是直接复述第三层高信息子样本的已有结论。

### 4.4 解释边界必须清楚

本轮若发现第二层变量覆盖率很差、complete-case 极少、训练不可执行，这不是失败，而是有效边界结论。

更稳妥的解释应是：

- 第二层在哪些变量上有潜力
- 第二层在哪些变量上应停止推进
- 第二层与第三层内部高信息子样本相比，到底新增了什么，或者并没有新增什么

## 5. 本轮总体原则

1. 原始数据只读，不允许原位修改。
2. 优先复用已有第二层主表与既有字段字典，不重新发明底表。
3. 所有新增或更新的 `.md` 文档必须使用中文。
4. 必须先审计、再建议后续模型链，不允许一上来直接开始正式建模。
5. 当前不做树模型、boosting、超参数优化。
6. 当前不保存模型文件。
7. 当前不进行跨州、跨年份、跨系统类型泛化性外推。
8. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)。
9. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送。

## 6. 本轮正式任务定义

### 6.1 主任务

本轮必须完成以下主任务：

1. 梳理第二层 `facility-month` 当前可用的候选变量字段
2. 审计以下变量在第二层中的覆盖率：
   - `pH`
   - `alkalinity`
   - `TOC`
   - `free_chlorine`
   - `total_chlorine`
3. 审计上述变量与 `TTHM` 的 pairwise 重合情况
4. 审计关键组合的 complete-case 可执行性
5. 给出第二层 baseline 候选与增强候选的建议清单
6. 给出哪些变量进入 `V5.1`、`V5.2`、`V5.3`，哪些应暂缓

### 6.2 必做的组合检查

至少必须检查以下组合：

1. `TTHM + pH`
2. `TTHM + alkalinity`
3. `TTHM + TOC`
4. `TTHM + free_chlorine`
5. `TTHM + total_chlorine`
6. `TTHM + pH + alkalinity`
7. `TTHM + pH + alkalinity + TOC`
8. `TTHM + pH + alkalinity + TOC + free_chlorine`
9. `TTHM + pH + alkalinity + TOC + total_chlorine`

### 6.3 本轮至少应产出的判断

本轮至少应形成以下判断：

1. 第二层 baseline 该围绕哪些变量或结构特征构建
2. 第二层第一轮增强最稳妥是否仍应从 `pH + alkalinity` 开始
3. `TOC` 是否值得作为第二层下一轮正式增量变量
4. `free_chlorine` 与 `total_chlorine` 当前是否值得继续进入第二层正式链
5. 第二层后续更适合作为“机制支撑模块”“高信息增强模块”，还是两者兼有

## 7. 输入、输出与目录要求

### 7.1 输入

本轮优先使用：

- 第二层原型主表
- 第二层字段字典
- 第二层构建说明
- `V4` 阶段的框架总结文档

### 7.2 输出目录

本轮所有结果应统一写入新的本地目录，建议命名为：

- `data_local/V5_Chapter1_Part1_Facility_Month_Module/V5_0/`

如目录不存在，应按项目规范新建，但不得写回原始数据路径。

### 7.3 输出文档

本轮至少应新增：

1. 第二层候选变量覆盖率与重合度审计报告
2. 第二层可执行性判断说明
3. 第二层后续 baseline 与增强链建议文档

文档标题、说明、结论必须使用中文。

## 8. 结果汇报要求

完成后请至少汇报以下内容：

1. 第二层 `facility-month` 当前最值得保留的候选变量有哪些
2. 哪些变量 pairwise 仍有价值
3. 哪些 complete-case 组合已经不具备正式训练条件
4. 第二层 baseline 应如何定义
5. 第二层第一轮正式增强是否建议采用：
   - `baseline`
   - `baseline + pH + alkalinity`
   - `baseline + pH + alkalinity + TOC`
6. `free_chlorine` 和 `total_chlorine` 当前应继续还是暂停
7. 第二层最终更可能承担什么角色

## 9. 明确禁止事项

当前禁止：

1. 直接把第三层内部第二级样本结果重写成第二层结论
2. 还没审计完就直接开始第二层大规模正式训练
3. 一开始就做大而全整合模型
4. 在没有覆盖率与重合度支持的前提下强行推进 `free_chlorine` 或 `total_chlorine`
5. 跳过 `codex.md` 更新
6. 未经用户确认直接执行 Git commit 或 push

## 10. 当前阶段一句话总结

`V5.0` 的任务不是直接做第二层正式模型，而是先把真正第二层 `facility-month` 的变量覆盖率、重合度与可执行边界审清楚，判断第二层是否值得被正式发展为一个独立的高信息增强 / 机制支撑模块，并据此为 `V5.1` 到 `V5.4` 建立清晰边界。
