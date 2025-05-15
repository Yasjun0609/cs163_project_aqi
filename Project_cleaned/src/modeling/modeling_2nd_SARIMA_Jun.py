# modeling_2nd_SARIMA_Jun.py

from config import PROJECT_ROOT
import pandas as pd
import numpy as np
from datetime import datetime, timedelt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import ttest_ind


# ******************************************************************************************

# 2: 2nd SARIMA Attempt_Jun

# ******************************************************************************************

# Load data
merged_df = pd.read_csv(PROJECT_ROOT/"data"/"processed"/"ready_pm25_fresno_with_Date.csv")
merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df = merged_df.sort_values('date')
merged_df.set_index('date', inplace=True)

# Target series
series = merged_df['aqi_smoothed'].dropna()

# Train/test split
split = int(len(series) * 0.8)
train, test = series.iloc[:split], series.iloc[split:]


# Assuming train/test are defined
model = SARIMAX(train,
                order=(1,1,1),
                seasonal_order=(1,1,1,7),
                enforce_stationarity=False,
                enforce_invertibility=False)
results = model.fit(disp=False)

# Forecast
forecast = results.forecast(steps=len(test))

# Metrics
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))
r2 = r2_score(test, forecast)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")
