# 本地项目数据完整性审计报告

- 生成时间：2026-04-15 10:21:28（Asia/Hong_Kong）
- 审计范围：`data_local/` 本地项目产物、已记录原始 SYR4 数据目录的存在性与 0 字节检查。
- 审计方式：只读检查文件大小、修改时间、首段哈希、CSV 表头和行数、JSON/Markdown 可读性、关键数据集预期行列数。

## 1. 总体结论

- `data_local/` 共检查 `167` 个文件，总大小 `1179312040` bytes。
- 三个关键本地数据集均通过预期行数和字段数校验。
- 原始 SYR4 数据目录存在，未发现 0 字节文件。
- 当前不建议把 `data_local/` 大型本地数据文件直接提交到 GitHub；建议提交脚本、文档、恢复记录和本审计报告，数据本体继续本地保存。

## 2. 文件状态统计

| 状态 | 文件数 |
|---|---:|
| `binary_not_deep_checked` | `1` |
| `ok` | `165` |
| `zero_bytes` | `1` |

## 3. 关键数据集校验

| 文件 | 预期行数 | 实际行数 | 预期字段数 | 实际字段数 | 结论 |
|---|---:|---:|---:|---:|---|
| `data_local/V3_Chapter1_Part1_Prototype_Build/V3_facility_month_master.csv` | `1442728` | `1442728` | `98` | `98` | `passed` |
| `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.csv` | `259500` | `259500` | `130` | `130` | `passed` |
| `data_local/V4_Chapter1_Part1_ML_Ready/V4_pws_year_ml_ready.csv` | `259500` | `259500` | `38` | `38` | `passed` |

## 4. 0 字节文件检查

- `data_local/V3_Chapter1_Part1_Prototype_Build/V3_pws_year_master.zero_byte_20260401_091846.csv`

说明：本轮审计的 `data_local/` 中仍保留 `V3_pws_year_master.zero_byte_20260401_091846.csv` 作为事故证据备份，该文件不应被视为当前正式业务输入。

## 5. 读取错误检查

- 未发现 CSV/JSON/Markdown 读取错误。

## 6. 原始数据目录检查

| 原始数据目录 | 是否存在 | 文件数 | 0 字节文件数 | 总大小 bytes | 状态 |
|---|---|---:|---:|---:|---|
| `D:\Syr4_Project\syr4_DATA_CSV` | `True` | `133` | `0` | `13016387125` | `ok` |
| `D:\SYR4_Data\syr4_DATA_excel` | `False` | `0` | `0` | `0` | `missing` |

## 7. Git 备份建议

建议进入 GitHub 的内容：

- `scripts/` 下的审计、恢复和建模脚本。
- `docs/` 下的协议、报告、恢复记录和数据字典。
- `codex.md`、`.gitignore` 等项目级配置和说明。
- 本轮生成的轻量审计报告与轻量摘要表。

不建议进入 GitHub 的内容：

- `data_local/` 下大型 CSV、JSON 结果、Excel 或中间文件。
- 原始 SYR4 数据目录。
- `scratch/` 临时输出。
- 事故证据备份 `V3_pws_year_master.zero_byte_20260401_091846.csv`。

## 8. 后续建议

- 若需要长期异地备份大型本地数据，应使用外部硬盘、对象存储、NAS 或专门的数据版本工具，而不是 GitHub 普通仓库。
- 若需要 GitHub 记录数据状态，应提交本报告、校验 JSON/CSV、恢复记录和生成脚本，而不是提交数据本体。
- 每次重建关键本地数据后，应重新运行本审计脚本并更新报告。
