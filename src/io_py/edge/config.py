"""
Configuration for LLM models used in voice interface
"""

import os
from dotenv import load_dotenv

load_dotenv()


class LLMConfigVoice:
    """Configuration for voice-enabled chat interface"""

    # gpt-oss:20b is 14GB VRAM
    model_name = "gpt-oss:20b"
    temperature = 0.7
    max_tokens = 2000
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = True
    stt_model = "whisper"
    tts_model = "piper"


# *************MAIN PC*************************************************
class LLMConfigPeon:
    """Configuration for worker agent"""

    # Granite 4 Micro is 1.9GB VRAM, 128k context (Micro-H is 1m context hybrid model)
    model_name = "granite4:micro-h"
    temperature = 0.0
    max_tokens = 8192
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigArchitect:
    """Configuration for head honcho deep agent"""

    # gpt-oss:20b is 14GB VRAM
    model_name = "granite4:small-h"  # Default model for chat
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


# *************MINI-ITX PC*************************************************
# *************************************************************************


class LLMConfigOverseer:
    """Configuration for manager level agent"""

    # THIS GOES ON THE MAIN PC
    # granite4:micro is 2.1GB VRAM
    model_name = "granite4:micro"  # Default model for chat
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigScribe:
    """Configuration for summarization model."""

    # THIS GOES ON THE MINI-ITX
    # granite4:tiny-h is 4.2GB VRAM
    model_name = "granite4:tiny-h"  # Default model for summarization with only 1 GPU
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Remote execution settings
    use_remote = True  # Run on mini-itx
    remote_host = "mini"
    remote_port = 11436  # SSH tunnel port for mini-itx

    # Voice-specific settings
    voice_enabled = False


# SSH Tunnel Configuration
MINI_SSH_CONFIG = {
    "host": "mini",
    "user": os.getenv("MINI_USER", "david-barnes"),
    "password": os.getenv("MINI_PASSWORD"),
    "local_port": 11436,  # Port on this PC that forwards to mini-itx
    "remote_port": 11434,  # Ollama port on mini-itx
}
