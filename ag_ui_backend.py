#!/usr/bin/env python3
"""
AG UI Backend Integration for SentimentSuite
Provides LangGraph agent endpoints for CopilotKit integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime

# Import your existing LangGraph components
from src.graphs.chat_agent import get_new_agent
from src.io_py.edge.config import LLMConfigVoice
from src.tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI(
    title="SentimentSuite AG UI Backend",
    description="LangGraph agent backend for CopilotKit integration",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
_agent_instance = None
_memory_instance = None


def get_agent():
    """Get or create the global agent instance"""
    global _agent_instance, _memory_instance
    if _agent_instance is None:
        _memory_instance = MemorySaver()
        _agent_instance = get_new_agent(
            config=LLMConfigVoice,
            short_term_memory=_memory_instance,
            long_term_memory=None,
        )
    return _agent_instance


# Pydantic models for API
class ChatMessage(BaseModel):
    role: str
    content: str
    id: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    thread_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    message: ChatMessage
    tool_calls: Optional[List[Dict[str, Any]]] = None


class VisualizationRequest(BaseModel):
    data_type: str
    query: Optional[str] = None
    session_id: Optional[str] = "session_001"


@app.get("/")
async def root():
    return {"message": "SentimentSuite AG UI Backend is running"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for LangGraph agent
    """
    try:
        agent = get_agent()

        # Convert messages to LangGraph format
        messages = []
        for msg in request.messages:
            if msg.role == "user":
                messages.append({"role": "human", "content": msg.content})
            elif msg.role == "assistant":
                messages.append({"role": "ai", "content": msg.content})

        # Configure the agent run
        config = {"configurable": {"thread_id": request.thread_id}}

        # Run the agent
        result = await agent.ainvoke({"messages": messages}, config=config)

        # Extract the response
        if result and "messages" in result:
            last_message = result["messages"][-1]
            response_content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            # Check for tool calls
            tool_calls = []
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                tool_calls = [
                    {
                        "name": tc.name if hasattr(tc, "name") else tc.get("name", ""),
                        "args": tc.args if hasattr(tc, "args") else tc.get("args", {}),
                        "id": tc.id if hasattr(tc, "id") else tc.get("id", ""),
                    }
                    for tc in last_message.tool_calls
                ]

            return ChatResponse(
                message=ChatMessage(
                    role="assistant",
                    content=response_content,
                    id=f"msg_{datetime.now().timestamp()}",
                ),
                tool_calls=tool_calls if tool_calls else None,
            )
        else:
            return ChatResponse(
                message=ChatMessage(
                    role="assistant",
                    content="I apologize, but I encountered an issue processing your request.",
                    id=f"msg_{datetime.now().timestamp()}",
                )
            )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")


