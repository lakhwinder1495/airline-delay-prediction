using System.Net.Http.Json;
using AirlineDelay.Api.Models;
using Microsoft.AspNetCore.Mvc;

namespace AirlineDelay.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionsController : ControllerBase
{
    private readonly HttpClient _httpClient;

    public PredictionsController(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    [HttpPost]
    public async Task<ActionResult<FlightPredictionResponse>> Predict(
        FlightPredictionRequest request)
    {
        var pythonRequest = new Dictionary<string, object>
        {
            ["YEAR"] = request.Year,
            ["MONTH"] = request.Month,
            ["DAY_OF_MONTH"] = request.DayOfMonth,
            ["DAY_OF_WEEK"] = request.DayOfWeek,
            ["FL_DATE"] = request.FlightDate,
            ["OP_UNIQUE_CARRIER"] = request.Carrier,
            ["OP_CARRIER_FL_NUM"] = request.FlightNumber,
            ["ORIGIN_AIRPORT_ID"] = request.OriginAirportId,
            ["DEST_AIRPORT_ID"] = request.DestinationAirportId,
            ["CRS_DEP_TIME"] = request.ScheduledDeparture,
            ["CRS_ARR_TIME"] = request.ScheduledArrival,
            ["CRS_ELAPSED_TIME"] = request.ScheduledElapsedTime,
            ["DISTANCE"] = request.Distance
        };

        try
        {
            var response = await _httpClient.PostAsJsonAsync(
                "https://airline-delay-ml-api.onrender.com/predict",
                pythonRequest);

            var responseBody = await response.Content.ReadAsStringAsync();

            if (!response.IsSuccessStatusCode)
            {
                return StatusCode(
                    StatusCodes.Status502BadGateway,
                    $"ML service returned {(int)response.StatusCode}: {responseBody}");
            }

            var result =
                System.Text.Json.JsonSerializer.Deserialize<FlightPredictionResponse>(
                    responseBody,
                    new System.Text.Json.JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

            if (result is null)
            {
                return StatusCode(
                    StatusCodes.Status502BadGateway,
                    $"Invalid response from ML service: {responseBody}");
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            return StatusCode(
                StatusCodes.Status502BadGateway,
                $"Could not connect to ML service: {ex.Message}");
        }
    }
}