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
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  useEffect(() => {
    return () => {
      if (socket) {
        socket.close();
      }
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
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
          const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
              channelCount: 1,
              sampleRate: 16000,
              echoCancellation: true,
              noiseSuppression: true,
            } 
          });
          
          const mediaRecorder = new MediaRecorder(stream, {
            mimeType: "audio/webm;codecs=opus"
          });
          mediaRecorderRef.current = mediaRecorder;

          mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
              ws.send(event.data);
            }
          };

          mediaRecorder.onstop = () => {
            stream.getTracks().forEach(track => track.stop());
            ws.close();
          };

          mediaRecorder.start(1000); // Send data every second
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
            setTimeout(() => setStatus("Listening..."), 2000);
          } else if (message.type === "ERROR") {
            console.error("❌ Transcription error:", message.message);
            setStatus("Error: " + message.message);
          }
        } catch (error) {
          console.error("❌ Message parse error:", error);
        }
      };

      ws.onclose = () => {
        console.log("🎤 WebSocket closed");
        setIsRecording(false);
        setStatus("Ready");
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

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
    setStatus("Stopping...");
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
