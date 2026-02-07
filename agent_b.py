"""
Agent B: Task Executor
Performs specific tasks like fetching weather data from APIs.
"""
import httpx
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class AgentB:
    """Agent B performs specific tasks like fetching weather data."""
    
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
        
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task based on the task type.
        
        Args:
            task: Dictionary containing task_type and parameters
            
        Returns:
            Dictionary with task results
        """
        task_type = task.get("task_type")
        
        if task_type == "get_weather":
            return await self.get_weather(task.get("parameters", {}))
        elif task_type == "summarize_weather":
            return await self.summarize_weather(task.get("parameters", {}))
        else:
            return {
                "success": False,
                "error": f"Unknown task type: {task_type}"
            }
    
    async def get_weather(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch current weather data for a given city.
        
        Args:
            parameters: Dictionary containing 'city' parameter
            
        Returns:
            Dictionary with weather data
        """
        city = parameters.get("city", "New York")
        
        if not self.openweather_api_key:
            # Return mock data if no API key is configured
            return {
                "success": True,
                "data": {
                    "city": city,
                    "temperature": 72,
                    "description": "Partly cloudy",
                    "humidity": 65,
                    "wind_speed": 8,
                    "note": "This is mock data. Configure OPENWEATHER_API_KEY for real data."
                }
            }
        
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.openweather_api_key,
                "units": "imperial"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "success": True,
                    "data": {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"]
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch weather data: {str(e)}"
            }
    
    async def summarize_weather(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a summary of weather data.
        
        Args:
            parameters: Dictionary containing 'weather_data'
            
        Returns:
            Dictionary with weather summary
        """
        weather_data = parameters.get("weather_data", {})
        
        if not weather_data:
            return {
                "success": False,
                "error": "No weather data provided for summarization"
            }
        
        # Simple rule-based summary
        city = weather_data.get("city", "Unknown")
        temp = weather_data.get("temperature", 0)
        description = weather_data.get("description", "unknown")
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        
        summary = (
            f"The current weather in {city} is {description} with a temperature of {temp}°F. "
            f"The humidity is {humidity}% and wind speed is {wind_speed} mph."
        )
        
        # Add simple observations
        if temp > 80:
            summary += " It's quite hot outside."
        elif temp < 40:
            summary += " It's quite cold outside."
        else:
            summary += " The temperature is comfortable."
            
        if wind_speed > 15:
            summary += " It's quite windy."
        
        return {
            "success": True,
            "data": {
                "summary": summary
            }
        }
