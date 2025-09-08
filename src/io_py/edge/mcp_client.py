from pathlib import Path
from dataclasses import dataclass
from src.tools import *

@dataclass
class LLMConfigVoice:

    tools = []
    model_name: str = "Qwen2.5-Coder-32B.gguf",
    max_completion_tokens: int = 8192,
    temperature: float = 0.2
    stream_outputs=True,