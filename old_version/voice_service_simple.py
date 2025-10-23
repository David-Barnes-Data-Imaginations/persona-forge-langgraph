"""
Simplified Voice Service using standard OpenAI Whisper
This version works with your local whisper-large-v3 model
"""

import asyncio
import tempfile
import subprocess
import torch
import os
from typing import Dict, Any, Optional
from fastapi import UploadFile


class SimpleVoiceService:
    """Simplified voice service using OpenAI Whisper directly"""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialized = False
        self.whisper_model = None

        # Try to initialize
        self._initialize_whisper()

    def _initialize_whisper(self):
        """Initialize OpenAI Whisper model"""
        try:
            import whisper

            # Check for local models - prioritize smaller turbo version
            turbo_model_path = "/home/david-barnes/openai/whisper-large-v3-turbo"
            large_model_path = "/home/david-barnes/openai/whisper-large-v3"

            print("🚀 Loading Whisper model...")

            # Try turbo model first (smaller, faster)
            if os.path.exists(turbo_model_path):
                print(f"📁 Found turbo model at: {turbo_model_path}")
                try:
                    self.whisper_model = whisper.load_model("large-v3-turbo", device=self.device)
                    print("✅ Whisper large-v3-turbo model loaded successfully")
                    self._initialized = True
                    return
                except Exception as e:
                    print(f"⚠️ Turbo model loading failed: {e}")

            # Fallback to regular large model
            elif os.path.exists(large_model_path):
                print(f"📁 Found large model at: {large_model_path}")
                try:
                    self.whisper_model = whisper.load_model("large-v3", device=self.device)
                    print("✅ Whisper large-v3 model loaded successfully")
                    self._initialized = True
                    return
                except Exception as e:
                    print(f"⚠️ Large model loading failed: {e}")

            # Fallback to smaller model
            try:
                print("🔄 Trying smaller model for demo...")
                self.whisper_model = whisper.load_model("base", device=self.device)
                print("✅ Whisper base model loaded successfully")
                self._initialized = True
            except Exception as e:
                print(f"❌ Model loading failed: {e}")

        except ImportError:
            print("⚠️ OpenAI Whisper not available")
            print("💡 Install with: pip install openai-whisper")
        except Exception as e:
            print(f"❌ Whisper initialization failed: {e}")

    def is_available(self) -> bool:
        """Check if voice services are available"""
        return self._initialized

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio data to text using OpenAI Whisper

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
                # Transcribe with Whisper
                result = self.whisper_model.transcribe(tmp_path, language="en")

                return {
                    "text": result["text"].strip(),
                    "language": result.get("language", "en"),
                    "segments": result.get("segments", [])
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
        (Same as the original implementation)
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
                print(f"⚠️ Piper model {voice}.onnx not found")
                return None

            # Run Piper TTS
            subprocess.run(
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

    async def process_audio_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded audio file and return transcription"""
        try:
            content = await file.read()
            result = await self.transcribe_audio(content)
            return result
        except Exception as e:
            return {"error": str(e), "text": ""}


# Create instance
simple_voice_service = SimpleVoiceService()