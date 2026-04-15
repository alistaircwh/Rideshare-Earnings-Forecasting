"""
Download NYC TLC For-Hire Vehicle High-Volume (FHVHV) trip data.

Downloads monthly Parquet files from the NYC TLC public dataset for the
months configured in DOWNLOAD_MONTHS. Output files are saved to data/raw/.

Usage:
    python scripts/download.py
"""

import os
from urllib.request import urlretrieve
from urllib.error import URLError

# Output directory for raw Parquet files
RAW_DATA_DIR = "./data/raw"

# NYC TLC public dataset base URL
URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_"

# Months to download (May–October 2023 for training; November is the test holdout)
DOWNLOAD_MONTHS = {
    "2023": range(5, 11),
}

os.makedirs(RAW_DATA_DIR, exist_ok=True)

for year, months in DOWNLOAD_MONTHS.items():
    for month in months:
        month_str = str(month).zfill(2)
        url = f"{URL_TEMPLATE}{year}-{month_str}.parquet"
        output_path = os.path.join(RAW_DATA_DIR, f"{year}-{month_str}.parquet")

        print(f"Downloading {year}-{month_str} ...")
        try:
            urlretrieve(url, output_path)
            print(f"  Saved to {output_path}")
        except URLError as e:
            print(f"  ERROR: Could not download {url} — {e}")
