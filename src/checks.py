
import pandas as pd


def run_checks(df: pd.DataFrame) -> None:

    errors = []

    # Check 1: Dataset must not be empty
    if len(df) == 0:
        errors.append("No rows")

    # Check 2: Temperatures must not be missing
    if df["temp_c"].isna().any():
        errors.append("Missing temperatures")

    # Check 3: City and date combinations must be unique
    if df.duplicated(subset=["city", "date_key"]).any():
        errors.append("Duplicate city + date")

    # Check 4: Temperatures must be within a reasonable range
    if ((df["temp_c"] < -60) | (df["temp_c"] > 60)).any():
        errors.append("Temperature out of range")

    # Report any validation failures
    if errors:
        raise ValueError(f"Data quality FAILED: {errors}")

    print(f"All checks passed: {len(df)} rows")
