"""
Configuration for LLM models used in voice interface
"""


class LLMConfigVoice:
    """Configuration for voice-enabled chat interface"""

    # gpt-oss:20b is 14GB VRAM
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

    # qwen3:4b is 2.4GB VRAM
    model_name = "qwen3:4b"  # Default model for chat
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

    # gpt-oss:20b is 14GB VRAM
    model_name = "gpt-oss:20b"  # Default model for chat
    # qwen3:4b is 2.4GB VRAM
    # model_name = "qwen3:4b"  # Default model for chat
    temperature = 0.0
    max_tokens = 2048
    reasoning = True  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigAltScribe:
    """Configuration for summarization model. Run on separate GPU if possible."""

    # "mistral-nemo:12b is 7.1GB VRAM
    model_name = "mistral-nemo:12b"  # Default model for summarization
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False


class LLMConfigScribe:
    """Configuration for summarization model."""

    # granite3.3:8b is 4.9GB VRAM
    model_name = "granite3.3:8b"  # Default model for summarization with only 1 GPU
    temperature = 0.0
    max_tokens = 4096
    reasoning = False  # Add reasoning parameter for LangGraph compatibility

    # Voice-specific settings
    voice_enabled = False
