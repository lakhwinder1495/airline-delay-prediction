import pandas as pd


DATA_PATH = "data/flights_2025/flights_2025.csv"


def load_and_prepare_data(path=DATA_PATH):
    print("Loading flight data...")

    df = pd.read_csv(path)

    print(f"Original rows: {len(df):,}")

    # ---------------------------------------------------------
    # Remove cancelled and diverted flights.
    # These flights do not represent normal completed flights.
    # ---------------------------------------------------------
    df = df[
        (df["CANCELLED"] == 0) &
        (df["DIVERTED"] == 0)
    ].copy()

    # ---------------------------------------------------------
    # ARR_DEL15 is our target:
    # 1 = arrival delay >= 15 minutes
    # 0 = arrival delay < 15 minutes
    #
    # Remove rows where the target is missing.
    # ---------------------------------------------------------
    df = df.dropna(subset=["ARR_DEL15"])

    # Convert target to integer.
    df["ARR_DEL15"] = df["ARR_DEL15"].astype(int)

    # ---------------------------------------------------------
    # Convert scheduled departure time (HHMM) into useful
    # numerical features.
    #
    # Example:
    # 700  -> 07:00
    # 2215 -> 22:15
    # ---------------------------------------------------------
    df["DEP_HOUR"] = (df["CRS_DEP_TIME"] // 100).astype(int)
    df["DEP_MINUTE"] = (df["CRS_DEP_TIME"] % 100).astype(int)

    # Scheduled arrival hour.
    df["ARR_HOUR"] = (df["CRS_ARR_TIME"] // 100).astype(int)

    # ---------------------------------------------------------
    # Convert flight date into date-based features.
    # ---------------------------------------------------------
    df["FL_DATE"] = pd.to_datetime(
        df["FL_DATE"],
        format="%m/%d/%Y %I:%M:%S %p"
    )

    df["DAY_OF_YEAR"] = df["FL_DATE"].dt.dayofyear

    # ---------------------------------------------------------
    # Select model features.
    #
    # We intentionally do NOT use ARR_DEL15 as a feature.
    # CANCELLED and DIVERTED have already been used for filtering.
    # ---------------------------------------------------------
    feature_columns = [
        "YEAR",
        "MONTH",
        "DAY_OF_MONTH",
        "DAY_OF_WEEK",
        "OP_UNIQUE_CARRIER",
        "OP_CARRIER_FL_NUM",
        "ORIGIN_AIRPORT_ID",
        "DEST_AIRPORT_ID",
        "CRS_DEP_TIME",
        "CRS_ARR_TIME",
        "CRS_ELAPSED_TIME",
        "DISTANCE",
        "DEP_HOUR",
        "DEP_MINUTE",
        "ARR_HOUR",
        "DAY_OF_YEAR",
    ]

    X = df[feature_columns].copy()
    y = df["ARR_DEL15"].copy()

    print(f"Rows after cleaning: {len(df):,}")
    print(f"Features: {len(feature_columns)}")

    print("\nTarget distribution:")
    print(y.value_counts())
    print("\nTarget percentage:")
    print(y.value_counts(normalize=True).mul(100).round(2))

    return X, y


if __name__ == "__main__":
    X, y = load_and_prepare_data()

    print("\nFeature sample:")
    print(X.head())

    print("\nTarget sample:")
    print(y.head())