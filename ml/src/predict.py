import joblib
import pandas as pd


MODEL_PATH = "models/airline_delay_model.joblib"


def predict_flight(flight):
    model = joblib.load(MODEL_PATH)

    df = pd.DataFrame([flight])

    # Convert scheduled departure time into features.
    df["DEP_HOUR"] = (df["CRS_DEP_TIME"] // 100).astype(int)
    df["DEP_MINUTE"] = (df["CRS_DEP_TIME"] % 100).astype(int)

    # Convert scheduled arrival time into hour.
    df["ARR_HOUR"] = (df["CRS_ARR_TIME"] // 100).astype(int)

    # Convert flight date into day of year.
    df["FL_DATE"] = pd.to_datetime(
        df["FL_DATE"],
        format="%m/%d/%Y %I:%M:%S %p"
    )

    df["DAY_OF_YEAR"] = df["FL_DATE"].dt.dayofyear

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "will_be_delayed": bool(prediction),
        "delay_probability": round(float(probability), 4),
    }


if __name__ == "__main__":

    flight = {
        "YEAR": 2025,
        "MONTH": 12,
        "DAY_OF_MONTH": 15,
        "DAY_OF_WEEK": 1,
        "FL_DATE": "12/15/2025 12:00:00 AM",
        "OP_UNIQUE_CARRIER": "AA",
        "OP_CARRIER_FL_NUM": 100,
        "ORIGIN_AIRPORT_ID": 12478,
        "DEST_AIRPORT_ID": 12892,
        "CRS_DEP_TIME": 700,
        "CRS_ARR_TIME": 1035,
        "CRS_ELAPSED_TIME": 395,
        "DISTANCE": 2475,
    }

    result = predict_flight(flight)

    print("\nFlight Prediction")
    print("=================")
    print("Delayed:", "YES" if result["will_be_delayed"] else "NO")
    print(
        f"Delay probability: "
        f"{result['delay_probability'] * 100:.2f}%"
    )