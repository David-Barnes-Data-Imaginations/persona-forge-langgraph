"""
Configuration for LLM models used in voice interface
"""


class LLMConfigVoice:
    """Configuration for voice-enabled chat interface"""

    model_name = "gpt-oss:20b"  # Default model for chat
    temperature = 0.7
    max_tokens = 2000
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = True
    stt_model = "whisper"
    tts_model = "piper"


class LLMConfigPeon:
    """Configuration for worker agent"""

    # qwen3:1.7b is 1.4GB VRAM
    model_name = "qwen3:1.7b"  # Default model for chat
    temperature = 0.0
    max_tokens = 2048
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigArchitect:
    """Configuration for head honcho deep agent"""

    # gpt-oss:20b is 14GB VRAM
    model_name = "gpt-oss:20b"  # Default model for chat
    temperature = 0.0
    max_tokens = 4096
    reasoning = True  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigOverseer:
    """Configuration for manager level agent"""

    # qwen3:4b is 2.4GB VRAM
    model_name = "qwen3:4b"  # Default model for chat
    temperature = 0.0
    max_tokens = 2048
    reasoning = True  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigScribe:
    """Configuration for summarization model. Run on separate GPU if possible."""

    # qwen3:1.7b is 7.1GB VRAM
    model_name = "mistral-nemo:12b"  # Default model for summarization
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigSmolScribe:
    """Configuration for summarization model. Run on separate GPU if possible."""

    # gemma3:1b is 815MB VRAM
    model_name = "gemma3:1b"  # Default model for summarization
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False
