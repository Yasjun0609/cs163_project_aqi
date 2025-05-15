# 🏁 Project Start: AQI Trend Analysis with ISR Policy Impact

## Project Overview
This project analyzes long-term air quality trends in California’s San Joaquin Valley (SJV), the most polluted region in the state, using data from the U.S. EPA. Our goal is to evaluate the effectiveness of the Indirect Source Review (ISR) Rule 9510, implemented in 2006 to reduce pollution from new developments.

We focus on six major pollutants (PM2.5, PM10, CO, NO2, SO2, Ozone) and apply statistical and machine learning models—including LSTM, SARIMA, and Kriging—to assess trends and policy impact over the past two decades.

👉 [Visit our project website for more details](https://noted-episode-452618-p2.wl.r.appspot.com/)



## How to get started

### 1. Open&Run "1_Major Finding_T-testing hypothesis.ipynb"
Starting with SJV data from 1980 to 2025 that we have gathered during EDA stage, we have successfully deduced that AQI values-
has been significantly increased in all seven counties in San Joaquin Valley which sparked our initial hypothesis of this project.

### 2. Open&Run "2_Preprocessing.ipynb"

This file includes a clear chronologically ordered pipeline of preprocessing. First, we handle the missing values. Second, we detect and smooth the outliers.


### 3. Open&Run "3_Major Finding_SARIMA Model Analyses.ipynb"
This file attempts Seasonal ARIMA modeling and AQI prediction on near future days past the point of last data entry.
Two attempts were made; one without preprocessed data, and one with preprocessed data.

### 4. Open&Run "4_LSTM_Model_Assumption_Testing.ipynb"

This file tests if the PM 2.5 daily data is seasonal, which is what the LSTM model assumes and requires. We found out that the data is multi-seasonal by visualization, and thus, LSTM can successfully be applied.


### 5. Open&Run "5_LSTM_Correlation_Analysis_and_Training_With_Meteorological_Features.ipynb"

This file executes correlation analysis between PM 2.5 and Meteorological data such as wind speed, temperature, humidity, and solar radiation. This file also trains LSTM models with and without these features to determine if it improves the performance or not. We found out that wind speed has somewhat mild non-linear relationship but not strong enough to improve the LSTM model.  


### 6. Open&Run "6_LSTM_Production_Level_Training.ipynb"

This file executes the final step of the LSTM model development pipeline: the training part. Since preprocessing and feature engineering informed us a lot, this file directly executes the final training of the best LSTM model we could train. The trained model was directly saved and then later used in the website. 


### 7. Open&Run "Kriging_Model_Assumption_Testing.ipynb"

This file tests whether the PM 2.5 data has spatial autocorrelation using the Moran's I test. We found out that it successfully passes this assumption.


### 8. Open&Run "8_Kriging_Production_Level_Training.ipynb"

This file goes over exactly how we implemented the Kriging Model for daily PM 2.5 prediction in San Joaquin Valley. We don't train the model in this file, as it trains daily Kriging Models in real time in the website. This file instead shows that this exact strategy was used in the website. 


### 9. Open&Run "9_Major Finding_Streamlit.app for Cross Comparison with Pima County.ipynb"
This notebook features fetching hourly sample data of PM2.5 of both Fresno and Pima county for cross validation/comparison-
to see if a presence of ISR in 2006 was exclusive factor for AQI improvement in Fresno county.
It also features how to deploy dual-map for cross comparison of Fresno county VS Pima cuonty AQI values on local.




# Link to our Website!

[https://noted-episode-452618-p2.wl.r.appspot.com/](https://noted-episode-452618-p2.wl.r.appspot.com/)