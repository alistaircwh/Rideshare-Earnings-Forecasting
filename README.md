# NYC Rideshare Earnings Prediction

Predicting driver earnings for Uber and Lyft trips in New York City using NYC TLC For-Hire Vehicle High-Volume (FHVHV) trip records from May–November 2023.

## Results

| Model | RMSE | R² |
|---|---|---|
| Linear Regression | $4.88 | 0.850 |
| Lasso Regression (L1, λ=1) | $5.42 | 0.815 |

**Key findings:**
- Airport pick-up zones (JFK, LGA, EWR) consistently yield the highest earnings per hour
- Earnings peak between 5–8 AM and 10 PM–midnight, driven by commuter and late-night demand
- Uber (HV0003) trips earn slightly more per hour on average than Lyft (HV0005)
- Weather features (feels-like temperature, precipitation) have a modest but measurable effect on earnings

## Methodology

```
NYC TLC (FHVHV)          External Data
May–Oct 2023       ──┐   (weather, holidays,
                      ├──► Preprocessing ──► Feature Engineering ──► Model Training
Nov 2023 (holdout) ──┘   taxi zone shapefiles)                            │
                                                                           ▼
                                                                     Evaluation +
                                                                     EDA / Maps
```

**Train/test split:** Months 5–10 as training set (~90M trips), November 2023 as a temporal holdout (~15M trips) to simulate real-world generalisation.

**Features:** One-hot encoded license type (Uber/Lyft), standardised trip distance, day-of-week and hour-of-day encodings, pickup location encoding (NYC taxi zones), weather conditions (feels-like temperature, precipitation type/amount), and a public holiday indicator.

**Outlier removal:** Domain-aware IQR rule with threshold `(√log(N) − 0.5) × IQR` — more permissive than the standard 1.5×IQR multiplier to avoid over-filtering high-value trips.

## Tech Stack

| Tool | Purpose |
|---|---|
| PySpark 3.5 | Distributed data processing and ML |
| pandas / NumPy | Local data manipulation and visualisation prep |
| geopandas + folium | Geospatial analysis and interactive maps |
| scikit-learn / XGBoost | Supporting modelling utilities |
| matplotlib / seaborn | Static visualisations |

## Data Source

[NYC TLC For-Hire Vehicle High-Volume trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) — publicly available monthly Parquet files. Only FHVHV records (Uber: HV0003, Lyft: HV0005) are used.

External datasets: hourly NYC weather data (May 2023–May 2024) and NYC public holiday calendar.

## Setup

**Requirements:** Python 3.12, Java (for PySpark)

```bash
pip install -r requirements.txt
```

## Running the Pipeline

Run these steps in order:

1. **Download raw data**
   ```bash
   python scripts/download.py
   ```
   Downloads FHVHV Parquet files for May–October 2023 into `data/raw/`.

2. **Preprocess** — `notebook/preprocess.ipynb`
   Cleans, filters, and feature-engineers the trip data. Also processes the external weather and holidays datasets. Outputs curated Parquet files to `data/curated/`.

3. **Analysis** — `notebook/analysis.ipynb`
   Exploratory data analysis with geospatial choropleth maps (folium) and earnings visualisations. Outputs to `plots/`.

4. **Model** — `notebook/model.ipynb`
   Trains Linear Regression and Lasso models with PySpark ML. Evaluates against the November 2023 holdout set.

## Future Improvements

- **Richer feature set:** incorporate traffic density, surge multiplier data, or driver ratings
- **Non-linear models:** benchmark against gradient boosting (XGBoost, LightGBM) or a neural network
- **Per-zone analysis:** fit separate models per borough or zone cluster to capture spatial heterogeneity
- **Real-time scoring:** deploy the model as a lightweight API for live earnings estimation

## Report

A full write-up of the methodology, analysis, and results is available in [report/report.pdf](report/report.pdf).
