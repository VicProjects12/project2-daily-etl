
import os
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found. Check your .env file.")


def load() -> None:

    # Read the clean CSV
    csv_path = pathlib.Path("data/clean/weather_today.csv")
    df = pd.read_csv(csv_path)

    # Create a connection to PostgreSQL
    engine = create_engine(DATABASE_URL)

    # Insert records into PostgreSQL
    with engine.begin() as connection:

        for _, row in df.iterrows():

            # Convert the date into a Python date object
            date_value = pd.to_datetime(row["date_key"]).date()

            # Insert the date into the date dimension first
            connection.execute(
                text("""
                    INSERT INTO dim_date
                    (date_key, year, month, day, weekday)
                    VALUES (:date_key, :year, :month, :day, :weekday)
                    ON CONFLICT (date_key) DO NOTHING
                """),
                {
                    "date_key": date_value,
                    "year": date_value.year,
                    "month": date_value.month,
                    "day": date_value.day,
                    "weekday": date_value.strftime("%A"),
                },
            )

            # Insert or update the weather record
            connection.execute(
                text("""
                    INSERT INTO fact_weather
                    (city, date_key, temp_c)
                    VALUES (:city, :date_key, :temp_c)
                    ON CONFLICT (city, date_key)
                    DO UPDATE SET
                        temp_c = EXCLUDED.temp_c
                """),
                {
                    "city": row["city"],
                    "date_key": date_value,
                    "temp_c": row["temp_c"],
                },
            )

    print(f"Successfully loaded {len(df)} rows into PostgreSQL.")


if __name__ == "__main__":
    load()
