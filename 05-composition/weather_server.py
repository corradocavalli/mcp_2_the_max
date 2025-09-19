from fastmcp import FastMCP

weather_mcp = FastMCP(name="WeatherServer")


@weather_mcp.tool
def get_forecast(city: str) -> dict:
    """Get weather forecast."""
    return {"city": city, "forecast": "Sunny"}
