#!/usr/bin/env python3
"""
Test the debug audio file created by Gradio
"""

import os
import glob
from faster_whisper import WhisperModel

def test_debug_audio():
    """Test any debug audio files in the project"""

    # Find debug audio files
    debug_files = glob.glob("./debug_audio_*.wav")

    if not debug_files:
        print("❌ No debug audio files found")
        print("💡 Record and transcribe in the app first")
        return

    print(f"📁 Found {len(debug_files)} debug audio files:")
    for f in debug_files:
        print(f"   - {f}")

    # Use the first debug file
    test_file = debug_files[0]
    print(f"\n🎵 Testing: {test_file}")

    # Load model
    model_path = "./faster-whisper-large-v3-turbo-ct2"
    model = WhisperModel(model_path, device="cpu", compute_type="int8")

    # Transcribe
    segments, info = model.transcribe(test_file, beam_size=5, language="en")

    print(f"📊 Language: {info.language} (confidence: {info.language_probability:.2f})")
    print(f"⏱️  Duration: {info.duration:.2f}s")

    transcription = ""
    for segment in segments:
        print(f"[{segment.start:.2f}s-{segment.end:.2f}s] {segment.text}")
        transcription += segment.text

    print(f"\n🎯 Full transcription: '{transcription.strip()}'")

if __name__ == "__main__":
    test_debug_audio()