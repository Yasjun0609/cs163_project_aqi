# visualize.py
from config import PROJECT_ROOT
from testing import ttest_df
from modeling import forecast_df, train ,test,forecast
import matplotlib.pyplot as plt
import seaborn as sns

# This file plots and creates various visuals that we had in this project.
# Goes in order of; 

# 1. SARIMA_1st attempt by Jun
# 2. SARIMA_2nd attempt by Jun
# 3. T-testing hypothesis by Jun
# 4.









# ******************************************************************************************

# 1: 1st SARIMA Attempt_Jun

# ******************************************************************************************

# --- PLOT: Per pollutant per timescale ---
for scale in ['daily', 'monthly', 'yearly']:
    scale_df = forecast_df[forecast_df['scale'] == scale]
    for pollutant in scale_df['pollutant'].unique():
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=scale_df[scale_df['pollutant'] == pollutant], x='date', y='predicted_value', hue='county', marker='o')
        plt.title(f"Forecast for {pollutant} ({scale.capitalize()})")
        plt.xticks(rotation=45)
        plt.ylabel("Predicted Value (µg/m³)")
        plt.xlabel("Date")
        plt.tight_layout()
        plt.show()

# --- PLOT: Combined plot per scale, averaged across counties ---
for scale in ['daily', 'monthly', 'yearly']:
    combined = (
        forecast_df[forecast_df['scale'] == scale]
        .groupby(['date', 'pollutant'])['predicted_value']
        .mean()
        .reset_index()
    )
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=combined, x='date', y='predicted_value', hue='pollutant', marker='o')
    plt.title(f"Average Forecast per Pollutant ({scale.capitalize()})")
    plt.xticks(rotation=45)
    plt.ylabel("Average Predicted Value (µg/m³)")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.show()



# ******************************************************************************************

# 2: 2nd SARIMA Attempt_Jun

# ******************************************************************************************

# Plot
plt.figure(figsize=(14,6))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Test', color='orange')
plt.plot(test.index, forecast, label='Forecast', color='green')
plt.title('SARIMA Forecast vs Actual AQI')
plt.xlabel('Date')
plt.ylabel('AQI (Smoothed)')
plt.legend()
plt.grid(True)
plt.show()




# ******************************************************************************************

# 3: T-Testing with Hypothesis by Jun

# ******************************************************************************************

ttest_df

# Filter the ttest_df to only include PM2.5 rows
df_pm25_ttest = ttest_df[ttest_df['pollutant'] == 'PM10 Total 0-10um STP']

# Calculate the percentage change and direction for the table
df_pm25_ttest['Change'] = ((df_pm25_ttest['post_mean'] - df_pm25_ttest['pre_mean']) / df_pm25_ttest['pre_mean']) * 100
df_pm25_ttest['Change'] = df_pm25_ttest['Change'].round(1).astype(str) + '%'

# Round Pre-ISR and Post-ISR averages to 2 decimal places
df_pm25_ttest[['pre_mean', 'post_mean']] = df_pm25_ttest[['pre_mean', 'post_mean']].round(2)

# Add direction symbols based on the change value
df_pm25_ttest['Direction'] = df_pm25_ttest['Change'].apply(lambda x: '↓' if '-' in x else '↑')

# Create the final table with selected columns
df_pm25_ttest_table = df_pm25_ttest[['county', 'pollutant', 'pre_mean', 'post_mean', 'Change', 'Direction']]

# Display the table
df_pm25_ttest_table

# Create a figure with subplots for each pollutant
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Barplot for PM10
pm10_data = ttest_df[ttest_df['pollutant'].str.contains("PM10")]
axes[0].bar(pm10_data['county'], pm10_data['pre_mean'], width=0.4, label='Pre-ISR', align='center', color='darkgreen')
axes[0].bar(pm10_data['county'], pm10_data['post_mean'], width=0.4, label='Post-ISR', align='edge', color='lightgreen')
axes[0].set_title('PM10 - Pre vs Post ISR')
axes[0].set_xlabel('County')
axes[0].set_ylabel('AQI')
axes[0].legend()

# Barplot for PM2.5
pm25_data = ttest_df[ttest_df['pollutant'].str.contains("PM2.5")]
axes[1].bar(pm25_data['county'], pm25_data['pre_mean'], width=0.4, label='Pre-ISR', align='center', color='darkgreen')
axes[1].bar(pm25_data['county'], pm25_data['post_mean'], width=0.4, label='Post-ISR', align='edge', color='lightgreen')
axes[1].set_title('PM2.5 - Pre vs Post ISR')
axes[1].set_xlabel('County')
axes[1].set_ylabel('AQI')
axes[1].legend()

# Adjust layout and show the plots
plt.tight_layout()
plt.show()



# ******************************************************************************************

# 4: 

# ******************************************************************************************