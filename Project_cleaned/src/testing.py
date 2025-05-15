# modeling.py
from config import PROJECT_ROOT
from modeling import counties, pollutants, ISR_YEAR,df
import pandas as pd
from scipy.stats import ttest_ind

# This file has various testings had in this project.
# Goes in order of; 

# 1. T-testing Hypothesis by Jun with SJV_1980_2025.csv
# 2. 
# 3.
# 4.





# ***************************************************************************************

# 1. T-testing Hypothesis by Jun with SJV_1980_2025.csv

# ****************************************************************************************

# --- T-TEST: Pre vs Post ISR ---
ttest_results = []

for county in counties:
    for pollutant in pollutants:
        data = df[(df['county'] == county) & (df['pollutant'] == pollutant)]
        pre = data[data['year'] < ISR_YEAR]['value'].dropna()
        post = data[data['year'] >= ISR_YEAR]['value'].dropna()
        if len(pre) > 10 and len(post) > 10:
            t_stat, p_val = ttest_ind(pre, post, equal_var=False)
            ttest_results.append({
                'county': county,
                'pollutant': pollutant,
                'pre_mean': pre.mean(),
                'post_mean': post.mean(),
                't_stat': t_stat,
                'p_value': p_val,
                'significant': p_val < 0.05
            })

ttest_df = pd.DataFrame(ttest_results)

# Save results to a CSV file
ttest_df.to_csv(PROJECT_ROOT/"data"/"processed"/"ISR_TTest_Results.csv", index=False)

# Print all results (not just significant ones)
print("T-test completed. All results:\n")
print(ttest_df)  # This will print all results, including non-significant ones

