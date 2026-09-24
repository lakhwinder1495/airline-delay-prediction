var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddHttpClient();

builder.Services.AddCors(options =>
{
    options.AddPolicy("ReactApp", policy =>
    {
        policy
            .WithOrigins(
                "http://localhost:5173"
            )
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors("ReactApp");

app.UseAuthorization();

app.MapGet("/", () => Results.Ok(new
{
    service = "Airline Delay Prediction API",
    status = "running",
    version = "1.0"
}));

app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy"
}));

app.MapControllers();

app.Run();