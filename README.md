# Agentic AI Mini Project

A multi-agent system built with FastAPI that demonstrates agent-based task decomposition and execution. The system uses two agents that communicate to process natural language requests, specifically handling weather queries.

## 🎯 Project Overview

This project implements a program with two cooperating agents:

- **Agent A (Task Planner)**: Takes a user's natural language request and breaks it into smaller, manageable tasks
- **Agent B (Task Executor)**: Performs the smaller tasks (like fetching weather data) and returns the results

The agents communicate programmatically to complete the overall task and provide the final answer to the user.

## 🏗️ Architecture

```
User Request → Agent A (Planner) → Agent B (Executor) → Agent A (Compiler) → Final Response
```

### Example Workflow

**User Input:**
```
"Get the current weather in New York and give me a short summary."
```

**Agent A Process:**
1. Understands the request
2. Breaks it into two tasks:
   - Task 1: Get weather data for New York
   - Task 2: Summarize the weather data

**Agent B Process:**
- Fetches current weather data from OpenWeatherMap API (or returns mock data)
- Provides the data back to Agent A

**Final Step:**
- Agent B creates a short summary of the weather data using rule-based logic
- Agent A compiles the results and outputs the final response

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/parth6sharma/agentic-ai-mini-project.git
cd agentic-ai-mini-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Note:** The system works with mock data if no API keys are configured. To use real weather data, get a free API key from [OpenWeatherMap](https://openweathermap.org/api).

### Running the Server

Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## 📡 API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns API information and example usage.

### 2. Health Check
```
GET /health
```
Checks if the agents are active and running.

### 3. Process Request
```
POST /process
```

**Request Body:**
```json
{
  "request": "Get the current weather in New York and give me a short summary."
}
```

**Response:**
```json
{
  "success": true,
  "tasks_executed": 2,
  "response": "The current weather in New York is partly cloudy with a temperature of 72°F. The humidity is 65% and wind speed is 8 mph. The temperature is comfortable.",
  "error": null
}
```

### Interactive API Documentation

FastAPI provides interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 💡 Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{"request": "Get the current weather in New York and give me a short summary."}'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/process",
    json={"request": "Get the current weather in London and give me a short summary."}
)

print(response.json())
```

### Using JavaScript fetch

```javascript
fetch('http://localhost:8000/process', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    request: 'Get the current weather in Paris and give me a short summary.'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔧 Project Structure

```
agentic-ai-mini-project/
│
├── main.py              # FastAPI server and endpoints
├── agent_a.py           # Agent A: Task Planner
├── agent_b.py           # Agent B: Task Executor
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🌟 Features

- ✅ Natural language request processing
- ✅ Task decomposition and planning (Agent A)
- ✅ Task execution with external API integration (Agent B)
- ✅ Weather data fetching from OpenWeatherMap API
- ✅ Rule-based weather summary generation
- ✅ RESTful API with FastAPI
- ✅ Interactive API documentation
- ✅ Mock data support for testing without API keys
- ✅ Async/await for efficient request handling

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key (optional - uses mock data if not provided)
- `OPENAI_API_KEY`: Your OpenAI API key (optional - for future AI-powered features)

## 🧪 Testing

You can test the system using the interactive documentation at `http://localhost:8000/docs` or by sending POST requests to the `/process` endpoint.

Example test queries:
- "Get the current weather in New York and give me a short summary."
- "What's the weather in London and summarize it"
- "Get weather for Tokyo and give me a summary"

## 🛠️ Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for API calls
- **python-dotenv**: Environment variable management
- **uvicorn**: ASGI server for running FastAPI

## 📝 Assignment Requirements Met

✅ Two agents that communicate programmatically  
✅ Agent A breaks down natural language requests into smaller tasks  
✅ Agent B performs tasks and returns results  
✅ Agents communicate to complete the overall task  
✅ System handles end-to-end user queries  
✅ Uses Python as the programming language  
✅ Integrates with external API (OpenWeatherMap)  
✅ Provides natural language processing for weather requests  

## 🚦 Future Enhancements

- Add more task types beyond weather queries
- Integrate OpenAI API for AI-powered summaries
- Add user authentication and rate limiting
- Support for multiple simultaneous requests
- Add caching for frequently requested weather data
- Expand to handle more complex multi-step workflows

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Parth Sharma

---

**Weekend Project** - A demonstration of multi-agent systems in action!
