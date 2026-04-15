# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MAST30034 (Applied Data Science) project at the University of Melbourne. Goal: predict earnings for rideshare services (Uber/Lyft via NYC TLC FHVHV data) for May–November 2023. Training data: May–October 2023; test set: November 2023.

## Setup

```bash
pip install -r requirements.txt
```

Requires Python 3.12. PySpark 3.5.2 is the primary processing engine — a local JVM must be available.

## Execution Pipeline (run in order)

1. **Download raw data**
   ```bash
   python scripts/download.py
   ```
   Fetches NYC TLC FHVHV Parquet files into `data/raw/`.

2. **Preprocess** — run `notebook/preprocess.ipynb`
   Cleans data, one-hot encodes categorical features (license/day/hour/location/precipitation), standardizes numerics, applies IQR outlier removal (domain-aware: only for groups with N > 100). Outputs curated Parquet files to `data/curated/`.

3. **Analysis** — run `notebook/analysis.ipynb`
   EDA and geospatial visualizations (geopandas + folium). Outputs HTML maps and PNG plots to `plots/`.

4. **Modelling** — run `notebook/model.ipynb`
   PySpark ML `LinearRegression` trained on months 5–10, evaluated on month 11. Metrics: RMSE and R².

## Architecture

```
scripts/
  download.py       # Downloads raw data from NYC TLC
  functions.py      # Reusable utilities: IQR outlier removal, standardization helpers
notebook/
  preprocess.ipynb  # Step 2: cleaning & feature engineering
  analysis.ipynb    # Step 3: EDA & geospatial maps
  model.ipynb       # Step 4: Linear regression with PySpark ML
data/
  raw/              # Raw FHVHV Parquet files (gitignored)
  curated/          # Processed Parquet output from preprocessing
  raw_csv/          # External reference data (taxi zone shapefiles, weather)
  results/          # Model output artifacts
plots/              # Generated visualizations (PNG + interactive HTML)
report/             # Final PDF report
```

**Data flow:** `download.py` → `data/raw/` → `preprocess.ipynb` → `data/curated/` → `analysis.ipynb` + `model.ipynb` → `plots/` + `data/results/`

## Key Technical Notes

- **Uber = HV0003, Lyft = HV0005** — these are the license type filters applied in preprocessing.
- Utility functions in `scripts/functions.py` (IQR removal, standardization) are imported directly into the notebooks via `sys.path` — keep the module importable from notebook context.
- PySpark sessions are created locally inside each notebook; no external cluster required.
- `analysis.ipynb` is large (~8.5 MB) due to embedded cell outputs — avoid re-running all cells unnecessarily.
