from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from utils.agent import main_agent

router = APIRouter()


async def generate_weather_stream(query: str) -> AsyncGenerator[str, None]:
    """
    Generator function that yields streaming data chunks.
    Replace this logic with your actual streaming implementation.
    """
    try:
        async for event in main_agent.astream_events(
            {"messages": [{"role": "user", "content": query}]}
        ):
            # print(f"Event: {event['event']}, Data: {event['data']}")
            if event["event"] == "on_chat_model_stream":
                token = event["data"]["chunk"].content
                if token:
                    yield f"data: {token}\n\n"
    except Exception as e:
        print("Error in generate_weather_stream:", e)
        raise e


@router.get("/weather")
async def stream_weather(query: str = ""):
    """
    Streaming endpoint that returns weather data progressively.

    Args:
        query: The query string containing the weather request details (query parameter)

    Returns:
        StreamingResponse with text/event-stream content type
    """
    try:
        if not query:
            return JSONResponse(
                {"error": "Query parameter is required."},
                status_code=400,
                media_type="application/json",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                },
            )
        return StreamingResponse(
            generate_weather_stream(query),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    except Exception as e:
        print("Error in stream_weather endpoint:", e)
        return JSONResponse(
            {"error": "Sorry, an error occurred with your request."},
            status_code=500,
            media_type="application/json",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
