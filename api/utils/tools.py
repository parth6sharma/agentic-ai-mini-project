import aiohttp
from langchain.tools import tool


@tool(
    "weather",
    description="Get the current weather for a location by coordinates (latitude and longitude).",
)
async def weather_tool(longitude: float, latitude: float) -> str:
    print("Weather Tool Used")
    print("Fetching weather data for coordinates:", longitude, latitude)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
            ) as response:
                print("Status:", response.status)
                html = await response.text()

        return html
    except Exception as e:
        print("Error fetching weather data:", e)
        return "Sorry, I couldn't fetch the weather data at the moment."
