# IMPORTS AT THE TOP

import os
import json
from pgeocode import Nominatim
import requests
from dotenv import load_dotenv
from IPython.display import Image, display
import pandas as pd

# ENVIRON VARIABLES & CONSTANTS
load_dotenv() 
DEGREE_SIGN = u"\n{DEGREE SIGN}"

# FUNCTIONS
def query_postal_code(zip_code, country_code="US"):
    nomi = Nominatim(country_code)
    return nomi.query_postal_code(zip_code)

def get_forecast_url(latitude, longitude):
    request_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        parsed_response = json.loads(response.text)
        return parsed_response["properties"]["forecast"]
    except requests.RequestException as e:
        print(f"Error fetching forecast URL: {e}")
        return None

def display_forecast(zip_code):
    geo = query_postal_code(zip_code)
    if geo.empty or pd.isna(geo["latitude"]) or pd.isna(geo["longitude"]):
        print("Geolocation data not found.")
        return[]

    forecast_url = get_forecast_url(geo["latitude"], geo["longitude"])
    if not forecast_url:
        print("Forecast URL not found.")
        return[]

    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        parsed_forecast_response = json.loads(forecast_response.text)

        periods = parsed_forecast_response["properties"]["periods"]
        daytime_periods = [period for period in periods if period["isDaytime"]]

        for period in daytime_periods:
            print("----------------")
            print(period["name"], period["startTime"][0:10])
            print(period["shortForecast"], f"{period['temperature']} {DEGREE_SIGN}{period['temperatureUnit']}")
            display(Image(url=period["icon"]))
    except requests.RequestException as e:
        print(f"Error fetching forecast data: {e}")

if __name__ == "__main__":

# WORKING CODE
    zip_code = input("Please input a zip code (e.g. 06510): ") or "O6510"
    display_forecast(zip_code)

