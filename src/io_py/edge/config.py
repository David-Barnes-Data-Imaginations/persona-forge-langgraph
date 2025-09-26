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