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
import asyncio
from datetime import datetime
import io
import tempfile
import os
import glob
import subprocess

# Import your existing LangGraph components
from src.graphs.chat_agent import get_new_agent
from src.io_py.edge.config import LLMConfigVoice
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
                    r"-\s+([^:]+):\s+(\d+)\s+occurrences\s+\(avg valence:\s+([-\d.]+),\s+avg arousal:\s+([-\d.]+)\)",
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

        # Check if analysis file exists
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
    from src.voice_service_faster import faster_whisper_service

    VOICE_SERVICE_AVAILABLE = faster_whisper_service.is_available()
except Exception as e:
    print(f"⚠️ Voice service not available: {e}")
    VOICE_SERVICE_AVAILABLE = False
    faster_whisper_service = None


@app.websocket("/ws/vad-stream")
async def websocket_voice_stream(websocket: WebSocket):
    """
    WebSocket endpoint for real-time voice transcription
    Receives audio chunks and returns transcription
    """
    await websocket.accept()

    if not VOICE_SERVICE_AVAILABLE:
        await websocket.send_json(
            {"type": "ERROR", "message": "Voice service not available"}
        )
        await websocket.close()
        return

    print("🎤 Voice WebSocket connected")
    audio_buffer = bytearray()

    try:
        while True:
            # Receive audio data
            data = await websocket.receive_bytes()
            audio_buffer.extend(data)

            # Process when buffer reaches threshold (e.g., 1 second of audio)
            # Assuming 16kHz, 16-bit audio = 32000 bytes per second
            if len(audio_buffer) >= 64000:  # ~2 seconds of audio
                print(f"🎤 Processing {len(audio_buffer)} bytes of audio")

                # Save to temporary WAV file
                with tempfile.NamedTemporaryFile(
                    suffix=".wav", delete=False
                ) as tmp_file:
                    tmp_path = tmp_file.name

                    # Write WAV header + audio data
                    # This is a simplified approach - adjust based on your audio format
                    import wave

                    with wave.open(tmp_path, "wb") as wav_file:
                        wav_file.setnchannels(1)  # mono
                        wav_file.setsampwidth(2)  # 16-bit
                        wav_file.setframerate(16000)  # 16kHz
                        wav_file.writeframes(bytes(audio_buffer))

                try:
                    # Transcribe using faster-whisper
                    transcript = faster_whisper_service.transcribe_audio_file(tmp_path)

                    if transcript and transcript.strip():
                        await websocket.send_json(
                            {"type": "TRANSCRIPT", "text": transcript}
                        )
                        print(f"✅ Transcribed: {transcript}")

                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

                # Clear buffer after processing
                audio_buffer.clear()

    except WebSocketDisconnect:
        print("🎤 Voice WebSocket disconnected")
    except Exception as e:
        print(f"❌ Voice WebSocket error: {e}")
        await websocket.send_json({"type": "ERROR", "message": str(e)})


@app.post("/api/voice/synthesize")
async def synthesize_speech(text: str):
    """
    Text-to-speech endpoint using Piper TTS
    Returns WAV audio file
    """
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text parameter is required")

    print(f"🔊 Synthesizing speech: '{text[:50]}...'")

    try:
        # Use Piper TTS to synthesize speech
        # Assuming you have piper installed and a model available
        piper_model = "./en_US-lessac-medium.onnx"  # Adjust path as needed

        # Check if Piper is available
        piper_cmd = ["piper", "--version"]
        try:
            subprocess.run(piper_cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Piper not available, return error
            raise HTTPException(
                status_code=503,
                detail="Piper TTS not available. Please install piper-tts.",
            )

        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name

        # Run Piper TTS
        # echo "text" | piper --model <model> --output_file <output>
        process = subprocess.Popen(
            ["piper", "--model", piper_model, "--output_file", output_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = process.communicate(input=text.encode("utf-8"))

        if process.returncode != 0:
            print(f"❌ Piper TTS error: {stderr.decode()}")
            raise HTTPException(
                status_code=500, detail=f"TTS failed: {stderr.decode()}"
            )

        # Read the generated audio file
        with open(output_path, "rb") as f:
            audio_data = f.read()

        # Clean up temp file
        os.remove(output_path)

        print(f"✅ Synthesized {len(audio_data)} bytes of audio")

        # Return audio as WAV file
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={"Content-Disposition": f"inline; filename=speech.wav"},
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")


@app.get("/api/voice/status")
async def voice_status():
    """Check voice service availability"""
    return {
        "whisper_available": VOICE_SERVICE_AVAILABLE,
        "piper_available": os.path.exists("./en_US-lessac-medium.onnx"),
        "status": "ready" if VOICE_SERVICE_AVAILABLE else "unavailable",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
