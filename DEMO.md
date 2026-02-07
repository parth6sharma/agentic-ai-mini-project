# Multi-Agent System Demonstration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                             │
│      "Get weather in New York and give me a summary"            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER                              │
│                    (main.py - Port 8000)                         │
│                                                                  │
│  Endpoints:                                                      │
│  • GET  /         - API information                             │
│  • GET  /health   - Health check                                │
│  • POST /process  - Process requests                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT A (Planner)                           │
│                      agent_a.py                                  │
│                                                                  │
│  Responsibilities:                                               │
│  1. Parse natural language request                              │
│  2. Extract city name from request                              │
│  3. Break down into smaller tasks:                              │
│     • Task 1: Get weather data                                  │
│     • Task 2: Summarize weather (if requested)                  │
│  4. Coordinate task execution                                   │
│  5. Compile final response                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT B (Executor)                            │
│                      agent_b.py                                  │
│                                                                  │
│  Capabilities:                                                   │
│  • execute_task(task) - Main task router                        │
│  • get_weather(city) - Fetch weather from API                   │
│  • summarize_weather(data) - Create weather summary             │
│                                                                  │
│  External Integration:                                           │
│  • OpenWeatherMap API (with fallback to mock data)              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FINAL RESPONSE                              │
│                                                                  │
│  {                                                               │
│    "success": true,                                             │
│    "tasks_executed": 2,                                         │
│    "response": "The current weather in New York is..."          │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Communication Flow

### Example 1: Request with Summary

**Input:**
```
"Get the current weather in New York and give me a short summary."
```

**Agent A Processing:**
1. Identifies "weather" keyword → weather request
2. Extracts "New York" as city name
3. Detects "summary" keyword → needs summarization
4. Creates task list:
   - Task 1: `{"task_type": "get_weather", "parameters": {"city": "New York"}}`
   - Task 2: `{"task_type": "summarize_weather", "parameters": {"weather_data": null}}`

**Agent B Execution:**
1. Receives Task 1 from Agent A
2. Calls OpenWeatherMap API (or returns mock data)
3. Returns weather data: `{"city": "New York", "temperature": 72, ...}`
4. Receives Task 2 from Agent A with weather data
5. Applies rule-based summarization logic
6. Returns summary text

**Agent A Compilation:**
1. Receives results from both tasks
2. Compiles final response using summary from Task 2
3. Returns: "The current weather in New York is Partly cloudy with a temperature of 72°F..."

**Response:**
```json
{
  "success": true,
  "tasks_executed": 2,
  "response": "The current weather in New York is Partly cloudy with a temperature of 72°F. The humidity is 65% and wind speed is 8 mph. The temperature is comfortable."
}
```

### Example 2: Simple Weather Request

**Input:**
```
"What is the weather in Tokyo"
```

**Agent A Processing:**
1. Identifies "weather" keyword
2. Extracts "Tokyo" as city name
3. No summary keyword detected
4. Creates single task:
   - Task 1: `{"task_type": "get_weather", "parameters": {"city": "Tokyo"}}`

**Agent B Execution:**
1. Receives Task 1 from Agent A
2. Fetches weather data for Tokyo
3. Returns raw weather data

**Agent A Compilation:**
1. Receives result from single task
2. Formats basic weather response
3. Returns structured weather data

**Response:**
```json
{
  "success": true,
  "tasks_executed": 1,
  "response": "Weather in Tokyo: Partly cloudy, Temperature: 72°F, Humidity: 65%, Wind Speed: 8 mph"
}
```

## Key Features Demonstrated

### ✅ Agent Communication
- **Programmatic**: Agents communicate via function calls (async/await)
- **Sequential**: Tasks executed in order with data passing between them
- **Coordinated**: Agent A orchestrates, Agent B executes

### ✅ Task Decomposition
Agent A breaks complex requests into:
1. Data fetching tasks (Agent B)
2. Processing tasks (Agent B)
3. Compilation (Agent A)

### ✅ Natural Language Processing
- Pattern matching for intent detection
- City name extraction using regex
- Summary detection via keyword matching

### ✅ External API Integration
- OpenWeatherMap API for real weather data
- Graceful fallback to mock data
- Async HTTP requests with httpx

### ✅ Rule-Based Intelligence
Agent B's summary logic:
- Temperature evaluation (hot/cold/comfortable)
- Wind condition assessment
- Natural language generation

## Testing the System

### Method 1: Using cURL
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"request": "Get weather in London and summarize it"}'
```

### Method 2: Using Python
```python
import requests
response = requests.post(
    "http://localhost:8000/process",
    json={"request": "Get weather in Paris and give me a summary"}
)
print(response.json())
```

### Method 3: Using the Test Script
```bash
python test_api.py
```

### Method 4: Interactive Documentation
Navigate to: `http://localhost:8000/docs`

## Assignment Requirements ✅

| Requirement | Implementation | Status |
|------------|----------------|--------|
| Two agents | Agent A (Planner) + Agent B (Executor) | ✅ |
| Agent A breaks down requests | Natural language parsing → task list | ✅ |
| Agent B performs tasks | Weather fetching, summarization | ✅ |
| Agents communicate | Async function calls with data passing | ✅ |
| Handle end-to-end queries | Complete workflow from request to response | ✅ |
| Python language | FastAPI, Pydantic, httpx | ✅ |
| External API | OpenWeatherMap integration | ✅ |
| Natural language processing | Pattern matching, entity extraction | ✅ |

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation and settings management
- **httpx**: Async HTTP client
- **python-dotenv**: Environment variable management
- **uvicorn**: ASGI server

## Project Structure

```
agentic-ai-mini-project/
├── main.py              # FastAPI server and endpoints
├── agent_a.py           # Agent A: Task Planner
├── agent_b.py           # Agent B: Task Executor
├── test_api.py          # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # Documentation
```

## Future Enhancements

1. **AI-Powered Summaries**: Integrate OpenAI API for more intelligent summaries
2. **More Task Types**: Support queries beyond weather (news, stocks, etc.)
3. **Multi-Step Workflows**: Handle complex requests requiring multiple data sources
4. **Conversation Memory**: Maintain context across multiple requests
5. **User Authentication**: Add API key validation and rate limiting
6. **Caching**: Cache weather data to reduce API calls
7. **Websockets**: Real-time streaming responses

---

**Demonstration Complete** ✨