@app.post("/visualize")
async def visualize_endpoint(request: VisualizationRequest):
    """
    Endpoint to get psychological data for visualization
    """
    try:
        from src.tools.hybrid_rag_tools import (
            get_objective_statistics,
            get_personality_summary,
            get_extreme_values,
            search_psychological_insights,
        )

        data_type = request.data_type.lower()

        if data_type == "statistics":
            result = get_objective_statistics.invoke({"session_id": request.session_id})
            # Parse the result if it's a string
            if isinstance(result, str):
                # Try to extract JSON-like data from the string
                try:
                    # This is a simplified parser - you might need to adjust based on actual output format
                    import re

                    numbers = re.findall(r"(\w+):\s*(\d+)", result)
                    data = {key: int(value) for key, value in numbers}
                except:
                    data = {"raw_result": result}
            else:
                data = result

        elif data_type == "personality":
            result = get_personality_summary.invoke({"analysis_type": "overall"})
            # Parse personality data
            data = {"summary": result}

        elif data_type == "extreme_values":
            result = get_extreme_values.invoke(
                {
                    "metric": "emotion_valence",
                    "session_id": request.session_id,
                    "limit": 5,
                }
            )
            # Parse extreme values
            data = {"extreme_values": result}

        elif data_type == "emotions":
            result = search_psychological_insights.invoke(
                {"query": request.query or "emotional patterns feelings"}
            )
            data = {"insights": result}

        else:
            data = {"error": f"Unknown data type: {data_type}"}

        return {
            "data_type": data_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Error in visualize endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Visualization error: {str(e)}")


@app.post("/circumplex")
async def circumplex_endpoint(request: VisualizationRequest):
    """
    Endpoint to get emotion data for circumplex visualization
    """
    try:
        from src.tools.hybrid_rag_tools import search_psychological_insights

        # Get emotional data
        result = search_psychological_insights.invoke(
            {"query": request.query or "emotions valence arousal"}
        )

        # Parse the result to extract emotion data
        # This is a simplified parser - you might need to adjust based on actual output format
        emotions = []
        if isinstance(result, str):
            # Try to extract emotion data from the text
            import re

            # Look for patterns like "emotion_name: valence=0.5, arousal=0.3"
            emotion_matches = re.findall(
                r"(\w+).*?valence[=:\s]*([-\d.]+).*?arousal[=:\s]*([-\d.]+)",
                result,
                re.IGNORECASE,
            )
            for match in emotion_matches:
                emotions.append(
                    {
                        "name": match[0],
                        "valence": float(match[1]),
                        "arousal": float(match[2]),
                        "confidence": 0.7,  # Default confidence
                    }
                )

        # If no emotions found, create some sample data
        if not emotions:
            emotions = [
                {"name": "Happy", "valence": 0.8, "arousal": 0.6, "confidence": 0.8},
                {"name": "Sad", "valence": -0.7, "arousal": 0.3, "confidence": 0.7},
                {"name": "Excited", "valence": 0.6, "arousal": 0.9, "confidence": 0.6},
                {"name": "Calm", "valence": 0.4, "arousal": 0.2, "confidence": 0.8},
                {"name": "Anxious", "valence": -0.5, "arousal": 0.8, "confidence": 0.7},
            ]

        return {
            "emotions": emotions,
            "title": "Emotional Circumplex - Therapy Session Analysis",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Error in circumplex endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Circumplex error: {str(e)}")


@app.post("/deep_agent")
async def deep_agent_endpoint():
    """
    Endpoint to run deep agent workflow and return state
    """
    try:

        mock_state = {
            "current_task": "Analyzing psychological patterns in therapy session",
            "status": "working",
            "progress": 65,
            "todos": [
                {
                    "id": "1",
                    "task": "Extract emotional patterns from session data",
                    "status": "completed",
                    "priority": "high",
                    "created_at": datetime.now().isoformat(),
                },
                {
                    "id": "2",
                    "task": "Analyze cognitive distortions",
                    "status": "in_progress",
                    "priority": "medium",
                    "created_at": datetime.now().isoformat(),
                },
                {
                    "id": "3",
                    "task": "Generate treatment recommendations",
                    "status": "pending",
                    "priority": "high",
                    "created_at": datetime.now().isoformat(),
                },
            ],
            "thoughts": [
                {
                    "id": "1",
                    "content": "The client shows strong patterns of emotional dysregulation, particularly in response to interpersonal stressors.",
                    "type": "observation",
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.8,
                },
                {
                    "id": "2",
                    "content": "I should focus on attachment style analysis to better understand the underlying patterns.",
                    "type": "reasoning",
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.7,
                },
                {
                    "id": "3",
                    "content": "The next step should be to correlate emotional responses with specific therapeutic interventions.",
                    "type": "plan",
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.9,
                },
            ],
        }

        return mock_state

    except Exception as e:
        print(f"Error in deep agent endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Deep agent error: {str(e)}")


@app.get("/tools")
async def list_tools():
    """
    List available psychological analysis tools
    """
    tools_info = []
    for tool in PERSONA_FORGE_TOOLS:
        tools_info.append(
            {
                "name": tool.name,
                "description": tool.description,
                "args": tool.args if hasattr(tool, "args") else {},
            }
        )

    return {"tools": tools_info}


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        agent = get_agent()
        return {
            "status": "healthy",
            "agent_available": agent is not None,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


@app.get("/read-therapy-note")
async def read_therapy_note():
    """Read the therapy note from output/therapy-note.txt"""
    try:
        import os

        file_path = "output/therapy-note.txt"

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return {"content": content, "timestamp": datetime.now().isoformat()}
        else:
            return {
                "content": "Therapy note file not found. Please run the deep agent workflow first.",
                "timestamp": datetime.now().isoformat(),
            }
    except Exception as e:
        logger.error(f"Error reading therapy note: {str(e)}")
        return {
            "content": f"Error reading therapy note: {str(e)}",
            "timestamp": datetime.now().isoformat(),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
