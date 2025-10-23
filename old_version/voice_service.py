"""
Voice Service for SentimentSuite
Integrates WhisperX STT and Piper TTS into the chat interface
"""

import asyncio
import tempfile
import subprocess
import torch
import numpy as np
from typing import Dict, Any, Optional
from fastapi import UploadFile
from io import BytesIO
import base64
import wave
import os


class VoiceService:
    """Voice service for STT/TTS integration with SentimentSuite chat"""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"

        self.whisper_model = None
        self.align_model = None
        self.align_metadata = None

        self._initialized = False

        # Try to initialize models
        self._initialize_models()

    def _initialize_models(self):
        """Initialize STT models (lazy loading)"""
        try:
            import whisperx

            print("🚀 Loading WhisperX model...")

            # Check for local Whisper model first
            import os
            local_model_path = "/home/david-barnes/openai/whisper-large-v3"

            if os.path.exists(local_model_path):
                print(f"📁 Found local Whisper model at: {local_model_path}")

                # Try different approaches for local model loading
                model_loaded = False

                # Approach 1: Try loading as HuggingFace model path
                try:
                    self.whisper_model = whisperx.load_model(
                        local_model_path,
                        self.device,
                        compute_type=self.compute_type,
                        language="en"
                    )
                    print("✅ Local model loaded via path")
                    model_loaded = True
                except Exception as path_error:
                    print(f"⚠️ Path loading failed: {path_error}")

                # Approach 2: Try with transformers cache path
                if not model_loaded:
                    try:
                        print("🔄 Setting up local cache path...")
                        os.environ['TRANSFORMERS_CACHE'] = os.path.dirname(local_model_path)
                        os.environ['HF_DATASETS_OFFLINE'] = '1'
                        os.environ['TRANSFORMERS_OFFLINE'] = '1'

                        # Try to use the model without downloading
                        self.whisper_model = whisperx.load_model(
                            "openai/whisper-large-v3",
                            self.device,
                            compute_type=self.compute_type,
                            language="en"
                        )
                        print("✅ Local cached model loaded")
                        model_loaded = True
                    except Exception as cache_error:
                        print(f"⚠️ Cached model loading failed: {cache_error}")

                # Approach 3: Try with local_files_only
                if not model_loaded:
                    try:
                        print("🔄 Trying with local_files_only...")
                        # Reset environment to allow downloads
                        if 'TRANSFORMERS_OFFLINE' in os.environ:
                            del os.environ['TRANSFORMERS_OFFLINE']
                        if 'HF_DATASETS_OFFLINE' in os.environ:
                            del os.environ['HF_DATASETS_OFFLINE']

                        self.whisper_model = whisperx.load_model(
                            "large-v3",
                            self.device,
                            compute_type=self.compute_type,
                            language="en"
                        )
                        print("✅ Downloaded model loaded")
                        model_loaded = True
                    except Exception as download_error:
                        print(f"⚠️ Download loading failed: {download_error}")

                if not model_loaded:
                    print("💡 Your Whisper model is in HuggingFace format, but WhisperX needs faster-whisper format.")
                    print("💡 To fix this, you could:")
                    print("   - Download faster-whisper compatible model, or")
                    print("   - Convert your model using faster-whisper tools")
                    print("💡 For demo purposes, UI will show with voice disabled.")
                    return
            else:
                print(f"📥 Local model not found at: {local_model_path}")
                print("🔄 Trying standard model...")
                try:
                    self.whisper_model = whisperx.load_model(
                        "large-v3",
                        self.device,
                        compute_type=self.compute_type,
                        language="en"
                    )
                    print("✅ Standard WhisperX model loaded successfully")
                except Exception as model_error:
                    print(f"❌ Model loading failed: {model_error}")
                    return

            # Try to load alignment model
            try:
                self.align_model, self.align_metadata = whisperx.load_align_model(
                    language_code="en",
                    device=self.device
                )
            except Exception as align_error:
                print(f"⚠️ Alignment model not available: {align_error}")

            self._initialized = True
            print("✅ WhisperX models loaded successfully")

        except ImportError:
            print("⚠️ WhisperX not available - STT functionality disabled")
        except Exception as e:
            print(f"⚠️ WhisperX model loading failed: {e}")
            print("📝 Voice transcription will be disabled for this demo")
            print("💡 To enable: export HF_TOKEN=your_token or use cached models")

    def is_available(self) -> bool:
        """Check if voice services are available"""
        return self._initialized

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio data to text

        Args:
            audio_data: Raw audio bytes (WAV format)

        Returns:
            Dict containing transcription results
        """
        if not self._initialized:
            return {"error": "Voice service not initialized", "text": ""}

        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name

            try:
                import whisperx

                # Load and transcribe
                audio = whisperx.load_audio(tmp_path)
                result = self.whisper_model.transcribe(
                    audio,
                    batch_size=16,
                    language="en"
                )

                # Align for word-level timestamps
                result = whisperx.align(
                    result["segments"],
                    self.align_model,
                    self.align_metadata,
                    audio,
                    self.device,
                    return_char_alignments=False
                )

                # Extract just the text
                text = " ".join([segment["text"] for segment in result["segments"]]).strip()

                return {
                    "text": text,
                    "segments": result["segments"],
                    "language": "en"
                }

            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        except Exception as e:
            return {"error": str(e), "text": ""}

    def synthesize_speech(self, text: str, voice: str = "en_GB-alba-medium") -> Optional[bytes]:
        """
        Convert text to speech using Piper TTS

        Args:
            text: Text to convert to speech
            voice: Voice model to use

        Returns:
            WAV audio bytes or None if error
        """
        if not text.strip():
            return None

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            # Check if piper is available
            result = subprocess.run(["which", "piper"], capture_output=True)
            if result.returncode != 0:
                print("⚠️ Piper not found in PATH")
                return None

            # Check for model files in common locations
            model_paths = [
                f"/home/davidbarnes/piper/{voice}.onnx",
                f"/home/{os.getenv('USER', 'user')}/piper/{voice}.onnx",
                f"./models/{voice}.onnx"
            ]

            model_path = None
            for path in model_paths:
                if os.path.exists(path):
                    model_path = path
                    break

            if not model_path:
                print(f"⚠️ Piper model {voice}.onnx not found in expected locations")
                print(f"📝 Searched: {model_paths}")
                return None

            # Run Piper TTS
            process_result = subprocess.run(
                [
                    "piper",
                    "--model", model_path,
                    "--output_file", tmp_path
                ],
                input=text,
                text=True,
                capture_output=True,
                check=True
            )

            # Read generated audio
            with open(tmp_path, 'rb') as f:
                audio_data = f.read()

            return audio_data

        except subprocess.CalledProcessError as e:
            print(f"❌ Piper TTS failed: {e}")
            return None
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return None
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def text_to_speech_base64(self, text: str) -> Optional[str]:
        """
        Convert text to speech and return as base64 encoded string

        Args:
            text: Text to convert

        Returns:
            Base64 encoded WAV audio or None
        """
        audio_data = self.synthesize_speech(text)
        if audio_data:
            return base64.b64encode(audio_data).decode('utf-8')
        return None

    async def process_audio_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Process uploaded audio file and return transcription

        Args:
            file: Uploaded audio file

        Returns:
            Transcription results
        """
        try:
            # Read file content
            content = await file.read()

            # Process transcription
            result = await self.transcribe_audio(content)

            return result

        except Exception as e:
            return {"error": str(e), "text": ""}


# Try to use the faster-whisper service first (proven to work)
try:
    from .voice_service_faster import faster_whisper_service
    voice_service = faster_whisper_service
    print("🔄 Using faster-whisper service (production ready)")
except ImportError:
    try:
        from .voice_service_working import working_voice_service
        voice_service = working_voice_service
        print("🔄 Using working transformers-based service")
    except ImportError:
        try:
            from .voice_service_simple import simple_voice_service
            voice_service = simple_voice_service
            print("🔄 Using simplified Whisper service")
        except ImportError:
            # Fallback to original WhisperX service
            voice_service = VoiceService()
            print("🔄 Using WhisperX service")