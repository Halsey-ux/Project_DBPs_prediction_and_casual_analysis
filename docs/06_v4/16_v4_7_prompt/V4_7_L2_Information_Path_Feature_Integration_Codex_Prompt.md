# V4.7 L2 Information Path Feature Integration Codex Prompt

你当前正在 `D:\Project_DBPs_prediction_and_casual_analysis` 项目中工作。请严格遵守项目根目录 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md) 的全部要求，并优先参考以下 V4 文档：

- [V4_Training_Protocol.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_Training_Protocol.md)
- [V4_TTHM_Model_Task_Definition.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/01_protocol/V4_TTHM_Model_Task_Definition.md)
- [V4_Experiment_Roadmap.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/04_v4_plan/V4_Experiment_Roadmap.md)
- [V4_5_PWS_Year_Structural_Conditional_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/13_v4_5_execution/V4_5_PWS_Year_Structural_Conditional_Increment_Execution_Report.md)
- [V4_6_PWS_Year_Treatment_Summary_Increment_Execution_Report.md](D:/Project_DBPs_prediction_and_casual_analysis/docs/06_v4/15_v4_6_execution/V4_6_PWS_Year_Treatment_Summary_Increment_Execution_Report.md)

## 1. 当前任务定位

你当前要执行的是 `V4.7` 更新。

`V4.7` 的正式主题是：

- `L2 information path feature integration`

这一轮更新的核心目标不是立刻重写当前正式主模型，也不是切换模型、上树模型或做超参数优化，而是：

- 在第二层高信息样本 `第二级样本` 中，把“系统背景通路”与“水质特征通路”的特征放入同一对照体系中
- 检验两条信息通路在高信息样本中是互补、部分重叠，还是大部分重复
- 判断当系统背景通路已经进入模型后，`pH + alkalinity + TOC` 是否仍提供独立增量价值
- 判断当水质特征通路已经进入模型后，`structural + treatment` 是否仍提供稳定附加价值
- 为后续“基于不同信息通路的 DBP 高风险场景分层预测框架”提供方法学证据

## 2. 必须继承的前序结论

在开始 `V4.7` 之前，你必须接受并沿用以下已确认判断：

1. `V4.5` 已确认：在第三层 `第一级样本` 全国主线上，`baseline + structural conditional` 带来明显且稳定的预测提升。
2. `V4.6` 已确认：在第三层 `第一级样本` 全国主线上，`treatment summary` 单独相对 `baseline` 收益较弱，但在控制 `V4.5 structural conditional` 后仍保留小而稳定的剩余增益。
3. 当前第三层正式主模型的最稳妥表述是：`baseline + structural + treatment` 构成“系统背景通路”的当前正式版本，定位为“基于美国 SYR4 的全国尺度 DBP 高风险场景正式主模型”。
4. 当前第二层高信息样本的最稳妥表述是：`baseline + pH + alkalinity + TOC` 构成“水质特征通路”的当前版本，定位为高信息样本下的水质增强预测与机制支撑组合。
5. 当前项目已经从单一模型思路，推进到“基于不同信息通路的 DBP 高风险场景分层预测框架”思路。
6. 因此 `V4.7` 的自然下一步不是直接宣布新的统一主模型，而是在 `第二级样本` 中探索性检验两条信息通路合并后的大模型效果。

## 3. 当前实验边界与解释要求

### 3.1 `V4.7` 是探索性整合实验，不是正式主模型改写

`V4.7` 的角色必须明确为：

- 第二层高信息样本中的信息通路整合实验
- 方法学层面的互补/重叠检验
- 对现有分层预测框架的补充验证

当前不得预设：

- `V4.7` 一定会产生新的正式主模型
- `V4.7` 的 full integration 结果一定替代第三层 `第一级样本` 正式主模型
- `V4.7` 的结果可以直接写成“通用 DBP 预测模型”

### 3.2 必须固定在 `第二级样本`

本轮主实验固定在：

- `第二级样本`

原因是：

- `pH + alkalinity + TOC` 的当前主要证据基础在 `第二级样本`
- `第二级样本` 是当前定义的高信息样本层
- `V4.7` 的目标是检验两条信息通路在同一高信息样本层中的关系，而不是重新争夺第三层全国主线

### 3.3 必须区分两条信息通路

本轮必须明确使用以下术语：

- 系统背景通路
- 水质特征通路

其中：

- 系统背景通路当前由 `baseline + structural + treatment` 构成
- 水质特征通路当前由 `baseline + pH + alkalinity + TOC` 构成

### 3.4 解释边界必须清楚

即使 full integration 带来更强预测表现，也不能直接写成：

