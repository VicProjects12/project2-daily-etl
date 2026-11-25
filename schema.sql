CREATE TABLE IF NOT EXISTS dim_date(
    date_key DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday TEXT
);

CREATE TABLE IF NOT EXISTS raw_weather (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    loaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fact_weather (
    city Text,
    date_key DATE REFERENCES dim_date(date_key),
    temp_c NUMERIC, humidity NUMERIC, wind_kph NUMERIC,
    PRIMARY KEY (city, date_key)
);