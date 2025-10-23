from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
import requests
import os
from dotenv import load_dotenv
import json
import asyncio
import numpy as np

# Load environment variables from .env file
load_dotenv()
# Removed heavy ML imports - focusing on gpt-oss only
import pandas as pd
from pydantic import BaseModel
from typing import Tuple, Dict, List
import re
import io
from typing import Any, Optional
from datetime import datetime
from src.analysis.enhanced_visualisation import (
    create_sentiment_dashboard_plotly,
    create_emotion_dashboard_plotly,
)
from src.analysis.sentiment_dashboard_tabs import build_dashboard_tabbed
from src.analysis.circumplex_plot import create_circumplex_plot
from src.analysis.distortion_detection import detect_distortions
from fastapi.responses import HTMLResponse, StreamingResponse
from src.analysis.emotion_mapping import modernbert_va_map
from src.graphs.framework_analysis import process_therapy_session
from src.graphs.create_kg import process_kg_creation
from src.ui.langgraph_chat import create_chat_app
from src.voice_service_faster import faster_whisper_service

# for the whisperx version
# from src.voice_service import voice_service
import gradio as gr
import math
import io

# Removed torch configuration - focusing on gpt-oss only

# Initialize FastAPI app
app = FastAPI(
    title="SentimentSuite", description="AI-Powered Therapy Analysis Platform"
)

# Mount Gradio chat interface
try:
    chat_app = create_chat_app()
    app = gr.mount_gradio_app(app, chat_app, path="/chat")
    print("✅ Gradio chat interface mounted at /chat")
