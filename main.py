"""
FastAPI Server for Multi-Agent System
Handles user requests and coordinates between Agent A and Agent B.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent_a import AgentA
import uvicorn

app = FastAPI(
    title="Multi-Agent Weather System",
    description="A system with two agents that work together to process weather requests",
    version="1.0.0"
)

# Initialize Agent A (which will initialize Agent B internally)
agent_a = AgentA()


class UserRequest(BaseModel):
    """Model for user request."""
    request: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "request": "Get the current weather in New York and give me a short summary."
            }
        }


class AgentResponse(BaseModel):
    """Model for agent response."""
    success: bool
    tasks_executed: Optional[int] = None
    response: str
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Multi-Agent Weather System API",
        "endpoints": {
            "/process": "POST - Process a natural language request",
            "/health": "GET - Check API health",
            "/docs": "GET - API documentation"
        },
        "example_request": "Get the current weather in New York and give me a short summary."
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": {
            "agent_a": "active",
            "agent_b": "active"
        }
    }


@app.post("/process", response_model=AgentResponse)
async def process_request(user_request: UserRequest):
    """
    Process a natural language request using Agent A and Agent B.
    
    Args:
        user_request: User's natural language request
        
    Returns:
        Response from the agent system
        
    Example:
        POST /process
        {
            "request": "Get the current weather in New York and give me a short summary."
        }
    """
    try:
        # Agent A will process the request and coordinate with Agent B
        result = await agent_a.process_request(user_request.request)
        
        return AgentResponse(
            success=result.get("success", False),
            tasks_executed=result.get("tasks_executed"),
            response=result.get("response", ""),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
