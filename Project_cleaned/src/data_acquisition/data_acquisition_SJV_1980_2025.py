# data acquisition.py

# *******************************
# this file should fetch all necessary data needed for this project.
# *******************************

from config import PROJECT_ROOT

import requests
import pandas as pd
import time  # To avoid hitting API rate limits
from datetime import datetime, timedelta


# ******************************************************************************************
# This codeblock fetches SJV data from 1980 to 2025, required for initial T-testing.

# ******************************************************************************************

# API endpoint for county-level data
url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

# API Credentials
email = "dksxowns69@gmail.com"
api_key = "aquabird37"

# Pollutant parameter codes
params_list = [#"61101", # Wind Speed_Simple
               #"61103", # Wind Speed_ Resultant (Vector-based)
               #"61104", # Wind direction
               #"62101", # Outdoor Temperature
               #"62201", # Relative Humidity
               #"64101", # Barometric Pressure
               #"42101", # Carbon monoxide
               #"63101", # Visibility
               #"63011", # Solar Radiation
               "88101", # PM2.5
               "85129", # PM10
               "42602", # NO2
               "44201", # Ozone

]

# Year range
years = range(1980, 2025)

# California state code
state_code = "06"

# San Joaquin Valley county codes
county_codes = {
    "San Joaquin": "077",
    "Stanislaus": "099",
    "Merced": "047",
    "Fresno": "019",
    "Kings": "031",
    "Tulare": "107",
    "Kern": "029"
}

# Empty list to store data
all_data = []

# Loop through pollutants, counties, and years
for param in params_list:
    for county_name, county_code in county_codes.items():
        for year in years:
            print(f"Fetching {param} for {county_name} ({county_code}) in {year}...")

            params = {
                "email": email,
                "key": api_key,
                "param": param,
                "bdate": f"{year}0101",
                "edate": f"{year}1231",
                "state": state_code,
                "county": county_code
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if "Data" in data and data["Data"]:
                    all_data.extend(data["Data"])
                    print(f"Success: {len(data['Data'])} records added.")
                else:
                    print(f"No data found for {param} in {county_name} ({year}).")
            else:
                print(f"Error: {response.status_code}, {response.text}")

            time.sleep(1)  # Avoid exceeding API rate limits

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save to CSV for future analysis
df.to_csv(PROJECT_ROOT/"data"/"raw"/"SJV_AQI_1980_2025.csv", index=False)

print(f"Final dataset contains {df.shape[0]} records.")


# ******************************************************************************************
# This codeblock fetches SJV data from 1980 to 2025, required for initial T-testing.

# ******************************************************************************************