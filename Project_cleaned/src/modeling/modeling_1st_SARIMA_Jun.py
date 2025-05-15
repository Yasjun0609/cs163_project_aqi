# modeling_1st_SARIMA_Jun.py

from config import PROJECT_ROOT
import pandas as pd
import numpy as np
from datetime import datetime, timedelt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import ttest_ind


# ******************************************************************************************

# 1: 1st SARIMA Attempt_Jun

# ******************************************************************************************

# --- PARAMETERS ---
ISR_YEAR = 2006  # Easy to update for Setting where Pre VS POST lies.
forecast_start_date = "2024-11-01"
pollutants = ['PM10 Total 0-10um STP', 'PM2.5 - Local Conditions', 'Ozone', 'Nitrogen dioxide (NO2)']
counties = ['San Joaquin', 'Stanislaus', 'Merced', 'Fresno', 'Kings', 'Tulare', 'Kern']

# --- LOAD AND CLEAN ---
df = pd.read_csv(PROJECT_ROOT/"data"/"raw"/"SJV_AQI_1980_2025.csv")
df = df[df['county'].isin(counties) & df['parameter'].isin(pollutants)]
df = df[df['metric_used'] == 'Daily Mean']


# Fix datetime and group
df['datetime'] = pd.to_datetime(df['first_max_datetime'], errors='coerce')
df = df.dropna(subset=['datetime'])
df['date'] = df['datetime'].dt.date
df['month'] = pd.to_datetime(df['datetime'].dt.to_period('M').astype(str))
df['year'] = df['datetime'].dt.year
df = df.rename(columns={'parameter': 'pollutant', 'arithmetic_mean': 'value'})


# --- FUNCTION: Forecast by time unit ---
def forecast_by_timescale(grouped, freq, periods, label):
    results = []
    for (county, pollutant), group in grouped.groupby(['county', 'pollutant']):
        ts = group.set_index('date').asfreq(freq)['value'].fillna(method='ffill')
        if len(ts.dropna()) < 36:
            continue
        try:
            model = SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12), enforce_stationarity=False, enforce_invertibility=False)
            fit = model.fit(disp=False)
            start = len(ts)
            end = start + periods - 1
            forecast_index = pd.date_range(ts.index[-1] + pd.tseries.frequencies.to_offset(freq), periods=periods, freq=freq)
            forecast = fit.predict(start=start, end=end)
            results.append(pd.DataFrame({
                'date': forecast_index,
                'predicted_value': forecast.values,
                'county': county,
                'pollutant': pollutant,
                'scale': label
            }))
        except:
            continue
    return pd.concat(results)



# --- FORECAST EXECUTION ---
daily = df.groupby(['county', 'pollutant', 'datetime'])['value'].mean().reset_index()
daily = daily.rename(columns={'datetime': 'date'})
monthly = df.groupby(['county', 'pollutant', 'month'])['value'].mean().reset_index()
monthly = monthly.rename(columns={'month': 'date'})
yearly = df.groupby(['county', 'pollutant', 'year'])['value'].mean().reset_index()
yearly['date'] = pd.to_datetime(yearly['year'].astype(str) + "-01-01")

daily_forecast = forecast_by_timescale(daily, 'D', 10, 'daily')
monthly_forecast = forecast_by_timescale(monthly, 'MS', 10, 'monthly')
yearly_forecast = forecast_by_timescale(yearly, 'YS', 10, 'yearly')

forecast_df = pd.concat([daily_forecast, monthly_forecast, yearly_forecast])
forecast_df.to_csv(PROJECT_ROOT/"data"/"processed"/"SJV_AQI_Predictions_AllScales.csv", index=False)


