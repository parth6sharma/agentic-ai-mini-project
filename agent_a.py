"""
Agent A: Task Planner
Breaks down natural language requests into smaller tasks and orchestrates execution.
"""
import re
from typing import Dict, Any, List
from agent_b import AgentB


class AgentA:
    """Agent A analyzes requests and breaks them into tasks."""
    
    def __init__(self):
        self.agent_b = AgentB()
        
    async def process_request(self, user_request: str) -> Dict[str, Any]:
        """
        Process a natural language request by breaking it into tasks
        and coordinating their execution.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Dictionary with final response
        """
        # Step 1: Understand and break down the request
        tasks = self.break_down_request(user_request)
        
        if not tasks:
            return {
                "success": False,
                "error": "Could not understand the request",
                "response": "I'm sorry, I couldn't understand your request. Please try asking about weather in a city."
            }
        
        # Step 2: Execute tasks through Agent B
        results = []
        for task in tasks:
            result = await self.agent_b.execute_task(task)
            results.append(result)
        
        # Step 3: Compile final response
        final_response = self.compile_response(tasks, results)
        
        return final_response
    
    def break_down_request(self, request: str) -> List[Dict[str, Any]]:
        """
        Analyze the request and break it into smaller tasks.
        
        Args:
            request: Natural language request
            
        Returns:
            List of task dictionaries
        """
        request_lower = request.lower()
        tasks = []
        
        # Check if this is a weather-related request
        if "weather" in request_lower:
            # Extract city name
            city = self.extract_city(request)
            
            # Task 1: Get weather data
            tasks.append({
                "task_type": "get_weather",
                "parameters": {
                    "city": city
                }
            })
            
            # Task 2: Summarize if requested
            if any(word in request_lower for word in ["summary", "summarize", "tell me", "give me"]):
                tasks.append({
                    "task_type": "summarize_weather",
                    "parameters": {
                        "weather_data": None  # Will be filled with result from Task 1
                    }
                })
        
        return tasks
    
    def extract_city(self, request: str) -> str:
        """
        Extract city name from request.
        
        Args:
            request: Natural language request
            
        Returns:
            City name
        """
        # Common patterns for city extraction
        patterns = [
            r"weather in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"weather for ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"weather at ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request)
            if match:
                return match.group(1)
        
        # Default to New York if no city found
        return "New York"
    
    def compile_response(self, tasks: List[Dict[str, Any]], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compile the final response from task results.
        
        Args:
            tasks: List of tasks that were executed
            results: List of results from task execution
            
        Returns:
            Final response dictionary
        """
        # Check if any task failed
        for result in results:
            if not result.get("success", False):
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "response": f"Sorry, I encountered an error: {result.get('error', 'Unknown error')}"
                }
        
        # Build final response based on tasks
        if len(results) == 1:
            # Only weather data requested
            weather_data = results[0].get("data", {})
            response = (
                f"Weather in {weather_data.get('city', 'Unknown')}: "
                f"{weather_data.get('description', 'N/A')}, "
                f"Temperature: {weather_data.get('temperature', 'N/A')}°F, "
                f"Humidity: {weather_data.get('humidity', 'N/A')}%, "
                f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} mph"
            )
            if "note" in weather_data:
                response += f"\n\nNote: {weather_data['note']}"
        elif len(results) >= 2:
            # Weather data and summary
            # Update second task parameters with first task results
            if tasks[1]["task_type"] == "summarize_weather" and tasks[1]["parameters"]["weather_data"] is None:
                tasks[1]["parameters"]["weather_data"] = results[0].get("data", {})
                # Re-execute summary task with actual data
                import asyncio
                result = asyncio.get_event_loop().run_until_complete(
                    self.agent_b.execute_task(tasks[1])
                )
                results[1] = result
            
            summary_data = results[1].get("data", {})
            response = summary_data.get("summary", "No summary available")
        else:
            response = "Request processed successfully"
        
        return {
            "success": True,
            "tasks_executed": len(tasks),
            "response": response
        }
