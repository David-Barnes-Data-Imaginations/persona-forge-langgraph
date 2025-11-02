"use client";
import { useState, useRef, useEffect } from "react";
import { Mic, MicOff, Volume2 } from "lucide-react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";

interface VoiceControlProps {
  handleTranscript: (transcript: string) => void;
}

export default function VoiceControl({ handleTranscript }: VoiceControlProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [status, setStatus] = useState<string>("Ready");
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    return () => {
      if (socket) {
        socket.close();
      }
      if (processorRef.current) {
        processorRef.current.disconnect();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [socket]);

  const startRecording = async () => {
    try {
      setStatus("Connecting...");
      const wsUrl = BACKEND_URL.replace(/^http/, "ws");
      const ws = new WebSocket(`${wsUrl}/ws/vad-stream`);
      setSocket(ws);

      ws.onopen = async () => {
        console.log("🎤 WebSocket connected");
        setStatus("Listening...");
        
        try {
          // Get microphone stream
          const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
              channelCount: 1,
              sampleRate: 16000,
              echoCancellation: true,
              noiseSuppression: true,
              autoGainControl: true,
            } 
          });
          streamRef.current = stream;

          // Create audio context
          const audioContext = new AudioContext({ sampleRate: 16000 });
          audioContextRef.current = audioContext;

          const source = audioContext.createMediaStreamSource(stream);
          
          // Create script processor to get raw audio data
          const processor = audioContext.createScriptProcessor(4096, 1, 1);
          processorRef.current = processor;

          let chunkCount = 0;
          processor.onaudioprocess = (e) => {
            if (ws.readyState === WebSocket.OPEN) {
              const inputData = e.inputBuffer.getChannelData(0);
              
              // Convert float32 to int16 PCM
              const pcmData = new Int16Array(inputData.length);
              for (let i = 0; i < inputData.length; i++) {
                const s = Math.max(-1, Math.min(1, inputData[i]));
                pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
              }
              
              // Send raw PCM data
              ws.send(pcmData.buffer);
              chunkCount++;
              
              // Log every 50 chunks (roughly every 2 seconds)
              if (chunkCount % 50 === 0) {
                console.log(`📦 Sent ${chunkCount} audio chunks (${pcmData.length} samples each)`);
              }
            }
          };

          source.connect(processor);
          processor.connect(audioContext.destination);
          
          setIsRecording(true);
        } catch (error) {
          console.error("❌ Microphone access error:", error);
          setStatus("Microphone access denied");
          ws.close();
        }
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === "TRANSCRIPT" && message.text) {
            console.log("✅ Received transcript:", message.text);
            handleTranscript(message.text);
            setStatus("Transcribed!");
            
            // Close WebSocket after receiving transcript
            setTimeout(() => {
              console.log("✅ Closing WebSocket after successful transcription");
              if (ws) ws.close();
            }, 500);
          } else if (message.type === "ERROR") {
            console.error("❌ Transcription error:", message.message);
            setStatus("Error: " + message.message);
            if (ws) ws.close();
          } else if (message.type === "STATUS") {
            console.log("ℹ️ Status:", message.message);
            if (ws) ws.close();
          }
        } catch (error) {
          console.error("❌ Message parse error:", error);
        }
      };

      ws.onclose = () => {
        console.log("🎤 WebSocket closed");
        setIsRecording(false);
        setStatus("Ready");
        cleanup();
      };

      ws.onerror = (error) => {
        console.error("❌ WebSocket error:", error);
        setStatus("Connection error");
        setIsRecording(false);
      };
    } catch (error) {
      console.error("❌ Start recording error:", error);
      setStatus("Failed to start");
      setIsRecording(false);
    }
  };

  const cleanup = () => {
    if (processorRef.current) {
      processorRef.current.disconnect();
      processorRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
  };

  const stopRecording = () => {
    console.log("🛑 Stopping recording...");
    setStatus("Processing...");
    
    // Send UTTERANCE_END message to trigger transcription
    if (socket && socket.readyState === WebSocket.OPEN) {
      const endMessage = JSON.stringify({ type: "UTTERANCE_END" });
      console.log("📤 Sending UTTERANCE_END message:", endMessage);
      console.log("⏳ Keeping WebSocket open to receive transcription response...");
      socket.send(endMessage);
      
      // DON'T close immediately - wait for transcription response!
      // The onmessage handler will receive the response and close after
      // Set a timeout in case backend doesn't respond
      setTimeout(() => {
        if (socket && socket.readyState === WebSocket.OPEN) {
          console.log("⏰ Timeout waiting for transcription response, closing WebSocket");
          socket.close();
        }
      }, 30000);  // 30 second timeout
    } else {
      console.error("❌ Cannot send UTTERANCE_END - socket not open. State:", socket?.readyState);
    }
    
    // Stop audio capture but keep WebSocket open for response
    cleanup();
    setIsRecording(false);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="flex flex-col items-end space-y-2">
        {/* Status Badge */}
        {isRecording && (
          <div className="bg-white/90 backdrop-blur-sm rounded-full px-4 py-2 shadow-lg border border-blue-200 animate-pulse">
            <p className="text-sm text-gray-700 font-medium">{status}</p>
          </div>
        )}

        {/* Voice Control Button */}
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isSpeaking}
          className={`group relative w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${
            isRecording
              ? "bg-red-500 hover:bg-red-600 scale-110 animate-pulse"
              : isSpeaking
              ? "bg-purple-400 cursor-not-allowed"
              : "bg-gradient-to-br from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-110"
          }`}
          title={isRecording ? "Stop recording" : isSpeaking ? "AI is speaking" : "Start recording"}
        >
          {isSpeaking ? (
            <Volume2 className="w-7 h-7 text-white animate-bounce" />
          ) : isRecording ? (
            <MicOff className="w-7 h-7 text-white" />
          ) : (
            <Mic className="w-7 h-7 text-white" />
          )}

          {/* Pulsing ring animation when recording */}
          {isRecording && (
            <span className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-75"></span>
          )}
        </button>

        {/* Instruction Text */}
        {!isRecording && !isSpeaking && (
          <p className="text-xs text-gray-500 bg-white/80 backdrop-blur-sm rounded px-2 py-1">
            Click to speak
          </p>
        )}
      </div>
    </div>
  );
}