- 新的通用主模型已经建立
- 结构/coverage/treatment 与水质变量共同构成了环境机制模型
- 第三层正式主模型应立即被 `V4.7` 改写

更稳妥的解释应是：

- 在高信息样本中，两条信息通路合并后是否形成更强预测
- 两条信息通路之间是互补、部分重叠还是大部分重复
- `TOC` 等水质变量在控制系统背景通路后是否仍有独立价值

## 4. 本轮总体原则

1. 原始数据只读，不允许原位修改。
2. 统一基于第三层 `V4_pws_year_ml_ready.csv` 执行。
3. 统一通过 [io_v4_ml_ready.py](D:/Project_DBPs_prediction_and_casual_analysis/scripts/io_v4_ml_ready.py) 读取数据。
4. 统一复用当前 `group_by_pwsid` 切分，不重新随机切分。
5. 默认模型继续使用 `LogisticRegression`。
6. 当前不做树模型、boosting、超参数优化。
7. 当前不保存模型文件。
8. 所有新增或更新的 `.md` 文档必须使用中文。
9. 发生重要更新后必须同步更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)。
10. 完成后要向用户汇报结果，并询问是否执行 Git 提交与推送。

## 5. 本轮正式任务定义

### 5.1 正式任务

本轮继续至少跑两条正式任务：

1. `tthm_regulatory_exceedance_prediction`
2. `tthm_anchored_risk_prediction`

### 5.2 固定样本层级

本轮主实验固定为：

- `第二级样本`

### 5.3 两条信息通路的当前特征定义

#### 系统背景通路

当前定义为：

- `baseline + structural + treatment`

其中：

- `baseline`：沿用当前 `DEFAULT_BASELINE_FEATURES`
- `structural`：沿用 `V4.5 structural conditional` 特征组
- `treatment`：沿用 `V4.6 treatment summary` 特征组

#### 水质特征通路

当前定义为：

- `baseline + pH + alkalinity + TOC`

建议最小特征组包括：

- `ph_sample_weighted_mean`
- `alkalinity_sample_weighted_mean_mg_l`
- `toc_sample_weighted_mean_mg_l`
- `ph_missing_flag`
- `alkalinity_missing_flag`
- `toc_missing_flag`

如你基于现有 `V4.3`/`V4.4` 脚本结构判断应补充 no-missing-flags 敏感性版本，可补，但不得让敏感性版本取代主对照链。

## 6. 本轮必须保留的对照链

`V4.7` 不能只跑一个 full integration 版本，否则无法判断两条信息通路之间的关系。

至少必须保留以下 4 层 `第二级样本` 对照：

### 6.1 `第二级样本 baseline reference`

定义：

- 样本：全部 `第二级样本`
- 特征：`baseline`

作用：

- 作为两条信息通路的共同起点

### 6.2 `第二级样本 water-quality reference`

定义：

- 样本：全部 `第二级样本`
- 特征：`baseline + pH + alkalinity + TOC`

作用：

- 代表当前“水质特征通路”

### 6.3 `第二级样本 system-background reference`

定义：

- 样本：全部 `第二级样本`
- 特征：`baseline + structural + treatment`

作用：

- 代表当前“系统背景通路”在 `第二级样本` 上的对照版本

### 6.4 `第二级样本 full integration`

定义：

- 样本：全部 `第二级样本`
- 特征：`baseline + structural + treatment + pH + alkalinity + TOC`

作用：

- 检验两条信息通路在高信息样本中合并后是否形成额外增益

## 7. 建议补充的消融版本

如资源允许，建议补充以下版本，用于区分 `structural` 与 `treatment` 的相对作用：

### 7.1 `第二级样本 structural + water-quality`

- 特征：`baseline + structural + pH + alkalinity + TOC`

作用：

- 判断 `treatment` 是否仍有独立附加价值

### 7.2 `第二级样本 treatment + water-quality`

- 特征：`baseline + treatment + pH + alkalinity + TOC`

作用：

- 判断 `structural` 是否仍是更强的信息层

如资源有限，可优先完成第 6 节的四层主对照链。

## 8. 缺失处理要求

### 8.1 关于水质特征

对于 `pH`、`alkalinity`、`TOC`：

- 保留原始缺失
- 不允许在主表中覆盖式改写缺失值
- 数值列在 pipeline 中按既有规则使用中位数填补
- 缺失标记列保留并按既有流程进入模型

### 8.2 关于 treatment 二值字段

对于 `has_*_process` 系列字段：

- 保留原始缺失
- 不允许把缺失直接覆盖成 `0`
- 不允许把缺失简单解释为“没有该工艺”

### 8.3 关于结构/coverage 条件特征

- 继续沿用 `V4.5` 的定义
- 保持其在 `第二级样本` 中的原始语义，不做重新发明
- 文档中必须说明这类特征更偏系统背景、覆盖条件或制度代理信息

