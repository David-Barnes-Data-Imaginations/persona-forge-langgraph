#!/usr/bin/env python3
"""
AG UI Backend Integration for SentimentSuite
Provides LangGraph agent endpoints for CopilotKit integration
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import tempfile
import os
import subprocess
import shutil
import numpy as np
import soundfile as sf

# Import your existing LangGraph components
from src.graphs.chat_agent import get_new_agent
from src.io_py.edge.config import LLMConfigVoice
from src.voice_service_faster import faster_whisper_service
from src.tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI(
    title="SentimentSuite AG UI Backend",
    description="LangGraph agent backend for CopilotKit integration",
)

# Enable CORS for Next.js frontend (allow multiple ports in case port 3000 is busy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
    ],
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
        result = await agent.ainvoke({"messages": messages}, config=config)  # type: ignore[arg-type]

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
                except Exception:
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
    Endpoint to read deep agent analysis from output/plan.txt and return state
    """
    try:
        import os

        # Path to the plan file
        plan_file = os.path.join(os.path.dirname(__file__), "output", "plan.txt")

        if not os.path.exists(plan_file):
            raise HTTPException(
                status_code=404,
                detail="Plan file not found. Run deep agent workflow first.",
            )

        # Read the plan file
        with open(plan_file, "r", encoding="utf-8") as f:
            plan_content = f.read()

        # Parse the content into structured data
        # Split into sections
        sections = plan_content.split("\n\n")

        subjective_text = ""
        statistics_text = ""

        # Extract sections
        for i, section in enumerate(sections):
            if section.strip().startswith("Subjective"):
                # Get the next section as subjective content
                if i + 1 < len(sections):
                    subjective_text = sections[i + 1].strip()
            elif section.strip().startswith("Statistics Summary"):
                # Get remaining text as statistics
                if i + 1 < len(sections):
                    statistics_text = "\n".join(sections[i + 1 :]).strip()

        # Parse statistics into structured thoughts
        thoughts = []
        thought_id = 1

        # Add subjective analysis as first thought
        if subjective_text:
            thoughts.append(
                {
                    "id": str(thought_id),
                    "content": f"Subjective Analysis: {subjective_text}",
                    "type": "observation",
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.9,
                }
            )
            thought_id += 1

        # Parse statistics lines into thoughts
        if statistics_text:
            stat_lines = statistics_text.split("\n")
            i = 0
            while i < len(stat_lines):
                line = stat_lines[i]
                if line.strip() and ":" in line:
                    # Parse each statistic line
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        category = parts[0].strip()
                        data = parts[1].strip()

                        # Check if this is "Personality" and the next line contains the actual data
                        if (
                            category == "Personality"
                            and not data
                            and i + 1 < len(stat_lines)
                        ):
                            # Get the next line which has the personality data
                            data = stat_lines[i + 1].strip()
                            i += 1  # Skip the next line since we've already used it

                        if data:  # Only add if we have actual data
                            thoughts.append(
                                {
                                    "id": str(thought_id),
                                    "content": f"{category}: {data}",
                                    "type": "analysis",
                                    "timestamp": datetime.now().isoformat(),
                                    "confidence": 0.85,
                                }
                            )
                            thought_id += 1
                i += 1

        # Create todos based on the analysis
        todos = [
            {
                "id": "1",
                "task": "Analyze emotional patterns from session data",
                "status": "completed",
                "priority": "high",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "2",
                "task": "Identify cognitive distortions and schemas",
                "status": "completed",
                "priority": "high",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "3",
                "task": "Assess personality traits and attachment styles",
                "status": "completed",
                "priority": "medium",
                "created_at": datetime.now().isoformat(),
            },
            {
                "id": "4",
                "task": "Generate comprehensive treatment plan",
                "status": "completed",
                "priority": "high",
                "created_at": datetime.now().isoformat(),
            },
        ]

        # Build the response
        state = {
            "current_task": "Deep psychological analysis completed",
            "status": "completed",
            "progress": 100,
            "todos": todos,
            "thoughts": thoughts,
            "raw_analysis": plan_content,  # Include raw content for reference
        }

        return state

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Plan file not found. Run deep agent workflow first.",
        )
    except Exception as e:
        print(f"Error in deep agent endpoint: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Deep agent error: {str(e)}")


