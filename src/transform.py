from src.checks import run_checks
import json
import pathlib

import pandas as pd

def transform(day: str) -> pathlib.Path:

    # Locate the raw Json file
    raw_path = pathlib.Path(f"data/raw/weather_{day}.json")

    # Read the original json
    with raw_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract hourly information
    hourly = data["hourly"]

    # Convert the JSON information into a DataFrame
    df = pd.DataFrame({
        "time": hourly["time"],
        "temp_c": hourly["temperature_2m"],
    })

    # Convert timestamps into datetime values
    df["time"] = pd.to_datetime(df["time"])

    # Remove rows with missing temperatures
    df = df.dropna(subset=["temp_c"])

    # Calculate the daily average temperature
    daily_average = df["temp_c"].mean()

    # Create the final daily weather record
    clean_df = pd.DataFrame([{
        "city": "Bentonville",
        "date_key": df["time"].dt.date.iloc[0],
        "temp_c": round(daily_average, 1),
    }])

    # Create the clean data folder
    output_path = pathlib.Path("data/clean/weather_today.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

     # Validate the transformed data
    run_checks(clean_df)
    
     # Save the transformed data
    clean_df.to_csv(output_path, index=False)

    print(f"Transformation complete: {output_path}")

    return output_path


if __name__ == "__main__":
    transform("2026-11-24")