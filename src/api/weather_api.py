import requests
import pandas as pd

API_KEY = "57833017a7d3402732c660b6d9430246"

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# =====================================================
# CURRENT WEATHER
# =====================================================

def get_live_weather(city):

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"
    }

    response = requests.get(
        CURRENT_URL,
        params=params
    )

    data = response.json()

    if "main" not in data:

        fallback_data = {

            "City": city,

            "Temperature": 30,

            "Humidity": 70,

            "WindSpeed": 10,

            "Pressure": 1000,

            "RainProbability": 50,

            "Condition": "Unavailable"

        }

        return pd.DataFrame([fallback_data])

    weather_data = {

        "City": city,

        "Temperature": data["main"]["temp"],

        "Humidity": data["main"]["humidity"],

        "WindSpeed": data["wind"]["speed"],

        "Pressure": data["main"]["pressure"],

        "RainProbability": 50,

        "Condition": data["weather"][0]["main"]

    }

    return pd.DataFrame([weather_data])

# =====================================================
# WEATHER FORECAST
# =====================================================

def get_forecast(city):

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"
    }

    response = requests.get(
        FORECAST_URL,
        params=params
    )

    data = response.json()

    forecast_list = []

    if "list" not in data:

        return pd.DataFrame()

    for item in data["list"][:10]:

        forecast_data = {

            "Datetime": item["dt_txt"],

            "Temperature": item["main"]["temp"],

            "Humidity": item["main"]["humidity"],

            "Condition": item["weather"][0]["main"]

        }

        forecast_list.append(forecast_data)

    return pd.DataFrame(forecast_list)