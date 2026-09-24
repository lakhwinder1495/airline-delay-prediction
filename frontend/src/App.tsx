import { useState } from "react";
import axios from "axios";
import "./App.css";
import { airlines } from "./flightData";
import { airports } from "./airportData";

interface PredictionResponse {
  willBeDelayed: boolean;
  prediction: string;
  delayProbability: number;
  delayProbabilityPercent: number;
}

function App() {
  const [form, setForm] = useState({
    year: 2025,
    month: 12,
    dayOfMonth: 15,
    dayOfWeek: 1,
    flightDate: "2025-12-15",
    departureTime: "07:00",
    arrivalTime: "10:35",
    carrier: "AA",
    flightNumber: 100,
    originAirportId: 12478,
    destinationAirportId: 12892,
    scheduledDeparture: 700,
    scheduledArrival: 1035,
    scheduledElapsedTime: 395,
    distance: 2475,
  });

  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    setForm((previous) => ({
      ...previous,
      [name]: [
        "year",
        "month",
        "dayOfMonth",
        "dayOfWeek",
        "flightNumber",
        "originAirportId",
        "destinationAirportId",
        "scheduledDeparture",
        "scheduledArrival",
        "scheduledElapsedTime",
        "distance",
      ].includes(name)
        ? Number(value)
        : value,
    }));
  };

  const timeToNumber = (time: string) => {
    const [hours, minutes] = time.split(":").map(Number);

    return hours * 100 + minutes;
  };

  const getDayOfWeek = (date: string) => {
    const day = new Date(`${date}T00:00:00`).getDay();

    return day === 0 ? 7 : day;
  };

  const predictDelay = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {

      const selectedDate = new Date(`${form.flightDate}T00:00:00`);

      const request = {
        ...form,

        year: selectedDate.getFullYear(),
        month: selectedDate.getMonth() + 1,
        dayOfMonth: selectedDate.getDate(),
        dayOfWeek: getDayOfWeek(form.flightDate),

        scheduledDeparture: timeToNumber(form.departureTime),
        scheduledArrival: timeToNumber(form.arrivalTime),

        flightDate: `${selectedDate.toLocaleDateString("en-US")} 12:00:00 AM`,
      };

      const response = await axios.post(
        "http://localhost:5051/api/predictions",
        request
      );

      const data = response.data;

      const normalizedResult: PredictionResponse = {
        willBeDelayed:
          data.willBeDelayed ?? data.will_be_delayed,

        prediction:
          data.prediction,

        delayProbability:
          data.delayProbability ?? data.delay_probability,

        delayProbabilityPercent:
          data.delayProbabilityPercent ??
          data.delay_probability_percent,
      };

      setResult(normalizedResult);
    } catch (err: any) {
      console.error("Prediction error:", err);

      if (err.response) {
        setError(
          `API Error ${err.response.status}: ${typeof err.response.data === "string"
            ? err.response.data
            : JSON.stringify(err.response.data)
          }`
        );
      } else if (err.request) {
        setError(
          "Could not connect to ASP.NET API at http://localhost:5051."
        );
      } else {
        setError(`Request error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>✈️ Airline Delay Predictor</h1>
          <p>
            Predict the probability of an airline arrival delay using
            machine learning.
          </p>
        </header>

        <div className="card">
          <h2>Flight Details</h2>

          <div className="form-grid">
            <div className="field">
              <label>Flight Date</label>
              <input
                name="flightDate"
                type="date"
                value={form.flightDate}
                onChange={handleChange}
              />
            </div>

            <div className="field">
              <label>Departure Time</label>
              <input
                name="departureTime"
                type="time"
                value={form.departureTime}
                onChange={handleChange}
              />
            </div>

            <div className="field">
              <label>Arrival Time</label>
              <input
                name="arrivalTime"
                type="time"
                value={form.arrivalTime}
                onChange={handleChange}
              />
            </div>
            <div className="field">
              <label>Airline</label>
              <select
                name="carrier"
                value={form.carrier}
                onChange={handleChange}
              >
                {airlines.map((airline) => (
                  <option key={airline.code} value={airline.code}>
                    {airline.name} ({airline.code})
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label>Flight Number</label>
              <input
                name="flightNumber"
                type="number"
                value={form.flightNumber}
                onChange={handleChange}
              />
            </div>

            <div className="field">
              <label>Origin Airport ID</label>
              <select
                name="originAirportId"
                value={form.originAirportId}
                onChange={handleChange}
              >
                {airports.map((airport) => (
                  <option key={airport.id} value={airport.id}>
                    {airport.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label>Destination Airport ID</label>
              <select
                name="destinationAirportId"
                value={form.destinationAirportId}
                onChange={handleChange}
              >
                {airports.map((airport) => (
                  <option key={airport.id} value={airport.id}>
                    {airport.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Elapsed Time (minutes)</label>
              <input
                name="scheduledElapsedTime"
                type="number"
                value={form.scheduledElapsedTime}
                onChange={handleChange}
              />
            </div>

            <div className="field">
              <label>Distance (miles)</label>
              <input
                name="distance"
                type="number"
                value={form.distance}
                onChange={handleChange}
              />
            </div>
          </div>

          <button
            className="predict-button"
            onClick={predictDelay}
            disabled={loading}
          >
            {loading ? "Predicting..." : "Predict Flight Delay"}
          </button>

          {error && <div className="error">{error}</div>}

          {result && (
            <div className="result">
              <h2>Prediction Result</h2>

              <div className="prediction">
                {result.willBeDelayed
                  ? "⚠️ DELAY EXPECTED"
                  : "✅ ON TIME"}
              </div>

              <div className="probability">
                <span>Delay Probability</span>
                <strong>
                  {Number(result.delayProbabilityPercent).toFixed(2)}%
                </strong>
              </div>

              <div className="result-details">
                <p>
                  <strong>Prediction:</strong>{" "}
                  {result.prediction}
                </p>

                <p>
                  <strong>Probability:</strong>{" "}
                  {Number(result.delayProbability).toFixed(4)}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;