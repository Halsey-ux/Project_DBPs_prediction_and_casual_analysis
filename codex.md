# codex.md

## 1. Project Background

This project supports dissertation research based on the U.S. EPA SYR4 dataset.

The current dissertation focus is the first chapter:

- use SYR4 as a large-scale real-world regulatory monitoring dataset
- study regulated disinfection byproducts (DBPs), especially `TTHM` and `HAA5`
- build an interpretable system-level prediction and risk-analysis framework

The project does not treat SYR4 as a fine-scale single-plant mechanistic process database. It treats SYR4 as a real-world monitoring and regulatory data world for DBP risk identification, explanation, and prediction.

## 2. Overall Goal

The overall project goal is to support a dissertation that links:

- large-scale SYR4-based DBP risk and prediction analysis
- interpretable feature screening and scenario identification
- later experimental chapters for targeted or suspect screening under high-risk real-world conditions

## 3. Current Stage Goal

The current stage goal is to build the first-round `TTHM` analysis workflow:

- use `TOTAL TRIHALOMETHANES (TTHM).csv` as the main outcome table
- align a small set of first-round DBP-relevant chemistry variables
- support baseline Spearman analysis and first-round machine-learning feasibility testing

## 4. Directory Structure

Current project root:

- `D:\Project_DBPs_prediction_and_casual_analysis`

Current local structure:

```text
D:\Project_DBPs_prediction_and_casual_analysis
├─ .git/
├─ .gitignore
├─ README.md
├─ codex.md
├─ docs/
├─ scripts/
├─ data_local/
└─ scratch/
```

Directory roles:

- `docs/`
  - project notes
  - research design
  - project status
  - data logic documents
- `scripts/`
  - data conversion
  - merge
  - analysis
  - modeling scripts
- `data_local/`
  - large local-only files
  - not tracked by Git
- `scratch/`
  - temporary folders and repair/test outputs
  - not tracked by Git

## 5. Data Situation

Raw SYR4 data are local and should be treated as read-only input sources.

Current local source paths:

- `D:\Syr4_Project\syr4_DATA_CSV`
- `D:\SYR4_Data\syr4_DATA_excel`

Current high-priority first-round data sources:

- main table:
  - `D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv`
- first-round aligned chemistry tables:
  - `PH.csv`
  - `TOTAL ALKALINITY.csv`
  - `TOTAL ORGANIC CARBON.csv`
  - `FREE RESIDUAL CHLORINE (1013).csv`

## 6. Tech Stack

Preferred working stack:

- Python
- pandas
- numpy
- scipy
- scikit-learn
- xgboost / lightgbm when needed
- shap when needed
- PowerShell for local file inspection and project operations
- Git + GitHub for project tracking

## 7. Coding and Project Management Conventions

### 7.1 Raw data policy

- raw data are read-only
- do not overwrite local source SYR4 files
- do not rename raw source files in place

### 7.2 GitHub policy

GitHub should mainly track:

- scripts
- documentation
- reports
- configs
- lightweight metadata
- project-level explanatory files

GitHub should not directly track:

- raw SYR4 data
- large generated analysis tables
- large temporary outputs
- local scratch artifacts

### 7.3 codex.md update rule

`codex.md` is the long-lived project handbook.

It should be updated after every important project update, including:

- script creation or modification
- meaningful documentation updates
- completion of a data-processing stage
- completion of an analysis/modeling stage
- important restructuring of the project

### 7.4 Git update rule

After every important project update:

- update `codex.md`
- create a clear Git commit
- push to GitHub

Small temporary edits do not require immediate push.

### 7.5 Commit message rule

Each important update should use a concise and meaningful commit message that reflects the actual change.

## 8. Current Progress

The project has already completed:

- local conversion of SYR4 data into CSV and Excel forms
- interpretation of the major SYR4 data modules and directory structure
- clarification of template-based monitoring tables and special-purpose tables
- initial dissertation chapter-one design
- initial GitHub connection and repository setup via SSH
- initial project cleanup and root-directory restructuring

## 9. Latest Update

Last updated: 2026-03-23

Latest update summary:

- formalized long-term project-management rules
- created `codex.md` as the project handbook
- established the rule that important updates must also update `codex.md` and be pushed to GitHub

Related commit:

- pending current commit

## 10. Next Step

The next concrete step is:

- build the first-round `TTHM` analysis-ready dataset
- inspect merge compatibility of `TTHM`, `PH`, `TOTAL ALKALINITY`, `TOTAL ORGANIC CARBON`, and `FREE RESIDUAL CHLORINE`
- define first-round alignment rules
- prepare the dataset for baseline Spearman analysis

