using System.Text.Json.Serialization;

namespace AirlineDelay.Api.Models;

public class FlightPredictionResponse
{
    [JsonPropertyName("will_be_delayed")]
    public bool WillBeDelayed { get; set; }

    [JsonPropertyName("prediction")]
    public string Prediction { get; set; } = string.Empty;

    [JsonPropertyName("delay_probability")]
    public double DelayProbability { get; set; }

    [JsonPropertyName("delay_probability_percent")]
    public double DelayProbabilityPercent { get; set; }
}