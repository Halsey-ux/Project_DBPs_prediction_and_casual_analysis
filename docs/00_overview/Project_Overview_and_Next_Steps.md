# Project Overview and Next Steps

## 1. Research Background

This project studies disinfection byproducts (DBPs) using the EPA SYR4 compliance monitoring dataset. The current dissertation focus is to use SYR4 as a large-scale real-world dataset for:

- DBP risk recognition
- feature screening
- interpretable prediction
- scenario prioritization for later experimental chapters

The project emphasis is on `TTHM` and `HAA5`, with the understanding that SYR4 is strongest on nationwide monitoring coverage, system heterogeneity, and regulatory realism, but weaker on detailed process-mechanism reconstruction.

## 2. Local Data Situation

The main local SYR4 data resources are already prepared in CSV and Excel forms:

- CSV mirror:
  - `D:\Syr4_Project\syr4_DATA_CSV`
- Excel mirror:
  - `D:\SYR4_Data\syr4_DATA_excel`

These local data include:

- THMs
- HAAs
- DBP-related parameters
- disinfectant residuals
- microbial occurrence data
- paired microbes/residual data
- treatment and facility metadata
- corrective actions
- additional chemical and radiological modules

## 3. Current Project Understanding

The project has already established the following working conclusions:

- The SYR4 database describes a full drinking-water monitoring world from source-water context to treatment, distribution, occurrence results, and regulatory response.
- Template A occurrence tables share a common public-release schema and are suitable for structured alignment.
- Paired microbe/residual files are analysis-oriented subsets intended to support direct investigation of microbe/disinfectant-residual relationships.
- For DBP work, the most promising first-round path is not to merge everything at once, but to build an analysis-ready table around a main outcome.

## 4. Immediate Research Objective

The immediate objective is to build a first-round `TTHM` analysis dataset that can be used for:

- baseline exploratory statistics
- Spearman correlation analysis
- feature screening
- first-round machine-learning feasibility tests

## 5. First-Round Main Table

Main table:

- `D:\Syr4_Project\syr4_DATA_CSV\SYR4_THMs\TOTAL TRIHALOMETHANES (TTHM).csv`

Reason:

- `TTHM` is one of the most central regulated DBP outcomes
- it has large sample size
- it supports both statistical and prediction-oriented first-round work

## 6. First-Round Variables to Align

The first-round aligned variables should be limited to a small chemistry-focused set:

From `SYR4_DBP_Related Parameters`:

- `PH.csv`
- `TOTAL ALKALINITY.csv`
- `TOTAL ORGANIC CARBON.csv`

From `SYR4_Disinfectant Residuals`:

- `FREE RESIDUAL CHLORINE (1013).csv`

These variables are prioritized because they:

- have clear DBP relevance
- use compatible public-release table structures
- are easier to align than broader modules
- are sufficient for the first round of correlation analysis and baseline modeling

## 7. First-Round Technical Goal

Build a compact analysis-ready table with:

- `tthm_value` as the main target
- time fields (`year`, `month`, `quarter`)
- core system and facility context
- `ph_value`
- `alkalinity_value`
- `toc_value`
- `free_chlorine_value`
- a merge-quality indicator such as `match_level`

## 8. Suggested Merge Strategy

Preferred merge hierarchy:

1. exact match:
   - `PWSID`
   - `WATER_FACILITY_ID`
   - `SAMPLING_POINT_ID`
   - `SAMPLE_COLLECTION_DATE`
2. same-facility same-day match:
   - `PWSID`
   - `WATER_FACILITY_ID`
   - `SAMPLE_COLLECTION_DATE`
3. broader matching should only be considered after match-rate auditing

## 9. Immediate Analytical Direction

After the first-round dataset is built, the next analytical sequence should be:

1. audit usable coverage
2. inspect variable distributions
3. run baseline Spearman analyses
4. compare baseline and chemistry-enhanced feature sets
5. test first-round machine-learning models for `TTHM`

## 10. Overall Long-Term Goal

The broader dissertation goal is to construct an interpretable, system-level DBP prediction and risk-recognition framework that can:

- identify high-risk DBP scenarios
- screen stable explanatory factors
- support later sample prioritization for downstream experimental chapters

