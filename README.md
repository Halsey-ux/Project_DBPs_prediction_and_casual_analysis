# Project DBPs Prediction and Causal Analysis

This repository stores the code, documentation, and lightweight reports for a dissertation-oriented research project based on the U.S. EPA SYR4 dataset.

## Project Positioning

The current research focus is the first chapter of a dissertation:

- Use the SYR4 database as a large-scale real-world regulatory monitoring dataset
- Focus on system-level prediction and explanation of disinfection byproduct risks
- Start with regulated DBPs, especially `TTHM` and `HAA5`
- Build analysis-ready datasets for correlation analysis, feature screening, and machine learning

The project does **not** treat SYR4 as a fine-scale single-plant process reconstruction database. Instead, it treats SYR4 as a real-world training ground for identifying high-risk DBP scenarios and building interpretable predictive frameworks.

## Raw Data

Raw SYR4 data are **not** stored in this GitHub repository.

Current local raw-data locations:

- `D:\Syr4_Project\syr4_DATA_CSV`
- `D:\SYR4_Data\syr4_DATA_excel`

These source folders should be treated as read-only inputs.

## Current Status

The project has already completed:

- Conversion of SYR4 files into local CSV and Excel formats
- Preliminary interpretation of the SYR4 directory structure and data modules
- Identification of template-based monitoring tables and special-purpose tables
- Clarification of the role of paired microbes/disinfectant-residual files
- Draft research design for dissertation chapter one

The project is now entering the first implementation stage:

- Build a first-round `TTHM`-centered analysis dataset
- Align a small set of DBP-related chemistry variables into the `TTHM` main table
- Prepare for Spearman correlation analysis and baseline machine learning

## Immediate Next Step

The current priority is to construct a first-round analysis-ready dataset using:

- Main table:
  - `SYR4_THMs/TOTAL TRIHALOMETHANES (TTHM).csv`
- First-round aligned variables:
  - `PH.csv`
  - `TOTAL ALKALINITY.csv`
  - `TOTAL ORGANIC CARBON.csv`
  - `FREE RESIDUAL CHLORINE (1013).csv`

The first-round task is to:

1. inspect field compatibility
2. define merge rules
3. build a compact chemistry-enhanced `TTHM` dataset
4. support baseline Spearman analysis and machine-learning feasibility testing

## Repository Scope

This repository should mainly contain:

- `scripts/` style processing logic
- markdown reports and research notes
- lightweight metadata and summary outputs
- project documentation

Large raw datasets, temporary outputs, and generated heavy files should remain local and outside version control.

