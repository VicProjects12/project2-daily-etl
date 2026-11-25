import datetime
import json
import logging
import pathlib

import requests

logger = logging.getLogger(__name__)

def extract(day: str | None = None) -> pathlib.Path:
    # Use today's date if no date is provided
    day = day or datetime.date.today().isoformat()

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 36.67,
        "longitude": -94.21,
        "hourly": "temperature_2m",
        "forecast_days": 1,
    }

    # send the API request
    response = requests.get(url, params=params, timeout=30)

    # check for HTTP errors
    response.raise_for_status()

    # convert API response into python data
    data = response.json()

    # Create the raw data file path
    path = pathlib.Path(f"data/raw/weather_{day}.json")

    # Create the folder if not exixt
    path.parent.mkdir(parents=True, exist_ok=True)

    # Save the original API response
    path.write_text(json.dumps(data, indent=2), encoding="utf-8" )

    logger.info("Saved raw: %s", path)

    return path


if __name__ == "__main__":
    output_path = extract()
    print(f"Extraction complete: {output_path}")