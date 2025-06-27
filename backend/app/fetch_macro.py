import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

FRED_SERIES = {
    "interest_rate": "FEDFUNDS",
    "unemployment_rate": "UNRATE",
    "gdp_current": "GDPC1"  # Real GDP (quarterly, seasonally adjusted annual rate)
}

def get_latest_fred_value(series_id):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
        f"&observation_start={start_date.strftime('%Y-%m-%d')}"
        f"&observation_end={end_date.strftime('%Y-%m-%d')}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"FRED API error for {series_id}: {response.status_code}")

    data = response.json().get("observations", [])
    values = [float(obs["value"]) for obs in data if obs["value"] != "."]

    if not values:
        raise Exception(f"No valid data for {series_id}")

    return values[-1]

def get_yearly_inflation():
    end = datetime.today()
    start = end - timedelta(days=365)

    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id=CPIAUCSL"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
        f"&observation_start={start.strftime('%Y-%m-%d')}"
        f"&observation_end={end.strftime('%Y-%m-%d')}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch CPI data")

    data = response.json().get("observations", [])
    values = [float(obs["value"]) for obs in data if obs["value"] != "."]

    if len(values) < 2:
        raise Exception("Insufficient CPI data for inflation calculation")

    old = values[0]
    new = values[-1]
    return max(((new - old) / old) * 100, 1.0)  # minimum of 1.0

def get_gdp_growth_rate():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=540)  # ~18 months to get 3 quarters

    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={FRED_SERIES['gdp_current']}"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
        f"&observation_start={start_date.strftime('%Y-%m-%d')}"
        f"&observation_end={end_date.strftime('%Y-%m-%d')}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch GDP data")

    data = response.json().get("observations", [])
    values = [float(obs["value"]) for obs in data if obs["value"] != "."]

    if len(values) < 2:
        raise Exception("Insufficient GDP data for growth calculation")

    old = values[-2]
    new = values[-1]
    growth = ((new - old) / old) * 100
    return max(growth, 1.0)  # enforce minimum of 1.0 to match model training range

def get_macro_indicators():
    try:
        return {
            "interest_rate": max(get_latest_fred_value(FRED_SERIES["interest_rate"]), 1.0),
            "employment_rate": max(100 - get_latest_fred_value(FRED_SERIES["unemployment_rate"]), 1.0),
            "inflation_rate": round(get_yearly_inflation(), 2),
            "gdp_growth_rate": round(get_gdp_growth_rate(), 2)
        }
    except Exception as e:
        print("[WARN] Macro fetch failed:", e)
        return {
            "interest_rate": 5.0,
            "employment_rate": 95.0,
            "inflation_rate": 3.0,
            "gdp_growth_rate": 2.0
        }
