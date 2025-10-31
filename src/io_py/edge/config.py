"""
Configuration for LLM models used in voice interface
"""

import os
from dotenv import load_dotenv

load_dotenv()


class LLMConfigVoice:
    """Configuration for voice-enabled chat interface"""

    # openai/gpt-oss-20b is 14GB VRAM
    # model_name = "granite4:small-h"
    model_name = "openai/gpt-oss-20b"
    temperature = 0.1
    max_tokens = 8192
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


class LLMConfigGraphs:
    """Configuration for lead deep agent"""

    # openai/gpt-oss-20b is 14GB VRAM
    # model_name = "granite4:small-h"  # Default model for chat
    model_name = "openai/gpt-oss-20b"
    # model_name = "gemma3:12b"
    temperature = 0.0
    max_tokens = 16384  # Increased for long tool calls
    reasoning = True  # Reasoning mode can interfere with tool calling

    # Voice-specific settings
    voice_enabled = False


class LLMConfigArchitect:
    """Configuration for lead deep agent"""

    # openai/gpt-oss-20b is 14GB VRAM
    # model_name = "granite4:small-h"  # Default model for chat
    model_name = "openai/gpt-oss-20b"
    # model_name = "gemma3:12b"
    temperature = 0.0
    max_tokens = 16384  # Increased for long tool calls
    reasoning = True  # Reasoning mode can interfere with tool calling

    # Voice-specific settings
    voice_enabled = False


# *************MINI-ITX PC*************************************************
# *************************************************************************


class LLMConfigOverseer:
    """Configuration for manager level agent"""

    # THIS GOES ON THE MAIN PC
    # Randomblock1/nemotron-nano is 4.9GB VRAM
    model_name = "nvidia_nvidia-nemotron-nano-12b-v2@q4_k_m"
    temperature = 0.0
    max_tokens = 16384
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigScribe:
    """Configuration for summarization model."""

    # THIS GOES ON THE MINI-ITX
    # Randomblock1/nemotron-nano is 4.9GB VRAM
    # model_name = "Randomblock1/nemotron-nano:8b"
    model_name = (
        "gpt-oss:20b"  # GPT running on the mini also as its best by a long shot
    )
    temperature = 0.0
    max_tokens = 16384
    reasoning = True  # Add reasoning parameter for LangGraph compatibility

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
