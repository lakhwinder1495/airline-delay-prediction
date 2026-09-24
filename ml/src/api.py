import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


MODEL_PATH = "models/airline_delay_model.joblib"

app = FastAPI(
    title="Airline Delay Prediction API",
    version="1.0.0",
)

model = joblib.load(MODEL_PATH)


class FlightRequest(BaseModel):
    YEAR: int
    MONTH: int
    DAY_OF_MONTH: int
    DAY_OF_WEEK: int
    FL_DATE: str
    OP_UNIQUE_CARRIER: str
    OP_CARRIER_FL_NUM: int
    ORIGIN_AIRPORT_ID: int
    DEST_AIRPORT_ID: int
    CRS_DEP_TIME: int
    CRS_ARR_TIME: int
    CRS_ELAPSED_TIME: float
    DISTANCE: float


@app.get("/")
def root():
    return {
        "service": "Airline Delay Prediction API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/predict")
def predict(request: FlightRequest):

    flight = request.model_dump()

    df = pd.DataFrame([flight])

    # Scheduled departure time → hour/minute
    df["DEP_HOUR"] = (df["CRS_DEP_TIME"] // 100).astype(int)
    df["DEP_MINUTE"] = (df["CRS_DEP_TIME"] % 100).astype(int)

    # Scheduled arrival time → hour
    df["ARR_HOUR"] = (df["CRS_ARR_TIME"] // 100).astype(int)

    # Flight date → day of year
    df["FL_DATE"] = pd.to_datetime(
        df["FL_DATE"],
        format="%m/%d/%Y %I:%M:%S %p",
    )

    df["DAY_OF_YEAR"] = df["FL_DATE"].dt.dayofyear

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    return {
        "will_be_delayed": bool(prediction),
        "prediction": "DELAYED" if prediction == 1 else "ON_TIME",
        "delay_probability": round(probability, 4),
        "delay_probability_percent": round(probability * 100, 2),
    }