from urllib.request import urlretrieve

import os

# From the current directory, go back to the Project 1 directory
output_relative_dir = './data/'

# Check if it exists
# makedir will raise an error if it does exist
if not os.path.exists(output_relative_dir):
    os.makedirs(output_relative_dir)
    
# Create the path for the tlc_data
target_dir = 'raw'
    
if not os.path.exists(output_relative_dir + target_dir):
    os.makedirs(output_relative_dir + target_dir)

# Define the years desired
YEARS = ['2023']

# MONTHS = range(1, 13)
MONTHS = [range(5, 12), range(1, 1)]

# State the URL to retrieve
URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_"

# data output directory is `data/tlc_data/`
tlc_output_dir = output_relative_dir + target_dir

for year in YEARS:

    if year == '2023':
        month_index = 0
    else:
        month_index = 1

    for month in MONTHS[month_index]:
        # 0-fill i.e 1 -> 01, 2 -> 02, etc
        month = str(month).zfill(2) 
        print(f"Begin month {month}")

        # Generate urls
        url = f'{URL_TEMPLATE}{year}-{month}.parquet'

        # Generate output location and filename
        output_dir = f"{tlc_output_dir}/{year}-{month}.parquet"
    
        # Download
        urlretrieve(url, output_dir) 
        
        print(f"Completed month {month}")