from app.fetch_macro import get_macro_indicators

if __name__ == "__main__":
    indicators = get_macro_indicators()
    print("📊 Live Macroeconomic Indicators from FRED API:")
    for k, v in indicators.items():
        print(f"{k}: {v}")
