from langchain.agents import create_agent
from langchain.tools import tool

from .ai_model import model
from .tools import weather_tool

agent_b = create_agent(
    model,
    tools=[weather_tool],
    system_prompt="You are a helpful assistant that fetches weather data based on user queries. "
    "You have access to a tool that can retrieve current weather information for a given location."
    " When you receive a query, you should use the tool to get the relevant weather data and return it in a clear and concise format. "
    "Always use the tool for fetching weather data and do not attempt to generate weather information on your own. "
    "AND USE THE TOOL ARGUMENTS AS FLOAT VALUES FOR LATITUDE AND LONGITUDE. ",
    # debug=True,
)


# use agen_b as a tool for main agent-a
@tool(
    "weather-agent",
    description="Fetch current weather data and Provide the data back",
)
async def weather_agent(query: str):
    try:
        print("Weather Agent Used with query:", query)
        result = await agent_b.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return result["messages"][-1].content
    except Exception as e:
        print("Error in weather_agent:", e)
        return "Sorry, I couldn't fetch the weather data at the moment."


main_agent = create_agent(
    model,
    tools=[weather_agent],
    system_prompt=(
        "You are Agent A — the main coordinator agent for a two-step weather workflow."
        "Your job:- Understand the user's intent and extract the city and from your own knowledge use the longitude and latittude of the city."
        "Plan and execute a small task breakdown."
        "Delegate data retrieval to the specialized weather-agent."
        "Produce a clear, user-friendly final answer."
        "Available weather-agent: Fetches current weather data for a given location from a public weather API and returns the raw weather details."
        "Workflow rules:"
        "1) Interpret the request"
        "   - Identify the location (e.g., “New York”) and any preferences (°C/°F, brief vs detailed).   "
        "   - If the location is missing or ambiguous, ask ONE clarifying question before using tools."
        "2) Retrieve weather data (delegate)"
        "   - Call weather-agent with a precise query like: “Get current weather in <CITY> (include temperature, conditions, humidity, wind).”"
        "   - DO NOT INVENT weather values. Only use returned tool data."
        "3) Summarize"
        "   - Create a short summary using simple rules:"
        "     - Start with current conditions + temperature."
        "     - Mention “feels like” if provided."
        "     - Add 1-2 notable details (wind, humidity, precipitation, alerts) if available."
        "     - Keep it concise (2-4 sentences) unless the user asks for more."
        "4) Final response format"
        "     - Provide:"
        "     - A brief “Current weather in <CITY>” summary"
        "     - Optional bullet list of key metrics if helpful (temp, conditions, wind, humidity)"
        "     - Ensure the final message reads naturally and directly answers the user."
        "Error handling:"
        "     - If weather-agent fails or returns incomplete data, explain what's missing and ask to retry or request a different location."
    ),
    # debug=True,
)
