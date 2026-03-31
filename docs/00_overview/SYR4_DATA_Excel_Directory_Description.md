# SYR4_DATA_excel 目录说明

本文档整理了 `D:\SYR4_Data\syr4_DATA_excel` 目录下各子文件夹的真实含义，结合 EPA SYR4 官网下载页和用户指南进行说明。

参考来源：

- [EPA Six-Year Review 4 Compliance Monitoring Data (2012-2019)](https://www.epa.gov/dwsixyearreview/six-year-review-4-compliance-monitoring-data-2012-2019)
- [User Guide to Downloading and Using SYR4 Data (PDF)](https://www.epa.gov/system/files/documents/2024-11/user-guide-to-downloading-and-using-syr4-data_0.pdf)

## 总体理解

`syr4_DATA_excel` 是对 EPA SYR4 多个公开数据包的本地 Excel 化整理。整体上可以分成四类：

- 污染物或指标监测结果
- 专题配对或衍生结果
- 系统结构与处理工艺
- 监管与合规管理信息

其中大多数污染物结果文件都属于“监测结果表”，通常一行代表一条样品检测结果。

## 1. `syr4_adwr-compliance-data`

真实意义：

- 这是 `Aircraft Drinking Water Rule`，即飞机饮水规则的数据。
- 研究对象不是普通地面公共供水系统，而是航空器饮水系统。

主要文件：

- `Aircraft_pws_inventory.xlsx`
  - 飞机公共供水系统清单
  - 包含航空公司、飞机注册号、PWSID、状态、采样频率、机型等
- `Aircraft_samples_by_air_carrier.xlsx`
  - 飞机饮水样品记录
  - 包含样品类型、采样日期及微生物相关结果

适用场景：

- 分析飞机饮水系统合规性
- 与普通 PWS 数据分开使用更合理

## 2. `syr4_bromate_chlorite`

真实意义：

- 这是消毒副产物相关的两个专题污染物结果包：
  - `Bromate` 溴酸盐
  - `Chlorite` 亚氯酸盐

主要文件：

- `BROMATE.xlsx`
- `CHLORITE.xlsx`

适用场景：

- 分析臭氧、二氧化氯相关消毒副产物
- 与 THMs、HAA5 一起研究 DBP 风险

## 3. `syr4_corrective_actions`

真实意义：

- 这是整改措施或纠正行动数据。
- 不属于样品浓度结果，而是监管行动记录。

主要文件：

- `SYR4_Corrective_Actions.xlsx`

典型内容：

- 问题识别日期
- 整改类别
- 整改名称
- 应完成日期
- 实际完成日期

适用场景：

- 研究哪些系统被要求整改
- 分析整改时效和合规风险

## 4. `syr4_cryptobinning`

真实意义：

- 这是 `Cryptosporidium binning` 数据。
- 用于 LT2 规则下，对设施按隐孢子虫风险进行分箱。

主要文件：

- `SYR4_CryptoBinning.xlsx`

典型内容：

- 系统或设施标识
- 合规周期起止日期
- `BIN_NUMBER`

适用场景：

- 分析地表水或受地表水影响地下水设施的隐孢子虫风险等级

## 5. `SYR4_DBP_Related Parameters`

真实意义：

- 这是与消毒副产物形成密切相关的水质参数。
- 这类参数往往不是最终监管污染物本身，而是 DBP 前体或形成条件。

主要文件：

- `TOTAL ORGANIC CARBON.xlsx`
- `DOC.xlsx`
- `TOTAL ALKALINITY.xlsx`
- `PH.xlsx`
- `UV_ABSORBANCE.xlsx`
- `SUVA.xlsx`
- `Paired TOC-Alkalinity.xlsx`

各文件大意：

- `TOC`：总有机碳，重要的 DBP 前体指标
- `DOC`：溶解性有机碳
- `TOTAL ALKALINITY`：总碱度
- `PH`：酸碱度
- `UV_ABSORBANCE`：紫外吸光度
- `SUVA`：比紫外吸收值，用于表征有机物性质
- `Paired TOC-Alkalinity`：TOC 与碱度的月度配对结果，不是单条样品明细

适用场景：

- 解释 TTHM、HAA5 等 DBP 的形成机制
- 作为模型解释变量或特征变量

## 6. `SYR4_Disinfectant Residuals`

真实意义：

- 这是消毒剂及其残留浓度监测结果。
- 用于反映系统使用的消毒方式和管网中的残留水平。

主要文件：

- `CHLORINE (0999).xlsx`
- `TOTAL CHLORINE (1000).xlsx`
- `CHLORAMINE (1006).xlsx`
- `CHLORINE_DIOXIDE.xlsx`
- `RESIDUAL CHLORINE (1012).xlsx`
- `FREE RESIDUAL CHLORINE (1013).xlsx`

适用场景：

- 研究消毒策略
- 和微生物、DBP 数据联动分析

## 7. `syr4_ec_fc_hpc_giardia`

真实意义：

- 这是微生物和相关指标结果专题包。

主要文件：

- `ESCHERICHIA COLI (EC).xlsx`
- `FECAL COLIFORM (FC).xlsx`
- `HETEROTROPHIC PLATE COUNT (HPC).xlsx`
- `GIARDIA LAMBLIA.xlsx`
- `CRYPTOSPORIDIUM.xlsx`
- `COLIPHAGE.xlsx`
- `ENTEROCOCCI.xlsx`

适用场景：

- 微生物风险分析
- 与总大肠菌群、余氯和整改措施联动研究

## 8. `SYR4_HAAs`

真实意义：

- 这是卤乙酸类消毒副产物结果包。

主要文件：

- `HALOACETIC ACIDS (HAA5).xlsx`
- `MONOCHLOROACETIC_ACID.xlsx`
- `MONOBROMOACETIC_ACID.xlsx`
- `DICHLOROACETIC_ACID.xlsx`
- `DIBROMOACETIC_ACID.xlsx`
- `TRICHLOROACETIC_ACID.xlsx`

适用场景：

- 与 THMs 一起进行消毒副产物研究
- 比较 HAA5 总量及不同组分的谱型

## 9. `syr4_paired-microbes_dr`

真实意义：

- 这是微生物结果与消毒剂余量配对后的专题数据。
- 重点在于同一记录中同时保留微生物结果和残留消毒剂信息。

主要文件：

- `Paired EC_DR.xlsx`
- `Paired FC_DR.xlsx`
- `Paired TC_DR_2012.xlsx` 到 `Paired TC_DR_2019.xlsx`

适用场景：

- 分析余氯不足与微生物阳性之间的关系
- 研究管网控制状态与微生物风险之间的联系

## 10. `syr4_tc`

真实意义：

- 这是总大肠菌群 `Total Coliform` 数据。
- 按年份拆分发布。

主要文件：

- `TOTAL COLIFORM_2012.xlsx`
- `TOTAL COLIFORM_2013.xlsx`
- `TOTAL COLIFORM_2014.xlsx`
- `TOTAL COLIFORM_2015.xlsx`
- `TOTAL COLIFORM_2016.xlsx`
- `TOTAL COLIFORM_2017.xlsx`
- `TOTAL COLIFORM_2018.xlsx`
- `TOTAL COLIFORM_2019.xlsx`

适用场景：

- 年度趋势分析
- 与 EC、FC、余氯、整改措施联动

## 11. `SYR4_THMs`

真实意义：

- 这是三卤甲烷类消毒副产物结果包。
- 包含总量和四个组分。

主要文件：

- `TOTAL TRIHALOMETHANES (TTHM).xlsx`
- `BROMODICHLOROMETHANE.xlsx`
- `BROMOFORM.xlsx`
- `CHLOROFORM.xlsx`
- `DIBROMOCHLOROMETHANE.xlsx`

适用场景：

- TTHM 合规和形成机制分析
- THM 组分谱分析

## 12. `syr4_treatment`

真实意义：

- 这是系统、设施、处理工艺和流向的基础关系数据。
- 不是污染物浓度表，而是工艺结构表。

主要文件：

- `SYR4_Water_system_table.xlsx`
  - 水系统主表
- `SYR4_Water_system_facility_table.xlsx`
  - 设施主表
- `SYR4_Water_system_facility_plant_table.xlsx`
  - 处理厂层级信息
- `SYR4_Treatment_Process_table.xlsx`
  - 处理工艺信息
- `SYR4_Water_system_flows_table.xlsx`
  - 设施流向和连接关系

适用场景：

- 分析处理工艺与污染物结果之间的关系
- 构建系统级与设施级关联结构

说明：

- EPA 明确提示 treatment 数据未经过与 occurrence 数据同等级的 QA/QC，使用时应更谨慎。

## 13. `_syr4_phasechem_1-111-trichloroethane-to-atrazine`

真实意义：

- 这是第一批常规化学污染物监测结果。
- 每个 Excel 对应一个具体污染物。

文件特点：

- 文件名通常为 `SUMMARY_ANALYTE_*.xlsx`
- 例如 `ARSENIC`、`ATRAZINE`、`ALACHLOR` 等

适用场景：

- 单污染物 occurrence 分析
- 暴露水平与系统属性的关联研究

## 14. `_syr4_phasechem_2-barium-to-cyanide`

真实意义：

- 第二批常规化学污染物结果。

典型污染物：

- `BARIUM`
- `BENZENE`
- `CADMIUM`
- `CYANIDE`

适用场景：

- 常规化学污染物全国 occurrence 分析

## 15. `_syr4_phasechem_3-dalapon-to-hexachlorocyclopentadiene`

真实意义：

- 第三批常规化学污染物结果。

典型污染物：

- `DALAPON`
- `DINOSEB`
- `FLUORIDE`
- `GLYPHOSATE`

适用场景：

- 农药、无机物及有机污染物专题分析

## 16. `_syr4_phasechem_4-hybrid-nitrate-to-nitrate`

真实意义：

- 一组特殊或混合处理的常规化学污染物结果。

典型污染物：

- `HYBRID_NITRATE`
- `MERCURY`
- `LEAD`
- `NITRATE`

适用场景：

- 硝酸盐、重金属等重点污染物分析

## 17. `_syr4_phasechem_5-nitrate-nitrite-to-total-polychlorinated-biphenyls-pcb`

真实意义：

- 第五批常规化学污染物结果。

典型污染物：

- `NITRITE`
- `NITRATE-NITRITE`
- `SELENIUM`
- `SIMAZINE`
- `TOTAL_POLYCHLORINATED_BIPHENYLS(PCB)`

适用场景：

- 常规化学与农药污染物分析

## 18. `_syr4_phasechem_6-toxaphene-to-xylenes-total`

真实意义：

- 第六批常规化学污染物结果。

典型污染物：

- `TOXAPHENE`
- `TRICHLOROETHYLENE`
- `VINYL_CHLORIDE`
- `XYLENES_TOTAL`

适用场景：

- 挥发性有机物与农药类污染物分析

## 19. `_syr4_rads`

真实意义：

- 这是放射性指标结果数据。

主要文件：

- `SUMMARY_ANALYTE_COMBINED_URANIUM.xlsx`
- `SUMMARY_ANALYTE_COMBINED_RADIUM_226_228.xlsx`
- `SUMMARY_ANALYTE_GROSS_ALPHA_EXCL_RADON_U.xlsx`
- `SUMMARY_ANALYTE_GROSS_BETA_PARTICLE_ACTIVITY.xlsx`

适用场景：

- 放射性饮用水风险分析
- 与水源类型和区域地质背景结合研究

## 使用建议

如果你的目标是做整合分析，可以按下面的逻辑理解整个目录：

1. 以某个污染物结果文件作为主表
2. 用 `PWSID`、`WATER_FACILITY_ID`、日期等字段进行横向关联
3. 视需要补充：
   - `syr4_treatment` 的工艺和设施信息
   - `SYR4_DBP_Related Parameters` 的前体/环境变量
   - `SYR4_Disinfectant Residuals` 的消毒状态
   - `syr4_corrective_actions` 的监管背景

## 总结

`D:\SYR4_Data\syr4_DATA_excel` 不是一个单一数据集，而是一套围绕饮用水监测、处理、风险、整改和专题规则的数据体系。不同子目录分别对应：

- 污染物监测结果
- 微生物与消毒剂联动专题
- 处理工艺和设施结构
- 监管和整改信息
- 特定规则下的专题数据，如 ADWR 和 CryptoBinning

如果后续需要，可以在此基础上继续细化到：

- 每个子文件夹下每个 Excel 的字段级解释
- 哪些表之间可以通过 `PWSID`、`WATER_FACILITY_ID`、日期字段进行关联
- 哪些字段适合做机器学习建模输入