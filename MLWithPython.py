import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import warnings

# Suppress warnings from statsmodels (optional)
warnings.filterwarnings("ignore")

# -----------------------------
# Load your dataset
# -----------------------------
# Replace this with your data-loading method.
# For example, if your dataset is in a CSV file, use:
# df = pd.read_csv("delhi_aqi.csv")
# Here we assume `df` is already loaded with a structure similar to `delhi_aqi`
df = pd.read_csv("delhi_aqi.csv")

# -----------------------------
# Calculate AQI function
# -----------------------------
def calculate_aqi(co, no, no2, o3, so2, pm2_5, pm10, nh3):
    """
    Calculate the AQI based on given pollutant values.
    """
    aqi = (0.25 * co + 0.1 * no + 0.2 * no2 + 0.1 * o3 +
           0.15 * so2 + 0.1 * pm2_5 + 0.1 * pm10 + 0.1 * nh3) / 8
    return aqi

# -----------------------------
# Data Preparation
# -----------------------------
# Convert the 'date' column to datetime with UTC timezone and sort the DataFrame
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M", utc=True)
df = df.sort_values('date').reset_index(drop=True)

# Add the AQI column to the dataset
df['AQI'] = df.apply(lambda row: calculate_aqi(
    row['co'], row['no'], row['no2'], row['o3'],
    row['so2'], row['pm2_5'], row['pm10'], row['nh3']
), axis=1)

# -----------------------------
# Fit ARIMA Models
# -----------------------------
# Define the ARIMA orders for each pollutant as in the R code
model_orders = {
    'co': (2, 1, 3),
    'no': (2, 1, 3),
    'no2': (3, 1, 3),
    'o3': (2, 1, 5),
    'so2': (2, 1, 5),
    'pm2_5': (2, 1, 2),
    'pm10': (2, 1, 2),
    'nh3': (2, 1, 6)
}

# Fit an ARIMA model for each pollutant and store the models in a dictionary
models = {}
for pollutant, order in model_orders.items():
    series = df[pollutant]
    model = ARIMA(series, order=order)
    fitted_model = model.fit()
    models[pollutant] = fitted_model

# -----------------------------
# Prediction Function
# -----------------------------
def forecast_or_return_data(input_date_time, steps=24):
    """
    Given an input date_time string in the format "YYYY-MM-DD HH:MM",
    returns the corresponding row from the dataset if it exists.
    If the input date is after the last date in the dataset, forecast the pollutant values
    using ARIMA models and calculate the AQI.
    """
    try:
        # Parse the input date-time string
        input_dt = datetime.strptime(input_date_time, "%Y-%m-%d %H:%M")
        # Attach UTC timezone for comparison (using pandas UTC info)
        input_dt = pd.Timestamp(input_dt, tz='UTC')
    except ValueError:
        return None

    # Check if the input date exists in the dataset
    matching = df[df['date'] == input_dt]
    if not matching.empty:
        # Return the matching row as a dictionary
        return matching.iloc[0].to_dict()
    elif input_dt > df['date'].max():
        # Forecast new values if the input date is in the future
        forecast_results = {}
        for pollutant, model in models.items():
            # Forecast for the given number of steps and take the first forecasted value
            forecast_val = model.forecast(steps=steps)[0]
            forecast_results[pollutant] = forecast_val

        # Calculate AQI using the forecasted pollutant values
        forecast_results['AQI'] = calculate_aqi(
            forecast_results.get('co', np.nan),
            forecast_results.get('no', np.nan),
            forecast_results.get('no2', np.nan),
            forecast_results.get('o3', np.nan),
            forecast_results.get('so2', np.nan),
            forecast_results.get('pm2_5', np.nan),
            forecast_results.get('pm10', np.nan),
            forecast_results.get('nh3', np.nan)
        )
        return forecast_results
    else:
        # If the input date is before the available data, return None
        return None

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # Provide an example input date-time string
    example_input = "2025-01-01 12:00"
    result = forecast_or_return_data(example_input)
    if result:
        print("Forecast/Result:")
        print(result)
    else:
        print("Date not found in dataset.")
