from pathlib import Path
from dataclasses import dataclass

# Project root directory
ROOT_DIR=Path(__file__).parent

# Server configuration
SERVER_HOST="127.0.0.1"
SERVER_PORT=8005
SERVER_ENDPOINT=f"https://{SERVER_HOST}:{SERVER_PORT}/stdio"


@dataclass
class LLMConfigVoice:

    tools = []
    model_name: str = "gemma3:1b",
    max_completion_tokens: int = 8192,
    temperature: float = 0
    stream_outputs=True,
    reasoning = False,