namespace AirlineDelay.Api.Models;

public class FlightPredictionRequest
{
    public int Year { get; set; }
    public int Month { get; set; }
    public int DayOfMonth { get; set; }
    public int DayOfWeek { get; set; }
    public string FlightDate { get; set; } = string.Empty;

    public string Carrier { get; set; } = string.Empty;
    public int FlightNumber { get; set; }

    public int OriginAirportId { get; set; }
    public int DestinationAirportId { get; set; }

    public int ScheduledDeparture { get; set; }
    public int ScheduledArrival { get; set; }

    public double ScheduledElapsedTime { get; set; }
    public double Distance { get; set; }
}