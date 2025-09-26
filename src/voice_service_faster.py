"""
Production Voice Service using faster-whisper
Based on successful test with local model
"""

import os
import tempfile
import numpy as np
from typing import Optional, Tuple
from faster_whisper import WhisperModel


class FasterWhisperService:
    """Voice service using faster-whisper (production ready)"""

    def __init__(self):
        self.model = None
        self._initialized = False
        self.device = "cuda"  # Use GPU for better performance

        # Initialize model
        self._initialize_model()

    def _initialize_model(self):
        """Initialize faster-whisper model"""
        try:
            print("🚀 Loading faster-whisper model...")

            # Path to the working model
            model_path = "./faster-whisper-large-v3-turbo-ct2"

            if not os.path.exists(model_path):
                print(f"❌ Model path not found: {model_path}")
                return

            # For now, let's use CPU to avoid cuDNN issues
            # You can switch back to CUDA once cuDNN is properly installed
            print("🎯 Loading model with CPU (cuDNN issues detected)...")
            self.model = WhisperModel(
                model_path,
                device="cpu",
                compute_type="int8"
            )
            self.device = "cpu"
            print("✅ faster-whisper model loaded successfully with CPU!")

            # TODO: Uncomment this section once cuDNN is fixed:
            # try:
            #     print("🎯 Attempting to load model with CUDA...")
            #     self.model = WhisperModel(model_path, device="cuda", compute_type="float16")
            #     self.device = "cuda"
            #     print("✅ faster-whisper model loaded successfully with CUDA!")
            # except Exception as cuda_error:
            #     print(f"⚠️ CUDA failed: {cuda_error}")
            #     print("🔄 Falling back to CPU...")
            #     self.model = WhisperModel(model_path, device="cpu", compute_type="int8")
            #     self.device = "cpu"
            #     print("✅ faster-whisper model loaded successfully with CPU!")

            self._initialized = True

        except Exception as e:
            print(f"❌ faster-whisper initialization failed: {e}")
            self._initialized = False

    def is_available(self) -> bool:
        """Check if voice service is available"""
        return self._initialized and self.model is not None

    def transcribe_audio_numpy(self, audio_data: Tuple[int, np.ndarray]) -> str:
        """
        Transcribe audio from numpy array (Gradio format)

        Args:
            audio_data: Tuple of (sample_rate, numpy_array)

        Returns:
            Transcribed text
        """
        print("🔍 DEBUGGING: transcribe_audio_numpy called")
        print(f"   Audio data type: {type(audio_data)}")
        print(f"   Audio data: {audio_data}")

        if not self.is_available():
            print("❌ Voice service not available")
            return "Voice service not available"

        try:
            print("🔄 Extracting audio data...")
            sample_rate, audio_array = audio_data
            print(f"📊 Processing audio: {sample_rate}Hz, {len(audio_array)} samples")
            print(f"   Audio array shape: {audio_array.shape}")
            print(f"   Audio array dtype: {audio_array.dtype}")
            print(f"   Audio array min/max: {audio_array.min():.3f}/{audio_array.max():.3f}")

            # Save audio locally for debugging (your suggestion!)
            debug_path = f"./debug_audio_{sample_rate}hz.wav"
            print(f"💾 Saving debug audio to: {debug_path}")

            # Create temporary file for faster-whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                import soundfile as sf
                print("🔄 Writing audio with soundfile...")

                # Save both debug and temp versions
                sf.write(debug_path, audio_array, sample_rate)
                sf.write(tmp_file.name, audio_array, sample_rate)
                temp_path = tmp_file.name

                print(f"✅ Audio files created:")
                print(f"   Debug: {debug_path}")
                print(f"   Temp: {temp_path}")

            try:
                print("🎤 Starting faster-whisper transcription...")

                # Transcribe using faster-whisper
                print("🔄 Calling model.transcribe()...")
                segments, info = self.model.transcribe(
                    temp_path,
                    beam_size=5,
                    language="en"
                )
                print("✅ model.transcribe() completed")

                print(f"📊 Language: {info.language} (confidence: {info.language_probability:.2f})")

                # Collect all segments
                print("🔄 Collecting segments...")
                transcription = ""
                segment_count = 0
                for segment in segments:
                    print(f"   Segment {segment_count}: [{segment.start:.2f}s-{segment.end:.2f}s] '{segment.text}'")
                    transcription += segment.text
                    segment_count += 1

                result = transcription.strip()
                print(f"✅ Final transcription ({segment_count} segments): '{result}'")

                return result

            finally:
                print("🧹 Cleaning up temporary file...")
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    print("✅ Temp file removed")

        except Exception as e:
            error_msg = f"Transcription error: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            print("📋 Full traceback:")
            traceback.print_exc()
            return error_msg

    def transcribe_audio_file(self, file_path: str) -> str:
        """Transcribe audio from file path"""
        if not self.is_available():
            return "Voice service not available"

        try:
            print(f"📁 Transcribing file: {file_path}")

            segments, info = self.model.transcribe(
                file_path,
                beam_size=5,
                language="en"
            )

            # Collect transcription
            transcription = ""
            for segment in segments:
                transcription += segment.text

            result = transcription.strip()
            print(f"✅ File transcription: '{result}'")
            return result

        except Exception as e:
            error_msg = f"File transcription error: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg


# Create global instance
faster_whisper_service = FasterWhisperService()