## 9. 本轮需要回答的核心问题

完成本轮后，至少要回答以下问题：

1. 在 `第二级样本` 中，水质特征通路相对 baseline 是否已经形成稳定增益？
2. 在 `第二级样本` 中，系统背景通路相对 baseline 是否仍是更强或更稳定的增强层？
3. 在 full integration 中，`baseline + structural + treatment + pH + alkalinity + TOC` 是否继续优于两个单通路版本？
4. 当系统背景通路已经进入模型后，`pH + alkalinity + TOC` 是否仍保留独立增量价值？
5. 当水质特征通路已经进入模型后，`structural + treatment` 是否仍提供附加价值？
6. 两条信息通路之间更像互补、部分重叠，还是大部分重复？
7. `V4.7` 的结果是否足以动摇当前第三层正式主模型的定位，还是更适合作为高信息样本中的探索性整合证据？

## 10. 结果判断标准

完成本轮后，至少要给出以下判断：

1. `第二级样本 full integration` 是否较两个单通路版本都表现更强。
2. 如更强，这种提升是明显稳定，还是幅度有限。
3. 水质特征通路在控制系统背景通路后是否仍保留值得强调的独立价值。
4. 系统背景通路在高信息样本中是否仍占主导，还是被水质特征通路明显替代。
5. `V4.7` 更适合被写成：
   - 两条信息通路的互补证据
   - 还是两条信息通路高度重叠的证据
6. `V4.7` 是否只应作为框架内的探索性整合实验，而不是新的正式主模型结论。

## 11. 本轮明确禁止事项

本轮禁止：

1. 直接把 `V4.7` 预设为新的正式主模型替代实验。
2. 一开始就跳到 `第一级样本` 做同样的大模型合并。
3. 同时引入 `free_chlorine`、`total_chlorine` 等高稀疏变量扩大搜索范围。
4. 切换到树模型、boosting 或超参数优化。
5. 跳过 baseline / 单通路 reference，只保留 full integration。
6. 把结构、coverage、treatment 的提升直接写成环境机制发现。
7. 把 `第二级样本` 的结果直接改写成全国正式主模型结论。

## 12. 本轮输出要求

### 12.1 脚本

至少新增或更新以下脚本中的一部分：

- `scripts/v4_7_information_path_integration_common.py`
- `scripts/train_v4_tthm_regulatory_l2_information_path_integration.py`
- `scripts/train_v4_tthm_anchored_l2_information_path_integration.py`

如需要，可扩展现有共享训练脚本，但应保持命名清晰。

### 12.2 本地结果目录

本轮结果目录建议写入：

- `data_local/V4_Chapter1_Part1_Experiments/V4_7/tthm_regulatory_exceedance_prediction/`
- `data_local/V4_Chapter1_Part1_Experiments/V4_7/tthm_anchored_risk_prediction/`

文件名应尽量明确体现：

- `第二级样本`
- `baseline`
- `water_quality`
- `system_background`
- `full_integration`
- `logistic_regression`

### 12.3 文档

至少新增一份 `V4.7` 中文执行文档，建议放在：

- `docs/06_v4/17_v4_7_execution/`

文档必须包括：

- 本轮任务定义
- 为什么固定在 `第二级样本`
- 系统背景通路与水质特征通路的当前定义
- 主对照链与可选消融链
- 缺失处理方式
- validation / test 结果
- 两条信息通路的互补/重叠判断
- `V4.7` 对当前正式主模型定位有没有影响

## 13. 完成后的收尾要求

完成本轮后，必须：

1. 更新 [codex.md](D:/Project_DBPs_prediction_and_casual_analysis/codex.md)
2. 在 `codex.md` 中记录：
   - 更新时间
   - 本轮实验名称
   - 新增脚本
   - 新增文档
   - 关键结果摘要
   - `V4.7` 是否支持两条信息通路互补的判断
3. 向用户汇报：
   - `V4.7` 是否完成
   - 两条信息通路合并后是否更强
   - `TOC` 等水质变量在控制系统背景通路后是否仍保留独立价值
   - `V4.7` 是否影响当前正式主模型定位
4. 最后询问用户是否执行 Git 提交与推送

## 14. 一句话任务总结

当前请你执行 `V4.7`，明确目标为：

- 在第二层高信息样本 `第二级样本` 中，将系统背景通路与水质特征通路纳入同一对照体系
- 比较 `baseline`、`water-quality reference`、`system-background reference` 与 `full integration`
- 判断两条信息通路在高信息样本中是互补、部分重叠还是大部分重复
- 最终完成脚本、本地结果、中文执行文档和 `codex.md` 的同步更新
