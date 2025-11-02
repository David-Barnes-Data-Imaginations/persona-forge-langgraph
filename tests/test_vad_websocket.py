#!/usr/bin/env python3
"""
Test script for VAD WebSocket endpoint
Sends test audio data and checks response
"""
import asyncio
import websockets
import json
import numpy as np


async def test_vad_websocket():
    """Test the VAD WebSocket with synthetic audio"""
    uri = "ws://localhost:8001/ws/vad-stream"

    print("🔌 Connecting to WebSocket...")
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")

        # Generate test audio: 3 seconds of sine wave (simulates speech)
        sample_rate = 16000
        duration = 3
        frequency = 440  # A4 note

        t = np.linspace(0, duration, sample_rate * duration)
        audio = np.sin(2 * np.pi * frequency * t) * 0.3  # Float32 audio

        # Convert to int16 PCM
        audio_int16 = (audio * 32767).astype(np.int16)

        print(f"📤 Sending {len(audio_int16)} audio samples in chunks...")

        # Send audio in chunks (simulate streaming)
        chunk_size = 4096
        num_chunks = 0
        for i in range(0, len(audio_int16), chunk_size):
            chunk = audio_int16[i : i + chunk_size]
            await websocket.send(chunk.tobytes())
            num_chunks += 1

            if num_chunks % 10 == 0:
                print(f"  Sent {num_chunks} chunks...")

        print(f"✅ Sent {num_chunks} total chunks")

        # Send UTTERANCE_END
        print("📤 Sending UTTERANCE_END...")
        await websocket.send(json.dumps({"type": "UTTERANCE_END"}))

        # Wait for response
        print("⏳ Waiting for transcription response...")
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
            message = json.loads(response)
            print(f"\n📨 Received response:")
            print(f"   Type: {message.get('type')}")
            print(f"   Text: {message.get('text', message.get('message'))}")
            print(f"   Full: {message}")
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for response")
        except Exception as e:
            print(f"❌ Error receiving response: {e}")


if __name__ == "__main__":
    print("🧪 VAD WebSocket Test Script")
    print("=" * 50)
    asyncio.run(test_vad_websocket())