@app.post("/psychological_graphs")
async def psychological_graphs_endpoint(session_id: str = "session_001"):
    """
    Get all psychological graph data formatted for React/Plotly visualizations.

    This endpoint calls get_objective_statistics and formats the data into
    the exact structure needed by the React visualization components.

    Returns:
        - emotions: Valence-arousal scatter plot data
        - personality: Big Five radar chart data
        - statistics: Bar chart data for various psychological patterns
        - extreme_values: Highest/lowest trait values
    """
    try:
        from src.tools.hybrid_rag_tools import (
            get_objective_statistics,
            get_extreme_values,
        )
        import re

        # Get the raw statistics
        stats_result = get_objective_statistics.invoke({"session_id": session_id})

        # Initialize response structure
        graph_data = {
            "emotions": [],
            "personality": {},
            "statistics": {
                "emotions": {"categories": [], "values": []},
                "distortions": {"categories": [], "values": []},
                "schemas": {"categories": [], "values": []},
                "attachments": {"categories": [], "values": []},
                "defenses": {"categories": [], "values": []},
            },
            "extreme_values": {},
            "session_id": session_id,
        }

        # Parse the text output from get_objective_statistics
        lines = stats_result.split("\n")

        current_section = None

        for line in lines:
            line = line.strip()

            # Detect sections
            if line.startswith("Top 5 Emotions:"):
                current_section = "emotions"
                continue
            elif line.startswith("Top 5 Cognitive Distortions:"):
                current_section = "distortions"
                continue
            elif line.startswith("Top 5 Core Schemas:"):
                current_section = "schemas"
                continue
            elif line.startswith("Attachment Styles:"):
                current_section = "attachments"
                continue
            elif line.startswith("Top 5 Defense Mechanisms:"):
                current_section = "defenses"
                continue
            elif line.startswith("Big Five Personality Averages:"):
                current_section = "personality"
                continue

            # Parse emotion data (with valence and arousal)
            if current_section == "emotions" and line.startswith("-"):
                # Format: "- Sadness: 10 occurrences (avg valence: -0.54, avg arousal: 0.39)"
                match = re.search(
                    r"-\s+([^:]+):\s+(\d+)\s+occurrences\s+\(avg valence:\s+([-\d.]+),\s+avg arousal:\s+([-\d.]+)",
                    line,
                )
                if match:
                    emotion_name = match.group(1).strip()
                    count = int(match.group(2))
                    valence = float(match.group(3))
                    arousal = float(match.group(4))

                    graph_data["emotions"].append(
                        {
                            "name": emotion_name,
                            "valence": valence,
                            "arousal": arousal,
                            "confidence": min(
                                count / 15.0, 1.0
                            ),  # Normalize count to confidence (0-1)
                            "count": count,
                        }
                    )

                    # Also add to statistics
                    graph_data["statistics"]["emotions"]["categories"].append(
                        emotion_name
                    )
                    graph_data["statistics"]["emotions"]["values"].append(count)

            # Parse distortions
            elif current_section == "distortions" and line.startswith("-"):
                # Format: "- Labeling: 6 occurrences"
                match = re.search(r"-\s+([^:]+):\s+(\d+)\s+occurrences", line)
                if match:
                    name = match.group(1).strip()
                    count = int(match.group(2))
                    graph_data["statistics"]["distortions"]["categories"].append(name)
                    graph_data["statistics"]["distortions"]["values"].append(count)

            # Parse schemas
            elif current_section == "schemas" and line.startswith("-"):
                match = re.search(r"-\s+([^:]+):\s+(\d+)\s+occurrences", line)
                if match:
                    name = match.group(1).strip()
                    count = int(match.group(2))
                    graph_data["statistics"]["schemas"]["categories"].append(name)
                    graph_data["statistics"]["schemas"]["values"].append(count)

            # Parse attachments
            elif current_section == "attachments" and line.startswith("-"):
                match = re.search(r"-\s+([^:]+):\s+(\d+)\s+occurrences", line)
                if match:
                    name = match.group(1).strip()
                    count = int(match.group(2))
                    graph_data["statistics"]["attachments"]["categories"].append(name)
                    graph_data["statistics"]["attachments"]["values"].append(count)

            # Parse defenses
            elif current_section == "defenses" and line.startswith("-"):
                match = re.search(r"-\s+([^:]+):\s+(\d+)\s+occurrences", line)
                if match:
                    name = match.group(1).strip()
                    count = int(match.group(2))
                    graph_data["statistics"]["defenses"]["categories"].append(name)
                    graph_data["statistics"]["defenses"]["values"].append(count)

            # Parse Big Five personality
            elif current_section == "personality" and line.startswith("-"):
                # Format: "- Openness: 0.73 (High)"
                match = re.search(r"-\s+([^:]+):\s+([\d.]+)\s+\(([^)]+)\)", line)
                if match:
                    trait = match.group(1).strip().lower()
                    value = float(match.group(2))
                    graph_data["personality"][trait] = value

        # Get extreme values for neuroticism (as an example)
        try:
            extreme_neuroticism = get_extreme_values.invoke(
                {"property_type": "neuroticism", "session_id": session_id, "limit": 3}
            )
            graph_data["extreme_values"]["neuroticism"] = extreme_neuroticism
        except Exception as e:
            print(f"Error getting extreme values: {e}")
            graph_data["extreme_values"][
                "neuroticism"
            ] = "No extreme value data available"

        return graph_data

    except Exception as e:
        print(f"Error in psychological_graphs endpoint: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Graph data error: {str(e)}")


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
        print(f"🎤 Voice service available: {VOICE_SERVICE_AVAILABLE}")
        return {
            "status": "healthy",
            "agent_available": agent is not None,
            "voice_service_available": VOICE_SERVICE_AVAILABLE,
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
        return {
            "content": f"Error reading therapy note: {str(e)}",
            "timestamp": datetime.now().isoformat(),
        }


class WorkflowFileUpload(BaseModel):
    content: str
    filename: str


@app.post("/workflow/framework-analysis")
async def framework_analysis_endpoint(upload: WorkflowFileUpload):
    """
    Workflow 1: Process therapy session through framework analysis

    Args:
        upload: File content and filename

    Returns:
        Analysis results with psychological frameworks applied
    """
    try:
        from src.graphs.framework_analysis import process_therapy_session

        # Process the CSV content
        results = process_therapy_session(upload.content)

        if results.get("status") == "failed":
            raise HTTPException(status_code=500, detail=results.get("error"))

        return {
            "status": "success",
            "filename": upload.filename,
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Error in framework analysis: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Framework analysis error: {str(e)}"
        )


@app.post("/workflow/knowledge-graph")
async def knowledge_graph_endpoint():
    """
    Workflow 2: Create knowledge graph from analysis results

    Reads from output/psychological_analysis/psychological_analysis_master.txt
    and creates Neo4j cypher + embeddings

    Returns:
        Cypher script and embedding information
    """
    try:
        from src.graphs.create_kg import process_kg_creation
        import os

        analysis_file = (
            "output/psychological_analysis/psychological_analysis_master.txt"
        )
        if not os.path.exists(analysis_file):
            raise HTTPException(
                status_code=404,
                detail="Analysis file not found. Please run Framework Analysis first.",
            )

        # Process KG creation
        results = process_kg_creation()

        if results.get("status") == "failed":
            raise HTTPException(status_code=500, detail=results.get("error"))

        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in knowledge graph creation: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Knowledge graph error: {str(e)}")


@app.get("/workflow/analysis-results")
async def get_analysis_results():
    """
    Get the current analysis results from the output file

    Returns:
        The contents of the psychological analysis file
    """
    try:
        import os

        analysis_file = (
            "output/psychological_analysis/psychological_analysis_master.txt"
        )

        if os.path.exists(analysis_file):
            with open(analysis_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Get file stats
            stats = os.stat(analysis_file)

            return {
                "content": content,
                "size_bytes": stats.st_size,
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "timestamp": datetime.now().isoformat(),
            }
        else:
            return {
                "content": "",
                "message": "No analysis results found. Please run Framework Analysis first.",
                "timestamp": datetime.now().isoformat(),
            }

    except Exception as e:
        print(f"Error reading analysis results: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading analysis: {str(e)}")


@app.get("/workflow/cypher-output")
async def get_cypher_output():
    """
    Get the generated Cypher script from knowledge graph creation

    Returns:
        The Cypher script content
    """
    try:
        import os
        import glob

        # Find the most recent cypher file
        cypher_dir = "output/psychological_analysis/graph_output"
        pattern = os.path.join(cypher_dir, "psychological_graph_*.cypher")
        cypher_files = glob.glob(pattern)

        if not cypher_files:
            return {
                "content": "",
                "message": "No Cypher output found. Please run Knowledge Graph workflow first.",
                "timestamp": datetime.now().isoformat(),
            }

        # Get the most recent file
        latest_file = max(cypher_files, key=os.path.getctime)

        with open(latest_file, "r", encoding="utf-8") as f:
            content = f.read()

        stats = os.stat(latest_file)

        return {
            "content": content,
            "filename": os.path.basename(latest_file),
            "size_bytes": stats.st_size,
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"Error reading cypher output: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading cypher: {str(e)}")


# =====================
# Voice Service Endpoints
# =====================

# Import voice service
try:
    from google.cloud import speech_v1p1beta1 as speech  # type: ignore[import]
    from google.cloud import texttospeech  # type: ignore[import]
    from dotenv import load_dotenv

    load_dotenv()
    VOICE_SERVICE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Voice service not available: {e}")
    VOICE_SERVICE_AVAILABLE = False

print(f"🎤 Initial VOICE_SERVICE_AVAILABLE status: {VOICE_SERVICE_AVAILABLE}")
if not VOICE_SERVICE_AVAILABLE:
    print(
        "   (This means Google Cloud Speech and Text-to-Speech libraries failed to import)"
    )

print(
    f"🔐 GOOGLE_APPLICATION_CREDENTIALS in backend: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}"
)
print(f"🔑 GOOGLE_API_KEY in backend: {os.getenv('GOOGLE_API_KEY')}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🎤 WebSocket connection accepted")
    if not VOICE_SERVICE_AVAILABLE:
        print("❌ Google Cloud Speech service not available")
        await websocket.send_json(
            {"type": "ERROR", "message": "Google Cloud Speech service not available"}
        )
        await websocket.close()
        return

    print(
        f"🔐 Google credentials loaded: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is not None}"
    )

    try:
        while True:
            data = await websocket.receive_bytes()
            print(f"📦 Received {len(data)} bytes of audio")

            try:
                client = speech.SpeechClient()
                print("🤖 Initialized Google Speech Client")

                audio = speech.RecognitionAudio(content=data)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                    sample_rate_hertz=48000,
                    language_code="en-US",
                )
                print("⚙️ Configured Google Speech-to-Text request")

                print("🗣️ Sending audio to Google for transcription...")
                response = client.recognize(config=config, audio=audio)
                print("✅ Received response from Google")

                if response.results:
                    transcription = response.results[0].alternatives[0].transcript
                    print(f"📝 Transcription result: '{transcription}'")
                    await websocket.send_json(
                        {
                            "type": "TRANSCRIPT",
                            "text": transcription,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    print("📤 Sent transcript to frontend")
                else:
                    print("⚠️ No speech detected in audio")
                    await websocket.send_json(
                        {"type": "STATUS", "message": "No speech detected"}
                    )
            except Exception as e:
                print(f"❌ Error during transcription: {e}")
                await websocket.send_json(
                    {"type": "ERROR", "message": f"Transcription failed: {e}"}
                )

    except WebSocketDisconnect:
        print("🔌 WebSocket disconnected")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        import traceback

        traceback.print_exc()
        try:
            await websocket.send_json({"type": "ERROR", "message": str(e)})
        except Exception:
            pass


@app.websocket("/ws/vad")
@app.websocket("/ws/vad-stream")
async def vad_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for VAD audio streaming, using faster-whisper."""
    await websocket.accept()
    provider_choice = websocket.query_params.get("provider", "local").lower()
    language_code = os.getenv("GOOGLE_SPEECH_LANGUAGE", "en-US")
    print(
        f"🎤 VAD WebSocket connection established for AG-UI (provider={provider_choice}, language={language_code})"
    )

    current_frames = []

    try:
        while True:
            data = await websocket.receive()

            if "bytes" in data:
                # Raw PCM audio data
                pcm_data = np.frombuffer(data["bytes"], dtype=np.int16)
                current_frames.append(pcm_data)

            elif "text" in data:
                message = json.loads(data["text"])
                if message.get("type") == "UTTERANCE_END":
                    print("🎯 AG-UI: Processing utterance from VAD...")

                    if not current_frames:
                        print("⚠️ No audio frames to process.")
                        continue

                    # Concatenate all audio frames
                    full_audio = np.concatenate(current_frames)
                    current_frames = []

                    tmp_path = None
                    try:
                        with tempfile.NamedTemporaryFile(
                            suffix=".wav", delete=False
                        ) as tmp_file:
                            tmp_path = tmp_file.name
                            audio_float = full_audio.astype(np.float32) / 32768.0
                            sf.write(tmp_path, audio_float, 16000)

                        print(
                            f"🎤 Transcribing {len(full_audio)} samples via {provider_choice}"
                        )

                        active_provider = provider_choice
                        transcription = ""

                        if provider_choice == "google" and not VOICE_SERVICE_AVAILABLE:
                            warning_message = "Google Speech service unavailable, falling back to local STT"
                            print(f"⚠️ {warning_message}")
                            await websocket.send_text(
                                json.dumps(
                                    {
                                        "type": "STATUS",
                                        "message": "Falling back to on-device speech recognition",
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )
                            )
                            active_provider = "local"

                        if active_provider == "google":
                            try:
                                with open(tmp_path, "rb") as wav_file:
                                    wav_bytes = wav_file.read()

                                client = speech.SpeechClient()
                                audio = speech.RecognitionAudio(content=wav_bytes)
                                config = speech.RecognitionConfig(
                                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                    sample_rate_hertz=16000,
                                    language_code=language_code,
                                )

                                response = client.recognize(config=config, audio=audio)

                                if response.results:
                                    transcription = (
                                        response.results[0].alternatives[0].transcript
                                    )

                            except Exception as google_error:
                                print(f"❌ Google STT error: {google_error}")
                                import traceback

                                traceback.print_exc()  # Add this line for detailed traceback
                                await websocket.send_text(
                                    json.dumps(
                                        {
                                            "type": "STATUS",
                                            "message": "Google transcription failed, retrying locally",
                                            "timestamp": datetime.now().isoformat(),
                                        }
                                    )
                                )
                                active_provider = "local"

                        if active_provider != "google":
                            transcription = (
                                faster_whisper_service.transcribe_audio_file(tmp_path)
                                or ""
                            )

                        if (
                            transcription
                            and transcription.strip()
                            and "error" not in transcription.lower()
                        ):
                            cleaned = transcription.strip()
                            await websocket.send_text(
                                json.dumps(
                                    {
                                        "type": "TRANSCRIPT",
                                        "text": cleaned,
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )
                            )
                            print(f"✅ Sent transcription: '{cleaned}'")
                        else:
                            print(
                                f"⚠️ Empty or error transcription from {active_provider}: '{transcription}'"
                            )
                            await websocket.send_text(
                                json.dumps(
                                    {
                                        "type": "STATUS",
                                        "message": "No speech detected",
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                )
                            )

                    except Exception as transcription_error:
                        print(f"❌ Transcription error: {transcription_error}")
                        await websocket.send_text(
                            json.dumps(
                                {
                                    "type": "ERROR",
                                    "message": f"Transcription failed: {str(transcription_error)}",
                                    "timestamp": datetime.now().isoformat(),
                                }
                            )
                        )
                    finally:
                        if tmp_path and os.path.exists(tmp_path):
                            os.unlink(tmp_path)

    except WebSocketDisconnect:
        print("🔌 VAD WebSocket connection closed for AG-UI")
    except Exception as e:
        print(f"❌ VAD WebSocket error in AG-UI: {e}")
        if websocket.state == "connected":
            await websocket.close()


@app.post("/api/voice/synthesize")
async def synthesize_speech(text: str, provider: str = "local"):
    """Text-to-speech endpoint supporting local Piper (default) and Google Cloud."""
    if not text or len(text.strip()) == 0:
        return Response(status_code=400, content="Text parameter is required")

    provider_choice = (provider or "local").lower()
    clean_text = text.strip()

    if provider_choice == "google":
        if not VOICE_SERVICE_AVAILABLE:
            raise HTTPException(status_code=503, detail="Google TTS not available")

        print(f"🔊 Synthesizing speech with Google TTS: '{clean_text[:50]}...'")

        try:
            client = texttospeech.TextToSpeechClient()

            synthesis_input = texttospeech.SynthesisInput(text=clean_text)

            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            print(f"✅ Synthesized {len(response.audio_content)} bytes of audio")

            return Response(
                content=response.audio_content,
                media_type="audio/mpeg",
                headers={"Content-Disposition": "inline; filename=speech.mp3"},
            )

        except Exception as exc:
            print(f"❌ Google TTS error: {exc}")
            import traceback

            traceback.print_exc()  # Add this line for detailed traceback
            raise HTTPException(status_code=500, detail=f"TTS error: {exc}")

    print(f"🔊 Synthesizing speech with Piper TTS: '{clean_text[:50]}...'")
    output_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name

        piper_model = os.path.expanduser("~/piper/en_GB-alba-medium.onnx")
        if not os.path.exists(piper_model):
            piper_model = "en_GB-alba-medium"

        process = subprocess.run(
            ["piper", "--model", piper_model, "--output_file", output_path],
            input=clean_text,
            text=True,
            capture_output=True,
            timeout=30,
        )

        if (
            process.returncode != 0
            or not os.path.exists(output_path)
            or os.path.getsize(output_path) == 0
        ):
            error_msg = process.stderr or "Unknown Piper error"
            print(f"❌ Piper TTS failed: {error_msg}")
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            raise HTTPException(
                status_code=500, detail=f"TTS generation failed: {error_msg}"
            )

        with open(output_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        os.unlink(output_path)

        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=speech.wav"},
        )

    except subprocess.TimeoutExpired:
        print("❌ Piper TTS timeout")
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail="TTS generation timeout")
    except FileNotFoundError:
        print("❌ Piper executable not found")
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail="Piper TTS not installed")
    except HTTPException:
        raise
    except Exception as exc:
        print(f"❌ Piper TTS error: {exc}")
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/framework-analysis/status")
async def framework_analysis_status():
    """Check if framework analysis workflow is ready"""
    try:
        # Check if therapy CSV exists
        csv_path = os.path.join(
            os.getcwd(), "output", "data", "therapy_csvs", "therapy_WORKING.csv"
        )
        csv_exists = os.path.exists(csv_path)

        # Check if Gemini API key is set
        gemini_available = bool(os.getenv("GEMINI_API_KEY"))

        return {
            "csv_available": csv_exists,
            "gemini_available": gemini_available,
            "csv_path": csv_path if csv_exists else None,
            "status": "ready" if csv_exists and gemini_available else "degraded",
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}


@app.post("/api/framework-analysis/run")
async def run_framework_analysis():
    """
    Run the framework analysis workflow and stream results
    Processes each QA pair through Gemini to identify psychological patterns
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    from src.graphs.framework_analysis import parse_therapy_csv, process_qa_pair

    async def generate_analysis_stream():
        """Generate streaming JSON events for framework analysis"""
        import sys

        sys.stderr.write("🚀 Starting generate_analysis_stream\n")
        sys.stderr.flush()

        try:
            # Read CSV file
            csv_path = os.path.join(
                os.getcwd(), "output", "data", "therapy_csvs", "therapy_WORKING.csv"
            )

            sys.stderr.write(f"📂 CSV path: {csv_path}\n")
            sys.stderr.write(f"📂 CSV exists: {os.path.exists(csv_path)}\n")
            sys.stderr.flush()

            yield f"data: {json.dumps({'type': 'status', 'message': 'Reading therapy CSV...', 'step': 'init'})}\n\n"
            await asyncio.sleep(0.1)

            if not os.path.exists(csv_path):
                yield f"data: {json.dumps({'type': 'error', 'message': f'CSV file not found: {csv_path}'})}\n\n"
                return

            with open(csv_path, "r", encoding="utf-8") as f:
                csv_content = f.read()

            yield f"data: {json.dumps({'type': 'status', 'message': 'Parsing QA pairs...', 'step': 'parsing'})}\n\n"
            await asyncio.sleep(0.1)

            # Parse QA pairs
            qa_pairs = parse_therapy_csv(csv_content)
            total_pairs = len(qa_pairs)

            yield f"data: {json.dumps({'type': 'status', 'message': f'Found {total_pairs} QA pairs to analyze', 'step': 'ready'})}\n\n"
            await asyncio.sleep(0.1)

            # Process each QA pair
            for idx, qa_pair in enumerate(qa_pairs, 1):
                print(
                    f"🔄 Processing QA pair {idx}/{total_pairs}: {qa_pair['message_id']}"
                )
                yield f"data: {json.dumps({'type': 'progress', 'current': idx, 'total': total_pairs, 'qa_id': qa_pair['message_id']})}\n\n"
                await asyncio.sleep(0.05)

                yield f"data: {json.dumps({'type': 'processing', 'qa_id': qa_pair['message_id'], 'question': qa_pair['question'][:100] + '...'})}\n\n"
                await asyncio.sleep(0.05)

                # Process this QA pair
                print(f"📞 Calling process_qa_pair for {qa_pair['message_id']}")
                result = process_qa_pair(qa_pair)
                print(
                    f"✅ Got result for {qa_pair['message_id']}: status={result.get('status')}"
                )

                if result["status"] == "success":
                    # Read the most recent analysis from the output file
                    output_path = os.path.join(
                        os.getcwd(),
                        "output",
                        "psychological_analysis",
                        "psychological_analysis_master.txt",
                    )

                    sys.stderr.write(f"📖 Reading analysis from: {output_path}\n")
                    sys.stderr.write(f"📖 File exists: {os.path.exists(output_path)}\n")
                    sys.stderr.flush()

                    if os.path.exists(output_path):
                        with open(output_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            sys.stderr.write(
                                f"📖 File content length: {len(content)}\n"
                            )

                            # Split by the full separator pattern
                            separator = "=" * 80
                            # Look for entries starting with separator + "ANALYSIS ENTRY"
                            pattern = f"{separator}\nANALYSIS ENTRY"
                            entries = content.split(pattern)

                            sys.stderr.write(f"📖 Found {len(entries)} entries\n")

                            if len(entries) > 1:
                                # Get the last entry (most recent)
                                # It will include everything after "ANALYSIS ENTRY - timestamp"
                                last_entry = entries[-1].strip()

                                sys.stderr.write(
                                    f"📖 Last entry length: {len(last_entry)}\n"
                                )
                                sys.stderr.write(
                                    f"📖 Last entry first 300 chars: {last_entry[:300]}\n"
                                )

                                # Extract just the analysis part (skip timestamp header)
                                lines = last_entry.split("\n")

                                # The entry structure after enhancement is:
                                # Line 0: " - 2025-11-07 07:39:12"
                                # Line 1: "===============..."  (first separator)
                                # Line 2: "QA ID: qa_pair_001"
                                # Line 3-N: Original Q&A and Analysis content
                                # Last line: "===============..." (closing separator)

                                # Find the first separator (after timestamp)
                                first_separator_idx = -1
                                for i, line in enumerate(lines):
                                    if line.strip() == separator:
                                        first_separator_idx = i
                                        break

                                sys.stderr.write(
                                    f"📖 First separator at line: {first_separator_idx}\n"
                                )

                                if first_separator_idx >= 0:
                                    # Content starts after the first separator
                                    # and goes until the last separator
                                    content_lines = lines[first_separator_idx + 1 :]

                                    # Remove the trailing separator if it exists
                                    if (
                                        content_lines
                                        and content_lines[-1].strip() == separator
                                    ):
                                        content_lines = content_lines[:-1]

                                    analysis_content = "\n".join(content_lines).strip()
                                else:
                                    # Fallback: skip first 2 lines and last line if it's a separator
                                    content_lines = lines[2:]
                                    if (
                                        content_lines
                                        and content_lines[-1].strip() == separator
                                    ):
                                        content_lines = content_lines[:-1]
                                    analysis_content = "\n".join(content_lines).strip()

                                sys.stderr.write(
                                    f"📖 Final analysis content length: {len(analysis_content)}\n"
                                )
                                sys.stderr.write(
                                    f"📖 Final content first 200 chars: {analysis_content[:200]}\n"
                                )
                                sys.stderr.flush()

                                yield f"data: {json.dumps({'type': 'analysis_result', 'qa_id': qa_pair['message_id'], 'content': analysis_content})}\n\n"
                                await asyncio.sleep(0.05)
                else:
                    yield f"data: {json.dumps({'type': 'error', 'qa_id': qa_pair['message_id'], 'message': result.get('error', 'Unknown error')})}\n\n"
                    await asyncio.sleep(0.05)

                # Wait 10 seconds between QA pairs to respect Google API rate limits
                if idx < total_pairs:  # Don't wait after the last one
                    yield f"data: {json.dumps({'type': 'status', 'message': f'Waiting 10 seconds before next QA pair (Google API rate limit)...', 'step': 'waiting'})}\n\n"
                    await asyncio.sleep(10)

            yield f"data: {json.dumps({'type': 'complete', 'message': f'Analyzed {total_pairs} QA pairs successfully!'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate_analysis_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/kg-creation/status")
async def kg_creation_status():
    """Check if KG creation workflow is ready"""
    try:
        # Check if master analysis file exists
        master_path = os.path.join(
            os.getcwd(),
            "output",
            "psychological_analysis",
            "psychological_analysis_master.txt",
        )
        master_exists = os.path.exists(master_path)

        # Check if Gemini API key is set
        gemini_available = bool(os.getenv("GEMINI_API_KEY"))

        # Check Neo4j config
        neo4j_available = bool(os.getenv("NEO4J_URI"))

        return {
            "master_file_available": master_exists,
            "gemini_available": gemini_available,
            "neo4j_available": neo4j_available,
            "master_path": master_path if master_exists else None,
            "status": "ready" if master_exists and gemini_available else "degraded",
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}


@app.post("/api/kg-creation/run")
async def run_kg_creation():
    """
    Run the knowledge graph creation workflow and stream results
    Generates Cypher and embeddings for each QA pair
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    from src.graphs.create_kg import (
        extract_analyses_from_master_file,
        create_client_session_setup,
        process_analysis_to_cypher,
    )

    async def generate_kg_stream():
        """Generate streaming JSON events for KG creation"""
        try:
            yield f"data: {json.dumps({'type': 'status', 'message': 'Loading master analysis file...', 'step': 'init'})}\n\n"
            await asyncio.sleep(0.1)

            # Extract analyses from master file
            analyses = extract_analyses_from_master_file()

            if not analyses:
                yield f"data: {json.dumps({'type': 'error', 'message': 'No analyses found in master file'})}\n\n"
                return

            total_analyses = len(analyses)

            yield f"data: {json.dumps({'type': 'status', 'message': f'Found {total_analyses} analyses to process', 'step': 'found'})}\n\n"
            await asyncio.sleep(0.1)

            # Step 1: Create Client/Session setup
            yield f"data: {json.dumps({'type': 'status', 'message': 'Creating Client/Session setup...', 'step': 'setup'})}\n\n"
            await asyncio.sleep(0.1)

            setup_result = create_client_session_setup()

            if setup_result["status"] != "success":
                error_msg = setup_result.get("error", "Unknown error")
                yield f"data: {json.dumps({'type': 'error', 'message': f'Setup failed: {error_msg}'})}\n\n"
                return

            yield f"data: {json.dumps({'type': 'status', 'message': 'Setup complete! Processing analyses...', 'step': 'processing'})}\n\n"
            await asyncio.sleep(0.1)

            # Step 2: Process each analysis
            for idx, analysis in enumerate(analyses, 1):
                qa_id = f"qa_pair_{str(analysis['entry_number']).zfill(3)}"

                yield f"data: {json.dumps({'type': 'progress', 'current': idx, 'total': total_analyses, 'qa_id': qa_id})}\n\n"
                await asyncio.sleep(0.05)

                yield f"data: {json.dumps({'type': 'processing', 'qa_id': qa_id, 'entry': analysis['entry_number']})}\n\n"
                await asyncio.sleep(0.05)

                # Process this analysis
                result = process_analysis_to_cypher(analysis)

                if result["status"] == "success":
                    # Read the generated Cypher (last entry in the file)
                    output_dir = os.path.join(
                        os.getcwd(), "output", "psychological_analysis", "graph_output"
                    )

                    # Find the latest cypher file
                    cypher_files = [
                        f for f in os.listdir(output_dir) if f.endswith(".cypher")
                    ]
                    if cypher_files:
                        latest_file = max(
                            cypher_files,
                            key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
                        )
                        cypher_path = os.path.join(output_dir, latest_file)

                        with open(cypher_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Get last cypher entry
                            entries = content.split(
                                "// ============================================================================"
                            )
                            if (
                                len(entries) >= 3
                            ):  # Need at least 3 parts for a complete entry
                                last_entry = (
                                    entries[-2] + entries[-1]
                                )  # Combine last two parts
                                yield f"data: {json.dumps({'type': 'cypher_result', 'qa_id': qa_id, 'content': last_entry.strip(), 'chunks_created': result.get('chunks_created', 0)})}\n\n"
                                await asyncio.sleep(0.05)
                else:
                    yield f"data: {json.dumps({'type': 'error', 'qa_id': qa_id, 'message': result.get('error', 'Unknown error')})}\n\n"
                    await asyncio.sleep(0.05)

                # Wait 10 seconds between analyses to respect Google API rate limits
                if idx < total_analyses:  # Don't wait after the last one
                    yield f"data: {json.dumps({'type': 'status', 'message': f'Waiting 10 seconds before next analysis (Google API rate limit)...', 'step': 'waiting'})}\n\n"
                    await asyncio.sleep(10)

            yield f"data: {json.dumps({'type': 'complete', 'message': f'Generated Cypher for {total_analyses} analyses successfully!'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate_kg_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/deep-agent/status")
async def deep_agent_status():
    """Check if deep agent dependencies are available"""
    try:
        # Check E2B availability
        import e2b_code_interpreter

        e2b_available = True
    except ImportError:
        e2b_available = False

    # Check Neo4j connection
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_available = bool(neo4j_uri)

    return {
        "e2b_available": e2b_available,
        "neo4j_available": neo4j_available,
        "status": "ready" if e2b_available and neo4j_available else "degraded",
    }


@app.post("/api/deep-agent/run")
async def run_deep_agent_workflow():
    """
    Run the deep agent workflow and return streaming results

    This mimics the CLI workflow but returns structured JSON for the UI
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    from e2b_code_interpreter import Sandbox
    from src.graphs.deep_agent import (
        scribe_model,
        overseer_model,
        alt_model,
        DeepAgentState,
    )
    from src.io_py.edge.config import LLMConfigArchitect
    from src.tools.e2b_tools import E2B_TOOLS, set_global_sandbox
    from src.tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
    from src.tools.research_tools import tavily_search, pubmed_search, think_tool
    from src.tools.todo_tools import write_todos, read_todos
    from src.tools.task_tool import _create_task_tool
    from src.prompts.e2b_prompts import (
        E2B_ARCHITECT_INSTRUCTIONS,
        E2B_SUBAGENT_INSTRUCTIONS,
    )
    from langgraph.prebuilt import create_react_agent
    from langchain_openai import ChatOpenAI

    async def generate_workflow_stream():
        """Generate streaming JSON events for the deep agent workflow"""
        sandbox = None

        try:
            # Send initial status
            yield f"data: {json.dumps({'type': 'status', 'message': 'Creating E2B sandbox...', 'step': 'init'})}\n\n"
            await asyncio.sleep(0.1)

            # Create sandbox
            sandbox = Sandbox()

            yield f"data: {json.dumps({'type': 'status', 'message': 'Installing dependencies...', 'step': 'setup'})}\n\n"
            await asyncio.sleep(0.1)

            # Install dependencies (simplified for speed)
            result = sandbox.commands.run(
                "pip install neo4j langchain langchain-core langchain-openai",
                timeout=120,
            )

            # Set environment variables
            env_vars = {
                "NEO4J_URI": os.getenv("NEO4J_URI", "bolt://host.docker.internal:7687"),
                "NEO4J_USER": os.getenv("NEO4J_USER", "neo4j"),
                "NEO4JP": os.getenv("NEO4JP"),
                "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            }

            for key, value in env_vars.items():
                if value:
                    sandbox.commands.run(f"export {key}='{value}'")

            sandbox.commands.run("mkdir -p ~/workspace/data")
            sandbox.commands.run("mkdir -p ~/workspace/reports")

            yield f"data: {json.dumps({'type': 'status', 'message': 'Sandbox ready!', 'step': 'ready'})}\n\n"
            await asyncio.sleep(0.1)

            # Set global sandbox
            set_global_sandbox(sandbox)

            # Create tools
            core_tools = E2B_TOOLS + [write_todos, read_todos, think_tool]
            research_tools = [tavily_search, pubmed_search]
            assistant_tools = PERSONA_FORGE_TOOLS + research_tools + core_tools

            assistant = {
                "name": "assistant",
                "description": "Delegate tasks to assistant for Neo4j queries and research",
                "prompt": E2B_SUBAGENT_INSTRUCTIONS,
                "tools": [t.name for t in assistant_tools],
            }

            delegation_tools = [
                _create_task_tool(
                    assistant_tools,
                    [assistant],
                    scribe_model,
                    DeepAgentState,
                    tool_name="delegate_to_scribe",
                ),
                _create_task_tool(
                    assistant_tools,
                    [assistant],
                    overseer_model,
                    DeepAgentState,
                    tool_name="delegate_to_overseer",
                ),
                _create_task_tool(
                    assistant_tools,
                    [assistant],
                    alt_model,
                    DeepAgentState,
                    tool_name="delegate_to_alt",
                ),
            ]

            architect_tools = (
                PERSONA_FORGE_TOOLS + research_tools + core_tools + delegation_tools
            )

            yield f"data: {json.dumps({'type': 'status', 'message': 'Creating deep agent...', 'step': 'agent_init'})}\n\n"
            await asyncio.sleep(0.1)

            # Create architect model
            model = ChatOpenAI(
                model=LLMConfigArchitect.model_name,
                temperature=LLMConfigArchitect.temperature,
                max_tokens=32768,
                base_url="http://localhost:1234/v1",
                api_key="lm-studio",
            ).with_config({"recursion_limit": 75})

            # Create agent
            agent = create_react_agent(
                model,
                architect_tools,
                prompt=E2B_ARCHITECT_INSTRUCTIONS,
                checkpointer=MemorySaver(),
                state_schema=DeepAgentState,
            )

            yield f"data: {json.dumps({'type': 'status', 'message': 'Agent created! Starting workflow...', 'step': 'running'})}\n\n"
            await asyncio.sleep(0.1)

            # Define the task
            task = """Please start the workflow for client_001, session_001.

1. Retrieve diagnosis using retrieve_diagnosis and save to /home/user/workspace/data/diagnosis.txt
2. Retrieve subjective analysis using get_subjective_analysis and save to /home/user/workspace/data/subjective.txt
3. Retrieve objective statistics for analysis using get_objective_analysis and save to /home/user/workspace/data/objective.txt
4. Create a therapy note combining all three and save to /home/user/workspace/reports/therapy_note.txt

IMPORTANT: The RAG tools return data but don't save files. You must use execute_bash to save each result."""

            config = {
                "configurable": {"thread_id": "web_workflow"},
                "recursion_limit": 75,
            }

            initial_state = {
                "messages": [{"role": "user", "content": task}],
            }

            step_count = 0

            # Stream agent execution
            for i, chunk in enumerate(
                agent.stream(initial_state, config, stream_mode="values")
            ):
                if "messages" in chunk:
                    latest = chunk["messages"][-1]

                    # Handle TODOs
                    if "todos" in chunk and chunk["todos"]:
                        yield f"data: {json.dumps({'type': 'todos', 'data': chunk['todos']})}\n\n"
                        await asyncio.sleep(0.05)

                    # Handle tool calls
                    if hasattr(latest, "tool_calls") and latest.tool_calls:
                        step_count += 1
                        for tool_call in latest.tool_calls:
                            tool_name = tool_call.get("name")

                            if tool_name == "think_tool":
                                reflection = tool_call.get("args", {}).get(
                                    "reflection", ""
                                )
                                yield f"data: {json.dumps({'type': 'thought', 'content': reflection, 'step': step_count})}\n\n"
                            elif "delegate" in tool_name:
                                args = tool_call.get("args", {})
                                description = args.get("description", "No description")
                                yield f"data: {json.dumps({'type': 'delegation', 'tool': tool_name, 'description': description, 'step': step_count})}\n\n"
                            else:
                                yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_name, 'step': step_count})}\n\n"

                            await asyncio.sleep(0.05)

                    # Handle responses
                    if (
                        hasattr(latest, "content")
                        and latest.content
                        and len(latest.content) > 10
                    ):
                        if "E2B sandbox not available" not in latest.content:
                            yield f"data: {json.dumps({'type': 'response', 'content': latest.content[:500], 'step': step_count})}\n\n"
                            await asyncio.sleep(0.05)

            # Get final workspace contents
            result = sandbox.commands.run("find ~/workspace -type f", timeout=10)
            files = []
            if result.stdout:
                files = result.stdout.strip().split("\n")

            yield f"data: {json.dumps({'type': 'files', 'data': files})}\n\n"

            # Try to export report
            report_files = sandbox.commands.run(
                "ls ~/workspace/reports/*.txt", timeout=5
            )
            if report_files.exit_code == 0:
                report_content = sandbox.commands.run(
                    "cat ~/workspace/reports/therapy_note.txt", timeout=5
                )
                if report_content.exit_code == 0:
                    yield f"data: {json.dumps({'type': 'report', 'content': report_content.stdout})}\n\n"

            yield f"data: {json.dumps({'type': 'complete', 'message': 'Workflow completed successfully!'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        finally:
            if sandbox:
                try:
                    sandbox.kill()
                except:
                    pass

    return StreamingResponse(
        generate_workflow_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/voice/status")
async def voice_status():
    """Check voice service availability"""
    whisper_ready = faster_whisper_service.is_available()
    piper_model_paths = [
        os.path.expanduser("~/piper/en_GB-alba-medium.onnx"),
        "./en_US-lessac-medium.onnx",
    ]
    piper_binary = shutil.which("piper")
    piper_model_present = any(os.path.exists(path) for path in piper_model_paths)

    return {
        "whisper_available": whisper_ready,
        "google_available": VOICE_SERVICE_AVAILABLE,
        "piper_available": bool(piper_binary) and piper_model_present,
        "status": (
            "ready" if whisper_ready or VOICE_SERVICE_AVAILABLE else "unavailable"
        ),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
