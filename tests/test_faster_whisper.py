#!/usr/bin/env python3
"""
Test script for faster-whisper with local model and test audio file
"""

import os
import sys

def test_faster_whisper():
    """Test faster-whisper with local model and test file"""

    print("🧪 Testing faster-whisper setup...")

    # Check if faster-whisper is installed
    try:
        from faster_whisper import WhisperModel
        print("✅ faster-whisper imported successfully")
    except ImportError as e:
        print(f"❌ faster-whisper not available: {e}")
        print("💡 Install with: pip install faster-whisper")
        return False

    # Model and test file paths
    model_path = "./faster-whisper-large-v3-turbo-ct2"
    test_file = os.path.join(model_path, "test5.wav")

    print(f"📁 Model path: {model_path}")
    print(f"🎵 Test file: {test_file}")

    # Check if paths exist
    if not os.path.exists(model_path):
        print(f"❌ Model path not found: {model_path}")
        return False

    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False

    print("✅ Paths verified")

    try:
        print("🚀 Loading faster-whisper model...")

        # Load the model - try CPU first to test basic functionality
        print("🔄 Trying CPU mode first...")
        try:
            model = WhisperModel(
                model_path,
                device="cpu",
                compute_type="int8"
            )
            print("✅ CPU model loaded successfully!")
        except Exception as cpu_error:
            print(f"❌ CPU loading failed: {cpu_error}")
            print("🔄 Trying GPU mode...")
            model = WhisperModel(
                model_path,
                device="cuda",
                compute_type="float16"
            )
            print("✅ GPU model loaded successfully!")

        print("✅ Model loaded successfully!")

        print("🎤 Transcribing test audio...")

        # Transcribe the test file
        segments, info = model.transcribe(
            test_file,
            beam_size=5,
            language="en"
        )

        print(f"📊 Detected language: {info.language} (confidence: {info.language_probability:.2f})")
        print(f"⏱️  Duration: {info.duration:.2f}s")

        # Collect all segments
        transcription_text = ""
        print("\n📝 Transcription results:")
        print("-" * 50)

        for i, segment in enumerate(segments):
            print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
            transcription_text += segment.text

        print("-" * 50)
        print(f"🎯 Full transcription: '{transcription_text.strip()}'")

        return True

    except Exception as e:
        print(f"❌ faster-whisper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_system_info():
    """Check system information"""
    print("\n🖥️  System Information:")
    print(f"   Python version: {sys.version}")

    try:
        import torch
        print(f"   PyTorch version: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA version: {torch.version.cuda}")
    except ImportError:
        print("   PyTorch: Not installed")

    try:
        import faster_whisper
        print(f"   faster-whisper: Available")
    except ImportError:
        print("   faster-whisper: Not installed")

if __name__ == "__main__":
    print("🎤 Faster-Whisper Test Script")
    print("=" * 50)

    check_system_info()
    print()

    success = test_faster_whisper()

    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! faster-whisper is working correctly")
        print("💡 Now we can integrate this into the voice service")
    else:
        print("❌ Test failed - check the errors above")

    print("=" * 50)