except Exception as e:
    print(f"❌ Error mounting Gradio app: {e}")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Main homepage with navigation to all features"""
    return """
        <html>
            <head>
                <title>SentimentSuite - AI Therapy Analysis Platform</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 900px;
                        margin: 0 auto;
                        padding: 20px;
                        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
                        color: white;
                        min-height: 100vh;
                    }
                    .header {
                        text-align: center;
                        margin-bottom: 40px;
                        padding: 20px;
                        background: rgba(45, 45, 45, 0.8);
                        border-radius: 15px;
                        border: 2px solid #4CAF50;
                    }
                    .header h1 {
                        font-size: 2.5em;
                        margin: 0;
                        color: #4CAF50;
                    }
                    .header p {
                        font-size: 1.2em;
                        margin: 10px 0 0 0;
                        color: #ccc;
                    }
                    .features {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 20px;
                        margin: 30px 0;
                    }
                    .feature-card {
                        background: #3d3d3d;
                        padding: 25px;
                        border-radius: 10px;
                        border-left: 4px solid #2196F3;
                        transition: transform 0.3s ease;
                    }
                    .feature-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                    }
                    .feature-card.voice {
                        border-left-color: #9C27B0;
                    }
                    .feature-card.therapy {
                        border-left-color: #FF6B35;
                    }
                    .feature-card.sentiment {
                        border-left-color: #4CAF50;
                    }
                    .feature-card h3 {
                        margin: 0 0 15px 0;
                        font-size: 1.4em;
                    }
                    .feature-card p {
                        margin: 10px 0;
                        color: #ccc;
                        line-height: 1.6;
                    }
                    .feature-link {
                        display: inline-block;
                        margin: 15px 10px 5px 0;
                        padding: 10px 20px;
                        background-color: #2196F3;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                    }
                    .feature-link:hover {
                        background-color: #1976D2;
                    }
                    .feature-link.voice { background-color: #9C27B0; }
                    .feature-link.voice:hover { background-color: #7B1FA2; }
                    .feature-link.therapy { background-color: #FF6B35; }
                    .feature-link.therapy:hover { background-color: #E55A2B; }
                    .feature-link.sentiment { background-color: #4CAF50; }
                    .feature-link.sentiment:hover { background-color: #45a049; }
                    .status {
                        background: #2d2d2d;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                        border-left: 4px solid #4CAF50;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🧠 SentimentSuite</h1>
                    <p>AI-Powered Therapy Analysis Platform</p>
                </div>

                <div class="status">
                    <strong>🎤 Voice Features:</strong> Enabled with WhisperX Large-v3 + Piper TTS<br>
                    <strong>🤖 Analysis Engine:</strong> Hybrid Graph-RAG with LangGraph<br>
                    <strong>📊 Visualization:</strong> Advanced sentiment & emotion dashboards
                </div>

                <div class="features">
                    <div class="feature-card voice">
                        <h3>💬 Voice-Enabled Chat</h3>
                        <p>Interactive chat interface with speech-to-text and text-to-speech capabilities. Query your therapy data using voice commands and receive spoken responses.</p>
                        <p><strong>Features:</strong></p>
                        <ul>
                            <li>🎤 Voice input with Whisper Large-v3</li>
                            <li>🔊 Text-to-speech responses</li>
                            <li>🧠 Hybrid Graph-RAG integration</li>
                        </ul>
                        <a href="/chat" class="feature-link voice">Launch Chat Interface</a>
                    </div>

                    <div class="feature-card therapy">
                        <h3>🧠 Therapy Analysis</h3>
                        <p>Upload therapy session transcripts for comprehensive psychological analysis using multiple frameworks including Big Five, attachment styles, and cognitive distortions.</p>
                        <p><strong>Analysis Types:</strong></p>
                        <ul>
                            <li>📋 Psychological frameworks</li>
                            <li>🕸️ Knowledge graph creation</li>
                            <li>🔍 Vector embeddings</li>
                        </ul>
                        <a href="/upload-therapy-csv" class="feature-link therapy">Upload Therapy Data</a>
                        <a href="/psychological-results" class="feature-link therapy">View Results</a>
                    </div>

                    <div class="feature-card sentiment">
                        <h3>📊 Sentiment Analysis</h3>
                        <p>Analyze emotional content in text using multiple AI models. Generate comprehensive dashboards with valence-arousal mapping and emotion distribution analysis.</p>
                        <p><strong>Models Available:</strong></p>
                        <ul>
                            <li>🤖 Nous-Hermes LLM</li>
                            <li>🎯 ModernBERT classification</li>
                            <li>📈 Custom circumplex plotting</li>
                        </ul>
                        <a href="/upload-csv" class="feature-link sentiment">Sentiment Analysis</a>
                        <a href="/dashboard_all" class="feature-link sentiment">View Dashboard</a>
                    </div>
                </div>

                <div class="status">
                    <strong>🚀 Quick Start:</strong>
                    <a href="/chat" style="color: #9C27B0;">Try Voice Chat</a> |
                    <a href="/upload-therapy-csv" style="color: #FF6B35;">Upload Therapy Data</a> |
                    <a href="/dashboard_all" style="color: #4CAF50;">View Results</a>
                </div>
            </body>
        </html>
    """


# Updated the Sentiment2D class with
# more emotions and patterns
class Sentiment2D:
    def __init__(self):
        """Initialize the sentiment analyzer with expanded emotion keywords and their values"""
        self.emotion_map = {
            # Basic emotions
            "happy": (0.8, 0.5),
            "sad": (-0.6, -0.4),
            "angry": (-0.6, 0.8),
            "calm": (0.3, -0.6),
            "excited": (0.5, 0.8),
            "nervous": (-0.3, 0.7),
            "peaceful": (0.4, -0.7),
            "gloomy": (-0.5, -0.5),
            # Additional emotions and phrases to fit the forge
            "welcome": (0.6, 0.2),
            "problem": (-0.4, 0.3),
            "inform": (0.1, -0.2),
            "await": (0.0, 0.3),
            "service": (0.4, 0.0),
            "expletive": (-0.5, 0.6),
            "good": (0.7, 0.3),
            "bad": (-0.7, 0.3),
            "great": (0.8, 0.4),
            "terrible": (-0.8, 0.5),
            "wonderful": (0.9, 0.5),
            "awful": (-0.8, 0.4),
            "pleasant": (0.6, -0.2),
            "unpleasant": (-0.6, 0.2),
            "system": (0.0, -0.3),
            "leave": (-0.2, 0.1),
        }

        # Enhanced pattern matching
        self.patterns = {}
        for emotion in self.emotion_map:
            # Create patterns that match word boundaries and handle potential plurals
            pattern = r"\b" + emotion + r"(?:s|es|ing|ed)?\b"
            self.patterns[emotion] = re.compile(pattern, re.IGNORECASE)

    def get_utterance_class_scores(self, utterance: str) -> Dict[str, float]:
        """Calculate emotion scores with improved matching
        :type utterance: str
        """
        scores = {}
        utterance.lower().split()

        # Initialize all emotions with a small baseline value
        for emotion in self.emotion_map:
            scores[emotion] = 0.01  # Small baseline to avoid complete neutrality

        for emotion, pattern in self.patterns.items():
            # Count occurrences and weight them
            count = len(pattern.findall(utterance))
            if count > 0:
                scores[emotion] = count * 0.5  # Weight the matches

        # Normalize scores
        total = sum(scores.values())
        return {k: v / total for k, v in scores.items()}

    def get_utterance_valence_arousal(self, utterance: str) -> Tuple[float, float]:
        """Calculate valence and arousal with improved weighting"""
        scores = self.get_utterance_class_scores(utterance)

        valence = 0.0
        arousal = 0.0
        total_weight = 0.0

        for emotion, score in scores.items():
            v, a = self.emotion_map[emotion]
            # Apply score as weight
            valence += v * score
            arousal += a * score
            total_weight += score

        # Normalize and ensure non-zero output
        if total_weight > 0:
            valence = valence / total_weight
            arousal = arousal / total_weight
        else:
            valence = 0.0
            arousal = 0.0

        return (valence, arousal)

    def __call__(self, utterance: str) -> Tuple[float, float]:
        """Process the utterance and return valence-arousal pair"""
        return self.get_utterance_valence_arousal(utterance)


# Initialize Sentiment2D
sentiment2d = Sentiment2D()


class SentimentSummary(BaseModel):
    emotion: str
    mean: float
    std: float
    max_val: float
    min_val: float


def build_dashboard_tabbed(model_name: str, data, kind: str = "utterance"):
    if kind == "utterance":
        df = pd.DataFrame(data)
        df["distortions"] = df["utterance"].apply(
            lambda x: ", ".join([d["distortion"] for d in detect_distortions(x)])
            or "None"
        )

        main_figs = create_sentiment_dashboard_plotly(df)
        circ_fig = create_circumplex_plot(df)

        html_parts = [
            f"<h3>Model: {model_name}</h3>",
            f"<p><strong>Distortions Detected:</strong><br><pre style='color:#ccc'>{df[['utterance', 'distortions']].to_string(index=False)}</pre></p>",
            main_figs["scatter"].to_html(full_html=False, include_plotlyjs="cdn"),
            main_figs["valence_hist"].to_html(full_html=False, include_plotlyjs=False),
            main_figs["arousal_hist"].to_html(full_html=False, include_plotlyjs=False),
            circ_fig.to_html(full_html=False, include_plotlyjs=False),
        ]

    elif kind == "summary":
        df = pd.DataFrame(
            [s.__dict__ if isinstance(s, SentimentSummary) else s for s in data]
        )
        summary_figs = create_emotion_dashboard_plotly(df)
        html_parts = [
            f"<h3>Model: {model_name}</h3>",
            summary_figs["box"].to_html(full_html=False, include_plotlyjs="cdn"),
            summary_figs["mean_std"].to_html(full_html=False, include_plotlyjs=False),
            summary_figs["range_bar"].to_html(full_html=False, include_plotlyjs=False),
        ]
    else:
        html_parts = ["<p>Unsupported data type</p>"]

    return "".join(html_parts)


@app.get("/dashboard_all", response_class=HTMLResponse)
def dashboard_all_models():
    from SentimentSuite import analysis_store

    tabs_html = []

    for model_name, result_data in analysis_store.results.items():
        if not result_data:
            continue
        kind = "utterance" if model_name in ["nous-hermes"] else "summary"
        tab_html = build_dashboard_tabbed(model_name, result_data, kind)
        tabs_html.append(
            f"""
            <div class='tab-content' id='{model_name}' style='display:none'>
                <div class="tab-container">
                    {tab_html}
                </div>
            </div>
        """
        )

    buttons = "".join(
        [
            f"<button class='tab-button' onclick=\"showTab('{model}')\">{model.title()}</button>"
            for model in analysis_store.results
            if analysis_store.results[model]
        ]
    )

    return HTMLResponse(
        content=f"""
        <html>
        <head>
            <title>SentimentSuite Dashboard</title>
            <style>
                body {{ 
                    background:#1a1a1a; 
                    color:white; 
                    font-family:sans-serif;
                    margin: 0;
                    padding: 20px;
                }}
                .tab-button {{ 
                    margin:5px; 
                    padding:10px 20px; 
                    background:#2d2d2d; 
                    border:none; 
                    color:white; 
                    cursor:pointer;
                    border-radius: 5px;
                }}
                .tab-button:hover {{ background:#444; }}
                .tab-button.active {{ background:#4a4a8e; }}
                .tab-content {{ 
                    padding: 20px; 
                    background:#0d0c1d; 
                    margin-top: 10px; 
                    border-radius: 10px;
                    width: 100%;
                }}
                .js-plotly-plot {{ 
                    width: 100% !important; 
                    height: 600px !important;
                }}
                pre {{ 
                    white-space: pre-wrap; 
                    word-wrap: break-word;
                    max-height: 300px;
                    overflow-y: auto;
                    background: #2d2d2d;
                    padding: 10px;
                    border-radius: 5px;
                }}
                .dashboard-button {{ 
                    margin-top: 20px; 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background: #2196F3; 
                    color: white; 
                    border: none; 
                    border-radius: 8px; 
                    text-decoration: none; 
                    font-weight: bold; 
                }}
                .dashboard-button:hover {{ background: #1976D2; }}
            </style>
        </head>
        <body>
            <h1>SentimentSuite Dashboard</h1>
            <div class="tab-buttons">{buttons}</div>
            <div style='margin-top:30px;'>
                <a href="/upload-csv" class="dashboard-button">Upload New CSV</a>
            </div>
            <div class="tab-container">{''.join(tabs_html)}</div>

            <script>
                function showTab(id) {{
                    // Update buttons
                    document.querySelectorAll('.tab-button').forEach(btn => {{
                        if (btn.textContent.toLowerCase() === id) {{
                            btn.classList.add('active');
                        }} else {{
                            btn.classList.remove('active');
                        }}
                    }});

                    // Update content
                    document.querySelectorAll('.tab-content').forEach(div => {{
                        div.style.display = 'none';
                    }});
                    const tab = document.getElementById(id);
                    if (tab) {{
                        tab.style.display = 'block';
                        // Trigger Plotly to resize
                        const plots = tab.getElementsByClassName('js-plotly-plot');
                        for (let plot of plots) {{
                            if (window.Plotly) {{
                                Plotly.relayout(plot, {{
                                    'xaxis.autorange': true,
                                    'yaxis.autorange': true,
                                    'width': plot.offsetWidth,
                                    'height': 600
                                }});
                            }}
                        }}
                    }}
                }}

                // Initialize first tab
                window.onload = () => {{
                    const firstButton = document.querySelector('.tab-button');
                    if (firstButton) {{
                        showTab(firstButton.textContent.toLowerCase());
                    }}
                }};

                // Handle window resize
                window.addEventListener('resize', () => {{
                    const activeTab = document.querySelector('.tab-content[style*="block"]');
                    if (activeTab) {{
                        const plots = activeTab.getElementsByClassName('js-plotly-plot');
                        for (let plot of plots) {{
                            if (window.Plotly) {{
                                Plotly.relayout(plot, {{
                                    'width': plot.offsetWidth,
                                    'height': 600
                                }});
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
    """
    )


# Removed ModernBERT - focusing on gpt-oss only
classifier = None


class SentimentSummary(BaseModel):
    emotion: str
    mean: float
    std: float
    max_val: float
    min_val: float


# Add this class to store analysis results
class AnalysisResults:
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.timestamp: Optional[datetime] = None


analysis_store = AnalysisResults()
analysis_store.results = {"modernbert": [], "nous-hermes": [], "psychological": {}}


def infer_emotion_from_va(valence: float, arousal: float) -> str:
    """
    Match a valence/arousal pair to the closest ModernBERT emotion using Euclidean distance.
    """
    closest = "neutral"
    min_dist = float("inf")
    for emotion, (vx, vy) in modernbert_va_map.items():
        dist = math.sqrt((valence - vx) ** 2 + (arousal - vy) ** 2)
        if dist < min_dist:
            min_dist = dist
            closest = emotion
    return closest


@app.post("/analyze/nous-hermes")
def analyze_nous_hermes(file: UploadFile = File(...)):
    content = file.file.read()
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))
    df.columns = [c.strip().lower() for c in df.columns]
    if "utterance" not in df.columns:
        raise HTTPException(
            status_code=400, detail="CSV must contain an 'utterance' column"
        )

    speaker_col = "speaker" if "speaker" in df.columns else None
    results = []

    utterances = df["utterance"]

    for _, row in df.iterrows():
        utt = row["utterance"]
        speaker = row[speaker_col] if speaker_col else None
        try:
            # First try the Nous-Hermes server
            payload = {
                "prompt": f"Analyze the emotional tone of: '{utt}' and return in format: {{valence: float, arousal: float}}.",
                "temperature": 0.7,
                "max_tokens": 200,
            }

            try:
                # Try to connect to Nous-Hermes with a short timeout
                response = requests.post(
                    "http://localhost:1234/v1/completions",
                    json=payload,
                    timeout=1,  # 1 second timeout
                )
                response_data = response.json()
                record = {
                    "utterance": utt,
                    "model": "nous-hermes",
                    "raw_output": response_data.get("choices", [{}])[0].get("text", ""),
                }
                if speaker_col:
                    record["speaker"] = speaker
                results.append(record)
            except (requests.exceptions.RequestException, KeyError):

                # If Nous-Hermes fails, fallback to our Sentiment2D
                valence, arousal = sentiment2d(utt)
                emotion = infer_emotion_from_va(valence, arousal)
                record = {
                    "utterance": utt,
                    "model": "sentiment2d-fallback",
                    "valence": round(valence, 3),
                    "arousal": round(arousal, 3),
                    "emotion": emotion,
                }
                if speaker_col:
                    record["speaker"] = speaker
                results.append(record)
        except Exception as e:
            record = {"utterance": utt, "model": "error", "error": str(e)}
            if speaker_col:
                record["speaker"] = speaker
            results.append(record)

    # Store the results before returning
    analysis_store.results["nous-hermes"] = results
    analysis_store.timestamp = datetime.now()
    return results


@app.get("/upload-csv", response_class=HTMLResponse)
async def upload_form():
    return """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #1a1a1a;
                        color: white;
                    }
                    .upload-form {
                        border: 2px dashed #ccc;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        background: #2d2d2d;
                    }
                    .submit-btn {
                        margin-top: 10px;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    .method-select {
                        margin: 10px 0;
                        padding: 5px;
                        border-radius: 5px;
                    }
                    #results {
                        margin-top: 20px;
                        padding: 10px;
                        background: #3d3d3d;
                        border-radius: 5px;
                        white-space: pre-wrap;
                        max-height: 300px;
                        overflow-y: auto;
                    }
                    .view-dashboard {
                        display: inline-block;
                        margin: 10px 0;
                        padding: 10px 20px;
                        background-color: #2196F3;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                    .button-container {
                        margin: 20px 0;
                    }
                    .nav-tabs {
                        display: flex;
                        background: #2d2d2d;
                        border-radius: 10px 10px 0 0;
                        margin-bottom: 20px;
                        overflow: hidden;
                    }
                    .nav-tab {
                        flex: 1;
                        padding: 15px 20px;
                        text-align: center;
                        background: #3d3d3d;
                        border: none;
                        color: white;
                        text-decoration: none;
                        transition: background 0.3s;
                        border-right: 1px solid #555;
                    }
                    .nav-tab:hover {
                        background: #4d4d4d;
                    }
                    .nav-tab.active {
                        background: #4CAF50;
                    }
                    .nav-tab:last-child {
                        border-right: none;
                    }
                </style>
            </head>
            <body>
                <div class="nav-tabs">
                    <a href="/upload-csv" class="nav-tab active">📊 Sentiment Analysis</a>
                    <a href="/upload-therapy-csv" class="nav-tab">🧠 Therapy Analysis</a>
                    <a href="/chat" class="nav-tab">💬 Chat Agent</a>
                    <a href="/psychological-results" class="nav-tab">📈 Results</a>
                </div>
                <h2>Upload CSV File for Sentiment Analysis</h2>
                <div class="upload-form">
                    <form id="uploadForm" enctype="multipart/form-data">
                        <select name="method" class="method-select">
                            <option value="nous-hermes">Nous-Hermes Analysis</option>
                            <option value="modernbert">ModernBERT Analysis</option>
                        </select>
                        <br>
                        <input name="file" type="file" accept=".csv">
                        <br>
                        <div class="button-container">
                            <button type="submit" class="submit-btn">Upload and Analyze</button>
                            <a href="/dashboard_all" class="view-dashboard">View Dashboard</a>
                            <button type="button" class="submit-btn" onclick="createGraph()" style="background-color: #FF6B35;">Create Graph</button>
                        </div>
                    </form>
                    <div id="results"></div>
                </div>

                <script>
                    document.getElementById('uploadForm').onsubmit = async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const method = formData.get('method');
                        let endpoint = '';

                        switch(method) {
                            case 'nous-hermes': endpoint = '/analyze/nous-hermes'; break;
                            case 'modernbert': endpoint = '/upload-csv-process'; break;
                        }

                        try {
                            const response = await fetch(endpoint, {
                                method: 'POST',
                                body: formData
                            });
                            const data = await response.json();
                            document.getElementById('results').innerHTML =
                                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                        } catch (error) {
                            document.getElementById('results').innerHTML =
                                '<p style="color: red;">Error: ' + error.message + '</p>';
                        }
                    };

                    async function createGraph() {
                        // Show loading message
                        document.getElementById('results').innerHTML = '<p style="color: #FF6B35;">Creating knowledge graph... This may take several minutes.</p>';
                        
                        try {
                            const response = await fetch('/create-graph', {
                                method: 'POST'
                            });
                            const data = await response.json();
                            
                            if (data.status === 'completed') {
                                document.getElementById('results').innerHTML = 
                                    `<p style="color: #4CAF50;">Knowledge graph creation completed!</p>
                                     <p>Total Analyses: ${data.total_analyses}</p>
                                     <p>Successful: ${data.successful}</p>
                                     <p>Errors: ${data.errors}</p>
                                     <a href="/graph-results" style="color: #2196F3; text-decoration: underline;">View graph results</a>`;
                            } else {
                                document.getElementById('results').innerHTML = 
                                    '<p style="color: red;">Graph creation failed: ' + (data.error || 'Unknown error') + '</p>';
                            }
                        } catch (error) {
                            document.getElementById('results').innerHTML =
                                '<p style="color: red;">Error: ' + error.message + '</p>';
                        }
                    }
                </script>
            </body>
        </html>
    """


@app.post("/upload-csv-process", response_model=List[SentimentSummary])
async def upload_csv_process(file: UploadFile = File(...)):
    if classifier is None:
        raise HTTPException(
            status_code=503,
            detail="ModernBERT model not available. Please ensure the model is properly installed.",
        )

    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))

        all_scores = {}
        for row in df["utterance"]:
            try:
                outputs = classifier(row)[0]
                for item in outputs:
                    label = item["label"]
                    score = item["score"]
                    all_scores.setdefault(label, []).append(score)
            except Exception as e:
                print(f"Error processing row: {row}, Error: {str(e)}")
                continue

        summary = []
        for emotion, values in all_scores.items():
            if values:
                series = pd.Series(values)
                try:
                    mean_val = float(series.mean())
                    std_val = float(series.std())
                    max_val = float(series.max())
                    min_val = float(series.min())
                    if all(
                        abs(x) < 1e308 for x in [mean_val, std_val, max_val, min_val]
                    ):
                        summary.append(
                            SentimentSummary(
                                emotion=emotion,
                                mean=mean_val,
                                std=std_val,
                                max_val=max_val,
                                min_val=min_val,
                            )
                        )
                except Exception as e:
                    print(f"Error calculating stats for emotion {emotion}: {str(e)}")
                    continue

        if not summary:
            return []

        analysis_store.results["modernbert"] = summary
        analysis_store.timestamp = datetime.now()
        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/psychological")
async def analyze_psychological(file: UploadFile = File(...)):
    """
    Process therapy CSV through LangGraph psychological analysis workflow.
    """
    try:
        content = await file.read()
        csv_content = content.decode("utf-8")

        # Process the therapy session
        results = process_therapy_session(csv_content)

        # Store results
        analysis_store.results["psychological"] = results
        analysis_store.timestamp = datetime.now()

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing psychological analysis: {str(e)}"
        )


@app.get("/upload-therapy-csv", response_class=HTMLResponse)
async def upload_therapy_form():
    """
    Upload form specifically for therapy CSV files for psychological analysis.
    """
    return """
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #1a1a1a;
                        color: white;
                    }
                    .upload-form {
                        border: 2px dashed #ccc;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        background: #2d2d2d;
                    }
                    .submit-btn {
                        margin-top: 10px;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    #results {
                        margin-top: 20px;
                        padding: 10px;
                        background: #3d3d3d;
                        border-radius: 5px;
                        white-space: pre-wrap;
                        max-height: 400px;
                        overflow-y: auto;
                    }
                    .view-dashboard {
                        display: inline-block;
                        margin: 10px 5px;
                        padding: 10px 20px;
                        background-color: #2196F3;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                    .button-container {
                        margin: 20px 0;
                    }
                    .info-box {
                        background: #3d3d3d;
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                        border-left: 4px solid #2196F3;
                    }
                    .nav-tabs {
                        display: flex;
                        background: #2d2d2d;
                        border-radius: 10px 10px 0 0;
                        margin-bottom: 20px;
                        overflow: hidden;
                    }
                    .nav-tab {
                        flex: 1;
                        padding: 15px 20px;
                        text-align: center;
                        background: #3d3d3d;
                        border: none;
                        color: white;
                        text-decoration: none;
                        transition: background 0.3s;
                        border-right: 1px solid #555;
                    }
                    .nav-tab:hover {
                        background: #4d4d4d;
                    }
                    .nav-tab.active {
                        background: #4CAF50;
                    }
                    .nav-tab:last-child {
                        border-right: none;
                    }
                </style>
            </head>
            <body>
                <div class="nav-tabs">
                    <a href="/upload-csv" class="nav-tab">📊 Sentiment Analysis</a>
                    <a href="/upload-therapy-csv" class="nav-tab active">🧠 Therapy Analysis</a>
                    <a href="/chat" class="nav-tab">💬 Chat Agent</a>
                    <a href="/psychological-results" class="nav-tab">📈 Results</a>
                </div>
                <h2>Upload Therapy CSV for Psychological Analysis</h2>
                <div class="info-box">
                    <p><strong>CSV Format Required:</strong></p>
                    <p>Columns: <code>Therapist</code>, <code>Client</code>, <code>message_id</code></p>
                    <p>This will process each QA pair through LangGraph with psychological frameworks including Big Five, attachment styles, cognitive distortions, and more.</p>
                </div>
                <div class="upload-form">
                    <form id="uploadForm" enctype="multipart/form-data">
                        <input name="file" type="file" accept=".csv">
                        <br>
                        <div class="button-container">
                            <button type="submit" class="submit-btn">Upload and Analyze</button>
                            <a href="/psychological-results" class="view-dashboard">View Results</a>
                            <button type="button" class="submit-btn" onclick="createGraph()" style="background-color: #FF6B35;">Create Graph</button>
                            <button type="button" class="submit-btn" onclick="createEmbeddings()" style="background-color: #9C27B0;">Create Embeddings</button>
                            <a href="/upload-csv" class="view-dashboard">Regular Analysis</a>
                        </div>
                    </form>
                    <div id="results"></div>
                </div>

                <script>
                    document.getElementById('uploadForm').onsubmit = async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);

                        // Show loading message
                        document.getElementById('results').innerHTML = '<p style="color: #2196F3;">Processing... This may take several minutes for large files.</p>';

                        try {
                            const response = await fetch('/analyze/psychological', {
                                method: 'POST',
                                body: formData
                            });
                            const data = await response.json();

                            if (data.status === 'completed') {
                                document.getElementById('results').innerHTML =
                                    `<p style="color: #4CAF50;">Analysis completed successfully!</p>
                                     <p>Total QA pairs: ${data.total_pairs}</p>
                                     <p>Successful: ${data.successful}</p>
                                     <p>Errors: ${data.errors}</p>
                                     <a href="/psychological-results" style="color: #2196F3; text-decoration: underline;">View detailed results</a>`;
                            } else {
                                document.getElementById('results').innerHTML =
                                    '<p style="color: red;">Analysis failed: ' + (data.error || 'Unknown error') + '</p>';
                            }
                        } catch (error) {
                            document.getElementById('results').innerHTML =
                                '<p style="color: red;">Error: ' + error.message + '</p>';
                        }
                    };

                    async function createGraph() {
                        // Show loading message
                        document.getElementById('results').innerHTML = '<p style="color: #FF6B35;">Creating knowledge graph... This may take several minutes.</p>';

                        try {
                            const response = await fetch('/create-graph', {
                                method: 'POST'
                            });
                            const data = await response.json();

                            if (data.status === 'completed') {
                                document.getElementById('results').innerHTML =
                                    `<p style="color: #4CAF50;">Knowledge graph creation completed!</p>
                                     <p>Total Analyses: ${data.total_analyses}</p>
                                     <p>Successful: ${data.successful}</p>
                                     <p>Errors: ${data.errors}</p>
                                     <a href="/graph-results" style="color: #2196F3; text-decoration: underline;">View graph results</a>`;
                            } else {
                                document.getElementById('results').innerHTML =
                                    '<p style="color: red;">Graph creation failed: ' + (data.error || 'Unknown error') + '</p>';
                            }
                        } catch (error) {
                            document.getElementById('results').innerHTML =
                                '<p style="color: red;">Error: ' + error.message + '</p>';
                        }
                    }

                    async function createEmbeddings() {
                        // Get the file from the form
                        const fileInput = document.querySelector('input[name="file"]');
                        if (!fileInput.files[0]) {
                            document.getElementById('results').innerHTML = '<p style="color: red;">Please select a CSV file first.</p>';
                            return;
                        }

                        // Show loading message
                        document.getElementById('results').innerHTML = '<p style="color: #9C27B0;">Creating embeddings... This may take several minutes.</p>';

                        try {
                            const formData = new FormData();
                            formData.append('file', fileInput.files[0]);

                            const response = await fetch('/analyze/embeddings', {
                                method: 'POST',
                                body: formData
                            });
                            const data = await response.json();

                            if (data.status === 'completed') {
                                document.getElementById('results').innerHTML =
                                    `<p style="color: #4CAF50;">Embedding creation completed!</p>
                                     <p>Total QA pairs: ${data.total_pairs}</p>
                                     <p>Successful: ${data.successful}</p>
                                     <p>Errors: ${data.errors}</p>
                                     <p style="color: #9C27B0;">Embeddings have been generated and saved for vector search.</p>`;
                            } else {
                                document.getElementById('results').innerHTML =
                                    '<p style="color: red;">Embedding creation failed: ' + (data.error || 'Unknown error') + '</p>';
                            }
                        } catch (error) {
                            document.getElementById('results').innerHTML =
                                '<p style="color: red;">Error: ' + error.message + '</p>';
                        }
                    }
                </script>
            </body>
        </html>
    """


@app.get("/psychological-results", response_class=HTMLResponse)
async def psychological_results():
    """
    Display psychological analysis results with download functionality.
    """
    if (
        "psychological" not in analysis_store.results
        or not analysis_store.results["psychological"]
    ):
        return HTMLResponse(
            content="""
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a1a; color: white; }
                        .error { background: #3d2d2d; padding: 20px; border-radius: 10px; border-left: 4px solid #ff4444; }
                        .button { display: inline-block; margin: 10px 0; padding: 10px 20px; background-color: #2196F3; color: white; text-decoration: none; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <div class="error">
                        <h2>No Results Found</h2>
                        <p>No psychological analysis results available. Please upload and analyze a therapy CSV file first.</p>
                        <a href="/upload-therapy-csv" class="button">Upload Therapy CSV</a>
                    </div>
                </body>
            </html>
        """
        )

    results = analysis_store.results["psychological"]
    timestamp_str = (
        analysis_store.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if analysis_store.timestamp
        else "Unknown"
    )

    # Generate summary statistics
    summary_html = f"""
        <div class="summary">
            <h3>Analysis Summary</h3>
            <p><strong>Total QA Pairs:</strong> {results.get('total_pairs', 0)}</p>
            <p><strong>Successfully Processed:</strong> {results.get('successful', 0)}</p>
            <p><strong>Errors:</strong> {results.get('errors', 0)}</p>
            <p><strong>Processing Time:</strong> {timestamp_str}</p>
        </div>
    """

    # Generate results table
    results_html = "<div class='results-table'><h3>Individual Results</h3>"
    if "results" in results:
        for i, result in enumerate(results["results"][:10]):  # Show first 10
            status_color = "#4CAF50" if result["status"] == "success" else "#ff4444"
            results_html += f"""
                <div class="result-item">
                    <h4>QA Pair {result.get('qa_id', i+1)} <span style="color: {status_color};">({result['status']})</span></h4>
                    <p><strong>Question:</strong> {result.get('question', '')[:200]}...</p>
                    <p><strong>Answer:</strong> {result.get('answer', '')[:200]}...</p>
                </div>
            """
        if len(results["results"]) > 10:
            results_html += (
                f"<p><em>... and {len(results['results']) - 10} more results</em></p>"
            )
    results_html += "</div>"

    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>Psychological Analysis Results</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #1a1a1a;
                        color: white;
                    }}
                    .summary {{
                        background: #2d2d2d;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        border-left: 4px solid #2196F3;
                    }}
                    .results-table {{
                        background: #2d2d2d;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .result-item {{
                        background: #3d3d3d;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 5px;
                    }}
                    .button {{
                        display: inline-block;
                        margin: 10px 5px;
                        padding: 10px 20px;
                        background-color: #2196F3;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .button.download {{ background-color: #4CAF50; }}
                    .button-container {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Psychological Analysis Results</h1>
                
                {summary_html}
                
                <div class="button-container">
                    <a href="/download-psychological-results" class="button download">Download Results</a>
                    <a href="/upload-therapy-csv" class="button">New Analysis</a>
                    <a href="/dashboard_all" class="button">Sentiment Dashboard</a>
                </div>
                
                {results_html}
            </body>
        </html>
    """
    )


@app.get("/download-psychological-results")
async def download_psychological_results():
    """
    Download the psychological analysis results as a text file.
    """
    if (
        "psychological" not in analysis_store.results
        or not analysis_store.results["psychological"]
    ):
        raise HTTPException(
            status_code=404, detail="No psychological analysis results found"
        )

    from fastapi.responses import Response

    # Extract just the serializable data, filtering out LangGraph objects
    results = analysis_store.results["psychological"]

    # Create a clean summary for download
    download_content = f"""Psychological Analysis Results
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total QA Pairs: {results.get('total_pairs', 0)}
Successfully Processed: {results.get('successful', 0)}
Errors: {results.get('errors', 0)}

=== ANALYSIS RESULTS ===

"""

    # Add each QA pair result
    if "results" in results:
        for i, result in enumerate(results["results"], 1):
            download_content += f"\n--- QA Pair {result.get('qa_id', i)} ---\n"
            download_content += f"Question: {result.get('question', 'N/A')}\n"
            download_content += f"Answer: {result.get('answer', 'N/A')[:200]}...\n"
            download_content += f"Status: {result.get('status', 'unknown')}\n"
            if result.get("status") == "error":
                download_content += f"Error: {result.get('error', 'N/A')}\n"
            download_content += "\n"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"psychological_analysis_{timestamp}.txt"

    response = Response(
        content=download_content,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    return response


@app.post("/create-graph")
async def create_knowledge_graph():
    """
    Process the psychological analysis master file and create knowledge graph Cypher queries.
    """
    try:
        results = process_kg_creation()

        # Store results in analysis_store for later viewing
        analysis_store.results["knowledge_graph"] = results
        analysis_store.timestamp = datetime.now()

        return results

    except Exception as e:
        return {"error": str(e), "status": "failed"}


@app.post("/analyze/embeddings")
async def create_embeddings():
    """
    Create embeddings for the knowledge graph (same as create-graph).
    This endpoint exists for compatibility with the embeddings button.
    """
    try:
        results = process_kg_creation()

        # Store results in analysis_store for later viewing
        analysis_store.results["knowledge_graph"] = results
        analysis_store.timestamp = datetime.now()

        return results

    except Exception as e:
        return {"error": str(e), "status": "failed"}


@app.get("/graph-results", response_class=HTMLResponse)
async def graph_results():
    """
    Display knowledge graph creation results.
    """
    if (
        "knowledge_graph" not in analysis_store.results
        or not analysis_store.results["knowledge_graph"]
    ):
        return HTMLResponse(
            content="""
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a1a; color: white; }
                        .error { background: #3d2d2d; padding: 20px; border-radius: 10px; border-left: 4px solid #ff4444; }
                        .button { display: inline-block; margin: 10px 0; padding: 10px 20px; background-color: #2196F3; color: white; text-decoration: none; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <div class="error">
                        <h2>No Graph Results Found</h2>
                        <p>No knowledge graph creation results available. Please create a graph first.</p>
                        <a href="/upload-csv" class="button">Create Knowledge Graph</a>
                    </div>
                </body>
            </html>
        """
        )

    results = analysis_store.results["knowledge_graph"]
    timestamp_str = (
        analysis_store.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if analysis_store.timestamp
        else "Unknown"
    )

    # Generate summary statistics
    summary_html = f"""
        <div class="summary">
            <h3>Graph Creation Summary</h3>
            <p><strong>Total Analyses:</strong> {results.get('total_analyses', 0)}</p>
            <p><strong>Successfully Processed:</strong> {results.get('successful', 0)}</p>
            <p><strong>Errors:</strong> {results.get('errors', 0)}</p>
            <p><strong>Processing Time:</strong> {timestamp_str}</p>
        </div>
    """

    # Generate results table
    results_html = "<div class='results-table'><h3>Individual Results</h3>"
    if "results" in results:
        for i, result in enumerate(results["results"][:10]):  # Show first 10
            status_color = "#4CAF50" if result["status"] == "success" else "#ff4444"
            results_html += f"""
                <div class="result-item">
                    <h4>Analysis {result.get('analysis_id', i+1)} <span style="color: {status_color};">({result['status']})</span></h4>
                    <p><strong>Content:</strong> {result.get('content', 'N/A')}</p>
                </div>
            """
        if len(results["results"]) > 10:
            results_html += (
                f"<p><em>... and {len(results['results']) - 10} more results</em></p>"
            )
    results_html += "</div>"

    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>Knowledge Graph Results</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #1a1a1a;
                        color: white;
                    }}
                    .summary {{
                        background: #2d2d2d;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        border-left: 4px solid #FF6B35;
                    }}
                    .results-table {{
                        background: #2d2d2d;
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }}
                    .result-item {{
                        background: #3d3d3d;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 5px;
                    }}
                    .button {{
                        display: inline-block;
                        margin: 10px 5px;
                        padding: 10px 20px;
                        background-color: #2196F3;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .button.orange {{ background-color: #FF6B35; }}
                    .button-container {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Knowledge Graph Creation Results</h1>
                
                {summary_html}
                
                <div class="button-container">
                    <a href="/upload-csv" class="button orange">Create New Graph</a>
                    <a href="/dashboard_all" class="button">Sentiment Dashboard</a>
                </div>
                
                {results_html}
            </body>
        </html>
    """
    )


def create_sentiment_dashboard(data):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # Create figure
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Convert data to DataFrame if it's not already
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(
            [
                {
                    "utterance": item["utterance"],
                    "valence": item.get("valence", 0),
                    "arousal": item.get("arousal", 0),
                }
                for item in data
                if "utterance" in item
            ]
        )
    else:
        df = data

    # 1. Valence-Arousal Scatter Plot
    ax1 = fig.add_subplot(gs[0, :])
    scatter = ax1.scatter(
        df["valence"], df["arousal"], c=np.arange(len(df)), cmap="viridis", s=100
    )
    ax1.set_title("Valence-Arousal Space")
    ax1.set_xlabel("Valence")
    ax1.set_ylabel("Arousal")

    # Set specific axis limits
    ax1.set_xlim(-0.37, 0.28)
    ax1.set_ylim(df["arousal"].min() - 0.1, df["arousal"].max() + 0.1)

    ax1.axhline(y=0, color="gray", linestyle="-", alpha=0.3)
    ax1.axvline(x=0, color="gray", linestyle="-", alpha=0.3)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label("Utter")

    # Add tooltips with smaller font and adjusted position
    for i, txt in enumerate(df["utterance"]):
        shortened_text = txt[:20] + "..." if len(txt) > 20 else txt
        ax1.annotate(
            shortened_text,
            (df["valence"].iloc[i], df["arousal"].iloc[i]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,  # Smaller font size
            alpha=0.8,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
        )

    # 2. Valence Distribution
    ax2 = fig.add_subplot(gs[1, 0])
    sns.histplot(data=df, x="valence", kde=True, ax=ax2)
    ax2.set_title("Valence Distribution")

    # 3. Arousal Distribution
    ax3 = fig.add_subplot(gs[1, 1])
    sns.histplot(data=df, x="arousal", kde=True, ax=ax3)
    ax3.set_title("Arousal Distribution")

    plt.tight_layout()
    return fig


def create_emotion_dashboard(data):
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Create figure
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Convert data to DataFrame if it's not already
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(
            [
                {
                    "emotion": item.emotion,
                    "mean": item.mean,
                    "std": item.std,
                    "max_val": item.max_val,
                    "min_val": item.min_val,
                }
                for item in data
            ]
        )
    else:
        df = data

    # 1. Boxplot of emotion statistics
    ax1 = fig.add_subplot(gs[0, :])
    df_melted = pd.melt(
        df, id_vars=["emotion"], value_vars=["mean", "std", "max_val", "min_val"]
    )
    sns.boxplot(data=df_melted, x="emotion", y="value", hue="variable", ax=ax1)
    ax1.set_title("Distribution of Emotion Statistics")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    # 2. Mean vs Std scatter with adjusted legend
    ax2 = fig.add_subplot(gs[1, 0])
    scatter = sns.scatterplot(data=df, x="mean", y="std", ax=ax2, s=100, hue="emotion")
    # Move legend outside the plot
    ax2.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
    ax2.set_title("Mean vs Standard Deviation")

    # 3. Range plot
    ax3 = fig.add_subplot(gs[1, 1])
    df["range"] = df["max_val"] - df["min_val"]
    sns.barplot(data=df, x="emotion", y="range", ax=ax3)
    ax3.set_title("Emotion Range (Max - Min)")
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)

    plt.tight_layout()
    return fig


# Update the dashboard endpoint
@app.get("/dashboard/{analysis_type}")
async def get_dashboard(analysis_type: str):
    if analysis_type not in analysis_store.results:
        raise HTTPException(
            status_code=404,
            detail=f"No {analysis_type} analysis results found. Please run analysis first.",
        )

    # Get the latest analysis results
    if analysis_type == "modernbert":
        figs = create_emotion_dashboard_plotly(analysis_store.results[analysis_type])
        html_parts = [
            figs["box"].to_html(full_html=False, include_plotlyjs="cdn"),
            figs["mean_std"].to_html(full_html=False, include_plotlyjs=False),
            figs["range_bar"].to_html(full_html=False, include_plotlyjs=False),
        ]
    else:  # nous-hermes
        figs = create_sentiment_dashboard_plotly(analysis_store.results[analysis_type])
        html_parts = [
            figs["scatter"].to_html(full_html=False, include_plotlyjs="cdn"),
            figs["valence_hist"].to_html(full_html=False, include_plotlyjs=False),
            figs["arousal_hist"].to_html(full_html=False, include_plotlyjs=False),
        ]

        # Convert plot to base64 string
        """ buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode()"""

        # Create HTML with timestamp
        timestamp_str = (
            analysis_store.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if analysis_store.timestamp
            else "Unknown"
        )
        html_content = f"""
            <html>
                <head>
                    <title>Sentiment Analysis Dashboard</title>
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 20px;
                            background: #1a1a1a;
                            color: white;
                        }}
                        .dashboard {{
                            max-width: 1200px;
                            margin: 0 auto;
                            background: #2d2d2d;
                            padding: 20px;
                            border-radius: 10px;
                        }}
                        img {{
                            width: 100%;
                            height: auto;
                        }}
                        .timestamp {{
                            color: #888;
                            font-size: 0.8em;
                            margin-top: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="dashboard">
                        <h1>{analysis_type.title()} Analysis Dashboard</h1>
                          {"".join(html_parts)}
                        <div class="timestamp">Last analyzed: {timestamp_str}</div>
                    </div>
                </body>
            </html>
        """
        return HTMLResponse(content=html_content)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_home():
    return """
        <html>
            <head>
                <title>Sentiment Analysis Dashboard</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: #1a1a1a;
                        color: white;
                    }
                    .dashboard-links {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #2d2d2d;
                        border-radius: 10px;
                    }
                    .dashboard-link {
                        display: block;
                        margin: 10px 0;
                        padding: 10px;
                        background: #3d3d3d;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                    .dashboard-link:hover {
                        background: #4d4d4d;
                    }
                </style>
            </head>
            <body>
                <div class="dashboard-links">
                    <h1>Sentiment Analysis Dashboards</h1>
                    <a href="/upload-csv" class="dashboard-link">Upload New Data</a>
                    <a href="/dashboard/modernbert" class="dashboard-link">ModernBERT Dashboard</a>
                    <a href="/dashboard/nous-hermes" class="dashboard-link">Nous-Hermes Dashboard</a>
                </div>
            </body>
        </html>
    """


# WebSocket endpoint for VAD audio streaming
@app.websocket("/ws/vad-stream")
async def vad_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for VAD audio streaming"""
    await websocket.accept()
    print("🎤 VAD WebSocket connection established")

    current_frames = []

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            # Receive data from client
            try:
                data = await websocket.receive()
            except WebSocketDisconnect:
                print("🔌 VAD WebSocket connection closed by client")
                break

            if "bytes" in data:
                # Raw PCM audio data
                pcm_data = np.frombuffer(data["bytes"], dtype=np.int16)
                current_frames.append(pcm_data)

            elif "text" in data:
                # Control message
                try:
                    message = json.loads(data["text"])
                    if message.get("type") == "UTTERANCE_END":
                        print("🎯 Processing utterance from VAD...")

                        if current_frames:
                            # Concatenate all audio frames
                            full_audio = np.concatenate(current_frames)
                            current_frames = []

                            # Create temporary file for transcription
                            import tempfile
                            import soundfile as sf

                            try:
                                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                                    # Convert to float32 for soundfile
                                    audio_float = full_audio.astype(np.float32) / 32768.0
                                    sf.write(tmp_file.name, audio_float, 16000)

                                    # Transcribe using faster-whisper
                                    print(f"🎤 Transcribing {len(audio_float)} samples...")
                                    transcription = faster_whisper_service.transcribe_audio_file(tmp_file.name)

                                    # Clean up temp file
                                    os.unlink(tmp_file.name)

                                    # Only send non-empty transcriptions
                                    if transcription and transcription.strip() and "error" not in transcription.lower():
                                        # Send transcription back to client
                                        if websocket.client_state == WebSocketState.CONNECTED:
                                            await websocket.send_text(json.dumps({
                                                "type": "TRANSCRIPT",
                                                "text": transcription.strip(),
                                                "timestamp": datetime.now().isoformat()
                                            }))
                                            print(f"✅ Sent transcription: '{transcription.strip()}'")
                                    else:
                                        print(f"⚠️ Empty or error transcription: '{transcription}'")
                                        # Send status update instead
                                        if websocket.client_state == WebSocketState.CONNECTED:
                                            await websocket.send_text(json.dumps({
                                                "type": "STATUS",
                                                "message": "No speech detected",
                                                "timestamp": datetime.now().isoformat()
                                            }))

                            except Exception as transcription_error:
                                print(f"❌ Transcription error: {transcription_error}")
                                if websocket.client_state == WebSocketState.CONNECTED:
                                    await websocket.send_text(json.dumps({
                                        "type": "ERROR",
                                        "message": f"Transcription failed: {str(transcription_error)}",
                                        "timestamp": datetime.now().isoformat()
                                    }))

                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON received")

    except WebSocketDisconnect:
        print("🔌 VAD WebSocket connection closed")
    except Exception as e:
        print(f"❌ VAD WebSocket error: {e}")
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()
        except:
            pass  # Ignore close errors

# Voice API endpoints
@app.post("/api/voice/transcribe")
async def transcribe_voice(file: UploadFile = File(...)):
    """Transcribe uploaded audio file to text"""
    try:
        result = await fasterwhisperservice.process_audio_file(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/synthesize")
async def synthesize_voice(text: str):
    """Convert text to speech using Piper and return audio"""
    try:
        import subprocess
        import tempfile
        import os
        from fastapi.responses import FileResponse

        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            output_path = tmp_file.name

        # Piper model path (adjust to your installation)
        piper_model = os.path.expanduser("~/piper/en_GB-alba-medium.onnx")

        # Check if model exists
        if not os.path.exists(piper_model):
            # Try alternative path
            piper_model = "en_GB-alba-medium"  # Let piper find it automatically

        # Run Piper TTS
        print(f"🔊 Generating TTS for: '{text[:50]}...'")
        process = subprocess.run(
            ["piper", "--model", piper_model, "--output_file", output_path],
            input=text,
            text=True,
            capture_output=True,
            timeout=30
        )

        if process.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print("✅ TTS generated successfully")

            # Return the audio file
            async def cleanup():
                try:
                    os.unlink(output_path)
                except:
                    pass

            # Use FileResponse with cleanup
            return FileResponse(
                output_path,
                media_type="audio/wav",
                filename="speech.wav",
                background=cleanup
            )
        else:
            print(f"❌ Piper TTS failed: {process.stderr}")
            # Clean up on failure
            if os.path.exists(output_path):
                os.unlink(output_path)
            raise HTTPException(status_code=500, detail=f"TTS generation failed: {process.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ Piper TTS timeout")
        raise HTTPException(status_code=500, detail="TTS generation timeout")
    except FileNotFoundError:
        print("❌ Piper not found - please install piper TTS")
        raise HTTPException(status_code=500, detail="Piper TTS not installed")
    except Exception as e:
        print(f"❌ TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voice/status")
async def voice_status():
    """Get voice service status"""
    return {
        "available": faster_whisper_service.is_available(),
        "stt_enabled": faster_whisper_service._initialized,
        "tts_enabled": True,  # Piper should generally be available
        "device": faster_whisper_service.device,
    }

@app.get("/test-vad", response_class=HTMLResponse)
async def test_vad():
    """Simple test page for VAD WebSocket connection"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VAD WebSocket Test</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #1a1a1a; color: white; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .connected { background: #2d5a2d; }
            .disconnected { background: #5a2d2d; }
            .error { background: #5a4d2d; }
            button { padding: 10px 20px; margin: 10px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>🎤 VAD WebSocket Test</h1>
        <div id="status" class="status disconnected">Not connected</div>
        <button onclick="testConnection()">Test WebSocket Connection</button>
        <button onclick="testMicrophone()">Test Microphone Access</button>
        <div id="log" style="background: #2d2d2d; padding: 10px; margin-top: 20px; border-radius: 5px; max-height: 300px; overflow-y: auto;"></div>

        <script>
            let socket;

            function log(message) {
                const logDiv = document.getElementById('log');
                logDiv.innerHTML += new Date().toISOString() + ': ' + message + '<br>';
                logDiv.scrollTop = logDiv.scrollHeight;
                console.log(message);
            }

            function updateStatus(message, className) {
                const statusDiv = document.getElementById('status');
                statusDiv.textContent = message;
                statusDiv.className = 'status ' + className;
            }

            function testConnection() {
                log('🔗 Testing WebSocket connection...');

                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/vad-stream`;
                log('Connecting to: ' + wsUrl);

                socket = new WebSocket(wsUrl);

                socket.onopen = () => {
                    log('✅ WebSocket connected successfully!');
                    updateStatus('Connected', 'connected');
                };

                socket.onmessage = (event) => {
                    log('📨 Received: ' + event.data);
                };

                socket.onerror = (error) => {
                    log('❌ WebSocket error: ' + error);
                    updateStatus('Error', 'error');
                };

                socket.onclose = () => {
                    log('🔌 WebSocket closed');
                    updateStatus('Disconnected', 'disconnected');
                };
            }

            async function testMicrophone() {
                log('🎤 Testing microphone access...');
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    log('✅ Microphone access granted');
                    stream.getTracks().forEach(track => track.stop());
                } catch (error) {
                    log('❌ Microphone access denied: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """
