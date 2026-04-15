# legacy_root_imports 清理审计报告

- 生成时间：2026-04-15 10:40:22（Asia/Hong_Kong）
- 审计范围：`docs/**/legacy_root_imports/` 下的 Markdown 文件。
- 审计目的：识别早期迁移目录中的重复文件和需要人工确认的旧资料。
- 本报告先执行审计；经用户确认后，已删除 `3` 个内容完全重复的 legacy 副本。

## 1. 总体统计

- legacy 文件总数：`10`
- 可安全删除候选：`3`
- 需要人工复核：`4`
- 仅 legacy 存在、暂时保留：`3`

## 2. 可安全删除候选

这些文件在正式位置存在完全相同内容的副本。建议在用户确认后删除 legacy 副本。

| legacy 文件 | 对应正式文件 | 原因 |
|---|---|---|
| `docs/00_overview/legacy_root_imports/GITHUB_AND_LOCAL_PROJECT_STATUS.md` | `docs/00_overview/GitHub_and_Local_Project_Status.md` | 存在正式位置文件与 legacy 文件内容完全一致。 |
| `docs/04_v3/legacy_root_imports/V3_prototype_audit_report.md` | `docs/04_v3/V3_Prototype_Audit_Report.md` | 存在正式位置文件与 legacy 文件内容完全一致。 |
| `docs/04_v3/legacy_root_imports/V3_pws_year_build_notes.md` | `docs/04_v3/V3_PWS_Year_Build_Notes.md` | 存在正式位置文件与 legacy 文件内容完全一致。 |

## 3. 需要人工复核

这些文件存在名称相近的正式位置文件，但内容不同。删除前必须确认是否仍保留历史价值。

| legacy 文件 | 对应正式文件 | 原因 |
|---|---|---|
| `docs/00_overview/legacy_root_imports/SYR4_dataset_logic_guide_cn.md` | `docs/00_overview/SYR4_Dataset_Logic_Guide_CN.md` | 存在名称相近的正式位置文件，但内容不同。 |
| `docs/04_v3/legacy_root_imports/V3_pws_year_dictionary.md` | `docs/04_v3/V3_PWS_Year_Dictionary.md` | 存在名称相近的正式位置文件，但内容不同。 |
| `docs/04_v3/legacy_root_imports/V3_Raw Data Mapping Rules.md` | `docs/04_v3/V3_Raw_Data_Mapping_Rules.md` | 存在名称相近的正式位置文件，但内容不同。 |
| `docs/05_v3_5/legacy_root_imports/V3_5_V4_ML_Ready_Codex_Prompt.md` | `docs/05_v3_5/V3_5_V4_ML_Ready_Codex_Prompt.md` | 存在名称相近的正式位置文件，但内容不同。 |

## 4. 仅 legacy 存在，暂时保留

这些文件没有找到对应正式位置文件。建议暂时保留，除非后续确认已经无历史价值。

| legacy 文件 | 对应正式文件 | 原因 |
|---|---|---|
| `docs/01_design/legacy_root_imports/SYR4_第一章高风险场景定义框架.md` | `未找到` | 未找到对应正式位置文件，可能是旧资料或尚未迁移内容。 |
| `docs/04_v3/legacy_root_imports/V3_pws_year_ML字段筛选规范.md` | `未找到` | 未找到对应正式位置文件，可能是旧资料或尚未迁移内容。 |
| `docs/04_v3/legacy_root_imports/V3_最后一个小更新_原始数据映射法则_Codex_Prompt.md` | `未找到` | 未找到对应正式位置文件，可能是旧资料或尚未迁移内容。 |

## 5. 建议

- 当前不建议自动删除全部 `legacy_root_imports`。
- `safe_to_remove_candidate` 中 `3` 个完全重复的 legacy 副本已在 2026-04-15 10:43（Asia/Hong_Kong）删除。
- `needs_manual_review` 和 `legacy_only_keep_until_reviewed` 应先人工确认，再决定是否迁移、合并或删除。

## 6. 已执行清理

本次只删除审计表中状态为 `safe_to_remove_candidate` 且在正式位置存在完全相同 SHA256 内容的 legacy 副本：

| 已删除 legacy 文件 | 保留的正式文件 |
|---|---|
| `docs/00_overview/legacy_root_imports/GITHUB_AND_LOCAL_PROJECT_STATUS.md` | `docs/00_overview/GitHub_and_Local_Project_Status.md` |
| `docs/04_v3/legacy_root_imports/V3_prototype_audit_report.md` | `docs/04_v3/V3_Prototype_Audit_Report.md` |
| `docs/04_v3/legacy_root_imports/V3_pws_year_build_notes.md` | `docs/04_v3/V3_PWS_Year_Build_Notes.md` |

以下类型文件未删除：

- `needs_manual_review`：存在名称相近的正式位置文件，但内容不同，需要人工比较后再决定。
- `legacy_only_keep_until_reviewed`：仅 legacy 目录存在，暂时保留，避免丢失历史资料。
